"""ECGO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""


from django.conf.urls import include, url
from django.contrib import admin
from . import views
import Gamble.views as g
admin.autodiscover()

urlpatterns = [

    url(r'^homepage/$', g.homepage),
    url(r'^accounts/logout/$', g.Logout),
    url(r'^accounts/register/$', g.register),
    url(r'^errors/pwdnotmatch/$', g.passworderrors),
    url(r'^errors/regerror/$', g.registererrors),
    url(r'^accounts/login/$', g.Login),
    url(r'^errors/login/$', g.loginerrors),
    url(r'^accounts/profile/$', g.profile),
    url(r'^successful/register/$', g.successful),
    url(r'^match/$', g.match),
    url(r'^accounts/buy/', g.buy),
    url(r'^buybuybuy/$', g.reload),
    url(r'^errors/addvalue/$', g.adderror),
    #url(r'^match/$', g.buy),
    url(r'^teams/get/$', g.result),
    url(r'^errors/cannotbuy/$', g.matchfinisherr),
    url(r'^errors/notexistid/$', g.matchnotfound),
    url(r'^errors/nomoney/$', g.valueisnotenough),
    url(r'^successful/$', g.success),
    url(r'^successful/addvalue/$', g.addvaluedone),
    url(r'^errors/informationwrong/$', g.addvalueerror),
    url(r'^usersinfo/$', g.printinfo),
    url(r'^record/$', g.record),
    url(r'^pending/$', g.pending),



############Team URL:###########


    url(r'^teams/get/AFC Ajax/$', g.AFC_Ajax),
    url(r'^teams/get/APOEL FC/$', g.APOEL_FC),
    url(r'^teams/get/Arsenal FC/$', g.Arsenal_FC),
    url(r'^teams/get/FC Astana/$', g.FC_Astana),
    url(r'^teams/get/FC Barcelona/$', g.FC_Barcelona),
    url(r'^teams/get/FC Basel 1893/$', g.FC_Basel_1893),
    url(r'^teams/get/FC BATE Borisov/$', g.FC_BATE_Borisov),
    url(r'^teams/get/SL Benfica/$', g.SL_Benfica),
    url(r'^teams/get/Celtic FC/$', g.Celtic_FC),
    url(r'^teams/get/Chelsea FC/$', g.Chelsea_FC),
    url(r'^teams/get/Club Brugge KV/$', g.Club_Brugge_KV),
    url(r'^teams/get/Crusaders FC/$', g.Crusaders_FC),
    url(r'^teams/get/PFC CSKA Moskva/$', g.PFC_CSKA_Moskva),
    url(r'^teams/get/FC Dila Gori/$', g.FC_Dila_Gori),
    url(r'^teams/get/GNK Dinamo Zagreb/$', g.GNK_Dinamo_Zagreb),
    url(r'^teams/get/Dundalk FC/$', g.Dundalk_FC),
    url(r'^teams/get/FC Dynamo Kyiv/$', g.FC_Dynamo_Kyiv),
    url(r'^teams/get/FC Santa Coloma/$', g.FC_Santa_Coloma),
    url(r'^teams/get/CS Fola Esch/$', g.CS_Fola_Esch),
    url(r'^teams/get/SS Folgore/$', g.SS_Folgore),
    url(r'^teams/get/KAA Gent/$', g.KAA_Gent),
    url(r'^teams/get/Hibernians FC/$', g.Hibernians_FC),
    url(r'^teams/get/HJK Helsinki/$', g.HJK_Helsinki),
    url(r'^teams/get/Juventus/$', g.Juventus),
    url(r'^teams/get/SS Lazio/$', g.SS_Lazio),
    url(r'^teams/get/FC Levadia Tallinn/$', g.FC_Levadia_Tallinn),
    url(r'^teams/get/Bayer 04 Leverkusen/$', g.Bayer_04_Leverkusen),
    url(r'^teams/get/Lincoln FC/$', g.Lincoln_FC),
    url(r'^teams/get/PFC Ludogorets Razgrad/$', g.PFC_Ludogorets_Razgrad),
    url(r'^teams/get/Olympique Lyonnais/$', g.Olympique_Lyonnais),
    url(r'^teams/get/Maccabi Tel-Aviv FC/$', g.Maccabi_Tel_Aviv_FC),
    url(r'^teams/get/Manchester City FC/$', g.Manchester_City_FC),
    url(r'^teams/get/Manchester United FC/$', g.Manchester_United_FC),
    url(r'^teams/get/NK Maribor/$', g.NK_Maribor),
    url(r'^teams/get/FC Midtjylland/$', g.FC_Midtjylland),
    url(r'^teams/get/FC Milsami Orhei/$', g.FC_Milsami_Orhei),
    url(r'^teams/get/Molde FK/$', g.Molde_FK),
    url(r'^teams/get/AS Monaco FC/$', g.AS_Monaco_FC),
    url(r'^teams/get/Olympiacos FC/$', g.Olympiacos_FC),
    url(r'^teams/get/Panathinaikos FC/$', g.Panathinaikos_FC),
    url(r'^teams/get/Paris Saint-Germain/$', g.Paris_Saint_Germain),
    url(r'^teams/get/FK Partizan/$', g.FK_Partizan),
    url(r'^teams/get/FC Porto/$', g.FC_Porto),
    url(r'^teams/get/PSV Eindhoven/$', g.PSV_Eindhoven),
    url(r'^teams/get/FC Pyunik/$', g.FC_Pyunik),
    url(r'^teams/get/SK Rapid Wien/$', g.SK_Rapid_Wien),
    url(r'^teams/get/Real Madrid CF/$', g.Real_Madrid_CF),
    url(r'^teams/get/AS Roma/$', g.AS_Roma),
    url(r'^teams/get/FK Rudar Pljevlja/$', g.FK_Rudar_Pljevlja),
    url(r'^teams/get/FC Salzburg/$', g.FC_Salzburg),
    url(r'^teams/get/FK Sarajevo/$', g.FK_Sarajevo),
    url(r'^teams/get/Sevilla FC/$', g.Sevilla_FC),
    url(r'^teams/get/FC Shakhtar Donetsk/$', g.FC_Shakhtar_Donetsk),
    url(r'^teams/get/AC Sparta Praha/$', g.AC_Sparta_Praha),
    url(r'^teams/get/Sporting Clube de Portugal/$', g.Sporting_Clube_de_Portugal),
    url(r'^teams/get/Stjarnan/$', g.Stjarnan),
    url(r'^teams/get/The New Saints FC/$', g.The_New_Saints_FC),
    url(r'^teams/get/Valencia CF/$', g.Valencia_CF),
    url(r'^teams/get/FK Vardar/$', g.FK_Vardar),
    url(r'^teams/get/FK Ventspils/$', g.FK_Ventspils),
    url(r'^teams/get/Videoton FC/$', g.Videoton_FC),
    url(r'^teams/get/FK Vardar/$', g.FK_Vardar),
    url(r'^teams/get/FK Ventspils /$', g.FK_Ventspils ),
    url(r'^teams/get/Videoton FC/$', g.Videoton_FC),
    url(r'^teams/get/VfL Wolfsburg/$', g.VfL_Wolfsburg),
    url(r'^teams/get/BSC Young Boys/$', g.BSC_Young_Boys),
    url(r'^teams/get/FC Zenit/$', g.FC_Zenit),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^$', views.index)
]