from src.paper_status import PaperStatus
from selenium import webdriver


def scrap(journal_url: str, username: str, password: str) -> PaperStatus:
    TITLE_COLUMN = 2
    STATUS_DATE_COLUMN = 4
    STATUS_COLUMN = 5

    # dict with data to print
    data: PaperStatus = {
        "title": "No paper title found",
        "step": "No paper step found",
        "status": "No paper found",
        "status_date": "No paper status date found",
    }

    # open chrome and go to website
    driver = webdriver.Chrome()
    driver.get(journal_url)

    # fill in username and password
    username_input = driver.find_element_by_id("username")
    username_input.send_keys(username)
    password_input = driver.find_element_by_id("password")
    password_input.send_keys(password)

    # click login button by name
    login_button = driver.find_element_by_name("authorLogin")
    login_button.click()

    # wait for page to load
    driver.implicitly_wait(10)

    # get authorMainMenu form by id
    authorMainMenu = driver.find_element_by_id("authorMainMenu")

    # get second element with given html tag inside the menu
    clickable_elements = authorMainMenu.find_elements_by_tag_name("a")
    if len(clickable_elements) <= 1:
        return data
    data["step"] = clickable_elements[1].text

    # click on the second element
    clickable_elements[1].click()

    # wait for page to load
    driver.implicitly_wait(10)

    # get the table with the papers
    table = driver.find_element_by_id("datatable")

    # get first row of the table
    first_row = table.find_element_by_id("row1")

    # get all row columns
    fields = first_row.find_elements_by_tag_name("td")

    # get the title of the paper (3rd column)
    data["title"] = fields[TITLE_COLUMN].text

    # get the status of the paper (6th column)
    data["status"] = fields[STATUS_COLUMN].text

    # get status date (5th column)
    data["status_date"] = fields[STATUS_DATE_COLUMN].text

    # close chrome
    driver.close()

    return data
