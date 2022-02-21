from django.contrib.auth import get_user_model
from django.urls import reverse
from selenium.webdriver.common.by import By

from wagtail_guide.factories import MarkdownFactory


def demo(live_server, driver):
    with MarkdownFactory(f"demo.md", "Demo", driver, __name__) as doc:
        doc.p("A showcase of all available `MarkdownFactory` elements")

        # Markdown comment, will be in the `*.md` file, won't be in the HTML output.
        doc.comment("This is a comment")

        # This a RAW string
        # Markdown accepts all HTML. So this comment renders in the `*.md` file AND in the HTML output.
        doc.raw("<!-- Why do you inspect the HTML source? -->")

        doc.h2("Paragraph")
        doc.p(
            "Bacon ipsum dolor amet ribeye strip steak hamburger tongue turducken pastrami jerky, "
            "andouille buffalo shank turkey beef sirloin. T-bone frankfurter doner, sirloin jerky "
            "meatloaf short loin bresaola chicken kevin cupim."
        )
        doc.p(
            "Prosciutto flank buffalo, boudin pork chop doner burgdoggen swine. "
            "Capicola filet mignon ham hock pork belly pork, hamburger pig."
        )
        doc.p("**Inline styles** are _awesome_!")

        doc.h2("Unordered list")
        doc.ul(["Foo", "Bar", "Ni", ["This is", "a nested", "list"]])

        doc.h2("Ordered list.")
        doc.ol(["One", "Two", "Three"])

        doc.h2("Code")
        doc.code(
            "py",
            "from django.template.loader import render_to_string\n"
            "rendered = render_to_string('my_template.html', {'foo': 'bar'})",
        )

        doc.h2("Admonition")
        doc.note("Don't panic!")
        doc.warning("Watch your step.")

        # TODO Image, improve API
        doc.h2("Image")
        doc.raw("![Cat at work](https://placekitten.com/400/300)")

        doc.h2("Screenshot")
        doc.p("A automatic screenshot with highlighted element, and browser chrome.")

        username, password = "john", "secret"
        get_user_model().objects.create_superuser(
            username=username,
            password=password,
            is_active=True,
            email=f"{username}@example.com",
            first_name=username.title(),
        )

        url = live_server.url + reverse("wagtailadmin_logout")
        driver.get(url)

        url = live_server.url + reverse("wagtailadmin_login")
        driver.get(url)
        driver.input_text("username", username)
        driver.input_text("password", password)
        elm = driver.find_element(By.XPATH, f"//button")
        doc.img("login-browser.png", elm, browser=True)

        doc.p("A screenshot without highlighted element, and without browser chrome.")
        doc.img("login-element.png")

        doc.h2("Crop")
        doc.p("Crop of a specific element.")
        doc.crop("login-crop.png", elm)
