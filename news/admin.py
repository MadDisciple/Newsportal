from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Author, Category, Post, PostCategory, Comment

@admin.register(Post)
class PostAdmin(TranslationAdmin):
    list_display = ('title', 'author', 'post_type', 'rating', 'created_at')
    list_filter = ('post_type', 'author', 'categories', 'created_at')
    search_fields = ('title', 'text')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating')
    search_fields = ('user__username',)


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'get_text_preview', 'rating', 'created_at')
    list_filter = ('created_at', 'rating', 'user')
    search_fields = ('text', 'user__username', 'post__title')
    readonly_fields = ('created_at',)

    def get_text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    get_text_preview.short_description = 'Текст (превью)'


admin.site.register(PostCategory)