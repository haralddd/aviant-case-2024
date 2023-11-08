from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('calendar/', views.show_calendar, name='calendar'),
]
