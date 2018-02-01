from django.contrib import admin

from .models import Activity, TravelOption


class TravelOptionInline(admin.TabularInline):
    model = TravelOption


class ActivityAdmin(admin.ModelAdmin):
    inlines = [TravelOptionInline]


admin.site.register(Activity, ActivityAdmin)
