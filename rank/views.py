from django.shortcuts import render
from .models import Team, Criteria, Ranking, Sprint
from django.shortcuts import redirect, render, reverse
from .forms import RankingForm
from django.db.models import Sum
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
from django.contrib import messages
from datetime import date, timedelta
import time



def ranking(request):
    currentSprint = Sprint.objects.filter(isActive=True)[0]
    activeTeams = Team.objects.filter(isActive=True).order_by('-drawing__drawingDate')
    currentStandings = Team.objects.filter(isActive=True,ranking__criteria__isActive=True,ranking__sprint__isActive=True)\
        .values('name','profile_pic','id')\
        .annotate(total_points=Sum('ranking__points')).order_by('-total_points')
    context = {'activeTeams': activeTeams,'currentSprint':currentSprint,'currentStandings':currentStandings}
    return render(request, 'rank/index.html', context)

def teamSprintDates(request):

    # Get Date Range for Labels
    firstdate = Ranking.objects.filter(sprint__isActive=True).values('dataDate').order_by('dataDate')[0]
    delta = date.today() - firstdate.get('dataDate')  # timedelta
    dateListing = []
    for i in range(delta.days + 1):
        dateListing.append(firstdate.get('dataDate') + timedelta(days=i))

    return JsonResponse(dateListing, safe=False)

def teamSprintPoints(request,**kwargs):
    def cumulative_add(scoreListing):
        cumulativeListing = []
        for elt in scoreListing:
            if len(cumulativeListing) > 0:
                cumulativeListing.append(cumulativeListing[-1] + elt)
            else:
                cumulativeListing.append(elt)
        return cumulativeListing

    # Get Date Range for Labels
    firstdate = Ranking.objects.filter(sprint__isActive=True).values('dataDate').order_by('dataDate')[0]
    delta = date.today() - firstdate.get('dataDate')  # timedelta
    dateListing = []
    for i in range(delta.days + 1):
        dateListing.append(firstdate.get('dataDate') + timedelta(days=i))

    teamId = kwargs['teamId']
    scoreListing = []
    for x in dateListing:
        if Ranking.objects.filter(team_id=teamId, team__isActive=True, criteria__isActive=True,
                                  sprint__isActive=True,
                                  dataDate=x).exists():
            newEntry = Ranking.objects.filter(team_id=teamId, team__isActive=True, criteria__isActive=True,
                                              sprint__isActive=True, dataDate=x) \
                .values('dataDate') \
                .annotate(daily_points=Sum('points')).values('daily_points')[0]
            scoreListing.append(int(newEntry.get('daily_points')))
        else:
            scoreListing.append(0)

    cumulativeListing = list(cumulative_add(scoreListing))
    return JsonResponse(cumulativeListing, safe=False)

def teamSprintTrend(request,**kwargs):
    teamId = kwargs['teamId']
    data = Ranking.objects.filter(team_id=teamId, team__isActive=True, criteria__isActive=True, sprint__isActive=True) \
        .values('dataDate') \
        .annotate(daily_points=Sum('points')).order_by('dataDate')

    return JsonResponse(list(data), safe=False)

def sprintDetails(request,**kwargs):
    sprintid = kwargs['sprintid']
    sprintDetails= Ranking.objects.filter(sprint_id=sprintid).values('dataDate','points','criteria__name','team__name','sprint__name').order_by('-dataDate', 'team__name')
    context = {'sprintDetails': sprintDetails,'title':'Sprint Detail'}
    return render(request, 'rank/sprint.html', context)

def teamDetails(request,**kwargs):
    teamId = kwargs['teamId']
    teamDetailsActive= Ranking.objects.filter(team_id=teamId,sprint__isActive=1).values('dataDate','points','criteria__name','team__name','sprint__name').order_by('-dataDate')
    teamDetailsInactive= Ranking.objects.filter(team_id=teamId,sprint__isActive=0).values('dataDate','points','criteria__name','team__name','sprint__name').order_by('-dataDate','sprint__name')
    context = {'teamDetailsActive': teamDetailsActive,'teamDetailsInactive':teamDetailsInactive,'title':'Team Detail'}
    return render(request, 'rank/team.html', context)

def dataEntry(request, template_name='rank/data_entry.html'):
    sprintDetail= Ranking.objects.filter(criteria__isActive=True,sprint__isActive=True,team__isActive=True).values('id','dataDate','points','criteria__name','team__name','sprint__name').order_by('-dataDate', 'team__name')
    entry = Ranking()
    if request.POST:
        form = RankingForm(request.POST,instance=entry)
        if form.is_valid():
            defaults = {'points': request.POST['points']}
            try:
                obj = Ranking.objects.get(sprint=request.POST['sprint'],team=request.POST['team'],criteria=request.POST['criteria'],dataDate=request.POST['dataDate'])
                for key, value in defaults.items():
                    setattr(obj, key, value)
                obj.save()
                messages.success(request, 'The ranking was updated!')
                return redirect('dataentry')
            except Ranking.DoesNotExist:
                form.save()
                messages.success(request, 'A new ranking has been saved!')
                return redirect('dataentry')
        return redirect("dataentry")

    else:
        form = RankingForm(instance=entry)
        return render(request, template_name, {
            'rankingform': form,'sprintDetail':sprintDetail, 'render_form': True
        })

def editRanking(request, template_name='rank/data_entry.html',**kwargs):
    sprintDetail= Ranking.objects.filter(criteria__isActive=True,sprint__isActive=True,team__isActive=True).values('id','dataDate','points','criteria__name','team__name','sprint__name').order_by('-dataDate', 'team__name')
    rankingId = kwargs['rankingId']
    ranking = Ranking.objects.get(pk=rankingId)
    form = RankingForm(instance=ranking)
    return render(request, template_name, {
        'rankingform': form, 'sprintDetail':sprintDetail, 'render_form': True
    })

def deleteRanking(request,**kwargs):
    rankingId = kwargs['rankingId']
    try:
        r = Ranking.objects.get(pk=rankingId)
        r.delete()
    except Ranking.DoesNotExist:
        return redirect("dataentry")
    return redirect("dataentry")