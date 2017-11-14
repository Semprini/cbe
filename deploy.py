import os
import sys
import django

# Find the path to the current file and add the path to cbe to the system path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, 'cbe')) #cbe is a sub directory of this file

# Initialize django
os.environ['DJANGO_SETTINGS_MODULE'] = 'cbe.settings'
django.setup()

# Create a superuser
from django.contrib.auth.models import User
if User.objects.filter(username='john').count == 0:
    superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
