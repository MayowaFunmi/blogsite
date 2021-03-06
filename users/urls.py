from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # path('add_country/', views.add_country, name='add_country'),
    # path('add_city/', views.add_city, name='add_city'),
    path('user_signup/', views.signup, name='user_signup'),
    path('add_profile/', views.profile_create_view, name='add_profile'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),  # <-- this one here
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout, name='logout'),

]