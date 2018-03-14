from django.urls import path

from . import views


urlpatterns = [
    path(r'incentive/<int:metropia_id>/', views.IncentiveParamsDetail.as_view(),
         name='incentive_params_detail'),
]
