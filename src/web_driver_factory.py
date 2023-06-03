import os
from tempfile import mkdtemp
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver


def web_driver_factory(
    waiting_seconds: int = 5,
) -> tuple[webdriver.Chrome, WebDriverWait]:
    if bool(os.getenv("DEBUG_LOCAL")):
        driver = webdriver.Chrome()
    else:
        options = webdriver.ChromeOptions()
        options.binary_location = "/opt/chrome/chrome"
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280x1696")
        options.add_argument("--single-process")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-dev-tools")
        options.add_argument("--no-zygote")
        options.add_argument(f"--user-data-dir={mkdtemp()}")
        options.add_argument(f"--data-path={mkdtemp()}")
        options.add_argument(f"--disk-cache-dir={mkdtemp()}")
        options.add_argument("--remote-debugging-port=9222")
        driver = webdriver.Chrome("/opt/chromedriver", options=options)

    wait = WebDriverWait(driver, waiting_seconds)
    return driver, wait
