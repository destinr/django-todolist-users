from django.urls import path

from . import views

urlpatterns = [
    path('', views.loginpage),
    path('signup', views.sign_up),
    path('login', views.log_in),
    path('logout', views.log_out),
    path('userhome/<str:username>',views.userhome),
    path('userhome/<str:username>/addtask',views.add_task),
    path('userhome/<str:username>/<int:task_id>',views.task_detail),
    path('userhome/<str:username>/<int:task_id>/delete',views.delete_task),
    path('userhome/<str:username>/<int:task_id>/update',views.update_task),

]