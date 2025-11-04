from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))
    rating = models.IntegerField(default=0, verbose_name=_('Rating'))

    def update_rating(self):
        post_rating = self.post_set.all().aggregate(Sum('rating'))['rating__sum'] or 0
        post_rating_total = post_rating * 3

        comment_rating_total = self.user.comment_set.all().aggregate(Sum('rating'))['rating__sum'] or 0

        comment_to_posts_rating = Comment.objects.filter(post__author=self).aggregate(Sum('rating'))['rating__sum'] or 0

        self.rating = post_rating_total + comment_rating_total + comment_to_posts_rating
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Category Name'))
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories', verbose_name=_('Subscribers'))

    def __str__(self):
        return self.name


class Post(models.Model):
    ARTICLE = 'article'
    NEWS = 'news'
    POST_TYPES = [
        (ARTICLE, _('Article')),
        (NEWS, _('News')),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=_('Author'))
    post_type = models.CharField(
        max_length=10,
        choices=POST_TYPES,
        default=ARTICLE,
        verbose_name=_('Post Type')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    categories = models.ManyToManyField(
        Category,
        through='PostCategory',
        verbose_name=_('Categories')
    )
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    text = models.TextField(verbose_name=_('Text'))
    rating = models.IntegerField(default=0, verbose_name=_('Rating'))

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f"{self.text[:124]}..."

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.pk)])

    def __str__(self):
        return f"{self.title} (by {self.author.user.username})"


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_('Post'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Category'))

    def __str__(self):
        return f"{self.post.title} | {self.category.name}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_('Post'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    text = models.TextField(verbose_name=_('Comment Text'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    rating = models.IntegerField(default=0, verbose_name=_('Rating'))

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f"{_('Comment by')} {self.user.username} {_('on')} {self.post.title}"