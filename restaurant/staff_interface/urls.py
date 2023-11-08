from django.urls import include, path
from . import views


urlpatterns = [
    path('opening_hours/', views.show_calendar, name='opening_hours'),
]
