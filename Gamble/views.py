from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponseRedirect
import Gamble.models as g
from .forms import *
import json


login = False
username = ''
user = ''
message = ''
pend = []

def homepage(request):
    global login, username, user
    teams = g.team.objects.all()
    if request.method == "POST":
        search_form = UserForm(request.POST)
        if not search_form.is_valid():
            team = search_form.cleaned_data['username']
        try:
            t = g.team.objects.filter(teamname__icontains=team)
            return render_to_response('Result.html', {'teamname': t})
        except:
            return HttpResponseRedirect('/homepage/')
    else:
        search_form = UserForm()
    return render(request, 'homepage.html', {'teams': teams, 'Login': login, 'Username': username, 'user_form': search_form, 'Superuser': user})

def printinfo(request):
    all = g.user.objects.all()
    return render(request, 'printinfo.html', {'ALL': all})

def record(request):
    rec = g.wager.objects.all()
    return render(request, 'Record.html', {'Record': rec})

def pending(request):
    global pend
    rec = g.wager.objects.all()
    for i in range(len(rec)):
        if rec[i].match.score_host is None or rec[i].done is True:
            continue
        if rec[i].match.score_host > rec[i].match.score_guest:
            r = 'win'
        if rec[i].match.score_host == rec[i].match.score_guest:
            r = 'tie'
        if rec[i].match.score_host < rec[i].match.score_guest:
            r = 'lose'
        if r == rec[i].option and r == 'win':
            rec[i].users.balance += rec[i].fund * rec[i].match.odd_win
        if r == rec[i].option and r == 'tie':
            rec[i].users.balance += rec[i].fund * rec[i].match.odd_even
        if r == rec[i].option and r == 'lose':
            rec[i].users.balance += rec[i].fund * rec[i].match.odd_lose
        rec[i].users.save()
        rec[i].done = True
        rec[i].save()
    if request.method == "POST":
        pen_form = UserForm(request.POST)
        search_form = UserForm(request.POST)
        if not search_form.is_valid():
            decision = search_form.cleaned_data['username']
        if decision == 'yes':
            for p in pend:
                p.save()
                del p
            return HttpResponseRedirect('/homepage/')
        else:
            return HttpResponseRedirect('/homepage/')
    else:
        pen_form = UserForm()
    return render(request, 'Pending.html', {'user_form': pen_form, 'PEND': pend})


def register(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        #print request.POST
        if user_form.is_valid():
            user_name = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            password_confirm = user_form.cleaned_data['password_confirm']
            email = user_form.cleaned_data['email']
            if password_confirm != password:
                return HttpResponseRedirect('/errors/pwdnotmatch/')
            try:
                g.user.objects.get(username=user_name)
                return HttpResponseRedirect('/errors/regerror/')
            except:
                user = g.user(email=email, username=user_name, password=password)
                user.save()
                return HttpResponseRedirect('/successful/register/')
    else:
        user_form = UserForm()
    return render(request, 'Register.html', {'user_form': user_form})


def Login(request):
    global username, login, user
    if request.method == "POST":
        login_form = UserForm(request.POST)
        #print request.POST
        if not login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
        try:
            user = g.user.objects.get(username=username, password=password)
            login = True
            return HttpResponseRedirect('/homepage/')
        except:
            return HttpResponseRedirect('/errors/login/')
    else:
        user_form = UserForm()
    return render(request, 'Login.html', {'user_form': user_form})


def Logout(request):
    global username, login
    login = False
    username = ''
    return render_to_response('logout.html', {'Login': login})


def match(request):
    global user, message
    match = g.match.objects.all().order_by('score_host')
    if request.method == "POST":
        buy_form = UserForm(request.POST)
        if not buy_form.is_valid():
            id = buy_form.cleaned_data['username']
        try:
            message = g.match.objects.get(id=id)
            if message.score_host is not None:
                return HttpResponseRedirect('/errors/cannotbuy/')
            else:
                return HttpResponseRedirect('/accounts/buy/'+id+'/')
        except:
            return HttpResponseRedirect('/errors/notexistid/')
    else:
        buy_form = UserForm()
    return render(request, 'match.html', {'user_form': buy_form, 'Match': match, 'User': user})
    #return render_to_response('match.html', {'Match': match, 'User': user})


def buy(request):
    global user, message
    if request.method == "POST":
        budget = UserForm(request.POST)
        if not budget.is_valid():
            balance = budget.cleaned_data['username']
            option = budget.cleaned_data['password']
            print type(balance)
        try:
            if user.balance <= int(balance):
                return HttpResponseRedirect('/errors/nomoney/')
            if option not in ['win', 'tie', 'lose']:
                return HttpResponseRedirect('/errors/nomoney/')
            else:
                user.balance = user.balance - int(balance)
                user.save()
                b = g.wager(users=user, fund=float(balance), match=message, done=False, option=option)
                b.save()
                return HttpResponseRedirect('/successful/')
        except:
            return HttpResponseRedirect('/errors/informationwrong/')
    else:
        budget = UserForm()
    return render(request, 'gamble.html', {'user_form': budget, 'User': user, 'Message': message})


def reload(request):
    global user, pend
    if request.method == "POST":
        login_form = UserForm(request.POST)
        #print request.POST
        if not login_form.is_valid():
            value = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
        if user.password == password:
            if user.balance is None:
                user.balance = int(value)
                pend.append(user)
                # user.save()
            else:
                user.balance += int(value)
                pend.append(user)
                # user.save()
            return HttpResponseRedirect('/successful/addvalue')
        else:
            return HttpResponseRedirect('/errors/addvalue/')
    else:
        login_form = UserForm()
    return render(request, 'Reload.html', {'user_form': login_form, 'User': user})


def AFC_Ajax(request):
    a = g.team.objects.get(teamname='AFC Ajax')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host = []
    visit = []
    ability = []

    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})


