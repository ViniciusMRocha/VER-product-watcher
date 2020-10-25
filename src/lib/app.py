# # pip install selenium
import pprint
import json
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import datetime


# ================== Local Variables ==================
ONE_HOUR = 3600
SCRIPT = 'send-message.applescript'
DRIVER_PATH = '/Users/viniciusrocha/development/VER-product-watcher/src/web-driver/chromedriver'
PRODUCT_URL = 'https://www.amway.com/en_US/Pursue%26trade%3B-Disinfectant-Deodorizer-Spray-%28ORDER-LIMIT-5%29-p-E0023?searchTerm=pursue'
ELEMENT_XPATH = '/html/body/main/div[11]/div[2]/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/div/div/div[1]/div[2]/div/span/span[2]'

TODAYS_MESSAGE = """Product is in stock
{}""".format(PRODUCT_URL)

CONTACT_LIST = {
    "ContactList": [
        {"name": "Vini", "number": "17607990511"},
        {"name": "Beth", "number": "17609025715"}
    ]
}


# ================== Functions ==================
def get_availability(url, xpath):
    # Set Setting for chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(DRIVER_PATH, options=chrome_options)

    # Open Chrome on the URL
    driver.get(url)

    # Get test from the HTML element
    availability = driver.find_element_by_xpath(xpath).text

    # Wait a second and close the window
    time.sleep(1)
    driver.quit()

    return availability


def send_message(data):
    # Iterate over each contact
    for contact in data['ContactList']:
        name = contact['name']
        number = contact['number']

        print('Sending message to {} on number {}'.format(name, number))

        # Form message
        message = 'Hey {}, {}'.format(name, TODAYS_MESSAGE)

        # Form the command to send message
        command = 'osascript ../../scripts/{} {} "{}"'.format(
            SCRIPT, number, message)

        # Execute the send message command
        os.system(command)


# ================== App ==================
status = 'Temporarily Out-of-Stock'
while status == 'Temporarily Out-of-Stock':
    time.sleep(ONE_HOUR)
    print(datetime.datetime.now())
    status = get_availability(PRODUCT_URL, ELEMENT_XPATH)
    if status != 'Temporarily Out-of-Stock':
        send_message(CONTACT_LIST)
