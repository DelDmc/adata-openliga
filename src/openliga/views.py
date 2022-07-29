import requests
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from datetime import datetime

from django.views.generic.list import ListView

CURRENT_SEASON = str(datetime.now().year)
TODAY = datetime.today().date()


class IndexView(ListView):
    template_name = "index.html"
    leagues_shortcuts = ["bl1", "bl2", "bl3"]
    path_teams = "https://api.openligadb.de/getbltable/{}/{}"
    path_matches = "https://api.openligadb.de/getmatchdata/{}/{}"
    context_object_name = "matches"
    extra_context = "today_matches"

    @staticmethod
    def sort_func(unsorted_data):
        return unsorted_data['matchDateTimeUTC']

    def get_queryset(self):
        queryset = []
        for league in self.leagues_shortcuts:
            matches = self.get_matches_data(league, CURRENT_SEASON)
            for match in matches:
                queryset.append(match)
        queryset.sort(key=self.sort_func)
        return queryset

    def get_teams_stats(self):
        teams_stats = {league: self.get_leagues_data(league, CURRENT_SEASON) for league in self.leagues_shortcuts }
        return teams_stats

    def get_context_data(self, **kwargs):
        kwargs["teams_stats"] = self.get_teams_stats()
        kwargs["matches"] = self.get_queryset()
        kwargs["today_matches"] = self.get_today_matches(kwargs["matches"])
        print(kwargs["today_matches"])
        return kwargs

    def get_leagues_data(self, league, season):
        r = requests.get(self.path_teams.format(league, season))
        return r.json()

    def get_matches_data(self, league, season):
        r = requests.get(self.path_matches.format(league, season))
        return r.json()

    def get_today_matches(self, matches_data):
        # DO NOT FORGET TO CHANGE TODAY VARIABLE!!!
        today_matches = []
        today = '2022-08-05T16:30:00'
        today = datetime.fromisoformat(today).date()
        for match in matches_data:
            match['matchDateTime'] = datetime.fromisoformat(match['matchDateTime'])
            if match['matchDateTime'].date() == today:
                today_matches.append(match)
        return today_matches




