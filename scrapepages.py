from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import requests
from bs4 import BeautifulSoup


def scrape_zoolert(include_all: bool = False):
    sold_out = []
    in_stock = []
    url = 'https://www.zoolert.com/videogames/consoles/playstation5/'
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    for result in soup.find_all('tr'):
        link = result.find_all('a')
        if len(link) > 0:
            for href in link:
                link = href.get('href')
        text = result.get_text()
        if 'Sold Out' in text or len(link) < 1:
            sold_out.append(f'Sold Out: {text}')
        else:
            if 'ebay' not in text:
                in_stock.append(f'In Stock: {text} - {link}')
    if include_all:
        return {
            'sold_out': sold_out,
            'in_stock': in_stock
        }
    else:
        return in_stock


def scrape_sony_for_headset():
    sold_out = []
    in_stock = []
    url = 'https://direct.playstation.com/en-us/accessories/accessory/pulse-3d-wireless-headset.3005688'
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    headset_elem = (soup.find('div', attrs={'class': 'productHero-desc col-lg-6 order-lg-2'})).get_text().split('\n')
    if ' Out of Stock ' in headset_elem:
        sold_out.append("Sold Out - Playstation Direct")
    else:
        in_stock.append("Pulse 3D Wireless Headset - In Stock at https://direct.playstation.com/en-us/accessories/accessory/pulse-3d-wireless-headset.3005688")
    return {
        'sold_out': sold_out,
        'in_stock': in_stock
    }

# <div class="out-stock-wrpr js-out-stock-wrpr hide"> <p class="sony-text-body-1">Out of Stock</p> </div>
