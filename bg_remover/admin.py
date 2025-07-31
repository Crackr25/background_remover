from django.contrib import admin
from .models import ProcessedImage


@admin.register(ProcessedImage)
class ProcessedImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_original_filename', 'processing_status', 'uploaded_at', 'processed_at']
    list_filter = ['processing_status', 'uploaded_at']
    search_fields = ['original_image']
    readonly_fields = ['uploaded_at', 'processed_at']
    
    def get_original_filename(self, obj):
        return obj.get_original_filename()
    get_original_filename.short_description = 'Original File'
