from django.urls import path
from .views import *

urlpatterns = [
    # path('', views.index, name='index'),
    path('weather_map_view/', weather_map_view),
    path('add_location', add_location, name='add_location'),
    path('update_location', update_location, name='update_location'),
    path('deactivate_location', deactivate_location, name='deactivate_location'),
    path('location_list', location_list, name='location_list'),
    
    
]
