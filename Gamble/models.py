from django.db import models

# Create your models here.
class user(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=300)
    username = models.CharField(max_length=200)
    balance = models.FloatField(blank=True, null=True)
    password = models.CharField(max_length=20)
    superuser = models.BooleanField(default=False)


class team(models.Model):
    # id = models.AutoField(primary_key=True)
    teamname = models.CharField(primary_key=True, max_length=200)
    coach = models.CharField(max_length=200)

    def __unicode__(self):
        return self.teamname


class match(models.Model):
    id = models.AutoField(primary_key=True)
    hostteam = models.CharField(max_length=200, null=True)
    guestteam = models.CharField(max_length=200, null=True)
    score_host = models.IntegerField(null=True)
    score_guest = models.IntegerField(null=True)
    description = models.TextField(max_length=2000, null=True)
    date = models.CharField(null=True, max_length=300)
    odd_win = models.FloatField(null=True)
    odd_even = models.FloatField(null=True)
    odd_lose = models.FloatField(null=True)
    done = models.BooleanField(default=False)


class wager(models.Model):
    id = models.AutoField(primary_key=True)
    users = models.ForeignKey(user, on_delete=models.CASCADE)
    fund = models.FloatField()
    match = models.ForeignKey(match, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)
    option = models.CharField(max_length=100)

class battleArray(models.Model):
    id = models.AutoField(primary_key=True)
    match = models.ForeignKey(match, on_delete=models.CASCADE)
    array = models.CharField(max_length=200, null=True)
    description = models.TextField(max_length=2000)


class player(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(team, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    # club = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    height = models.FloatField()
    country = models.CharField(max_length=200)
    number = models.IntegerField()
    score = models.IntegerField()

    def __unicode__(self):
        return self.name


class Ability(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.ForeignKey(player, on_delete=models.CASCADE)
    speed = models.FloatField()
    attack = models.FloatField()
    technique = models.FloatField()
    sta = models.FloatField()
    defence = models.FloatField()
    power = models.FloatField()

