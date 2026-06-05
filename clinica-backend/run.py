import os
from decouple import config

# leer el puerto del archivo .env
PORT = config('API_PORT')

# ejecutar el servidor django
os.system(f'python manage.py runserver {PORT}')