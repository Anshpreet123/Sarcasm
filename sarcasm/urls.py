from django.urls import path
from .views import *
from .import views

urlpatterns=[
	path('',views.home, name='register'),
	path('login',views.login, name='login'),
	path('faqs',views.faqs, name='faqs'),
	path('validate_username/', views.validate_username, name='validate_username'),
	path('play',Play.as_view(), name='play'),
	path('logout', views.logout_view, name='logout'),
	path('bonus', views.bonus, name='bonus'),
	path('techsupport', views.support, name='support'),
	path('leaderboard', views.leaderboard, name='leaderboard'),
	path('skip', views.skip, name='skip')
]