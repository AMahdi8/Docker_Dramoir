from django.contrib.auth import get_user_model
import django
import os
# به جای dramoir.settings نام پروژه‌ت رو بزار
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MovieSeries.settings.prod')

django.setup()


User = get_user_model()

username = "8"
password = "8"
email = "8@8.com"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username, email=email, password=password)
    print("✅ Superuser '8' created.")
else:
    print("⚠️ Superuser '8' already exists.")
