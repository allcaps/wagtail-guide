import os
from typing import Sequence

from django.conf import settings


class Settings:
    @property
    def WAGTAIL_GUIDE_CHAPTERS(self) -> Sequence[str]:
        default_chapters = [
            # "wagtail_guide.markdown.getting_started",
            # "wagtail_guide.markdown.demo",
            "wagtail_guide.video.getting_started",
        ]
        return getattr(settings, "WAGTAIL_GUIDE_CHAPTERS", default_chapters)

    @property
    def WAGTAIL_GUIDE_BUILD_DIRECTORY(self) -> str:
        return getattr(settings, "WAGTAIL_GUIDE_BUILD_DIRECTORY", os.path.join(settings.BASE_DIR, "docs"))

    @property
    def WAGTAIL_GUIDE_TEXT_TO_SPEECH_URL(self) -> str:
        return getattr(settings, "WAGTAIL_GUIDE_TEXT_TO_SPEECH_URL", "http://localhost:5002/api/tts")

    @property
    def SELENIUM_CHROMEDRIVER_EXECUTABLE_PATH(self) -> str:
        return getattr(
            settings, "SELENIUM_CHROMEDRIVER_EXECUTABLE_PATH", "chromedriver"
        )


conf = Settings()
