# Wagtail Guide

A user guide for Wagtail powered sites.

Wagtail guide uses Pytest + Selenium + Markdown + MKDocs. 

1. **Pytest** runs tests
2. **Selenium** drives a browser and takes screenshots
3. Wagtail Guide **MarkDownFactory** generates Markdown files
4. **MKDocs** renders the documentation (optional)


## Prerequisites 

### Chrome Driver

Chrome Driver on OSX (foreground mode):

    brew install --cask chromedriver

Move ChromeDriver out of quarantine:

    xattr -d com.apple.quarantine /usr/local/bin/chromedriver
    spctl --add --label 'Approved' /usr/local/bin/chromedriver

If `chromedriver` isn't on your path, set `SELENIUM_CHROMEDRIVER_EXECUTABLE_PATH`.

If you don't like to install the Chrome Driver to your system, use Docker. 
This will execute in headless mode. Not suitable for development.

Apple Silicon:

    docker run -d -p 4444:4444 --shm-size="2g" seleniarm/standalone-chromium

Intel Silicon:

    docker run -d -p 4444:4444 --shm-size=2g selenium/standalone-chrome

### FFMPEG (optional)

If you'd like to output video:

    brew install ffmpeg

### TTS (optional)

If you like to output video. Text to speech:

    docker run -it -p 5002:5002 synesthesiam/mozillatts:en

## Install

    pip install git+https://github.com/allcaps/wagtail-guide#egg=wagtail_guide

    INSTALLED_APPS = [
        "wagtail_guide",
        ...
    ]

## Usage

Foreground mode (chromedriver required)

    python manage.py build_guide

Headless mode (Selenium Docker required)

    SELENIUM_REMOTE_URL=YOUR_HOST_IP python manage.py build_guide --headless


To convert markdown to documentation, I'd suggest using MkDocs. In your project root:

    pip install mkdocs
    mkdocs new .
    # Add pages to mkdocs.yml `nav` section.
    # Ref: https://www.mkdocs.org/getting-started/#adding-pages
    mkdocs serve


## Customise the documentation generation

Wagtail guide comes with Markdown, reStructuredText and video support.

The `WAGTAIL_GUIDE_CHAPTERS` are called in order with `live_server` and `driver` as arguments.

    WAGTAIL_GUIDE_CHAPTERS = [
            "wagtail_guide.markdown.getting_started",
            "wagtail_guide.markdown.demo",
    ]

Extend and/or customise the documentation generation. Add your callables to `WAGTAIL_GUIDE_CHAPTERS`.


# Big thanks to

- https://github.com/django/django
- https://github.com/wagtail/wagtail
- https://github.com/SeleniumHQ/selenium
- https://github.com/baijum/selenium-python
- https://github.com/pytest-dev/pytest
- https://github.com/pytest-dev/pytest-django
- https://github.com/mozilla/TTS
- https://github.com/quodlibet/mutagen
- https://github.com/FFmpeg/FFmpeg
- https://github.com/Zulko/moviepy
