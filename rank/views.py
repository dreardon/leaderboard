from django.shortcuts import render
from .models import Team, Criteria, Ranking, Sprint, SystemMessage
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render, reverse, get_object_or_404
from .forms import RankingForm, SystemMessageForm, SprintForm
from django.db.models import Sum
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
from django.contrib import messages
from datetime import date, timedelta
import time
import requests



def ranking(request):
    currentSprint = Sprint.objects.filter(isActive=True)[0]
    try:
        activeMessage = SystemMessage.objects.filter(isActive=True).values_list('content',flat=True)[0]
    except (SystemMessage.DoesNotExist, IndexError) as e:
        activeMessage = None
    activeTeams = Team.objects.filter(isActive=True).order_by('-drawing__drawingDate')
    currentStandings = Team.objects.filter(isActive=True,ranking__criteria__isActive=True,ranking__sprint__isActive=True)\
        .values('name','profile_pic','id')\
        .annotate(total_points=Sum('ranking__points')).order_by('-total_points')
    lastModified = Ranking.objects.filter(sprint__isActive=True).values_list('lastModified', flat=True).order_by('-lastModified')[0]
    context = {'activeTeams': activeTeams,'currentSprint':currentSprint,'currentStandings':currentStandings,'lastModified':lastModified,'activeMessage':activeMessage}
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
    sprintDetails= Ranking.objects.filter(sprint_id=sprintid).values('dataDate','points','comment','criteria__name','team__name','sprint__name').order_by('-dataDate', 'team__name')
    context = {'sprintDetails': sprintDetails,'title':'Sprint Detail'}
    return render(request, 'rank/sprint.html', context)

def teamDetails(request,**kwargs):
    teamId = kwargs['teamId']
    teamDetailsActive= Ranking.objects.filter(team_id=teamId,sprint__isActive=1).values('dataDate','points','comment','criteria__name','team__name','sprint__name').order_by('-dataDate')
    teamDetailsInactive= Ranking.objects.filter(team_id=teamId,sprint__isActive=0).values('dataDate','points','comment','criteria__name','team__name','sprint__name').order_by('-dataDate','sprint__name')
    context = {'teamDetailsActive': teamDetailsActive,'teamDetailsInactive':teamDetailsInactive,'title':'Team Detail'}
    return render(request, 'rank/team.html', context)

def dataEntry(request, template_name='rank/data_entry.html'):
    sprintDetail= Ranking.objects.filter(criteria__isActive=True,sprint__isActive=True,team__isActive=True).values('id','dataDate','points','comment','criteria__name','team__name','sprint__name','comment').order_by('-dataDate', 'team__name')
    entry = Ranking()
    if request.POST:
        form = RankingForm(request.POST,instance=entry)
        if form.is_valid():
            defaults = {'points': request.POST['points'], 'comment': request.POST['comment']}
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

def systemMessage(request, template_name='rank/system_message.html'):

    systemmessages = SystemMessage.objects.filter().values('id','name','lastModified','isActive','content').order_by('-lastModified')
    id = request.POST.get('messageid', None)
    if id != None:
        systemmessage = get_object_or_404(SystemMessage, id=id)
    else:
        systemmessage = SystemMessage()
    if request.POST:
        form = SystemMessageForm(request.POST,instance=systemmessage)
        if form.is_valid():
            active = request.POST.get("isActive", False)
            if active == 'on':
                active = True
            else:
                active = False
            defaults = {'content': request.POST['content'], 'isActive': active, 'name': request.POST['name']}
            try:
                obj = SystemMessage.objects.get(name=request.POST['name'])
                for key, value in defaults.items():
                    setattr(obj, key, value)
                obj.save()
                messages.success(request, 'The setting was updated!')
                redirect_url = reverse('systemmessages')
                return redirect(redirect_url)
            except SystemMessage.DoesNotExist:
                form.save()
                messages.success(request, 'The new setting was updated!')
                redirect_url = reverse('systemmessages')
                return redirect(redirect_url)
    else:
        form = SystemMessageForm(instance=systemmessage)
        return render(request, template_name, {
            'systemmessageform': form,'systemmessages':systemmessages, 'render_form': True
        })

def editSystemMessage(request, template_name='rank/system_message.html',**kwargs):
    systemmessages = SystemMessage.objects.filter().values('id','name','lastModified','isActive','content').order_by('-lastModified')
    systemmessageid = kwargs['messageid']
    systemmessage = SystemMessage.objects.get(pk=systemmessageid)
    form = SystemMessageForm(instance=systemmessage)
    return render(request, template_name, {
        'systemmessageform': form, 'systemmessages':systemmessages, 'render_form': True
    })

def deleteSystemMessage(request,**kwargs):
    systemmessageid = kwargs['messageid']
    try:
        r = SystemMessage.objects.get(pk=systemmessageid)
        r.delete()
        messages.success(request, 'The message was deleted')
    except SystemMessage.DoesNotExist:
        return redirect("systemmessages")
    return redirect("systemmessages")

def editRanking(request, template_name='rank/data_entry.html',**kwargs):
    sprintDetail= Ranking.objects.filter(criteria__isActive=True,sprint__isActive=True,team__isActive=True).values('id','dataDate','points','comment','criteria__name','team__name','sprint__name').order_by('-dataDate', 'team__name')
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

def sprints(request, template_name='rank/sprints.html'):

    sprints = Sprint.objects.filter().values('id','name','isActive',).order_by('-name')
    id = request.POST.get('editid',None)
    if id == 'None':
        id = None
    if id != None:
        sprint = get_object_or_404(Sprint, id=id)
    else:
        sprint = Sprint()
    if request.POST:
        form = SprintForm(request.POST,instance=sprint)
        if form.is_valid():
            active = request.POST.get("isActive", False)
            if active == 'on':
                active = True
            else:
                active = False
            defaults = {'isActive': active, 'name': request.POST['name'],'id': request.POST['editid']}
            try:
                if id == None:
                    form.save()
                    messages.success(request, 'The new sprint was updated!')
                    redirect_url = reverse('sprints')
                    return redirect(redirect_url)
                else:
                    obj = Sprint.objects.get(id=request.POST['editid'])
                    for key, value in defaults.items():
                        setattr(obj, key, value)
                    obj.save()
                    messages.success(request, 'The sprint was updated!')
                    redirect_url = reverse('sprints')
                    return redirect(redirect_url)
            except:
                return redirect(redirect_url)

    else:
        form = SprintForm(instance=sprint)
        return render(request, template_name, {
            'form': form,'sprints':sprints, 'render_form': True
        })

def editSprint(request, template_name='rank/sprints.html',**kwargs):
    sprints= Sprint.objects.filter().values('id','name','isActive').order_by('-name')
    sprintId = kwargs['sprintid']
    sprint = Sprint.objects.get(pk=sprintId)
    form = SprintForm(instance=sprint)
    return render(request, template_name, {
        'form': form, 'sprints':sprints, 'render_form': True
    })

def deleteSprint(request,**kwargs):
    sprintId = kwargs['sprintid']
    try:
        r = Sprint.objects.get(pk=sprintId)
        r.delete()
    except Sprint.DoesNotExist:
        return redirect("sprints")
    return redirect("sprints")

def updateCommits():
    response = requests.get('http://thedataishere.com', auth=('user', 'password'))
    data = response.json()