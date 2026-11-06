
from contextlib import contextmanager
from playwright.sync_api import sync_playwright


@contextmanager
def browser_session(headless=False):

    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(
            headless=headless
        )

        page = browser.new_page(
            viewport={
                "width": 1365,
                "height": 900
            }
        )

        try:
            yield page

        finally:
            browser.close()
