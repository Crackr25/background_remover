from django.db import models
from django.utils import timezone
import os


class ProcessedImage(models.Model):
    original_image = models.ImageField(upload_to='uploads/')
    processed_image = models.ImageField(upload_to='processed/', blank=True, null=True)
    uploaded_at = models.DateTimeField(default=timezone.now)
    processed_at = models.DateTimeField(blank=True, null=True)
    processing_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )
    error_message = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Image {self.id} - {self.processing_status}"

    def get_original_filename(self):
        return os.path.basename(self.original_image.name)

    def get_processed_filename(self):
        if self.processed_image:
            return os.path.basename(self.processed_image.name)
        return None
