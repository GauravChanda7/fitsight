from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from fitness_tracking.models import WorkoutSession, Set
from django.utils import timezone
from datetime import timedelta
import json
from django.db.models import Count
from collections import defaultdict
from .models import CustomUser, WeightEntry


# Create your views here.


def landing_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    return render(request, 'accounts/landing_page.html')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:dashboard')
    else:    
        form = CustomUserCreationForm()

    context = {'form' : form}
    return render(request, 'accounts/signup.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)

        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect('accounts:dashboard')
    else:
        form = AuthenticationForm()

    context = {'form' : form}
    return render(request, 'accounts/login.html', context)


@login_required(login_url='accounts:login')
def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@login_required(login_url='accounts:login')
def update_profile_view(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance = request.user)
        
        if form.is_valid():
            today = timezone.now().date()
            new_weight = form.cleaned_data.get('weight_kg')

            if new_weight is not None:
                obj, created = WeightEntry.objects.get_or_create(
                    user = request.user,
                    date = today,
                    defaults= {'weight_kg' : new_weight}
                )

                if not created and obj.weight_kg != new_weight:
                    obj.weight_kg = new_weight
                    obj.save()
            form.save()
            return redirect('accounts:dashboard')
        
    else: 
        form = CustomUserUpdateForm(instance= request.user)

    context = {'form' : form}
    return render(request, 'accounts/update_profile.html', context)
    

@login_required(login_url='accounts:login')
def dahsboard_view(request):
    if request.method == 'GET':
        recent_sessions = WorkoutSession.objects.filter(user = request.user).order_by('-date', '-id')[:5]

        all_sessions = WorkoutSession.objects.filter(user = request.user).order_by('-date')
        total_sessions = all_sessions.count()

        today = timezone.now().date()
        start_of_month = today.replace(day=1)
        workouts_this_month = WorkoutSession.objects.filter(
            user = request.user,
            date__gte = start_of_month,
            date__lte = today
        ).count()

        volume_chart_data = {
            "labels" : [],
            "data" : [],
        }
        sessions_for_volume_chart = reversed(all_sessions[:100])
        for session in sessions_for_volume_chart:
            volume_chart_data["labels"].append(session.date.strftime("%b %d"))
            volume_chart_data["data"].append(session.total_weight_lifted())

        
        sixty_days_ago = timezone.now().date() - timedelta(days=59)
        muscle_group_data = Set.objects.filter(
            session__user = request.user,
            session__date__gte = sixty_days_ago,
        ).values(
            'exercise_name__muscle_group'
        ).annotate(
            set_count = Count('id')
        ).order_by('-set_count')

        muscle_pie_chart_data = {
            "labels" : [item['exercise_name__muscle_group'] for item in muscle_group_data],
            "data" : [item['set_count'] for item in muscle_group_data],
        }


        today = timezone.now().date()
        seven_days_ago = today - timedelta(days=6)
        session_last_seven_days = WorkoutSession.objects.filter(
            user = request.user,
            date__gte = seven_days_ago,
        )

        workouts_by_day = defaultdict(float)
        for session in session_last_seven_days:
            workouts_by_day[session.date.strftime("%a")] += session.total_weight_lifted()

        weekly_frequency_data = {"labels": [], "data": []}

        for i in range(7):
            day = today - timedelta(days=i)
            day_abbr = day.strftime("%a")
            weekly_frequency_data['labels'].insert(0, day_abbr)
            weekly_frequency_data['data'].insert(0, workouts_by_day.get(day_abbr, 0))

        thirty_days_ago = today - timedelta(days=29)
        session_last_thirty_days = WorkoutSession.objects.filter(
            user = request.user,
            date__gte = thirty_days_ago,
        )

        workouts_by_date = defaultdict(float)
        for session in session_last_thirty_days:
            workouts_by_date[session.date] += session.total_weight_lifted()
        
        monthly_frequency_data = {"labels": [], "data": []}
        for i in range(30):
            day = thirty_days_ago + timedelta(days=i)
            monthly_frequency_data['labels'].append(day.strftime("%b %d"))
            monthly_frequency_data['data'].append(workouts_by_date.get(day, 0))

        weight_history_data = {"labels" : [], "data" : []}
        weight_entries = WeightEntry.objects.filter(user = request.user).order_by('date')

        for entry in weight_entries:
            weight_history_data["labels"].append(entry.date.strftime("%b %d"))
            weight_history_data["data"].append(entry.weight_kg)


        context = {
                'recent_sessions' : recent_sessions,
                'total_sessions' : total_sessions,
                'workouts_this_month' : workouts_this_month,
                'volume_chart_data' : json.dumps(volume_chart_data),
                'muscle_pie_chart_data' : json.dumps(muscle_pie_chart_data),
                'weekly_frequency_data' : json.dumps(weekly_frequency_data),
                'monthly_frequency_data' : json.dumps(monthly_frequency_data),
                'weight_history_data' : json.dumps(weight_history_data),
                }
        
        return render(request, 'accounts/dashboard.html', context)
    

@login_required(login_url='accounts:login')
def delete_account_view(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        return redirect('landing')
    
    return render(request, 'accounts/delete_account.html')
