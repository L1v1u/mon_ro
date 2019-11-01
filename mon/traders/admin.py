from django.contrib import admin

# Register your models here.
from .models import TraderType, Tradesman, TradesmanFeedback, TradesmanProfile


admin.site.register(TraderType)
admin.site.register(Tradesman)
admin.site.register(TradesmanFeedback)
admin.site.register(TradesmanProfile)