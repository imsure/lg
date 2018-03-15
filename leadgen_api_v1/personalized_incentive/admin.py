from django.contrib import admin

from .models import IncentiveParams
from .models import IncentivePoints

# Register your models here.
admin.site.register(IncentiveParams)
admin.site.register(IncentivePoints)
