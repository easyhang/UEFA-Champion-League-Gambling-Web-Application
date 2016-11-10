import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'ECGO.settings'
import Gamble.models as g

while 1:
    username = raw_input('############Please input your username############\n')
    try:
        g.user.objects.get(username=username)
        print '############username has been Registered. Please use another name.############\n'
        continue
    except:
        break
while 1:
    password = raw_input('############Please input your new password############\n')
    ensure = raw_input('############Please repeat your new password############\n')
    if password != ensure:
        print '############Two inputted Passwords not match!############\n'
        continue
    else:
        break
while 1:
    email = raw_input('############Please input your email############\n')
    if '@' not in email:
        print '########### Please input correct email!!###########\n'
        continue
    else:
        break

balance = raw_input('############How much values you want to add?############\n')

c = g.user(email=email, username=username, balance=balance, password=password)
c.save()

print '############ Congratuation!!!! You sucesses create a user!!! ############\n'