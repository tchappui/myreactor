import json

import numpy as np
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .forms import PlayerForm
from players.models import Player
from scores.models import Score

from casestudy import solvers


def index(request):
    form = PlayerForm()

    best_scores = Score.objects.order_by('total_reaction_time')[:5]

    return render(
        request, 'core/index.html', {"form": form, "scores": best_scores}
    )


def play(request, playerid):
    data = {
        'CA': solvers.CA0,
        'CB': solvers.CB0,
        'CC': solvers.CC0,
        'CD': solvers.CD0,
        'CE': solvers.CE0,
        'T': solvers.T0,
        'Tj': solvers.Tj0,
        'Tjset': solvers.Tjset0,
        'U': solvers.U0,
        'X': 0,
        'playerid': playerid,
        'slider1': solvers.slider10,
        'slider2': solvers.slider20,
        'slider3': solvers.slider30,
        'slider4': solvers.slider40,
        'slider5': solvers.slider50,
        'slider6': solvers.slider60,
        'slider7': solvers.slider70,
        'slider8': solvers.slider80,
        'slider9': solvers.slider90,
    }

    best_scores = Score.objects.order_by('total_reaction_time')[:5]

    return render(
        request,
        'core/play.html',
        {
            'data': json.dumps(data),
            'scores': best_scores,
            'slider10': solvers.slider10,
            'slider20': solvers.slider20,
            'slider30': solvers.slider30,
            'slider40': solvers.slider40,
            'slider50': solvers.slider50,
            'slider60': solvers.slider60,
            'slider70': solvers.slider70,
            'slider80': solvers.slider80,
            'slider90': solvers.slider90,
        },
    )


def info(request, playerid):
    best_scores = Score.objects.order_by('total_reaction_time')[:5]

    return render(
        request,
        'core/info.html',
        {'playerid': playerid, 'scores': best_scores},
    )


def register(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            name = form.cleaned_data["name"]

            player, created = Player.objects.get_or_create(email=email)
            player.first_name, player.name = first_name, name
            player.save()
            return redirect("core:info", playerid=player.id)
    return redirect("core:index")


def play_data(request):
    solvers.Dt = 60
    if request.is_ajax():
        data = {k: float(i) for k, i in request.POST.dict().items()}
        data['playerid'] = int(data['playerid'])
        while True:
            try:
                data = solvers.model(**data)
            except Exception as e:
                solvers.Dt = solvers.Dt / 1.5
                if solvers.Dt < 1e-6:
                    break
            else:
                break
        return JsonResponse(data)


def score(request):
    if request.is_ajax():
        data = {k: i for k, i in request.POST.dict().items()}
        player = Player.objects.get(pk=int(data['player']))
        score = Score(
            total_reaction_time=int(data['t']),
            final_conversion=float(data['X']),
            player=player,
        )
        score.save()
    return JsonResponse({'status': "recorded", "error": False})


def restart(request):
    return redirect('core:index')


def reset(request):
    Score.objects.all().delete()
    return redirect('core:index')
