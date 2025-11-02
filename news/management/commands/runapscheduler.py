import logging
from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from news.models import Post, Category

logger = logging.getLogger(__name__)


def send_weekly_newsletter():
    last_week = timezone.now() - timedelta(days=7)
    categories_with_new_posts_ids = Post.objects.filter(
        created_at__gte=last_week
    ).values_list('categories', flat=True).distinct()
    categories = Category.objects.filter(
        id__in=categories_with_new_posts_ids
    ).prefetch_related('subscribers')

    print(f"Найдено {categories.count()} категорий с новыми постами.")

    for category in categories:

        posts_for_category = Post.objects.filter(
            created_at__gte=last_week,
            categories=category
        )

        for subscriber in category.subscribers.all():


            subject = f'Дайджест новостей за неделю в категории «{category.name}»'

            html_content = render_to_string(
                'mail/weekly_newsletter.html',
                {
                    'user': subscriber,
                    'category': category,
                    'posts': posts_for_category,
                    'site_url': settings.SITE_URL,
                }
            )

            msg = EmailMultiAlternatives(
                subject,
                f"Здравствуй, {subscriber.username}! Новые статьи в разделе «{category.name}»\n"
                f"(К сожалению, HTML-версия не загрузилась)",
                settings.DEFAULT_FROM_EMAIL,  # От кого
                [subscriber.email],  # Кому
            )
            msg.attach_alternative(html_content, "text/html")

            try:
                msg.send(fail_silently=False)
                print(f"Письмо успешно отправлено {subscriber.email} по категории «{category.name}»")
            except Exception as e:
                print(f"Ошибка отправки {subscriber.email}: {e}")


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_weekly_newsletter,
            trigger=CronTrigger(day_of_week="mon", hour="08", minute="00"),
            id="send_weekly_newsletter",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'send_weekly_newsletter'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")