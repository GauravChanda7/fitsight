from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import WorkoutSessionForm, SetForm, AddExerciseForm
from .models import WorkoutSession, Set, Exercise
from django.core.paginator import Paginator
from django.db.models import Max, Sum, F
from django.http import JsonResponse

# Create your views here.

@login_required(login_url="accounts:login")
def create_session(request):
    if request.method == 'POST':
        form = WorkoutSessionForm(request.POST)

        if form.is_valid():
            workout_session = form.save(commit=False)
            workout_session.user = request.user
            workout_session.save()
            return redirect('fitness_tracking:live_workout', session_id = workout_session.id)
    
    else:
        form = WorkoutSessionForm()
    
    context = {'form' : form}
    return render(request, 'fitness_tracking/create_session.html', context)


@login_required(login_url="accounts:login")
def live_workout_view(request, session_id):
    workout_session = get_object_or_404(WorkoutSession, id=session_id, user=request.user)

    if request.method == 'POST':
        form = SetForm(request.POST, user=request.user)
        
        if form.is_valid():
            set_instance = form.save(commit=False)
            set_instance.session = workout_session
            set_instance.save()
            return redirect('fitness_tracking:live_workout', session_id = session_id)
        
    else:
        form = SetForm(user=request.user)

    completed_sets = Set.objects.filter(session = workout_session).order_by('-id')
    context = {'form' : form,
               'session' : workout_session,
               'completed_sets' : completed_sets}
    
    return render(request, 'fitness_tracking/live_workout.html', context)


@login_required(login_url="accounts:login")
def add_exercise_view(request, session_id):
    if request.method == 'POST':
        form = AddExerciseForm(request.POST)

        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.user = request.user
            exercise.save()
            return redirect('fitness_tracking:live_workout', session_id = session_id)
        
    else:
        form = AddExerciseForm()

    context = {'form' : form,
               'session_id' : session_id}
    
    return render(request, 'fitness_tracking/add_exercise.html', context)


@login_required(login_url='accounts:login')
def workout_history_view(request):
    if request.method == 'GET':
        history = WorkoutSession.objects.filter(user=request.user).order_by('-date')
        paginator = Paginator(history, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {"page_obj" : page_obj}
        return render(request, 'fitness_tracking/workout_history.html', context)
    

@login_required(login_url='accounts:login')
def workout_detail_view(request, session_id):
    if request.method == 'GET':
        session = get_object_or_404(WorkoutSession, id=session_id, user=request.user) 
        sets = Set.objects.filter(session = session_id).order_by('id')
        context = {'sets' : sets,
                   'session' : session}
        return render(request, 'fitness_tracking/workout_detail.html', context)


@login_required(login_url='accounts:login')
def get_last_set_data(request, exercise_id):
    last_set = Set.objects.filter(
        session__user = request.user,
        exercise_name__id = exercise_id,
    ).order_by('-session__date', '-id').first()

    if last_set:
        data = {
            'reps' : last_set.reps,
            'weight_kg' : last_set.weight_kg,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'reps' : '', 'weight_kg' : ''})


@login_required(login_url='accounts:login')
def exercise_progress_view(request):
    exercise_list = Exercise.objects.filter(user = request.user).order_by('exercise_name')
    context = {'exercise_list' : exercise_list}
    return render(request, 'fitness_tracking/exercise_progress.html', context)


@login_required(login_url='accounts:login')
def get_exercise_progress_data(request, exercise_id):
    sessions_with_exercise = WorkoutSession.objects.filter(
        user = request.user,
        set__exercise_name__id = exercise_id
    ).distinct().order_by('date')

    labels = []
    max_weight_data = []
    total_volume_data = []

    for session in sessions_with_exercise:
        labels.append(session.date.strftime('%b %d'))

        sets_in_session = Set.objects.filter(
            session = session,
            exercise_name__id = exercise_id,
        )

        max_weight = sets_in_session.aggregate(max_w = Max('weight_kg'))['max_w'] or 0
        max_weight_data.append(max_weight)

        total_volume = sets_in_session.aggregate(total_v = Sum(F('reps') * F('weight_kg')))['total_v'] or 0
        total_volume_data.append(total_volume)

    data = {
        'labels' : labels,
        'max_weight_data' : max_weight_data,
        'total_volume_data' : total_volume_data,
    }

    return JsonResponse(data)
