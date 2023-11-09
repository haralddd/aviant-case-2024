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
        cur_hours = hours_recurring.filter(day=cur_date.weekday())
        if not cur_hours:
            date_range[cur_date.strftime("%d.%m")] = "Closed"
        else:
            cur_hours = cur_hours[0].open_time.strftime("%H:%M") + " - " + cur_hours[0].close_time.strftime("%H:%M")
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
        Order.Status.PENDING.name: [],
        Order.Status.IN_PROGRESS.name: [],
        Order.Status.COMPLETED.name: [],
        Order.Status.CANCELLED.name: [],
    }
    
    all_orders = Order.objects.all().order_by('-datetime')
    
    for order in all_orders:
        items_query = order.items.all()
        if not items_query:
            continue
        
    
        context[order.get_status_str()].append(order)
        
    return render(request, 'orders.html',context=context)

def show_statistics(request: HttpRequest):
    context = {}
    
    all_orders = Order.objects.all().order_by('datetime')
    
    sums = [0,0,0,0,0,0,0]
    counts = [0,0,0,0,0,0,0]
    for order in all_orders:
        week_day = order.datetime.weekday()
        sums[week_day] += order.get_total_price()
        counts[week_day] += 1
    
    rec_hours_all = RecurringHours.objects.all()
    
    context['avg_weekday_orders'] = []
    context['weekly_open_hours'] = 0
    for i in range(7):
        avg_income = round(sums[i]/counts[i],2) if counts[i] != 0 else 0
        rec_hours = rec_hours_all.filter(day=i)
        
        if not rec_hours:
            open_time_str = "Closed"
            close_time_str = "Closed"
            context['weekly_open_hours'] += 0
            
        else:
            open_time = rec_hours[0].open_time if rec_hours else "Closed"
            close_time = rec_hours[0].close_time if rec_hours else "Closed"
            open_time_str = open_time.strftime('%H:%M')
            close_time_str = close_time.strftime('%H:%M')
            # Fix minutes some other    time
            context['weekly_open_hours'] += close_time.hour - open_time.hour
        
        context['avg_weekday_orders'].append([
            RecurringHours.weekdays.choices[i][1],
            open_time_str, close_time_str,
            counts[i], avg_income])
        
        
    context['weekly_open_hours_avg'] = round(context['weekly_open_hours']/7, 2)
    return render(request, 'statistics.html', context=context)

def show_menu(request: HttpRequest):
    return render(request, 'menu.html')

def submit_recurring_hours(request: HttpRequest):

    if request.method != 'POST':
        return redirect('calendar')
    
    form = request.POST
    
    edit_day = form['day']
    open_time = form['open']
    close_time = form['close']
    
    if 'closed' in form:
        RecurringHours.objects.filter(day=int(edit_day)).delete()
        return redirect('calendar')
    
    
    print(f"Day: {int(edit_day)}: {open_time} - {close_time}")
    print(f"Open as int: {int(open_time[:2])}, {int(open_time[3:-1])}")
    print(f"Close as int: {int(close_time[:2])}, {int(close_time[3:-1])}")
        
    existing_rule = RecurringHours.objects.filter(day=int(edit_day))
    if not existing_rule:
        RecurringHours.objects.create(
            day=int(edit_day),
            open_time=time(int(open_time[:2]), int(open_time[3:])),
            close_time=time(int(close_time[:2]), int(close_time[3:]))
            )
    else:
        existing_rule.update(
                    open_time=time(int(open_time[:2]), int(open_time[3:])),
                    close_time=time(int(close_time[:2]), int(close_time[3:]))
                    )
    
    return redirect('calendar')

def change_order_status(request: HttpRequest):
    if request.method != 'POST':
        return redirect('orders')
    
    form = request.POST
    
    order_id = form['order_id']
    move_dir = form['move_dir']
    
    print(f"Order id: {order_id}")
    
    order = Order.objects.filter(pk=int(order_id))
    if not order:
        return redirect('orders')
    
    new_status = order[0].status + int(1 if move_dir == ">>" else -1)
    order.update(status=new_status)
    
    print(f"Order {order_id} status changed to {new_status}")
    
    return redirect('orders')


