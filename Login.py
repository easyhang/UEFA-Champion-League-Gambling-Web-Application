import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'ECGO.settings'
import Gamble.models as g

while 1:
    username = raw_input('############Please input your username############\n')
    password = raw_input('############Please input your password############\n')
    try:
        u = g.user.objects.get(username=username, password=password)
        print '############Login success!!############\n'
        break
    except:
        print '############Username not exist or password is incorrect!!!############\n'
        continue

print 'username is ', u.username
print 'email is', u.email
print 'balance is', u.balance