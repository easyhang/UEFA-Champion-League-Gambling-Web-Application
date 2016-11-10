import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'ECGO.settings'
import Gamble.models as g
# p = 'FC Steaua Bucure?ti'
# r =  g.team.objects.get(teamname = unicode(p))
# print type(r)
#
# b.save()
# a = g.team.objects.filter(teamname__icontains='AS Roma')
# b = g.match.objects.all()
# for i in range(len(b)):
#     if b[i].hostteam in a[0].teamname:
#         print b[i].hostteam
#     if b[i].guestteam in a[0].teamname:
#         print b[i].guestteam

# a = g.match(hostteam="guozu", guestteam="meiguo", des)
# a.save()


# class Ability(models.Model):
#     id = models.AutoField(primary_key=True)
#     key = models.ForeignKey(player, on_delete=models.CASCADE)
#     speed = models.FloatField()
#     attack = models.FloatField()
#     technique = models.FloatField()
#     sta = models.FloatField()
#     defence = models.FloatField()
#     power = models.FloatField()
# team = models.ForeignKey(team, on_delete=models.CASCADE)
#     name = models.CharField(max_length=200)
#     age = models.IntegerField()
#     # club = models.CharField(max_length=200)
#     position = models.CharField(max_length=200)
#     height = models.FloatField()
#     country = models.CharField(max_length=200)
#     number = models.IntegerField()
#     score = models.IntegerField()