# write a function that uses selenium and uses email and password from a .env file to log into a website

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
#from dotenv import load_dotenv
#load_dotenv()


# get email and password from .env file
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

# open chrome and go to website
driver = webdriver.Chrome()
driver.get(os.getenv("JOURNAL_URL"))

# click login button

# enter email and password

# click login button

# click upload file button
