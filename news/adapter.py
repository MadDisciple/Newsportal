from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)

        if commit:
            user.save()
            common_group = Group.objects.get(name='common')
            common_group.user_set.add(user)
        return user