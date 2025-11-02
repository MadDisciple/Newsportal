from django import forms
from django.core.exceptions import ValidationError
from .models import Post
from allauth.account.forms import LoginForm, SignupForm

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'categories',
            'title',
            'text',
        ]

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