import json

import numpy as np
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .forms import PlayerForm
from .players.models import Player
from .scores.models import Score

from .casestudy import solvers


def index(request):
    form = PlayerForm()

    best_scores = Score.objects.order_by("total_reaction_time")[:5]

    return render(
        request, "myreactor/index.html", {"form": form, "scores": best_scores}
    )


def play(request, playerid):
    data = {
        "CA": solvers.CA0,
        "CB": solvers.CB0,
        "CC": solvers.CC0,
        "CD": solvers.CD0,
        "CE": solvers.CE0,
        "m": solvers.m0,
        "T": solvers.T0,
        "Tj": solvers.Tj0,
        "Tjset": solvers.Tjset0,
        "U": solvers.U0,
        "X": 0,
        "mdot": solvers.mdot0,
        "Vdot": solvers.Vdot0,
        "Dmdot": solvers.Dmdot,
        "playerid": playerid,
    }

    best_scores = Score.objects.order_by("total_reaction_time")[:5]

    return render(
        request,
        "myreactor/play.html",
        {"data": json.dumps(data), "scores": best_scores},
    )


def info(request, playerid):
    best_scores = Score.objects.order_by("total_reaction_time")[:5]

    return render(
        request,
        "myreactor/info.html",
        {"playerid": playerid, "scores": best_scores},
    )


def register(request):
    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]

            player, created = Player.objects.get_or_create(name=name)
            return redirect("myreactor:info", playerid=player.id)
    return redirect("myreactor:index")


def play_data(request):
    solvers.Dt = 60
    data = {k: float(i) for k, i in request.POST.dict().items()}
    data["playerid"] = int(data["playerid"])
    while True:
        try:
            data = solvers.morton(**data)
        except Exception as e:
            solvers.Dt /= 1.5
            if solvers.Dt < 1e-6:
                break
        else:
            break
    return JsonResponse(data)


def score(request):
    data = {k: i for k, i in request.POST.dict().items()}
    player = Player.objects.get(pk=int(data["player"]))
    score = Score(
        total_reaction_time=int(data["t"]),
        final_conversion=float(data["X"]),
        player=player,
    )
    score.save()
    return JsonResponse({"status": "recorded", "error": False})


def restart(request):
    return redirect("myreactor:index")


def reset(request):
    Score.objects.all().delete()
    return redirect("myreactor:index")
