import django_filters
from django import forms
from .models import Post, Author


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок'
    )

    author = django_filters.ModelChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        label='Автор'
    )

    created_after = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='Дата (позже чем)',
        widget=forms.DateInput(
            attrs={'type': 'date'},
            format='%Y-%m-%d'
        )
    )

    class Meta:
        model = Post
        fields = ['title', 'author', 'created_after']