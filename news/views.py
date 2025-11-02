from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Category
from django.utils import timezone
from django.core.exceptions import ValidationError



class PostList(ListView):
    model = Post
    ordering = ['-created_at']
    template_name = 'news/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'news/post_detail.html'
    context_object_name = 'post'


class PostSearch(ListView):
    model = Post
    ordering = ['-created_at']
    template_name = 'news/post_search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_create.html'
    permission_required = 'news.add_post'

    def form_valid(self, form):
        user = self.request.user
        today = timezone.now().date()
        post_count_today = Post.objects.filter(
            author__user=user,
            created_at__date=today
        ).count()

        if post_count_today >= 3:
            form.add_error(None, ValidationError(
                "Вы не можете публиковать более трех постов в сутки."
            ))
            return self.form_invalid(form)

        post = form.save(commit=False)
        post.post_type = Post.NEWS
        return super().form_valid(form)


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_create.html'
    permission_required = 'news.change_post'


class NewsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = 'news.delete_post'


class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_create.html'
    permission_required = 'news.add_post'

    def form_valid(self, form):
        user = self.request.user
        today = timezone.now().date()

        post_count_today = Post.objects.filter(
            author__user=user,
            created_at__date=today
        ).count()

        if post_count_today >= 3:
            form.add_error(None, ValidationError(
                "Вы не можете публиковать более трех постов в сутки."
            ))
            return self.form_invalid(form)

        post = form.save(commit=False)
        post.post_type = Post.ARTICLE
        return super().form_valid(form)


class ArticleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_create.html'
    permission_required = 'news.change_post'


class ArticleDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = 'news.delete_post'


@login_required
def become_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        messages.success(request, 'Поздравляем, вы теперь автор!')
    else:
        messages.info(request, 'Вы уже являетесь автором.')

    return redirect('/news/')

@login_required # Только для залогиненных
def toggle_subscription(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    user = request.user

    if category.subscribers.filter(id=user.id).exists():
        category.subscribers.remove(user)
        messages.info(request, f'Вы отписались от категории: {category.name}')
    else:
        category.subscribers.add(user)
        messages.success(request, f'Вы подписались на категорию: {category.name}')

    return redirect(request.META.get('HTTP_REFERER', '/news/'))