from __future__ import unicode_literals
from django.contrib import admin
from .models import Schedule

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ['name']

