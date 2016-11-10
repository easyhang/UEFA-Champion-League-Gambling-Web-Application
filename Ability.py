'''
This model is to calculate ability of each of player, we use the function is based on sophisticated algorithm created by
our team. We analyse the age, height, score and other parameters of each of player to design this algorithm. This ability
of each player can basically reflect real performance of player but some difference may happen. But in reality,
performance cannot represent player's real ability, which would depend on many complicated factors like mood, psychological
quality, current status, circumstances as well as coach, etc. Therefore, These abilities of players would just be regard
as a reference in our gamble system.We encourage user betting based on these abilities. BUT WE HAVE NO DUTY TO BE
RESPONSIBLE FOR THE LOSS OF USERS FOR THEY MISUSE, MISUNDERSTAND THESE ABILITIES.

Without the original author or copyright holder's permission, the m  following pictures shall not be reproduced, modified
or used in any form.

Our team reserve all the right for the final explanation
'''




import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'ECGO.settings'
import Gamble.models as g
import random




for i in range(1, 2093):
    a = g.player.objects.get(id=i)
    speed = (100 - a.age * 2) * (100 - abs(a.height - 175))/100.0
    speed = int(speed)
    technique = random.randint(50, 100)
    if a.position == ' Defender':
        attack = 5 + (100 - a.age * 3) + int(a.score * 2.225) + int(speed * 0.15) + int(technique * 0.2)
    if a.position == ' Goalkeeper':
        attack = (100 - a.age * 3) + int(a.score * 2.225) + int(technique * 0.05)
    if a.position == ' Midfield':
        attack = 15 + (100 - a.age * 3) + int(a.score * 2.225) + int(speed * 0.15) + int(technique * 0.2)
    if a.position == ' Forward':
        attack = 30 + (100 - a.age * 3) + int(a.score * 2.225) + int(speed * 0.15) + int(technique * 0.2)
    if attack > 100:
        attack = 100
    if attack < 0:
        attack = 0
    sta = random.randint(50, 100)
    power = random.randint(50, 100)
    if a.position == ' Defender':
        defence = 30 + (100 - a.age * 3) + int(speed * 0.15) + int(power * 0.2)
    if a.position == ' Goalkeeper':
        defence = 25 + (100 - a.age * 3) + int(power * 0.2)
    if a.position == ' Midfield':
        defence = 15 + (100 - a.age * 3) + int(speed * 0.15) + int(power * 0.2)
    if a.position == ' Forward':
        defence = 5 + (100 - a.age * 3) + int(speed * 0.15) + int(power * 0.2)
    if defence > 100:
        defence = 100
    if defence < 0:
        defence = 0
    b = g.Ability(key=a, speed=speed, attack=attack, technique=technique, sta=sta, defence=defence, power=power)
    b.save()

