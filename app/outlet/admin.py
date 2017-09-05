from __future__ import unicode_literals
from django.contrib import admin
from .models import Outlet

@admin.register(Outlet)
class OutletAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ['name']

