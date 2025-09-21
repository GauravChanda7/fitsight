from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import WorkoutSessionForm, SetForm, AddExerciseForm
from .models import WorkoutSession, Set, Exercise
from django.core.paginator import Paginator

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
    
def workout_detail_view(request, session_id):
    if request.method == 'GET':
        session = get_object_or_404(WorkoutSession, id=session_id, user=request.user) 
        sets = Set.objects.filter(session = session_id).order_by('id')
        context = {'sets' : sets,
                   'session' : session}
        return render(request, 'fitness_tracking/workout_detail.html', context)




