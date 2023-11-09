# restaurant/staff_interface/views.py

from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpRequest

from datetime import datetime, date, time, timedelta
from calendar import monthrange

from .models import RecurringHours, SpecificHours, Order

def index(request: HttpRequest):
    return render(request, 'index.html')


def show_calendar(request: HttpRequest):
    month = date.today().month
    
    year = date.today().year
        
    weekday_offset, end_day = monthrange(int(year), int(month))
    from_date = date(int(year), int(month), 1)
    to_date = date(int(year), int(month), end_day)
    
    hours_recurring = RecurringHours.objects.all()
    # print(from_date)
    # print(to_date)
    date_range={}
    cur_date = from_date
    
    while cur_date <= to_date:
        cur_hours = hours_recurring.filter(day=cur_date.weekday())[0]
        if cur_hours is None:
            date_range[cur_date.strftime("%d.%m")] = "Closed"
        else:
            cur_hours = cur_hours.open_time.strftime("%H:%M") + " - " + cur_hours.close_time.strftime("%H:%M")
            date_range[cur_date.strftime("%d.%m")] = cur_hours
        cur_date += timedelta(days=1)
    
 
    
        
    print(f"Showing calendar for: {month}")
    print(f"Offset: {weekday_offset}")
    # hours_specific = RecurringHoursSpecific.objects.all()
    
    context = {
        'weekdays': RecurringHours.weekdays.choices,
        'offset_range': range(weekday_offset),
        'days': date_range,
    }
    
    return render(request, 'calendar.html', context=context)
    
    
    
def show_orders(request: HttpRequest):
    context = {
        'PENDING': [],
        'IN_PROGRESS': [],
        'COMPLETED': [],
        'CANCELLED': [],
    }
    
    all_orders = Order.objects.all().order_by('datetime')
    
    for (i,key) in zip(Order.Status.values, context.keys()):
        for (j,order) in enumerate(all_orders.filter(status=i)):
            if order.items is None:
                continue
            
            items_query = order.items.all()
            
            # Make a nice string of all items in the order
            menu_items = [f"{item.name}" for item in items_query]
            
            order_details = ([str(order.name),
                            str(order.phone_number),
                            order.datetime.strftime('%Y-%m-%d: %H:%M')],
                            menu_items)
        
            context[key].append(order_details)
        
    return render(request, 'orders.html',context=context)

def show_statistics(request: HttpRequest):
    context = {}
    
    all_orders = Order.objects.all().order_by('datetime')
    
    # for 
        
    context['avg_weekday_orders'] = [0,0,0,0,0,0,0]
    
    return render(request, 'statistics.html', context=context)

def show_menu(request: HttpRequest):
    return render(request, 'menu.html')

def submit_recurring_hours(request: HttpRequest):

    if request.method != 'POST':
        return redirect('calendar')
    
    form = request.POST
    
    day = form['day']
    open_time = form['open']
    close_time = form['close']
    
    if day is None or open_time is None or close_time is None:
        return redirect('calendar')
    
    print(f"Day: {int(day)}: {open_time} - {close_time}")
    print(f"Open as int: {int(open_time[:2])}, {int(open_time[3:-1])}")
    print(f"Close as int: {int(close_time[:2])}, {int(close_time[3:-1])}")
        
    RecurringHours.objects.filter(day=int(day)
            ).update(
                open_time=time(int(open_time[:2]), int(open_time[3:])),
                close_time=time(int(close_time[:2]), int(close_time[3:]))
                )
    
    return redirect('calendar')