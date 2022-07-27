import requests
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from datetime import datetime


CURRENT_SEASON = str(datetime.now().year)


class IndexView(TemplateView):
    template_name = "index.html"
    leagues_shortcuts = ["bl1", "bl2", "bl3"]
    path_teams = "https://api.openligadb.de/getbltable/{}/{}"
    path_matches = "https://api.openligadb.de/getmatchdata/{}/{}"

    def get_context_data(self, **kwargs):

        for league in self.leagues_shortcuts:
            name = "matches_{}".format(league)
            kwargs[league] = self.get_leagues_data(league, CURRENT_SEASON)
            kwargs[name] = self.get_matches_data(league, CURRENT_SEASON)
        print(kwargs)
        return kwargs

    def get_leagues_data(self, league, season):
        r = requests.get(self.path_teams.format(league, season))
        return r.json()

    def get_matches_data(self, league, season):
        r = requests.get(self.path_matches.format(league, season))
        return r.json()
