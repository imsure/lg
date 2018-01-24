from django.urls import path

from . import views

urlpatterns = [
    path(r'activity/', views.activity_list, name='create_activity'),
    path(r'activity/<int:from_id>/<int:to_id>/', views.update_activity, name='update_activity'),
]
