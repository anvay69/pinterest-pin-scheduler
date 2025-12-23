# TODO: exception handling for:
# network error
# selector error
# startup error
# input error
# click interrupt error


# selenium/webdriver core
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# selenium utility
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# storing and loading cookies
from datetime import datetime, timedelta
# import time # might need it cuz I don't know asynchronous programming
import os
import json
# import re


# driver and other variables
driver = None
selectors = None
date_locations = None



# a custom class, no use really
class WhatInputException(Exception):
    def __init__(self, message):
        super().__init__(message)



# get index of a time value in the form of "HH:MM AM/PM"
def get_time_index(raw_time: str) -> int:
    '''
    returns the index (starting from 12:00 AM) of given time string
    '''
    raw_time = raw_time.upper()

    hours = raw_time[:2] 
    minutes = raw_time[3:5]
    daytime = raw_time[-2:]

    if hours == '12':
        base = 0
    else: base = 2 * int(hours)

    if int(minutes) >= 30:
        half_hour_adjust = 1
    else: half_hour_adjust = 0

    if daytime == 'AM':
        daytime_adjust = 0
    else: daytime_adjust = 24

    return base + half_hour_adjust + daytime_adjust



# method to set the profile of a user
def set_profile(user_directory, profile_directory) -> None:
    '''
    updates the profile-dir and user-data-dir in settings.json
    '''
    with open("settings.json", "r") as file:
        settings = json.load(file)

    settings["user-data-dir"] = user_directory
    settings["profile-dir"] = profile_directory

    with open("settings.json", "w") as file:
        json.dump(settings, file)



def start() -> None:
    '''
    loads the home page
    loads the stored cookies
    loads the pin builder
    '''
    global driver, selectors, date_locations

    # creating a service
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()

    # adding user data and profile arguments
    with open("settings.json", "r") as file:
        settings = json.loads(file.read())
        selectors = settings["selectors"]
        date_locations = settings["date_locations"]
        options.add_argument(f"user-data-dir={settings['user-data-dir']}")
        options.add_argument(f"profile-directory={settings['profile-dir']}")
    
    # our driver
    driver = webdriver.Chrome(service=service, options=options)

    # wait before loading the page
    driver.implicitly_wait(10)
    driver.get("https://in.pinterest.com/pin-builder")



# method to return adjust time index and max time index
def get_time_settings(modifier, start_date):
    '''
    takes the date modifier and start date.
    returns the adjust time index and max time index
    '''

    # if start date is today's date
    if datetime.strftime(datetime.now(), modifier) == start_date:
        adjust_time_index = get_time_index(datetime.strftime(datetime.now(), "%I:%M %p"))+1
        max_time_index = 47-adjust_time_index
    else:
        adjust_time_index = 0
        max_time_index = 47
    
    # returning a tuple
    return adjust_time_index, max_time_index



# creates pins
def create_pins(
        board: str, link: str, 
        images_folder: str, 
        num: int, location: str, 
        start_date: str, start_time: str) -> webdriver:
    '''
    creates ready to publish pins
    takes necessary arguments for duplicating boards
    duplicates boards, sends keys to image elements
    sets date and time for each board
    returns the driver
    '''

    # click the board dropdown menu
    board_select = WebDriverWait(driver=driver, timeout=10).until(
        EC.presence_of_element_located(("css selector", selectors["board_select"]))
    )
    board_select.click()

    # select the board
    board_row = WebDriverWait(driver=driver, timeout=10).until(
        EC.presence_of_element_located(
            ("css selector", 
             selectors["board_row"].replace("{[board-name]}", board))
        )
    )
    board_row.click()

    # enter the link in 'link input' element
    link_input = WebDriverWait(driver=driver, timeout=10).until(
        EC.presence_of_element_located(("css selector", selectors["link_input"]))
    )
    link_input.click()

    driver.implicitly_wait(3) # wait 3 seconds to detect click
    link_input.send_keys(link)
    # link_input.send_keys(Keys.ENTER)

    # clicking the publish later button before duplicating
    publish_later = WebDriverWait(driver=driver, timeout=10).until(
        EC.presence_of_element_located(("css selector", selectors["publish_later"]))
    )
    publish_later.click()

    # Duplicating the board
    for i in range(num-1):
        # That three dot menu on the top board
        option_menu = WebDriverWait(driver=driver, timeout=10).until(
            EC.presence_of_element_located(("css selector", selectors["option_menu"]))
        )
        option_menu.click()

        # Second option [duplicate] of the option menu
        duplicate_option = WebDriverWait(driver=driver, timeout=10).until(
            EC.presence_of_element_located(("css selector", selectors["duplicate_option"]))
        )
        duplicate_option.click()
    
    # getting the list of image files
    assert os.path.exists(images_folder), \
    "Path to Image Folder is invalid"

    images_list = os.listdir(images_folder)
    assert len(images_list) == num, \
    "Number of images doesn't match number of pins"

    # pin image input elements list
    image_inputs = WebDriverWait(driver=driver, timeout=10).until(
        EC.presence_of_all_elements_located(("css selector", selectors["image_input"]))
    )
    image_inputs = driver.find_elements(
        "css selector", selectors["image_input"])

    # setting up images for each pin
    for i in range(num):
        driver.implicitly_wait(5)
        image_inputs[i].send_keys(
            os.path.join(images_folder, images_list[i])
        )

    # get the date modifier
    modifier = date_locations[location]
    # get the adjust index and max index
    adjust_time_index, max_time_index = get_time_settings(modifier=modifier, start_date=start_date)
    # get and adjust the current time index
    curr_time_index = get_time_index(start_time) - adjust_time_index
    
    # list of date and time inputs
    date_inputs = driver.find_elements("css selector", selectors["date_input"])
    time_inputs = driver.find_elements("css selector", selectors["time_input"])

    # check if everything is alright
    assert len(date_inputs) == num and len(time_inputs) == num,\
        "Date or Time input number mismatch"
    
    # now updating the dates and times for each board
    for i in range(num):
        # sending the date to date input elements
        for _ in range(15):
            date_inputs[i].send_keys(Keys.BACKSPACE)
        driver.implicitly_wait(1)
        date_inputs[i].send_keys(start_date)

        # wait a little and click time menu
        driver.implicitly_wait(1)
        time_inputs[i].click()

        # click the time row with curr_time_index
        time_elem = WebDriverWait(driver=driver, timeout=10).until(
            EC.visibility_of_element_located((
                "css selector",
                selectors["time_element"].replace("{[time-index]}", str(curr_time_index))
            ))
        )
        time_elem.click()

        # check if we need to roll over to next day
        if curr_time_index == max_time_index:
            # resetting parameters
            curr_time_index = 0
            max_time_index = 47

            # rolling over
            initial_day = datetime.strptime(start_date, modifier)
            result_day = initial_day + timedelta(days=1)
            start_date = datetime.strftime(result_day, modifier)
        else:
            # else just move to next row
            curr_time_index += 1

    # returning driver so driver can be closed from outside the module
    return driver
