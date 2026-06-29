import csv

from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    with open(settings.BUS_STATION_CSV, encoding='utf-8') as csvfile:
        stations = list(csv.DictReader(csvfile))

    paginator = Paginator(stations, 10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    context = {
        'bus_stations': page,
        'page': page,
    }
    return render(request, 'stations/index.html', context)
