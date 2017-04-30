import os
import sys
import django
sys.path.append("/cbe/") #path to your project 
os.environ['DJANGO_SETTINGS_MODULE'] = 'cbe.settings'
django.setup()
from django.contrib.auth.models import User
self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
