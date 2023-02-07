from django.urls import path

from . import views

urlpatterns = [
    path('', views.sign_in, name='sign_in'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('request_ride/', views.request_ride, name='request_ride'),
    path('get_rides/', views.get_rides, name='get_rides'),
    path('account_info/', views.account_info, name='account_info'),
    path('edit_account/', views.edit_account, name='edit_account'),
    path('edit_vehicle/', views.edit_vehicle, name='edit_vehicle'),
    path('cancel_vehicle/', views.cancel_vehicle, name='cancel_vehicle'),
    path('ride_info/', views.ride_info, name='ride_info'),
    path('edit_ride/', views.edit_ride, name='edit_ride'),
    path('search_joinable_rides/', views.search_joinable_rides, name='search_joinable_rides'),
    path('search_ride_driver/', views.search_ride_driver, name='search_ride_driver'),
    path('get_rides_driver/', views.get_rides_driver, name='get_rides_driver'),
    path('deal_ride_driver/', views.deal_ride_driver, name='deal_ride_driver'),
    path('complete_ride_driver/', views.complete_ride_driver, name='complete_ride_driver'),
    path('join_ride/', views.join_ride, name='join_ride'),
]