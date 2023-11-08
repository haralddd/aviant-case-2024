# restaurant/staff_interface/views.py

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpRequest

from datetime import datetime, date, time
from calendar import monthrange

from .models import OpeningHours, OpeningHoursSpecific

def index(request: HttpRequest):
    return render(request, 'index.html')


def show_calendar(request: HttpRequest):
    month = request.GET.get('month')
    
    if month is not None:
        month = int(month)
    else:
        month = date.today().month
        
    weekday_offset, end_day = monthrange(date.today().year, int(month))
    offset_range = range(weekday_offset)
        
    from_date = date.today()
    to_date = from_date.day + end_day - 1 
        
    print(f"Showing calendar for: {month}")
    print(f"Offset: {weekday_offset}")
        
    hours_recurring = OpeningHours.objects.all()
    # Filtered get objects
    # hours_specific = OpeningHoursSpecific.objects.filter(date__range=[from_date, to_date])
    hours_specific = OpeningHoursSpecific.objects.all()
    
    return render(request, 'calendar.html', {'weekdays': OpeningHours.weekdays.choices,
                                             'offset_range': offset_range,
                                            'hours_recurring': hours_recurring,
                                            'hours_specific': hours_specific})