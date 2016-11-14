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


# class TeamForm(ModelForm):
#     class Meta:
#         model = mo.team
#         field = [
#             'teamname',
#             'coach'
#         ]
#
# class MatchForm(ModelForm):
#     class Meta:
#         model = mo.match
#         field = [
#             'date',
#             'score',
#             'odd',
#             'description'
#         ]
#         exclude = [
#             'id',
#             'hostness',
#             'team'
#         ]
#
#
# class WagerForm(ModelForm):
#     class Meta:
#         model = mo.wager
#         field = [
#             'user',
#             'fund',
#             'match'
#         ]
#         exclude = [
#             'id',
#             'done'
#         ]
#
#
# class BattleArrayForm(ModelForm):
#     class Meta:
#         model = mo.battleArray
#         field = [
#             'description',
#             'array',
#         ]
#         exclude = [
#             'id',
#             'match'
#         ]
#
#
# class PlayerForm(ModelForm):
#     class Meta:
#         model = mo.player
#         field = [
#             'team',
#             'name',
#             'age',
#             'positon',
#             'height',
#             'country',
#             'number',
#             'score'
#         ]
#         exclude = [
#             'id'
#         ]
#
#
# class AbilityrForm(ModelForm):
#     class Meta:
#         model = mo.Ability
#         field = [
#             'speed',
#             'attack',
#             'technique',
#             'sta',
#             'defence',
#             'power'
#         ]
#         exclude = [
#             'id',
#             'key'
#         ]