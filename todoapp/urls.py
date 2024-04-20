from django.urls import path
from . import views

urlpatterns = [
    path('', views.taskList, name = 'todotask'),
    path('update/<str:pk>/',views.updateTask, name = 'update_task'),
    path('delete/<str:pk>', views.deleteTask, name = 'delete_task'),

    path('login/', views.userlogin, name = 'login'),
    path('logout/', views.userlogout, name = 'ulogout'),
    path('register/', views.register, name = 'register'),
]