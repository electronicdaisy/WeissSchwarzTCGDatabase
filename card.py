# img
# trigger = attributes[12]
# http://ws-tcg.com/en/cardlist

# edit

import os
import requests
import sqlite3


def get_card(browser):
    attributes = browser.find_elements_by_xpath('//table[@class="status"]/tbody/tr/td')

    image = attributes[0].find_element_by_xpath('./img').get_attribute('src')

    if attributes[1].find_element_by_xpath('./span[@class="kana"]').text:
        card_name = attributes[1].find_element_by_xpath('./span[@class="kana"]').text
    else:
        card_name = None

    card_no = attributes[2].text if attributes[2].text else None
    rarity = attributes[3].text if attributes[3].text else None
    expansion = attributes[4].text if attributes[4].text else None

    if attributes[5].find_element_by_xpath('./img').get_attribute("src") == "http://ws-tcg.com/en/cardlist/partimages/w.gif":
        side = "Weiß"
    elif attributes[5].find_element_by_xpath('./img').get_attribute("src") == "http://ws-tcg.com/en/cardlist/partimages/s.gif":
        side = "Schwarz"
    else:
        side = None

    card_type = attributes[6].text if attributes[6].text else None

    if attributes[7].find_element_by_xpath('./img').get_attribute("src") == "http://ws-tcg.com/en/cardlist/partimages/yellow.gif":
        color = "Yellow"
    elif attributes[7].find_element_by_xpath('./img').get_attribute("src") == "http://ws-tcg.com/en/cardlist/partimages/green.gif":
        color = "Green"
    elif attributes[7].find_element_by_xpath('./img').get_attribute("src") == "http://ws-tcg.com/en/cardlist/partimages/red.gif":
        color = "Red"
    elif attributes[7].find_element_by_xpath('./img').get_attribute("src") == "http://ws-tcg.com/en/cardlist/partimages/blue.gif":
        color = "Blue"
    else:
        color = None

    level = attributes[8].text if attributes[8].text else None
    cost = attributes[9].text if attributes[9].text else None
    power = attributes[10].text if attributes[10].text else None

    soul = len(attributes[11].find_elements_by_xpath('./img[contains(@src, "http://ws-tcg.com/en/cardlist/partimages/soul.gif")]'))

    special_attribute = attributes[13].text if attributes[13].text else None
    text = attributes[14].text if attributes[14].text else None
    flavor_text = attributes[15].text if attributes[15].text else None

    if not os.path.exists("images"):
        os.makedirs("images")

    if not os.path.exists("images/" + card_no.split("/")[0]):
        os.makedirs("images/" + card_no.split("/")[0])

    r = requests.get(image, stream=True)
    if r.status_code == 200:
        with open("images/" + card_no + ".jpg", 'wb') as f:
            for chunk in r:
                f.write(chunk)


    card = (card_name, card_no, rarity, expansion, side, card_type, color, level, cost, power, soul,
            special_attribute, text, flavor_text)
    connection = sqlite3.connect('cards.sqlite3')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO cards (name, no, rarity, expansion, side, type, color, level, cost, power, soul,'
                   'special_attribute, text, flavor_text) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?)', card)
    connection.commit()
    connection.close()
