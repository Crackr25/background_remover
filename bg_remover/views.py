from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.core.files.base import ContentFile
from django.utils import timezone
from .models import ProcessedImage
from .forms import ImageUploadForm
import os
import io
from PIL import Image
from rembg import remove
import logging

logger = logging.getLogger(__name__)


def index(request):
    """Main page with upload form and recent images"""
    recent_images = ProcessedImage.objects.all()[:10]
    form = ImageUploadForm()
    
    context = {
        'form': form,
        'recent_images': recent_images,
    }
    return render(request, 'bg_remover/index.html', context)


def upload_image(request):
    """Handle image upload and background removal"""
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Save the uploaded image
                processed_image = form.save()
                processed_image.processing_status = 'processing'
                processed_image.save()
                
                # Process the image to remove background
                success = remove_background(processed_image)
                
                if success:
                    processed_image.processing_status = 'completed'
                    processed_image.processed_at = timezone.now()
                    messages.success(request, 'Background removed successfully!')
                else:
                    processed_image.processing_status = 'failed'
                    messages.error(request, 'Failed to process image. Please try again.')
                
                processed_image.save()
                return redirect('image_detail', pk=processed_image.pk)
                
            except Exception as e:
                logger.error(f"Error processing image: {str(e)}")
                messages.error(request, f'Error processing image: {str(e)}')
                return redirect('index')
        else:
            messages.error(request, 'Please select a valid image file.')
    
    return redirect('index')


def remove_background(processed_image):
    """Remove background from the uploaded image using rembg"""
    try:
        # Open the original image
        with processed_image.original_image.open('rb') as input_file:
            input_data = input_file.read()
        
        # Remove background using rembg
        output_data = remove(input_data)
        
        # Create a new filename for the processed image
        original_name = os.path.splitext(processed_image.get_original_filename())[0]
        processed_filename = f"{original_name}_no_bg.png"
        
        # Save the processed image
        processed_image.processed_image.save(
            processed_filename,
            ContentFile(output_data),
            save=False
        )
        
        return True
        
    except Exception as e:
        logger.error(f"Background removal failed: {str(e)}")
        processed_image.error_message = str(e)
        return False


def image_detail(request, pk):
    """Display the original and processed image"""
    image = get_object_or_404(ProcessedImage, pk=pk)
    context = {
        'image': image,
    }
    return render(request, 'bg_remover/detail.html', context)


def download_image(request, pk):
    """Download the processed image"""
    image = get_object_or_404(ProcessedImage, pk=pk)
    
    if not image.processed_image:
        messages.error(request, 'Processed image not available.')
        return redirect('image_detail', pk=pk)
    
    try:
        response = HttpResponse(
            image.processed_image.read(),
            content_type='image/png'
        )
        response['Content-Disposition'] = f'attachment; filename="{image.get_processed_filename()}"'
        return response
    except Exception as e:
        messages.error(request, f'Error downloading image: {str(e)}')
        return redirect('image_detail', pk=pk)


def delete_image(request, pk):
    """Delete an image and its files"""
    image = get_object_or_404(ProcessedImage, pk=pk)
    
    try:
        # Delete the actual files
        if image.original_image and os.path.exists(image.original_image.path):
            os.remove(image.original_image.path)
        if image.processed_image and os.path.exists(image.processed_image.path):
            os.remove(image.processed_image.path)
        
        # Delete the database record
        image.delete()
        messages.success(request, 'Image deleted successfully.')
        
    except Exception as e:
        messages.error(request, f'Error deleting image: {str(e)}')
    
    return redirect('index')
