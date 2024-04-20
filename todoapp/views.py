from django.shortcuts import render, redirect
from .models import Task
# Import authentication libraries
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Create flash messages about username
        checkUsername = authenticate(username = username, password = password)
        if checkUsername is not None:
            login(request, checkUsername)
            return redirect('todotask')
        else:
            messages.error(request,"the user doesn't exist")
            return redirect('/login')
        
    return render(request, 'todoapp\login.html')

def userlogout(request):
    logout(request)
    return redirect('/login')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Create flash messages about username
        checkUsername = User.objects.filter(username = username)
        if checkUsername:
            messages.error(request,'the username already exists')
            return redirect('/register')
        # Create flash messages about password
        if len(password) < 4:
            messages.error(request,'the password must be at least four characters')
            return redirect('/register')
        # Create user account
        user = User.objects.create_user(username=username, email = email, password=password)
        user.save()
        return redirect('/login')
    return render(request, 'todoapp\\register.html')

@login_required
def taskList(request):
    if request.method == 'POST':
        title = request.POST.get('task')
        new_task = Task(user = request.user, title=title)
        new_task.save()
        return redirect('/')  # Redirect to the task list page
    tasks = Task.objects.filter(user = request.user)
    context = {'tasks':tasks,'username':request.user.username}
    return render(request, 'todoapp/home.html', context)

@login_required
def updateTask(request, pk):
    task = Task.objects.get(id = pk)
    if request.method == 'POST':
        new_title = request.POST.get('new_title')
        task.title = new_title
        complete = request.POST.get('complete')
        task.complete = (complete == 'on')
        task.save()
        return redirect('todotask')  # Redirect to the task list page
    return render(request, 'todoapp/update_task.html', {'task': task})

@login_required
def deleteTask(request, pk):
    task = Task.objects.get(id = pk)
    if request.method == 'POST':
        task.delete()
        return redirect('todotask')  # Redirect to the task list page after deleting
    return render(request, 'todoapp/delete_task.html', {'task': task})
