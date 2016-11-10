import os
import urllib2
import re
import MySQLdb
import random

os.environ['DJANGO_SETTINGS_MODULE'] = 'ECGO.settings'
import Gamble.models as g
db = MySQLdb.connect('localhost','root','921026','ECGO_database')
cur = db.cursor()
db.set_character_set('utf8')
root_url = 'http://www.uefa.com'
url = 'http://www.uefa.com/uefachampionsleague/season=2016/standings/index.html'
try:
	request = urllib2.Request(url)
	response = urllib2.urlopen(request)
	content = response.read().decode('utf-8')
	pattern = re.compile('<div class="standings_group_link more innerText"><a title="" href="(.*?)".*?</a></div>',re.S)
	group_urls = re.findall(pattern, content)
	scorehost = []
	scoreguest = []
	for i in range(len(group_urls)):
		try:
			g_url = root_url + group_urls[i]
			g_request = urllib2.Request(g_url)
			g_response = urllib2.urlopen(g_request)
			g_content  = g_response.read().decode('utf-8')
			host_pattern = re.compile('<td class="r  home nob"><a href="/uefachampionsleague/season=2016/clubs/club=.*?>(.*?)</a></td>',re.S)
			guest_pattern = re.compile('<td class="l  away nob"><a href="/uefachampionsleague/season=2016/clubs/club=.*?>(.*?)</a></td>',re.S)
			date_pattern  = re.compile('<span class="b dateT".*?>(.*?) </span>')
			stadium_pattern = re.compile('<span class="stadium_name">(.*?), </span><span.*?>')
			score_pattern  = re.compile('<td class="c b score nob"><a class="sc" href=".*?>(.*?)<span class="minusResult">-</span>(.*?)</a>')
			score = re.findall(score_pattern, g_content)
			stadium = re.findall(stadium_pattern, g_content)
			date = re.findall(date_pattern, g_content)
			host = re.findall(host_pattern, g_content)
			guest = re.findall(guest_pattern, g_content)
			for x in range(len(host)):
				if x > (len(score)-1):
					score.append([None,None])
				scorehost.append(score[x][0])
				scoreguest.append(score[x][1])
				# print host[x],guest[x], score[x][0], score[x][1], stadium[x], date[x], random.uniform(1.1,7.6), random.uniform(1.1,7.6), random.uniform(1.1,7.6)
				b = g.match(id=(i+97),hostteam = host[x], guestteam = guest[x], score_host = score[x][0],score_guest = score[x][1],description = stadium[x],date = date[x],odd_win = random.uniform(1.1,2.3),odd_even = random.uniform(1.5,2.9),odd_lose = random.uniform(1.3,2.8))
				b.save()
				# personInfo = '", "'.join([host[x],guest[x], score[x][0], score[x][1], stadium[x], date[x], random.randint(1,7), random.randint(1,7), random.randint(1,7)])
				# sql = "INSERT INTO %s (%s) VALUES (%s)" % ('Gamble_match', 'hostteam,guestteam,score_host,score_guest,description,date,odd_win,odd_even,odd_lose', '"'+personInfo+'"',)
				# try:
				# 	result = cur.excute(sql)
				# 	insert_id = db.insert_id()
				# 	db.commit()
				# 	if result:
				# 		print insert_id
				# except MySQLdb.Error, e:
				# 	print e.args[0], e.args[1]
				# 	print 'wrong'
				# print x
		except urllib2.URLError, ee:
			if hasattr(ee, "code"):
				print ee.code
			if hasattr(ee, "reason"):
				print ee.reason
	n = g.match.objects.all()
	for i in range(len(n)):
		print scorehost[i]
		n[i].odd_win = random.uniform(1.1,2.3)
		n[i].odd_even = random.uniform(1.5,2.9)
		n[i].odd_lose = random.uniform(1.3,2.8)
		n[i].save()
		if n[i].score_host is not None:
			n[i].save()
except urllib2.URLError, e:
	if hasattr(e, "code"):
		print e.code
	if hasattr(e, "reason"):
		print e.reason