from django.contrib import admin

# Register your models here.
from .models import user, team, match,  wager, battleArray, player, Ability


# # Register your models here.
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'email', 'username')
#
#
# class AccountManagerAdmin(admin.ModelAdmin):
#     list_display = ('accountNumber', 'balance')
#
#
# class TeamAdmin(admin.ModelAdmin):
#     list_display = ('teamname', 'coach')
#
#
# class MatchAdmin(admin.ModelAdmin):
#     list_display = ('id', 'hostteam', 'time', 'score', 'odd', 'description')
#
#
# # class WagerAdmin(admin.ModelAdmin):
# #     list_display = ('id', 'user', 'fund', 'match')
#
#
# class BattleArrayAdmin(admin.ModelAdmin):
#     list_display = ('id', 'match')
#
#
# class GroupStageTeamAdmin(admin.ModelAdmin):
#     list_display = ('score', 'goaldifference', 'id', 'teamname', 'coach')
#
#
# class playerAdmin(admin.ModelAdmin):
#     list_display = ('id', 'team', 'name', 'age', 'position', 'height', 'country', 'number', 'score')


admin.site.register(user)
admin.site.register(team)
admin.site.register(match)
admin.site.register(wager)
admin.site.register(battleArray)
admin.site.register(player)
admin.site.register(Ability)