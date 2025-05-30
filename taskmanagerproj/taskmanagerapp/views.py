from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Task
from .forms import SignUpForm, SignInForm, TaskForm
from django.db.models import Q

def landing_view(request):
    return render(request, 'landing.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user) 
            return redirect('dashboard') 
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def signin_view(request):
    if request.method == 'POST':
        form = SignInForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('dashboard') 
    else:
        form = SignInForm()
    return render(request, 'signin.html', {'form': form})


def signout_view(request):
    logout(request)
    return redirect('landing')

from django.contrib.auth.decorators import login_required


@login_required
def dashboard_view(request):
    query = request.GET.get('q')
    sort_by = request.GET.get('sort_by')
    tasks = Task.objects.filter(user=request.user)

    if query:
        tasks = tasks.filter(
            Q(title__icontains=query) |
            Q(status__icontains=query) |
            Q(due_date__icontains=query)
        )

    if sort_by == 'priority':
        tasks = tasks.order_by('priority') 
    elif sort_by == 'due_date':
        tasks = tasks.order_by('due_date')

    return render(request, 'dashboard.html', {'tasks': tasks})


@login_required
def add_task_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('dashboard')
    else:
        form = TaskForm()
    return render(request, 'add_task.html', {'form': form})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('dashboard')

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)

    return render(request, 'edit_task.html', {'form': form})