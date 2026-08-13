from django.urls import path
from . import views

urlpatterns = [
    path('', views.todos_view, name='todos_view'),
    path('/<int:todo_id>', views.todo_view, name='todo_view'),
]