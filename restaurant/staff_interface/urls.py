from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('menu/', views.show_menu, name='menu'),
    path('calendar/', views.show_calendar, name='calendar'),
    path('orders/', views.show_orders, name='orders'),
    path('statistics/', views.show_statistics, name='statistics'),
    path('submit_recurring_hours/', views.submit_recurring_hours, name='submit_recurring_hours'),
]
