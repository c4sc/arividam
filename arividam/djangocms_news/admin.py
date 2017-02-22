from django.contrib import admin
from .models import PromotedNews

# Register your models here.
class PromotedNewsAdmin(admin.ModelAdmin):
    list_display = ['page', 'site']

admin.site.register(PromotedNews, PromotedNewsAdmin)
