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

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.ranking, name='ranking'),
    url(r'^dataentry/', views.dataEntry, name='dataentry'),
    url(r'^detail/sprint/(?P<sprintid>[0-9]+)/$', views.sprintDetails, name='sprintdetail'),
    url(r'^detail/team/(?P<teamId>[0-9]+)/$', views.teamDetails, name='teamdetail'),
    url(r'^ranking/delete/(?P<rankingId>[0-9]+)/$', views.deleteRanking, name='deleteranking'),
    url(r'^ranking/edit/(?P<rankingId>[0-9]+)/$', views.editRanking, name='editranking'),
    url(r'^detail/', views.sprintDetails, name='detail'),
    url(r'^api/teamSprintTrend/(?P<teamId>[0-9]+)/$', views.teamSprintTrend, name='teamSprintTrend'),
    url(r'^api/teamSprintDates/', views.teamSprintDates, name='teamSprintDates'),
    url(r'^api/teamSprintPoints/(?P<teamId>[0-9]+)/$', views.teamSprintPoints, name='teamSprintPoints'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
