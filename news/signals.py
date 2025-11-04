from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post
from .tasks import notify_subscribers_task


@receiver(m2m_changed, sender=Post.categories.through)
def notify_subscribers(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        post = instance
        for category_id in pk_set:
            notify_subscribers_task.delay(post.id, category_id)
            print(f"SIGNAL: Задача для категории {category_id} отправлена в Celery.")