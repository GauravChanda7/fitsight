from django.urls import path
from . import views

urlpatterns = [
    path('start-session/', views.create_session, name='create_session'),
    path('<int:session_id>/live/', views.live_workout_view, name='live_workout'),
    path('<int:session_id>/add-exercise/', views.add_exercise_view, name='add_exercise'),
]