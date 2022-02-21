import time

from django.contrib.auth import get_user_model
from django.urls import reverse

from selenium.webdriver.common.by import By

from wagtail_guide.factories import VideoFactory


def getting_started(live_server, driver):
    with VideoFactory(
            "out.mp4", "Getting started", driver, __name__
    ) as doc:

        doc.p("Open a browser, and go to slash admin.")
        doc.p("Enter your username and password.")
        doc.p("Click sign in.")

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
        doc.img("login.png", button)
        button.click()

        doc.p("Welcome to the administrative interface, or admin for short.")
        doc.img("admin.png")

        doc.p("This first page is called the dashboard – It shows a summary.")
        doc.img("dashboard.png", driver.find_element(By.CLASS_NAME, "summary"))

        doc.p("The gray bar on the side is the sidebar.")
        doc.img("sidebar.png", driver.find_element(By.CLASS_NAME, "sidebar"))

        doc.p("Wherever you are, you can always click the logo, to navigate back to the dashboard.")
        doc.img("main-navigation-logo.png", driver.find_element(By.CLASS_NAME, "sidebar-wagtail-branding__icon-wrapper"))

        doc.p("Use search to find content.")
        doc.img("search.png", driver.find_element(By.ID, "menu-search-q"))

        doc.p("The main navigation contains pages, images, and documents.")
        doc.p("In reports you'll find an audit trail, and other reports.")
        doc.p("In settings you can manage users, and configure your site.")
        doc.img("main-navigation.png", driver.find_element(By.CLASS_NAME, "sidebar-main-menu__list"))

        doc.p("Manage your personal details and preferences in the account settings menu.")
        elm = driver.find_element(By.CLASS_NAME, "sidebar-footer__account")
        elm.click()
        time.sleep(0.5)
        elm = driver.find_element(By.CLASS_NAME, "sidebar-footer")
        doc.img("account-settings.png", elm)

        doc.p("The log out option is in account settings.")
        doc.img("logout.png", driver.find_element(By.XPATH, '//*[@id="wagtail-sidebar"]/div/div/div/div/ul/li[2]/a'))
