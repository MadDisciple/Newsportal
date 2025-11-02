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
from django.shortcuts import redirect
from django.contrib import messages



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