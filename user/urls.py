from django.urls import path
from . import views

urlpatterns = [
    path('', views.users_view, name='users_view'),
    path('/<int:user_id>', views.user_view, name='user_view'),
    path('/<int:user_id>/todos', views.get_user_todos, name='user_todos_view')
]
