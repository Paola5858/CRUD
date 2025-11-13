import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from django.db import connection

cursor = connection.cursor()
cursor.execute("SHOW TABLES LIKE 'sensores_%'")
tables = cursor.fetchall()
print('Tables:', tables)
