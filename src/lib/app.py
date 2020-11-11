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
import config


# ================== Local Variables ==================
ONE_HOUR = 3600
SCRIPT = 'send-message.applescript'
DRIVER_PATH = '../web-driver/chromedriver'

PRODUCT_NAME = 'Disinfectant Deodorizer Spray'
PRODUCT_URL = 'https://www.amway.com/en_US/Pursue%26trade%3B-Disinfectant-Deodorizer-Spray-%28ORDER-LIMIT-5%29-p-E0023?searchTerm=pursue'

PRODUCT_NAME = 'CBD'
PRODUCT_URL = 'https://www.amway.com/XS%26trade%3B-CBD-Cream-p-296753?experience_id=139&scheme=nosearch1_rr'

ELEMENT_XPATH = '/html/body/main/div[11]/div[2]/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/div/div/div[1]/div[2]/div/span/span[2]'
TODAYS_MESSAGE = """{} is in stock\n{}""".format(PRODUCT_NAME, PRODUCT_URL)

CONTACT_LIST = {
    "ContactList": [
        {"name": "Vini", "number": "17607990511"}
        # ,
        # {"name": "Beth", "number": "17609025715"}
    ]
}

# Set Setting for chrome
chrome_options = Options()
# chrome_options.add_argument('--headless')
DRIVER = webdriver.Chrome(DRIVER_PATH, options=chrome_options)

# ================== Functions ==================


def login():
    DRIVER.get('https://www.amway.com/en_US/')
    sign_in = '//*[@id="mainHeader"]/div/header/div[2]/div/div[3]/div[3]/div/div[1]/button'
    DRIVER.find_element_by_xpath(sign_in).click()

    sign_in_menu = '/html/body/main/div[3]/div/div/ul/li[1]/a'
    DRIVER.find_element_by_xpath(sign_in_menu).click()

    time.sleep(7)

    amway_id_input = '/html/body/div/div/div/app-root/div/div[1]/div/app-signin/div/div/div/div/div/div/app-smart-id/div/app-form-field/div/input'
    amway_id_input = DRIVER.find_element_by_xpath(amway_id_input)
    amway_id_input.send_keys(config.email)

    password_input = '/html/body/div/div/div/app-root/div/div[1]/div/app-signin/div/div/div/div/div/div/password/div/div[2]/input'
    password_input = DRIVER.find_element_by_xpath(password_input)
    password_input.send_keys(config.password)

    sign_in_btn = '/html/body/div/div/div/app-root/div/div[1]/div/app-signin/div/div/div/div/div/div/app-button/button'
    DRIVER.find_element_by_xpath(sign_in_btn).click()


def get_availability(url, xpath):
    # Open Chrome on the URL
    DRIVER.get(url)

    # Get test from the HTML element
    availability = DRIVER.find_element_by_xpath(xpath).text

    # Wait a second and close the window
    time.sleep(1)
    DRIVER.quit()

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
login()
status = 'Temporarily Out-of-Stock'
while status == 'Temporarily Out-of-Stock':
    status = get_availability(PRODUCT_URL, ELEMENT_XPATH)
    print(datetime.datetime.now())
    time.sleep(ONE_HOUR)
    # time.sleep(2)
    if status != 'Temporarily Out-of-Stock':
        send_message(CONTACT_LIST)
