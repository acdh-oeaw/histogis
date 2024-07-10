from django.http import JsonResponse
from collections import Counter
import pandas as pd
import json
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.db.models import Avg, Sum, Count
from django.db.models.functions import TruncYear
from django.shortcuts import render
from django.views.generic import TemplateView

from shps.models import *


def make_href(row, entity="work", id="id", label=None):
    url = reverse("shapes:shape_detail", kwargs={"pk": row[id]})
    if label:
        element = """<a href="{}" target='_blank'>{}</a>""".format(url, row[label])
    else:
        element = """<a href="{}" target='_blank'>{}</a>""".format(url, "link2object")
    return element


def calculate_duration(row):
    if row["end_date"] and row["start_date"]:
        time = pd.to_timedelta(
            (row["end_date"] - row["start_date"]) + timedelta(days=1)
        ).__str__()
    else:
        time = pd.to_timedelta("0 days").__str__()
    return time


def get_datatables_data(request):
    pd.set_option("display.max_colwidth", -1)

    # PersonWorkRelation
    queryset = list(
        TempSpatial.objects.values(
            "id",
            "name",
            "start_date",
            "end_date",
        ).annotate(year=TruncYear("start_date"))
    )
    df = pd.DataFrame(queryset)
    df["name"] = df.apply(
        lambda row: make_href(row, entity="tempspatial", id="id", label="name"), axis=1
    )
    df["items_by_year"] = df.groupby("year")["year"].transform("count")
    df["duration"] = df.apply(lambda row: calculate_duration(row), axis=1)
    df["duration"] = df.apply(lambda row: calculate_duration(row), axis=1)
    payload = {}
    payload["data"] = df.values.tolist()
    payload["columns"] = list(df)
    return JsonResponse(payload)


class AnalyzeView(TemplateView):
    template_name = "analyze/basic.html"
