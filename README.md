# Django Background Remover

A Django web application that automatically removes backgrounds from uploaded images using AI-powered background removal.

## Features

- **Easy Upload**: Drag & drop or click to upload images
- **AI Background Removal**: Uses the `rembg` library for accurate background removal
- **Multiple Formats**: Supports JPG, PNG, GIF, BMP, and WebP formats
- **Download Results**: Download processed images with transparent backgrounds
- **Image History**: View recently processed images
- **Responsive Design**: Modern, mobile-friendly interface
- **File Management**: Delete unwanted images and files

## Installation

1. **Clone or download the project**
   ```bash
   cd C:\Users\CK-2\CascadeProjects\django-bg-remover
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Open your browser** and go to `http://localhost:8000`

## Usage

1. **Upload an Image**: 
   - Visit the homepage
   - Drag and drop an image or click to browse
   - Supported formats: JPG, PNG, GIF, BMP, WebP
   - Maximum file size: 10MB

2. **Process the Image**:
   - Click "Remove Background" 
   - Wait for the AI to process your image
   - View the result with transparent background

3. **Download Result**:
   - Click the download button to save the processed image
   - Images are saved as PNG files with transparency

4. **Manage Images**:
   - View your recent uploads on the homepage
   - Click "View" to see original vs processed comparison
   - Delete images you no longer need

## Technical Details

- **Framework**: Django 4.2.7
- **Background Removal**: rembg 2.0.50 (AI-powered)
- **Image Processing**: Pillow (PIL)
- **Frontend**: Bootstrap 5 with custom styling
- **Database**: SQLite (default)

## File Structure

```
django-bg-remover/
├── bg_remover/              # Main Django app
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── forms.py            # Form definitions
│   ├── urls.py             # URL patterns
│   └── admin.py            # Admin interface
├── bg_remover_project/      # Django project settings
│   ├── settings.py         # Project settings
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI configuration
├── templates/               # HTML templates
│   ├── base.html           # Base template
│   └── bg_remover/         # App-specific templates
├── media/                   # Uploaded and processed images
│   ├── uploads/            # Original images
│   └── processed/          # Background-removed images
├── static/                  # Static files (CSS, JS)
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## API Endpoints

- `/` - Homepage with upload form
- `/upload/` - Handle image upload and processing
- `/image/<id>/` - View image details
- `/download/<id>/` - Download processed image
- `/delete/<id>/` - Delete image and files

## Troubleshooting

**Installation Issues:**
- Make sure Python 3.8+ is installed
- Consider using a virtual environment
- On Windows, you might need Visual Studio Build Tools for some packages

**Processing Issues:**
- Ensure uploaded images are valid image files
- Check file size (max 10MB)
- Some complex images may take longer to process

**Performance:**
- First-time processing may be slower as models are downloaded
- Consider using a more powerful server for production use

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.
