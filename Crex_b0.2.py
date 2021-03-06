import requests
from bs4 import BeautifulSoup
import re
import xlsxwriter
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

workbook = xlsxwriter.Workbook("%UserProfile%/Desktop/CrexData.xlsx")

page = requests.get("https://spy.deckshop.pro/clan/PRUJPY2R")
soup = (BeautifulSoup(page.content, "html.parser"))
#print(soup.prettify())

tags = [re.sub("[^A-Za-z0-9]", "", i.get_text()) for i in soup.find_all("small", class_="text-muted")
        if re.sub("[^A-Za-z0-9#]", "", i.get_text()).startswith("#")]

names = [i.get_text() for i in soup.find_all("a", class_="h4")]

worksheet = workbook.add_worksheet("Names&Tags")
worksheet.write_column("A1", tags)
worksheet.write_column("B1", names)
"""
for i in range(len(tags)):
    page = requests.get("https://statsroyale.com/tr/profile/"+tags[i]+"/cards?sort=rarity")
    soup = (BeautifulSoup(page.content, "html.parser"))
    if "saniye" or "dakika" not in soup.find_all("div", class_="refresh__time")[0].get_text().split():  
        options = Options()
        options.add_argument("-headless")
        driver = webdriver.Firefox(firefox_options=options)
        driver.get("https://statsroyale.com/tr/profile/"+tags[i])
        button = driver.find_element_by_xpath('//*[@id="refresh-profile"]')
        button.click()
        driver.quit()
        print(100*i/38)

"""
for x in range(len(tags)):
    page = requests.get("https://statsroyale.com/tr/profile/"+tags[x]+"/cards?sort=rarity")
    soup = (BeautifulSoup(page.content, "html.parser"))
    #print(soup.prettify())

    card_names = [i.get_text() for i in soup.find_all("div", class_="ui__tooltip ui__tooltipTop ui__tooltipMiddle cards__tooltip")]
    #print(card_names)

    card_levels = []
    for i in soup.find_all("span", class_="profileCards__level"):
        if i.get_text() == "Maks Sv":
            card_levels.append(13)
        elif i.get_text() == "":
            card_levels.append(0)
        else:
            card_levels.append(int(re.sub("[^0-9]", "", i.get_text())))
    #print(card_levels)

    card_numbers = [int(i.get_text().split("/")[0]) for i in soup.find_all("div", class_="profileCards__meter__numbers")]
    for i in range(len(card_levels)):
        if card_levels[i] == 0:
            card_numbers.insert(i, 0)
    #print(card_numbers)

    worksheet = workbook.add_worksheet(tags[x])
    worksheet.write_column("A1", card_names)
    worksheet.write_column("B1", card_levels)
    worksheet.write_column("C1", card_numbers)
    worksheet.write(6, 9, names[x])

workbook.close()

