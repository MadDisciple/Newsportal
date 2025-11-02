from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import Post, Category

@receiver(m2m_changed, sender=Post.categories.through)
def notify_subscribers(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        post = instance

        subscribers = User.objects.none()
        for category_id in pk_set:
            category = Category.objects.get(pk=category_id)
            subscribers = subscribers | category.subscribers.all()

        unique_subscribers = subscribers.distinct()

        for subscriber in unique_subscribers:

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
                f"Здравствуй, {subscriber.username}. Новая статья в твоём любимом разделе!\n{post.title}\n{post.text[:50]}...",
                settings.DEFAULT_FROM_EMAIL, # От кого
                [subscriber.email], # Кому
            )
            msg.attach_alternative(html_content, "text/html")

            try:
                msg.send(fail_silently=False)
            except Exception as e:
                print(f"Ошибка отправки письма {subscriber.email}: {e}")