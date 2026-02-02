from django.contrib import admin
from .models import Activity, HeartRate

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'source', 'start_time', 'steps')

@admin.register(HeartRate)
class HeartRateAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'bpm')
