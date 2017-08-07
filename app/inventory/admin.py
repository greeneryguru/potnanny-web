from __future__ import unicode_literals
from django.contrib import admin
from .models import Sensor, Relay, Plugin

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ['name']

@admin.register(Relay)
class Relay(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ['name']

@admin.register(Plugin)
class Plugin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ['name']

