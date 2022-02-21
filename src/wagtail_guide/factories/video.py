import os
import tempfile

import requests
from moviepy.editor import (
    AudioClip,
    AudioFileClip,
    ColorClip,
    CompositeVideoClip,
    ImageClip,
    VideoFileClip,
    concatenate_audioclips,
    concatenate_videoclips,
)
from mutagen.wave import WAVE

from .mixins import ImageMixin
from wagtail_guide.conf import conf

image_filenames = []


def synth(text, filename):
    response = requests.get(conf.WAGTAIL_GUIDE_TEXT_TO_SPEECH_URL, params={"text": text})
    with open(filename, "wb") as fd:
        for chunk in response.iter_content(chunk_size=128):
            fd.write(chunk)


class VideoFactory(ImageMixin):
    def __init__(self, filename, title, driver, source_file):
        super().__init__()
        self.blocks = []
        self.build_directory = conf.WAGTAIL_GUIDE_BUILD_DIRECTORY
        self.filename = os.path.join(self.build_directory, filename)
        self.h1(title)
        self.driver = driver

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        clips = []
        audio_clips = []
        audio_duration = 0

        with tempfile.TemporaryDirectory() as directory:
            for idx, (block_type, content) in enumerate(self.blocks):
                # TODO, add title card
                # if block_type == "h1":
                #     bird = VideoFileClip("guide/tests/images/wagtail_trimmed.mov")
                #     bg = ColorClip((2048, 1288), color=(2, 125, 126), duration=bird.duration)
                #     clip = CompositeVideoClip([bg, bird.set_pos('center')])
                #     # clip.audio = concatenate_audioclips(audio_clips)
                #     clips.append(clip)
                if block_type in ["h1", "h2", "p"]:
                    audio_filename = f"{directory}/{idx}.wav"
                    synth(content, audio_filename)
                    audio_clips.append(AudioFileClip(audio_filename))
                    audio_duration += WAVE(audio_filename).info.length
                    breathing_time = 0.2
                    audio_clips.append(AudioClip(lambda t: 0, duration=breathing_time))
                    audio_duration += breathing_time
                elif block_type == "image":
                    clip = ImageClip(content).set_duration(
                        audio_duration + 0.3
                    )  # Some breathing time between clips
                    clip.audio = concatenate_audioclips(audio_clips)
                    clips.append(clip)
                    audio_clips = []
                    audio_duration = 0
                else:
                    raise NotImplementedError(block_type)

            final = concatenate_videoclips(clips)
            final.write_videofile(self.filename, fps=25, audio_codec="aac")

    def h1(self, content):
        self.blocks.append(("h1", content))

    def h2(self, content):
        self.blocks.append(("h2", content))

    def p(self, content):
        self.blocks.append(("p", content))

    def append_image_block(self, filepath):
        self.blocks.append(("image", filepath))
