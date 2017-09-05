from __future__ import unicode_literals
from django.contrib import admin
from .models import SensorData, RelayState, RetentionPeriod, TempDisplay

@admin.register(RetentionPeriod)
class RetentionPeriod(admin.ModelAdmin):
    pass

@admin.register(TempDisplay)
class TempDisplay(admin.ModelAdmin):
    pass
