import time

from django.contrib.auth import get_user_model
from django.urls import reverse
from selenium.webdriver.common.by import By

from wagtail_guide.factories import MarkdownFactory


def getting_started(live_server, driver):
    with MarkdownFactory("index.md", "Getting started", driver, __name__) as doc:

        doc.p("Log in, and get to know the Wagtail admin.")

        doc.h2("Log in")
        url = reverse("wagtailadmin_login")
        doc.ol(
            [
                f"Navigate to `{url}`",
                f"Enter your *username* and *password*",
                "Click *Sign in*",  # Why is the url `login` and the button `sign in`?
            ]
        )

        username, password = "jane", "secret"
        get_user_model().objects.create_superuser(
            username=username,
            password=password,
            is_active=True,
            email=f"{username}@example.com",
            first_name=username.title(),
        )

        url = live_server.url + reverse("wagtailadmin_login")
        driver.get(url)
        driver.input_text("username", username)
        driver.input_text("password", password)
        button = driver.find_element(By.XPATH, f"//button")
        doc.img("login.png", button, browser=True)
        doc.transcribe()
        button.click()

        doc.h2("Admin")
        doc.p("Welcome to the *administrative interface*, or *admin*.")
        doc.img("admin.png")

        doc.h2("Dashboard")
        doc.p("This first page is called *the dashboard*. It shows a *summary*.")
        doc.img("dashboard.png", driver.find_element(By.CLASS_NAME, "w-summary"))
        doc.transcribe()

        doc.h2("Sidebar")
        doc.p("The gray bar on the side is the *sidebar*.")
        doc.img("sidebar.png", driver.find_element(By.CLASS_NAME, "sidebar"))

        doc.h2("Logo")
        doc.p("You can always click the *logo*, to navigate back to the *dashboard*.")
        doc.img(
            "main-navigation-logo.png",
            driver.find_element(
                By.CLASS_NAME, "sidebar-wagtail-branding__icon-wrapper"
            ),
        )

        doc.h2("Search")
        doc.p("Use *search* to find content.")
        doc.img("search.png", driver.find_element(By.ID, "menu-search-q"))

        doc.h2("Main navigation")
        doc.p(
            "The main navigation contains *pages*, *images*, *documents*, *reports*, and *settings*."
        )
        doc.img(
            "main-navigation.png",
            driver.find_element(By.CLASS_NAME, "sidebar-main-menu__list"),
        )

        doc.h2("Account settings")
        doc.p("Manage your details and preferences via the  *account settings* menu.")
        elm = driver.find_element(By.CLASS_NAME, "sidebar-footer__account")
        elm.click()
        time.sleep(0.5)
        elm = driver.find_element(By.CLASS_NAME, "sidebar-footer")
        doc.img("account-settings.png", elm)

        doc.h2("Log out")
        doc.p("The *log out* option is in *account settings*.")
        doc.img(
            "logout.png",
            driver.find_element(
                By.XPATH, '//*[@id="wagtail-sidebar"]/div/div/div[2]/ul/li[2]/form/button'
            ),
        )
