import pytest
from django.utils.module_loading import import_string

from wagtail_guide.conf import conf


@pytest.mark.django_db
def test_main(live_server, driver, settings):
    """
    Test main

    Calls each callable in `WAGTAIL_GUIDE_CHAPTERS` with `live_server` and `driver` as arguments.

    Note:

        `live_server` triggers the transactional_db fixture,
        which flushes the db at the end of each test.

        Wagtail creates content via data migrations,
        this content is flushed after the first test. :/

        The workaround? Just run everything in a single test...
    """

    # `live_server` fails when ManifestFilesStorage is active.
    settings.STATICFILES_STORAGE = (
        "django.contrib.staticfiles.storage.StaticFilesStorage"
    )

    for chapter in conf.WAGTAIL_GUIDE_CHAPTERS:
        import_string(chapter)(live_server, driver)
