from django.contrib import admin
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'deadline', 'user', 'created_at', 'updated_at')
    search_fields = ('title', )
    list_filter = ('priority', )

