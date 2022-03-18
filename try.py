from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd

import time

def login(driver):
    driver.get("https://login.yahoo.com/")

    username = driver.find_element_by_name("username")
    username.send_keys('alozano8')
    driver.find_element_by_id("login-signin").send_keys(Keys.RETURN)

    time.sleep(2)

    password = driver.find_element_by_name("password")
    password.send_keys('0*Xg8NcJpenV')
    driver.find_element_by_id("login-signin").send_keys(Keys.RETURN)

def get_stats():
    chrome_options = Options()
    chrome_options.add_extension("tools/chrome-ublock.crx")
    chrome_options.add_argument("--enable-extensions")

    driver = webdriver.Chrome(executable_path="tools/chromedriver.exe", chrome_options=chrome_options)
    driver.set_page_load_timeout(30)

    print("Logging in")
    login(driver)

    driver.get('https://basketball.fantasysports.yahoo.com/nba/23349/matchup?week=21&date=2022-03-15&mid1=6&mid2=8')

    # Wait for the page to fully load
    time.sleep(5)

    # Step 2: Parse HTML code and grab tables with Beautiful Soup
    soup = BeautifulSoup(driver.page_source, 'lxml')

    tables = soup.find_all('table')

    # Step 3: Read tables with Pandas read_html()
    dfs = pd.read_html(str(tables))

    print(f'Total tables: {len(dfs)}')

    for d in dfs:
        print(d)
        print("------------------")

    driver.close()


if __name__ == "__main__":
    get_stats()