import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apisite.settings')
django.setup()

from django.contrib.auth.models import User

def add_users():
    # admin
    user = User.objects.create_user('admin', password='weyfvbgfhjkm')
    user.is_superuser = True
    user.is_staff = True
    user.save()
    # demo
    user = User.objects.create_user('demo', password='weyfvbgfhjkm')
    user.save()


def main():
    add_users()


if __name__ == "__main__":
    main()
