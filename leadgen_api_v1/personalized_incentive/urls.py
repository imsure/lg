from django.urls import path

from . import views


urlpatterns = [
    path(r'incentive_params/<int:metropia_id>/', views.IncentiveParamsDetail.as_view(),
         name='incentive_params_detail'),
    path(r'personalized_incentive/<int:metropia_id>/<from_city>/<to_city>/', views.personalized_incentive,
         name='personalized_incentive'),
    path(r'personalized_unit/<int:metropia_id>/', views.personalized_unit,
         name='personalized_unit'),
]
