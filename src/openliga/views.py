import requests

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
        return unsorted_data["matchDateTime"]

    def get_queryset(self):
        """
        Collects data of all matches for current season
        for all BL divisions in sorted by date order
        """
        queryset = []
        for league in self.leagues_shortcuts:
            matches = self.get_matches_data(league, CURRENT_SEASON)
            for match in matches:
                match["matchDateTime"] = datetime.fromisoformat(match["matchDateTime"])
                queryset.append(match)
        queryset.sort(key=self.sort_func)
        return queryset

    def get_context_data(self, **kwargs):
        kwargs["teams_stats"] = self.get_teams_stats()
        kwargs["matches"] = self.get_queryset()
        kwargs["today_matches"] = self.get_today_matches(kwargs["matches"])
        kwargs["next_day_matches"] = self.get_next_day_matches(kwargs["matches"])
        kwargs["next_day_matches_date"] = self.get_next_gameday_date(kwargs["next_day_matches"])
        return kwargs

    def get_teams_stats(self):
        teams_stats = {league: self.get_leagues_data(league, CURRENT_SEASON) for league in self.leagues_shortcuts}
        return teams_stats

    def get_leagues_data(self, league, season):
        r = requests.get(self.path_teams.format(league, season))
        return r.json()

    def get_matches_data(self, league, season):
        r = requests.get(self.path_matches.format(league, season))
        return r.json()

    @staticmethod
    def get_today_matches(matches_data):
        today_matches = []
        for match in matches_data:
            if match["matchDateTime"].date() == TODAY:
                today_matches.append(match)
        return today_matches

    @staticmethod
    def get_next_day_matches(matches_data):
        next_day_matches = []
        for i in range(len(matches_data) - 1):
            if matches_data[i]["matchDateTime"].date() > TODAY:
                if matches_data[i + 1]["matchDateTime"].day > matches_data[i]["matchDateTime"].day:
                    next_day_matches.append(matches_data[i])
                    break
                else:
                    next_day_matches.append(matches_data[i])
        return next_day_matches

    @staticmethod
    def get_next_gameday_date(next_day_matches):
        return next_day_matches[0]["matchDateTime"]
