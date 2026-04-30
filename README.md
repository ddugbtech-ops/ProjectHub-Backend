# ProjectHub - Django Collaboration Platform

A powerful dual-portal system for teachers to manage projects and students to collaborate seamlessly.

## Features

### For Teachers
- Create and manage projects
- Assign tasks to students
- Monitor student progress in real-time
- Track contributions and submissions

### For Students
- Join projects via unique codes
- Track assigned tasks
- Submit work easily
- Collaborate with team members

## Technology Stack

- **Backend**: Django 5.0+
- **Database**: SQLite (development), PostgreSQL (production)
- **Static Files**: Whitenoise
- **Environment Variables**: django-environ
- **Deployment**: PythonAnywhere compatible

## Setup Instructions

### Local Development
```bash
# Clone the repository
git clone <repository-url>
cd Contri_Tracker

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### PythonAnywhere Deployment
1. Create account at pythonanywhere.com
2. Clone this repository to your PythonAnywhere account
3. Set up virtual environment and install requirements
4. Configure WSGI file
5. Set environment variables
6. Collect static files
7. Reload web app

## Environment Variables
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to False in production
- `ALLOWED_HOSTS`: Your domain name

## Project Structure
```
Contri_Tracker/
- projecthub/          # Django project settings
- core/               # Main app with models and views
- templates/          # HTML templates
- static/            # CSS, JS, images
- media/             # User uploaded files
- requirements.txt   # Python dependencies
```

## License
MIT License
"# Contri_Tracker" 
