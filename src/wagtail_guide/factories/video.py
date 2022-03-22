import os
import tempfile

import requests
from moviepy.audio.fx.all import audio_fadeout, volumex
from moviepy.editor import (
    AudioClip,
    AudioFileClip,
    ColorClip,
    CompositeAudioClip,
    CompositeVideoClip,
    ImageClip,
    TextClip,
    VideoFileClip,
    concatenate_audioclips,
    concatenate_videoclips,
)
from mutagen.wave import WAVE

from wagtail_guide.conf import conf

from .mixins import ImageMixin

image_filenames = []


def synth(text, filename):
    response = requests.get(
        conf.WAGTAIL_GUIDE_TEXT_TO_SPEECH_URL, params={"text": text}
    )
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

        lead_in = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "images", "in.mp4"
        )
        lead_out = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "images", "out.mp4"
        )
        vanity_card = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "images",
            "vanity-card.png",
        )
        lead_audio = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "audio", "lead.mp3"
        )
        theme_audio = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "audio", "theme.wav"
        )

        with tempfile.TemporaryDirectory() as directory:
            clips.append(VideoFileClip(lead_in))
            clips.append(ImageClip(vanity_card).set_duration(2))
            for idx, (block_type, content) in enumerate(self.blocks):
                if block_type == "h1":
                    clip = TextClip(
                        size=(2048, 1288),
                        txt=content,
                        color="white",
                        bg_color="#000051",
                        fontsize=144,
                        font="Roboto-Bold",
                    )
                    clip = clip.set_pos("center").set_duration(3)
                    clips.append(clip)
                elif block_type in ["h2", "p"]:
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

            clips.append(ImageClip(vanity_card).set_duration(2))
            clips.append(VideoFileClip(lead_out))
            clips.append(ColorClip((2048, 1288), color=(0, 0, 0)).set_duration(0.2))
            final = concatenate_videoclips(clips)

            final_audio = [
                AudioFileClip(lead_audio).set_start(0.3),
                AudioFileClip(theme_audio)
                .set_start(2)
                .fx(volumex, 0.2)
                .set_duration(final.audio.duration + 3)
                .fx(audio_fadeout, 2),
                final.audio,
            ]
            final.audio = CompositeAudioClip(final_audio)
            final.write_videofile(self.filename, fps=25, audio_codec="aac")

    def h1(self, content):
        self.blocks.append(("h1", content))

    def h2(self, content):
        self.blocks.append(("h2", content))

    def p(self, content):
        self.blocks.append(("p", content))

    def append_image_block(self, filepath):
        self.blocks.append(("image", filepath))
