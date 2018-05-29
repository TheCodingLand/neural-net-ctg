
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'root.settings'
import django
django.setup()

from django.contrib.auth.management.commands.createsuperuser import get_user_model
if 'CREATE_SUPER_USER' in os.environ:

    if get_user_model().objects.filter(username=os.environ['SUPER_USER']):
        print('Super user already exists. SKIPPING...')
    else:
        print('Creating super user...')
        get_user_model()._default_manager.db_manager().create_superuser(
            username=os.environ['SUPER_USER'], email=os.environ['SUPER_USER_EMAIL'], password=os.environ['SUPER_USER_PASSWORD'])
        print('Super user created...')