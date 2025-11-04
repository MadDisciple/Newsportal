from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import Post, Category, User


@shared_task
def notify_subscribers_task(post_id, category_id):
    try:
        post = Post.objects.get(id=post_id)
        category = Category.objects.get(id=category_id)

        subscribers = category.subscribers.all()

        print(f"CELERY: Найдено {subscribers.count()} подписчиков для '{category.name}'.")

        for subscriber in subscribers:
            if subscriber == post.author.user:
                continue

            subject = post.title

            html_content = render_to_string(
                'mail/new_post_notification.html',
                {
                    'user': subscriber,
                    'post': post,
                    'site_url': settings.SITE_URL,
                }
            )

            msg = EmailMultiAlternatives(
                subject,
                f"Здравствуй, {subscriber.username}. ...",
                settings.DEFAULT_FROM_EMAIL,
                [subscriber.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

    except Post.DoesNotExist:
        print(f"CELERY Error: Пост {post_id} не найден.")
    except Category.DoesNotExist:
        print(f"CELERY Error: Категория {category_id} не найдена.")
    except Exception as e:
        print(f"CELERY Error: {e}")


@shared_task
def send_weekly_newsletter_task():
    last_week = timezone.now() - timedelta(days=7)
    categories = Category.objects.filter(
        post__created_at__gte=last_week
    ).distinct().prefetch_related('subscribers')

    print(f"CELERY BEAT: Запуск еженедельной рассылки. Найдено {categories.count()} категорий.")

    for category in categories:
        posts_for_category = Post.objects.filter(
            created_at__gte=last_week,
            categories=category
        ).distinct()

        if not posts_for_category.exists():
            continue

        subscribers = category.subscribers.all()

        for subscriber in subscribers:
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
                f'Дайджест новостей за неделю в «{category.name}»',
                f"Здравствуй, {subscriber.username}! ...",
                settings.DEFAULT_FROM_EMAIL,
                [subscriber.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            print(f"CELERY BEAT: Дайджест для {subscriber.email} по «{category.name}» отправлен.")