def APOEL_FC(request):
    a = g.team.objects.get(teamname='APOEL FC')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})


def Arsenal_FC(request):
    a = g.team.objects.get(teamname='Arsenal FC')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})


def FC_Astana(request):
    a = g.team.objects.get(teamname='FC Astana')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})


def FC_Barcelona(request):
    a = g.team.objects.get(teamname='FC Barcelona')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})


def FC_Basel_1893(request):
    a = g.team.objects.get(teamname='FC Basel 1893')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})


def FC_BATE_Borisov(request):
    a = g.team.objects.get(teamname='FC BATE Borisov')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})


def SL_Benfica(request):
    a = g.team.objects.get(teamname='SL Benfica')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})


def Celtic_FC(request):
    a = g.team.objects.get(teamname='Celtic FC')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})


def Chelsea_FC(request):
    a = g.team.objects.get(teamname='Chelsea FC')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    # print json.dumps(a.id)
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})


def Club_Brugge_KV(request):
    a = g.team.objects.get(teamname='Club Brugge KV')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})


def Crusaders_FC(request):
    a = g.team.objects.get(teamname='Crusaders FC')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})


def PFC_CSKA_Moskva(request):
    a = g.team.objects.get(teamname='PFC CSKA Moskva')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})


def FC_Dila_Gori(request):
    a = g.team.objects.get(teamname='FC Dila Gori')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})


def GNK_Dinamo_Zagreb(request):
    a = g.team.objects.get(teamname='GNK Dinamo Zagreb')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})


def Dundalk_FC(request):
    a = g.team.objects.get(teamname='Dundalk FC')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})


def FC_Dynamo_Kyiv(request):
    a = g.team.objects.get(teamname='FC Dynamo Kyiv')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})



def FC_Santa_Coloma(request):
    a = g.team.objects.get(teamname='FC Santa Coloma')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})




def CS_Fola_Esch(request):
    a = g.team.objects.get(teamname='CS Fola Esch')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})


def SS_Folgore(request):
    a = g.team.objects.get(teamname='SS Folgore')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})


def KAA_Gent(request):
    a = g.team.objects.get(teamname='KAA Gent')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})


def Hibernians_FC(request):
    a = g.team.objects.get(teamname='Hibernians FC')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def HJK_Helsinki(request):
    a = g.team.objects.get(teamname='HJK Helsinki')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'HJK Helsinki.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def Juventus(request):
    a = g.team.objects.get(teamname='Juventus')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def SS_Lazio(request):
    a = g.team.objects.get(teamname='SS Lazio')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def FC_Levadia_Tallinn(request):
    a = g.team.objects.get(teamname='FC Levadia Tallinn')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})


def Bayer_04_Leverkusen(request):
    a = g.team.objects.get(teamname='Bayer 04 Leverkusen')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def Lincoln_FC(request):
    a = g.team.objects.get(teamname='Lincoln FC')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def PFC_Ludogorets_Razgrad(request):
    a = g.team.objects.get(teamname='PFC Ludogorets Razgrad')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def Olympique_Lyonnais(request):
    a = g.team.objects.get(teamname='Olympique Lyonnais')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})


def Maccabi_Tel_Aviv_FC(request):
    a = g.team.objects.get(teamname='Maccabi Tel-Aviv FC')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})


