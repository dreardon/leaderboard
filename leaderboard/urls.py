"""leaderboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rank import views
from rank.views import editSprint, deleteSprint

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^(?P<sprintid>[0-9]+)/$', views.ranking, name='ranking'),
    url(r'^$', views.ranking, name='ranking'),
    url(r'^dataentry/', views.dataEntry, name='dataentry'),
    url(r'^updatecommits/', views.updateCommits, name='updatecommits'),
    url(r'^ranking/delete/(?P<rankingId>[0-9]+)/$', views.deleteRanking, name='deleteranking'),
    url(r'^ranking/edit/(?P<rankingId>[0-9]+)/$', views.editRanking, name='editranking'),
    url(r'^systemmessages/', views.systemMessage, name='systemmessages'),
    url(r'^message/edit/(?P<messageid>[0-9]+)/$', views.editSystemMessage, name='editsystemmessage'),
    url(r'^message/delete/(?P<messageid>[0-9]+)/$', views.deleteSystemMessage, name='deletesystemmessage'),
    url(r'^detail/sprint/(?P<sprintid>[0-9]+)/$', views.sprintDetails, name='sprintdetail'),
    url(r'^detail/team/(?P<teamId>[0-9]+)/$', views.teamDetails, name='teamdetail'),
    url(r'^detail/', views.sprintDetails, name='detail'),
    url(r'^api/teamSprintTrend/(?P<teamId>[0-9]+)/$', views.teamSprintTrend, name='teamSprintTrend'),
    url(r'^api/teamSprintTrend/(?P<teamId>[0-9]+)/(?P<sprintId>[0-9]+)/$', views.teamSprintTrend, name='teamSprintTrend'),
    #url(r'^api/teamSprintDates/', views.teamSprintDates, name='teamSprintDates'),
    url(r'^api/teamSprintDates/(?P<sprintid>[0-9]+)/$', views.teamSprintDates, name='teamSprintDates'),
    url(r'^api/teamSprintPoints/(?P<teamId>[0-9]+)/$', views.teamSprintPoints, name='teamSprintPoints'),
    url(r'^api/teamSprintPoints/(?P<teamId>[0-9]+)/(?P<sprintId>[0-9]+)/$', views.teamSprintPoints, name='teamSprintPoints'),
    url(r'^sprints/', views.sprints, name='sprints'),
    url(r'^sprint/edit/(?P<sprintid>[0-9]+)/$', views.editSprint, name='editsprint'),
    url(r'^sprint/delete/(?P<sprintid>[0-9]+)/$', views.deleteSprint, name='deletesprint'),
    url(r'^commits/', views.getCommits, name='teamcommits'),
    url(r'^commits/(?P<teamid>[0-9]+)/$', views.getCommits, name='commits'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

