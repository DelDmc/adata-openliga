import requests
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from datetime import datetime


CURRENT_SEASON = str(datetime.now().year)


class IndexView(TemplateView):
    template_name = "index.html"
    leagues_shortcuts = ['bl1', 'bl2', 'bl3']
    path_teams = "https://api.openligadb.de/getbltable/{}/{}"

    def get_context_data(self, **kwargs):
        for league in self.leagues_shortcuts:
            r = requests.get(self.path_teams.format(league, CURRENT_SEASON))
            kwargs[league] = r.json()
        return kwargs