def Manchester_City_FC(request):
    a = g.team.objects.get(teamname='Manchester City FC')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def Manchester_United_FC(request):
    a = g.team.objects.get(teamname='Manchester United FC')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def NK_Maribor(request):
    a = g.team.objects.get(teamname='NK Maribor')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def FC_Midtjylland(request):
    a = g.team.objects.get(teamname='FC Midtjylland')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def FC_Milsami_Orhei(request):
    a = g.team.objects.get(teamname='FC Milsami Orhei')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def Molde_FK(request):
    a = g.team.objects.get(teamname='Molde FK')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def AS_Monaco_FC (request):
    a = g.team.objects.get(teamname='AS Monaco FC')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def Olympiacos_FC(request):
    a = g.team.objects.get(teamname='Olympiacos FC')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def Panathinaikos_FC(request):
    a = g.team.objects.get(teamname='Panathinaikos FC')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def Paris_Saint_Germain(request):
    a = g.team.objects.get(teamname='Paris Saint-Germain')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})



def FK_Partizan(request):
    a = g.team.objects.get(teamname='FK Partizan')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def FC_Porto(request):
    a = g.team.objects.get(teamname='FC Porto')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})


def PSV_Eindhoven(request):
    a = g.team.objects.get(teamname='PSV Eindhoven')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def FC_Pyunik(request):
    a = g.team.objects.get(teamname='FC Pyunik')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def SK_Rapid_Wien(request):
    a = g.team.objects.get(teamname='SK Rapid Wien')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def Real_Madrid_CF(request):
    a = g.team.objects.get(teamname='Real Madrid CF')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def AS_Roma(request):
    a = g.team.objects.get(teamname='AS Roma')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def FK_Rudar_Pljevlja(request):
    a = g.team.objects.get(teamname='FK Rudar Pljevlja')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def FC_Salzburg(request):
    a = g.team.objects.get(teamname='FC Salzburg')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def FK_Sarajevo(request):
    a = g.team.objects.get(teamname='FK Sarajevo')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def Sevilla_FC(request):
    a = g.team.objects.get(teamname='Sevilla FC')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def FC_Shakhtar_Donetsk(request):
    a = g.team.objects.get(teamname='FC Shakhtar Donetsk')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def AC_Sparta_Praha(request):
    a = g.team.objects.get(teamname='AC Sparta Praha')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def Sporting_Clube_de_Portugal(request):
    a = g.team.objects.get(teamname='Sporting Clube de Portugal')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})



def Stjarnan(request):
    a = g.team.objects.get(teamname='Stjarnan')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def The_New_Saints_FC(request):
    a = g.team.objects.get(teamname='The New Saints FC')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def Valencia_CF(request):
    a = g.team.objects.get(teamname='Valencia CF')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def FK_Vardar(request):
    a = g.team.objects.get(teamname='FK Vardar')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def FK_Ventspils(request):
    a = g.team.objects.get(teamname='FK Ventspils')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def Videoton_FC(request):
    a = g.team.objects.get(teamname='Videoton FC')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def VfL_Wolfsburg(request):
    a = g.team.objects.get(teamname='VfL Wolfsburg')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def BSC_Young_Boys(request):
    a = g.team.objects.get(teamname='BSC Young Boys')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})

def FC_Zenit(request):
    a = g.team.objects.get(teamname='FC Zenit')
    p = g.player.objects.filter(team__teamname=a.teamname).order_by('position')
    b = g.match.objects.all()
    host =[]
    visit = []
    ability = []
    for i in range(len(b)):
        if b[i].hostteam in a.teamname:
            host.append(b[i])
        if b[i].guestteam in a.teamname:
            visit.append(b[i])
            print b[i].score_guest
    for i in range(len(p)):
        ab = g.Ability.objects.get(key=p[i].id)
        ability.append(ab)
    return render(request, 'teaminfo.html', {'Host': host, 'Visit': visit, 'team': a, 'Player': p, 'Ability': ability})
# def search(request):
#     if request.method == "POST":
#         search_form = UserForm(request.POST)
#         if not search_form.is_valid():
#             team = search_form.cleaned_data['username']
#         try:
#             t = g.team.objects.filter(teamname__icontains=team)
#             return render_to_response('Result.html', {'teamname': t})
#         except:
#             return HttpResponseRedirect('/homepage/')
#     else:
#         search_form = UserForm()
#     return render(request, 'search.html', {'user_form': search_form})


def successful(request):
    return render(request, "successful.html",)


def profile(request):
    p = g.user.objects.get(username=username)
    return render(request, 'profile.html', {'name': p.username, 'Balance': p.balance})


def passworderrors(request):
    return render(request, "passworderrors.html",)


def registererrors(request):
    return render(request, "registererrors.html",)


def loginerrors(request):
    return render(request, "loginerrors.html",)

def result(request):
    return render(request, "Result.html",)

def adderror(request):
    return render(request, "WrongValue.html")

def matchfinisherr(request):
    return render(request, "matchfinish.html")

def matchnotfound(request):
    return render(request, "match not found.html")

def valueisnotenough(request):
    return render(request, "Value not enough.html")

def addvaluedone(request):
    return render(request, "addvaluedone.html")

def addvalueerror(request):
    return render(request, "addvalueerror.html")

def success(request):
    return render(request,"success.html")