import logging
import os
from tempfile import mkdtemp

from selenium.webdriver.support.wait import WebDriverWait

from src.paper_status import PaperStatus
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def scrap(journal_url: str, username: str, password: str) -> PaperStatus:
    TITLE_COLUMN = 2
    STATUS_DATE_COLUMN = 4
    STATUS_COLUMN = 5

    # dict with data to print
    data: PaperStatus = PaperStatus(
        title="No paper title found",
        step="No paper step found",
        status="No paper found",
        status_date="No paper status date found",
    )
    print(f'starting{bool(os.getenv("DEBUG_LOCAL"))}')
    if bool(os.getenv("DEBUG_LOCAL")):
        driver = webdriver.Chrome()
    else:
        options = Options()
        options.binary_location = '/opt/headless-chromium'
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--single-process')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--start-maximized")
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--no-zygote")
        options.add_argument(f"--user-data-dir={mkdtemp()}")
        options.add_argument(f"--data-path={mkdtemp()}")
        options.add_argument(f"--disk-cache-dir={mkdtemp()}")
        driver = webdriver.Chrome('/opt/chromedriver', chrome_options=options)

    WAITING_SECONDS = 2
    wait = WebDriverWait(driver, WAITING_SECONDS)
    print("start")
    driver.get(journal_url)
    print("started")
    # switch to content iframe
    content_frame = wait.until(EC.visibility_of_element_located((By.ID, "content")))
    driver.switch_to.frame(content_frame)

    # switch to content iframe
    login_frame = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "iframe")))
    driver.switch_to.frame(login_frame)

    # fill in username and password
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys(username)
    password_input = driver.find_element(By.ID, "passwordTextbox")
    password_input.send_keys(password)

    # click login button by name
    login_button = driver.find_element(By.NAME, "authorLogin")
    login_button.click()
    logging.info("Logging in")

    # wait for page to load
    driver.implicitly_wait(WAITING_SECONDS)

    # switch to content iframe

    # for i in range(2):
    content_frame = wait.until(EC.element_to_be_clickable((By.ID, "content")))
    driver.switch_to.frame(content_frame)

    # get authorMainMenu form by id
    twoColLayoutItems = driver.find_element(By.ID, "twoColLayoutItems")

    # get second element with given html tag inside the menu
    clickable_elements = twoColLayoutItems.find_elements(By.TAG_NAME, "a")
    if len(clickable_elements) <= 1:
        return data
    data.step = clickable_elements[1].text

    # click on the second element
    clickable_elements[1].click()
    logging.info("Checking paper status")

    # wait for page to load
    driver.implicitly_wait(WAITING_SECONDS)

    # get the table with the papers
    # table = driver.find_element(By.ID, "datatable")
    table = wait.until(EC.visibility_of_element_located((By.ID, "datatable")))
    # get first row of the table
    first_row = table.find_element(By.ID, "row1")

    # get all row columns
    fields = first_row.find_elements(By.TAG_NAME, "td")

    # get the title of the paper (3rd column)
    data.title = fields[TITLE_COLUMN].text

    # get the status of the paper (6th column)
    data.status = fields[STATUS_COLUMN].text

    # get status date (5th column)
    data.status_date = fields[STATUS_DATE_COLUMN].text
    logging.info("Paper status found")
    # close chrome
    driver.close()

    return data
