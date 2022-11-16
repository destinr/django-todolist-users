from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from .models import AppUser as User, Task
from .forms import *

@csrf_exempt
def loginpage(request):
    return render(request, 'tdApp/loginpage.html')

@csrf_exempt
def userhome(request, username):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)
        data = {
            'user' : request.user,
            'tasks' : tasks,
            'form' : TaskForm()
        }
        return render(request,'tdapp/userhome.html',data)
         
    else:
        return JsonResponse({'user':None})
    
@csrf_exempt
def sign_up(request):
    if request.method == "POST":
        try:
            body=(request.POST)
            User.objects.create_user(username=body['username'], password=body['password'], email=body['username'])
        except Exception as e:
            print('oops!')
            print(str(e))
        return HttpResponseRedirect('login')
    else:
        return render(request, 'tdapp/signup.html')

@csrf_exempt
def log_in(request):
        if request.method == 'POST':
            body = request.POST
            email = body['email']
            password = body['password']
            
            # remember, we told django that our email field is serving as the 'username' 
            # this doesn't start a login session, it just tells us which user from the db belongs to these credentials
            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_active:
                    try:
                        login(request, user)
                    except Exception as e:
                        print('oops!')
                        print(str(e))
                    return HttpResponseRedirect(f'userhome/{user.username}')
                    # Redirect to a success page.
                else:
                    return HttpResponse('not active!')
                    # Return a 'disabled account' error message
            else:
                return HttpResponse('no user!')
                # Return an 'invalid login' error message.
        else:
            return render(request,'tdapp/loginpage.html')
            
        
@csrf_exempt
def log_out(request):
    logout(request)
    return render(request, 'tdApp/loginpage.html')

@csrf_exempt
def add_task(request, username):
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            newTask = Task(content =form.cleaned_data['content'], priority = form.cleaned_data['priority'], user_id = request.user.id)
            newTask.save()
            return HttpResponseRedirect(f'/userhome/{request.user}')
    else:
        return HttpResponseRedirect(f'/userhome/{request.user}')
    
@csrf_exempt
def task_detail(request,username,task_id):
    task = Task.objects.get(id=task_id)
    data = {
        'user':request.user,
        'task':task,
        'form':TaskForm()
    }
    return render(request,"tdapp/taskdetail.html",data)

@csrf_exempt
def delete_task(request,username,task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return HttpResponseRedirect(f'/userhome/{request.user}')

@csrf_exempt
def update_task(request,username,task_id):
    new_content = request.POST['content']
    new_priority = request.POST['priority']
    task = Task.objects.get(id=task_id)
    Task.objects.filter(id=task_id).update(content= new_content, priority=new_priority)
    task.refresh_from_db()
    return HttpResponseRedirect(f'/userhome/{request.user}')

