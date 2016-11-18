from django import forms
from django.forms import ModelForm
import Gamble.models as mo



class AddForm(forms.Form):
    a = forms.CharField()
    #b = forms.IntegerField()


class UserForm(ModelForm):
    password_confirm = forms.CharField()
    class Meta:
        model = mo.user
        field = [
            'username',
            'password',
            'email',
            'password'
        ]
        exclude = [
            'groups',
            'user_permissions',
            'is_staff',
            'is_active',
            'is_superuser',
            'last_login',
            'date_joined'
        ]


class LoginForm(ModelForm):
    class Meta:
        model = mo.user
        field = [
            'username',
            'password',
            'email',
            'password'
        ]
        exclude = [
            'groups',
            'user_permissions',
            'is_staff',
            'is_active',
            'is_superuser',
            'last_login',
            'date_joined'
        ]
