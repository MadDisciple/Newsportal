from django import forms
from django.core.exceptions import ValidationError
from .models import Post
from allauth.account.forms import LoginForm, SignupForm
from django.utils.translation import gettext_lazy as _


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'categories',
            'title',
            'text',
        ]

    def clean(self):
        cleaned_data = super().clean()

        text = cleaned_data.get("text")
        title = cleaned_data.get("title")

        if text is not None and len(text) < 20:
            raise ValidationError({
                "text": _("Текст статьи не может быть менее 20 символов.")
            })

        if title == text:
            raise ValidationError(
                _("Текст статьи не должен быть идентичным заголовку.")
            )

        return cleaned_data


class CustomLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class CustomSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})