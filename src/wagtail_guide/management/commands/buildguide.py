import os

import pytest
from django.core.management.base import BaseCommand

from wagtail_guide import tests


class Command(BaseCommand):
    """
    Build the user guide
    """

    help = __doc__

    def handle(self, *args, **options):
        tests_directory = os.path.abspath(tests.__file__)
        pytest.main(["-s", "-vvv", tests_directory])
