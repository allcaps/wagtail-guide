import os

from bs4 import BeautifulSoup

from .mixins import ImageMixin
from wagtail_guide.conf import conf


def nested_list(items, prefix=""):
    content = ""
    for item in items:
        if isinstance(item, list):
            content += "\n"
            # Note, 4 spaces.
            content += nested_list(item, prefix="    ")
        else:
            content += f"{prefix}- {item}\n"
    return content


class MarkdownFactory(ImageMixin):
    def __init__(self, filename, title, driver, source_file):
        super().__init__()
        self.blocks = []
        self.build_directory = conf.WAGTAIL_GUIDE_BUILD_DIRECTORY
        self.filename = os.path.join(self.build_directory, filename)
        self.comment(
            f"To update this file, edit `{source_file}` and run `python manage.py build_docs`."
        )
        self.h1(title)
        self.driver = driver

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        with open(self.filename, "w") as doc:
            doc.write("\n\n".join(self.blocks))

    def raw(self, content):
        self.blocks.append(content)

    def comment(self, content):
        self.blocks.append(f"[//]: # ({content})")

    def h1(self, content):
        self.blocks.append(f"# {content}")

    def h2(self, content):
        self.blocks.append(f"## {content}")

    def p(self, content):
        self.blocks.append(content)

    def ul(self, items):
        self.blocks.append(nested_list(items))

    def ol(self, items):
        self.blocks.append(
            "\n".join([f"{idx + 1}. {item}" for idx, item in enumerate(items)])
        )

    def code(self, type_, content):
        if type_:
            self.blocks.append(f"``` {type_}\n{content}\n```")
        else:
            self.blocks.append(f"```\n{content}\n```")

    def admonition(self, type_, content):
        # Prepend new lines with four spaces.
        content = "\n    ".join(content.split("\n"))
        self.blocks.append(f"!!! {type_}\n\n    {content}")

    def note(self, content):
        self.admonition("note", content)

    def warning(self, content):
        self.admonition("warning", content)

    def append_image_block(self, filepath):
        filename = os.path.basename(filepath)
        relative_filepath = f"images/{filename}"
        self.blocks.append(f"![alt]({relative_filepath})")

    def transcribe(self):
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        text_elements = soup.find_all(text=True)
        disallowed_list = [
            "header",
            "html",
            "meta",
            "input",
            "script",
            "symbol",
        ]
        content = ""
        for elm in text_elements:
            if elm.parent.name not in disallowed_list and elm:
                content += f"{elm}\n"

        # TODO: Use BeautifulSoup to remove redundant elements.
        # Drop some HTML comment hacks. They break the Markdown output.
        code = f"<code>{content}</code>".replace("[if lt IE 9]>", "").replace(
            "<![endif]", ""
        )

        # TODO: Maybe strip some repeating content that lives on each page?

        self.blocks.append(
            f"""<details><summary>Transcript</summary>{code}</details>"""
        )
