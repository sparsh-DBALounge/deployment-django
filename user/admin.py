from django.contrib import admin
from . import models


@admin.register(models.User)
class userAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'age', 'created_at', 'updated_at')
    search_fields = ('email', )