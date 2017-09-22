from django.shortcuts import render
from .models import Team, Criteria, Ranking, Sprint
from django.shortcuts import redirect, render, reverse
from .forms import RankingForm
from django.db.models import Sum


def ranking(request):
    currentSprint = Sprint.objects.filter(isActive=True)[0]
    activeTeams = Team.objects.filter(isActive=True).order_by('-drawing__drawingDate')
    currentStandings = Team.objects.filter(isActive=True,ranking__criteria__isActive=True,ranking__sprint__isActive=True).values('name','profile_pic','id').annotate(Sum('ranking__points'))
    context = {'activeTeams': activeTeams,'currentSprint':currentSprint,'currentStandings':currentStandings}
    return render(request, 'rank/index.html', context)

def sprintDetails(request,**kwargs):
    sprintid = kwargs['sprintid']
    sprintDetails= Ranking.objects.filter(sprint_id=sprintid).values('dataDate','points','criteria__name','team__name','sprint__name').order_by('-dataDate', 'team__name')
    context = {'sprintDetails': sprintDetails,'title':'Sprint Detail'}
    return render(request, 'rank/sprint.html', context)

def teamDetails(request,**kwargs):
    teamid = kwargs['teamid']
    teamDetailsActive= Ranking.objects.filter(team_id=teamid,sprint__isActive=1).values('dataDate','points','criteria__name','team__name','sprint__name').order_by('-dataDate')
    teamDetailsInactive= Ranking.objects.filter(team_id=teamid,sprint__isActive=0).values('dataDate','points','criteria__name','team__name','sprint__name').order_by('-dataDate','sprint__name')
    context = {'teamDetailsActive': teamDetailsActive,'teamDetailsInactive':teamDetailsInactive,'title':'Team Detail'}
    return render(request, 'rank/team.html', context)

def dataEntry(request, template_name='rank/data_entry.html'):
    sprintDetail= Ranking.objects.filter(criteria__isActive=True,sprint__isActive=True,team__isActive=True).values('dataDate','points','criteria__name','team__name','sprint__name').order_by('-dataDate', 'team__name')
    entry = Ranking()
    if request.POST:
        form = RankingForm(request.POST,instance=entry)
        if form.is_valid():
            form.save()
        return redirect("dataentry")

    else:
        form = RankingForm(instance=entry)
        return render(request, template_name, {
            'rankingform': form,'sprintDetail':sprintDetail, 'render_form': True
        })