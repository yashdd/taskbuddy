from email import message
from django.shortcuts import redirect, render
from django.http import HttpResponse
from todolist.models import Tasklist
from todolist.forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

#from taskmate.todolist.models import Tasklist
# Create your views here.

def index(request):
    context ={
            "index_text":"Welcome to Task Buddy App",
        }
    return render(request,'index.html',context)

@login_required
def todolist(request):
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            instance= form.save(commit=False)
            instance.owner = request.user
            instance.save()
        messages.success(request,('New Task Added'))
        return redirect('todolist')

    else:
        all_tasks = Tasklist.objects.filter(owner = request.user)
        context ={
            "welcome_text":"Welcome to Task Buddy App",
        }
        paginator = Paginator(all_tasks,5)
        page = request.GET.get('pg')
        all_tasks = paginator.get_page(page)
        
        return render(request,'todolist.html',{'all_tasks':all_tasks})

@login_required
def delete_task(request,task_id):
    if task.owner == request.user:
        task = Tasklist.objects.get(pk = task_id)
        task.delete()
    else:
         messages.error(request,('Access Denied. You donot have Permission'))
    return redirect('todolist')

@login_required
def complete_task(request,task_id):
    task = Tasklist.objects.get(pk = task_id)
    if task.owner == request.user:
        task.done = True
        task.save()
    else:
        messages.error(request,('Access Denied. You donot have Permission'))
    return redirect('todolist')

@login_required
def pending_task(request,task_id):
    task = Tasklist.objects.get(pk = task_id)
    if task.owner == request.user:
        task.done = False
        task.save()
    else:
        messages.error(request,('Access Denied. You donot have Permission'))
    return redirect('todolist')

@login_required
def edit_task(request,task_id):
    if request.method == "POST":
        task = Tasklist.objects.get(pk = task_id)
        form = TaskForm(request.POST or None, instance=task)
        if form.is_valid():
            form.save()
        messages.success(request,('Task Updated'))
        return redirect('todolist')
    else:
        task_obj = Tasklist.objects.get(pk = task_id)
        return render(request,'edit.html',{'task_obj':task_obj})

def aboutus(request):
    context ={
        "aboutus_text":"Welcome to About Us Page of Task Buddy App",
    }
    return render(request,'aboutus.html',context)

def contactus(request):
    context ={
        "contactus_text":"Welcome to Contact Page Task Buddy App",
    }
    return render(request,'contactus.html',context)
