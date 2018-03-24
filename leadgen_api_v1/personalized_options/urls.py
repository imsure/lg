from django.urls import path, register_converter

from . import views, converters

register_converter(converters.DayOfWeekConverter, 'day_of_week')
register_converter(converters.TimezoneConverter, 'timezone')

urlpatterns = [
    path(r'activity/', views.activity_list, name='activity_list'),
    path(r'activity/<int:pk>/', views.activity_detail, name='activity_detail'),
    path(r'activity/<int:pk>/<int:walk_time>/<int:bike_time>/',
         views.activity_walk_bike_time_update,
         name='activity_walk_bike_time_update'),
    path(r'activity/<int:from_id>/<int:to_id>/',
         views.create_update_activity,
         name='create_update_activity'),
    path(r'travel_options/<day_of_week:day_of_week>/',
         views.travel_options_by_day_of_week,
         name='travel_options_by_day_of_week'),
    path(r'travel_options/<day_of_week:day_of_week>/<int:slot_id>/',
         views.travel_options_by_day_of_week_slot,
         name='travel_options_by_day_of_week_slot'),
    path(r'travel_options/<day_of_week:day_of_week>/<int:slot_id_start>/<int:slot_id_end>/',
         views.travel_options_by_day_of_week_slot_range,
         name='travel_options_by_day_of_week_slot_range'),
    path(r'travel_options/<day_of_week:day_of_week>/<int:slot_id>/<timezone:tz>/',
         views.travel_options_by_day_of_week_slot_tz,
         name='travel_options_by_day_of_week_slot_tz'),
    path(r'travel_options/<int:pk>/', views.update_travel_options, name='update_travel_options'),
    path(r'personalized_options/<int:from_id>/<int:to_id>/<day_of_week:day_of_week>/<int:slot_id>/',
         views.personalized_options,
         name='personalized_options'),
]
