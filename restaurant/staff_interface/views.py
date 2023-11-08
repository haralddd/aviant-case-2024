# restaurant/staff_interface/views.py

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

from .models import Calendar
from .models import OpeningHours, OpeningHoursSpecific

# Create your views here.
def show_calendar(request):
    days = Calendar.objects.all()
    return render(request, 'htmx/calendar.html', {'days': days})

def show_opening_hours(request):
    hours_recurring = OpeningHours.objects.all()
    hours_specific = OpeningHoursSpecific.objects.all()
    
    return render(request, 'htmx/opening_hours.html', {'hours_recurring': hours_recurring,
                                                       'hours_specific': hours_specific})