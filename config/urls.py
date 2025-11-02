from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/news/', permanent=True)),
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),
    path('articles/', include('news.urls_articles')),
    path('accounts/', include('allauth.urls')),
]
