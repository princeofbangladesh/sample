import os ,django

os.environ.setdefault("DJANGO_DEFAULT_MODULE","Prince.settings")
django.setup()