from django.contrib import admin
from .models import AnalysisRequest

@admin.register(AnalysisRequest)
class AnalysisRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('url', 'id')