import os
import time
import yaml
import logging
from bs4 import BeautifulSoup
import pandas as pd
import datetime

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


_logger = logging.getLogger(__name__)


def _current_directory():
    return os.path.dirname(os.path.abspath(__file__))

    
def _wait_page_loads():
    
    WAIT_PAGE_LOADS = 2.0
    time.sleep(WAIT_PAGE_LOADS)
    


def _access_website():

    CHROME_DRIVE_APPLICATION = 'chromedriver.exe'
    crome_driver_path = os.path.join(os.path.dirname(_current_directory()), 
                            os.path.join('tools', CHROME_DRIVE_APPLICATION))
    
    WEBSITE_URL = 'https://login.yahoo.com/'
    
    chrome_options = webdriver.ChromeOptions()

    CHROME_DRIVE_EXTENSION = 'chrome-ublock.crx'
    chrome_ublock_path = os.path.join(os.path.dirname(_current_directory()), 
                            os.path.join('tools', CHROME_DRIVE_EXTENSION))

    chrome_options.add_extension(chrome_ublock_path)
    chrome_options.add_argument("--enable-extensions")

    driver = webdriver.Chrome(executable_path=crome_driver_path, chrome_options=chrome_options)
    driver.set_page_load_timeout(30)

    driver.get(WEBSITE_URL)

    _wait_page_loads()
    
    return driver

    
def _login(driver, settings):

    username = driver.find_element_by_name("username")
    username.send_keys(settings['user_name'])
    driver.find_element_by_id("login-signin").send_keys(Keys.RETURN)

    _wait_page_loads()

    try:
        password = driver.find_element_by_name("password")
        password.send_keys(settings['password'])
        driver.find_element_by_id("login-signin").send_keys(Keys.RETURN)

    except:
        print("I can't find the password box, please, resolve captcha")
        input('Press Enter to continue after resolving captcha.\n')
        password = driver.find_element_by_name("password")
        password.send_keys(settings['password'])
        driver.find_element_by_id("login-signin").send_keys(Keys.RETURN)


def _open_matchup(driver):

    MATCHUP_PAGE_URL = 'https://basketball.fantasysports.yahoo.com/nba/23349/matchup?week=21'
    driver.get(MATCHUP_PAGE_URL)        
    
    _wait_page_loads()

    
def _update_clock(driver):
    
    REGISTER_PAGE_URL = "/html/body/form/table/tbody/tr/td[3]/div/table/tbody/tr[4]/td[2]/div/table/tbody/tr[1]/td/fieldset/table/tbody/tr[1]/td/a"
    button = driver.find_element_by_xpath(REGISTER_PAGE_URL)

    action = ActionChains(driver)
    action.move_to_element(button).click().perform()

    _wait_page_loads()

def _get_result_info(driver):
    soup = BeautifulSoup(driver.page_source, 'lxml')
    tables = soup.find_all('table')
    dfs = pd.read_html(str(tables))
    return dfs[1]

def _get_week_info(driver, weekLinks):

    today = datetime.date.today()
    oldWeekInfo = []
    remainingWeekInfo = []

    for dayLink in weekLinks:
        dateString = dayLink.split('date=')[1].split('&')[0].split('-')
        date = datetime.date(int(dateString[0]), int(dateString[1]), int(dateString[2]))
        driver.get(dayLink)
        _wait_page_loads()
        soup = BeautifulSoup(driver.page_source, 'lxml')
        tables = soup.find_all('table')
        dfs = pd.read_html(str(tables))

        if date < today:
            oldWeekInfo.append(dfs[2])

        else:
            remainingWeekInfo.append(dfs[2])

    return oldWeekInfo, remainingWeekInfo


def _get_week_links(driver):

    monday_link = driver.find_element_by_partial_link_text('Mon,').get_attribute("href")
    tuesday_link = driver.find_element_by_partial_link_text('Tue,').get_attribute("href")
    wednesday_link = driver.find_element_by_partial_link_text('Wed,').get_attribute("href")
    thursday_link = driver.find_element_by_partial_link_text('Thu,').get_attribute("href")
    friday_link = driver.find_element_by_partial_link_text('Fri,').get_attribute("href")
    saturday_link = driver.find_element_by_partial_link_text('Sat,').get_attribute("href")
    sunday_link = driver.find_element_by_partial_link_text('Sun,').get_attribute("href")

    return [monday_link, tuesday_link, wednesday_link, thursday_link, friday_link, saturday_link, sunday_link]


def current_directory():
    return _current_directory()
    
    
def load_settings():
    
    file_path = os.path.join(os.path.dirname(_current_directory()), 
                    os.path.join('config', 'settings.yaml'))
    
    with open(file_path, 'r') as stream:    
        server_credentials = yaml.load(stream, Loader=yaml.FullLoader)        
        user = server_credentials['user']
        password = server_credentials['password']
        
    return user, password

    
def connect(settings = {}):

    driver = _access_website()
    _login(driver, settings)
    
    return driver

    
def getMatchupData(driver):

    _open_matchup(driver)
    resultInfo = _get_result_info(driver)
    weekLinks = _get_week_links(driver)
    oldWeekInfo, remainingWeekInfo = _get_week_info(driver, weekLinks)

    return resultInfo, oldWeekInfo, remainingWeekInfo

        
def close(driver):
    driver.quit()
