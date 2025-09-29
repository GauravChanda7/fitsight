from django.urls import path
from . import views

app_name = 'fitness_tracking'

urlpatterns = [
    path('start-session/', views.create_session, name='create_session'),
    path('<int:session_id>/live/', views.live_workout_view, name='live_workout'),
    path('<int:session_id>/add-exercise/', views.add_exercise_view, name='add_exercise'),
    path('history/', views.workout_history_view, name='workout_history'),
    path('<int:session_id>/detail/', views.workout_detail_view, name='workout_detail'),
    path('api/get-last-set/<int:exercise_id>/', views.get_last_set_data, name='get_last_set_data')
]