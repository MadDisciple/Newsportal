from django.urls import path
from .views import (
    PostList, PostDetail, PostSearch,
    NewsCreate, NewsUpdate, NewsDelete,
    become_author
)

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),

    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),

    path('search/', PostSearch.as_view(), name='post_search'),

    path('create/', NewsCreate.as_view(), name='news_create'),

    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),

    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),

    path('become_author/', become_author, name='become_author'),
]