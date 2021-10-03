import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import credentials
import time
import re

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
url = "https://monetwfo-eu.com/Monet5/Default.aspx/"
driver.get(url)

print(driver.title)
tenant = driver.find_element_by_id('txtTenantId')
tenant.send_keys(credentials.get_tenant())

username = driver.find_element_by_id('txtUserName')
username.send_keys(credentials.get_username())

password = driver.find_element_by_id('txtPassword')
password.send_keys(credentials.get_password(credentials.get_username()))
time.sleep(0)
submit_button = driver.find_element_by_id('btnSubmit')
submit_button.send_keys(Keys.RETURN)

try:
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'frameContent')))
    schedule_title = driver.find_element_by_css_selector("#scheduleTitle")
    activities = driver.find_element_by_css_selector('#activities')
    for activity in range(7):
        monet_activity = driver.find_element_by_css_selector('#activity' + str(activity))
        pattern = "[0-9]+\:\d[0-9]"
        eventTime = re.findall(pattern, monet_activity.text)
        for i, item in enumerate(eventTime):
            readable_time = schedule_title.text + " " + eventTime[i]
            f = open("schedules.txt", "a")
            datetime_object = datetime.strptime(readable_time, '%A, %b %w, %Y %H:%M')
            print(datetime_object)
            f.write(str(datetime_object)+ "\n")
            f.close()
            f = open("schedules.txt", "r")
            print(f.read())

except Exception as e:
    print(e)
finally:
    driver.quit()
