from django.urls import path
from . import views

urlpatterns = [
    # Authentication routes
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    
    # Application routes (all require authentication)
    path('home/', views.home_view, name='home'),
    path('add/', views.new_question_view, name='new_question'),
    path('question/<int:question_id>/', views.question_detail_view, name='question_detail'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
]