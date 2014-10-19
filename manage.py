#!/usr/bin/env python
import os
import sys


def filter_arguments(arguments):
    filtered = []
    is_production = False;
    for argument in arguments:
        if argument == '--production':
            is_production = True
        else:
            filtered.append(argument)

    return is_production, filtered


if __name__ == "__main__":
    is_production, sys.argv = filter_arguments(sys.argv)
    if is_production:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings_pro")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
