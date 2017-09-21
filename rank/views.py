from django.shortcuts import render
from .models import Team, Criteria, Ranking, Sprint
from django.shortcuts import redirect, render, reverse
from .forms import RankingForm
from django.db.models import Sum


def ranking(request):
    currentSprint = Sprint.objects.filter(isActive=True)[0]
    activeTeams = Team.objects.filter(isActive=True).order_by('-drawing__drawingDate')
    currentStandings = Team.objects.filter(isActive=True,ranking__criteria__isActive=True,ranking__sprint__isActive=True).values('name','profile_pic').annotate(Sum('ranking__points'))
    context = {'activeTeams': activeTeams,'currentSprint':currentSprint,'currentStandings':currentStandings}
    return render(request, 'rank/index.html', context)

def sprintDetails(request):
    teamDetail= Ranking.objects.filter(criteria__isActive=True,sprint__isActive=True,team__isActive=True).values('dataDate','points','criteria__name','team__name','sprint__name')

    context = {'teamDetail': teamDetail}
    return render(request, 'rank/detail.html', context)


def dataEntry(request, template_name='rank/data_entry.html'):
    entry = Ranking()
    if request.POST:
        form = RankingForm(request.POST,instance=entry)
        if form.is_valid():
            form.save()
        redirect_url = reverse('dataentry')
        return redirect(redirect_url)
    else:
        form = RankingForm(instance=entry)
        return render(request, template_name, {
            'rankingform': form,'render_form': True
        })