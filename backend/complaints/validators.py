import os
from django.core.exceptions import ValidationError
import mimetypes

def validate_file_size(file):
    """
    Validates that the uploaded file is no larger than 5MB.
    """
    max_size_kb = 5120 # 5MB
    if file.size > max_size_kb * 1024:
        raise ValidationError(f"File size cannot exceed 5MB. Current size is {round(file.size / (1024 * 1024), 2)}MB.")

def validate_mime_type(file):
    """
    Validates that the uploaded file is an image or PDF.
    """
    valid_mime_types = [
        'image/jpeg',
        'image/png',
        'image/gif',
        'application/pdf'
    ]
    
    # Check mime type from content_type if available (DRF UploadedFile usually has this)
    if hasattr(file, 'content_type'):
        if file.content_type not in valid_mime_types:
            raise ValidationError(f"Unsupported file type: {file.content_type}. Allowed types: JPEG, PNG, GIF, PDF.")
    
    # Fallback to extension checking
    ext = os.path.splitext(file.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf']
    if ext not in valid_extensions:
        raise ValidationError(f"Unsupported file extension: {ext}. Allowed extensions: .jpg, .png, .gif, .pdf.")
