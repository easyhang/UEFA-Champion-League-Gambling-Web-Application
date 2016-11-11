import urllib2
import re
import MySQLdb
import os


os.environ['DJANGO_SETTINGS_MODULE'] = 'ECGO.settings'
import Gamble.models as g
db = MySQLdb.connect('localhost','root','921026','ECGO_database')
cur = db.cursor()
db.set_character_set('utf8')
root_url = 'http://www.uefa.com'
url = 'http://www.uefa.com/uefachampionsleague/season=2016/clubs/atoz/index.html'
try:
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    content = response.read().decode('utf-8')
    pattern = re.compile('<td class="l"><a href="(.*?)".*?</a></td>',re.S)
    team_urls = re.findall(pattern,content)

    i = 0

    for item in team_urls:
        try:
            index_url = root_url + item
            requestindex = urllib2.Request(index_url)
            responsetext = urllib2.urlopen(requestindex)
            contentindex = responsetext.read().decode('utf-8')
            patternofteam = re.compile('<td class="playername l"><a href="(.*?)".*?</td>',re.S)
            teamnamepatt = re.compile('<h1 class="bigTitle"><a href.*?">(.*?)</a></h1>')
            person_urls = re.findall(patternofteam,contentindex)
            teamname = re.findall(teamnamepatt,contentindex)
            
        except urllib2.URLError, eee:
            if hasattr(eee, "code"):
                print eee.code
            if hasattr(eee, "reason"):
                print eee.reason
        j = 0
        print i
        personinfo = []
        if i not in [24,30,50,54,66,69,76]:
            print teamname
            print i
            for person in person_urls:
                try:
                    personPage = root_url + person
                    p_request = urllib2.Request(personPage)
                    p_response = urllib2.urlopen(p_request)
                    p_content = p_response.read().decode('utf-8')
                    p_pattern = re.compile('<div class="infoBox">(.*?)</div>',re.S)
                    p_info    = re.findall(p_pattern, p_content)
                except  urllib2.URLError, err:
                    if hasattr(err, "code"):
                        print err.code
                    if hasattr(err, "reason"):
                        print err.reason
                    continue
                for info in p_info:
                    text = []
                    replaceUL = re.compile('<ul class="innerText">|</ul>')
                    replaceLI = re.compile('<li>|<li class=.*?>')
                    replaceLi = re.compile('</li>')
                    repalceSPAN = re.compile('<span>|<span class.*?>|</span>')
                    replaceA = re.compile('<a href.*?>|</a>')
                    replaceBR = re.compile('<br />')
                    AgePattern = re.compile('((.*?))',re.S)
                    info = re.sub(replaceLI, "", info)
                    info = re.sub(replaceUL,"", info)
                    info = re.sub(repalceSPAN, "", info)
                    info = re.sub(replaceBR,"",info)
                    info = re.sub(replaceA,"", info)
                    info = re.sub(replaceLi,":",info)
                    text.append(map(unicode,info.split(':')))
                    
                    for x in range(len(text[0])):
                        if text[0][x] == 'Name':
                            playername = text[0][x+1]
                        if 'Position' in text[0][x]:
                            playerPos = text[0][x+1]
                        if text[0][x] == 'Date of birth (Age)':
                            Age = text[0][x+1][13:15]
                        if x == 11:
                            Clubname = text[0][x]
                        if text[0][x] == 'Height':
                            Height = text[0][x+1]
                        if text[0][x] == 'Squad number':
                            Number = text[0][x+1]
                        if text[0][x] == 'Goals':
                            Goal = text[0][x+1]
                        if text[0][x] == 'Country':
                            Country = text[0][x+1]

                    print j
                    j += 1
                    print type(teamname[0])
                    print str(teamname)
                    r = g.team.objects.get(teamname = teamname[0])
                    b = g.player(team = r, name = playername,age=int(Age), position= playerPos, height = int(Height[:4]), country = Country, number = int(Number), score= int(Goal))
                    b.save()
                    print playername, playerPos, Age, Clubname, Height, Number, Goal, Country
                personinfo.append(text)
        i += 1

except urllib2.URLError, e:
    if hasattr(e, "code"):
        print e.code
    if hasattr(e, "reason"):
        print e.reason
