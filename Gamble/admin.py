from django.contrib import admin

# Register your models here.
from .models import user, team, match,  wager, battleArray, player, Ability

admin.site.register(user)
admin.site.register(team)
admin.site.register(match)
admin.site.register(wager)
admin.site.register(battleArray)
admin.site.register(player)
admin.site.register(Ability)
