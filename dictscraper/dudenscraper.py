from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox

from bs4 import BeautifulSoup

options = Options()
options.add_argument("--headless")

browser = Firefox(options=options)

def get_syllables(URL: str) -> str:
    browser.get(URL)
    content = browser.page_source
    soup = BeautifulSoup(content, 'html.parser')
    try:
        rechtschreibung = soup.find('div', attrs={'class':'division'}).find('dd')
    except AttributeError:
        return ''
    return rechtschreibung.text

out_list = []
with open('autocomplete.txt', 'r') as file:
    while 1:
        word = file.readline()
        if not word:
            print('terminating')
            break
        url = f'https://www.duden.de/rechtschreibung/{word}'
        syls = get_syllables(url).replace('|',';')
        if syls:
            print(syls)
            out_list.append(syls)

with open('syllables_de.txt', 'w+') as file:
    for word in out_list:
        file.writeline(word)


