from django.contrib import admin
from guerrilla.models import GuerrillaDungeon
# Register your models here.

class GuerrillaDungeonAdmin(admin.ModelAdmin):
    list_display = ('name', 'startTime', 'endTime', 'server', 'group')


admin.site.register(GuerrillaDungeon, GuerrillaDungeonAdmin)