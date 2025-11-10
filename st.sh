#cd app
gunicorn --bind 0.0.0.0:7000 --timeout 120 --workers 1 wsgi:app
