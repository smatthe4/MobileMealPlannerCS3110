from django.urls import path, include
from . import views

urlpatterns = [
    #path function defines a url pattern
    #'' is empty to represent based path to app
    # views.index is the function defined in views.py
    # name='index' parameter is to dynamically create url
    # example in html <a href="{% url 'index' %}">Home</a>.
    path('', views.index, name='index'),
    path('meallist/', views.meal_list, name='meal_list'),
    path('profile/<int:profile_id>/updateProfile', views.updateProfile, name='update_profile'),

    #user accounts
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', views.registerPage, name = 'register-page'),
    path('accounts/logout', views.logoutView, name='logout'),
    path('user/', views.userPage, name='user_page'),
]