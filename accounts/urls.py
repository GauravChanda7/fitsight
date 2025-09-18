from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dahsboard_view, name='dashboard'),
    path('update-profile/', views.update_profile_view, name='update_profile'),
    path('logout/', views.logout_view, name='logout'),
]