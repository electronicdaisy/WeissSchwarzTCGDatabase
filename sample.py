from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import sqlite3
import time
from card import get_card


# some global variables, which are used
pause = 5

connection = sqlite3.connect('cards.sqlite3')
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS `cards` (" \
               "`id`                   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE," \
               "`name`                 TEXT NOT NULL," \
               "`no`                   TEXT NOT NULL UNIQUE," \
               "`rarity`               TEXT NOT NULL," \
               "`expansion`            TEXT NOT NULL," \
               "`side`                 TEXT NOT NULL," \
               "`type`                 TEXT NOT NULL," \
               "`color`                TEXT NOT NULL," \
               "`level`                NUMERIC," \
               "`cost`                 NUMERIC," \
               "`power`                NUMERIC," \
               "`soul`                 NUMERIC," \
               "`special_attribute`   TEXT," \
               "`text`                 TEXT," \
               "`flavor_text`          TEXT" \
               ");")

connection.commit()
connection.close()


browser = webdriver.Chrome(executable_path=r"C:\Users\Alex\PycharmProjects\chromedriver.exe")
browser.get("http://ws-tcg.com/en/cardlist/list/")
time.sleep(pause)


# loop for finding set and clicking on it
for i in range(len(browser.find_elements_by_xpath("//div[@id='expansionList']/div/ul/li/a"))):
    if i < 60:
        continue
    browser.find_elements_by_xpath("//div[@id='expansionList']/div/ul/li/a")[i].click()
    time.sleep(pause)
    browser.find_elements_by_xpath('//a[contains(@href, "?cardno=")]')[0].click()
    time.sleep(pause)

    get_card(browser=browser)

    disabled = True
    while disabled:
        try:
            browser.find_element_by_xpath('//p[@class="neighbor"]/span[@class="disable" and contains(text(), "next")]')
        except NoSuchElementException:
            browser.find_element_by_xpath("//p[@class='neighbor']/a[contains(text(), 'next')]").click()
            time.sleep(pause)

            get_card(browser=browser)

            continue
        else:
            disabled = False

browser.quit()
