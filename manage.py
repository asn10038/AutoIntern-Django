import os
import sys

if __name__ == "__main__":
    SETTINGS = "mysite.settings.base"
    try:
        if os.environ["ENVIRONMENT"] == 'UAT':
            SETTINGS = "mysite.settings.uat"
        if os.environ["ENVIRONMENT"] == 'PROD':
            SETTINGS = "mysite.settings.prod"
    except KeyError as ke:
        pass

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
