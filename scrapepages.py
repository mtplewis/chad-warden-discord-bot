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


pages = {
    'Amazon': {
        'url': 'https://www.amazon.com/PlayStation-5-Console/dp/B08FC5L3RG?tag=gamespot-preorderguides-20',
        'unavailable element': (By.XPATH, '//div[@class="a-box-inner"]//span[contains(text(),"Currently unavailable")]'),
        'method': 'webdriver'
    },
    'Amazon digital': {
        'url': 'https://www.amazon.com/PlayStation-5-Console/dp/B08FC6MR62?tag=gamespot-preorderguides-20&th=1',
        'unavailable element': (By.XPATH, '//div[@class="a-box-inner"]//span[contains(text(),"Currently unavailable")]'),
        'method': 'webdriver'
    },
    'Target - digital': {
        'url': 'https://www.target.com/p/playstation-5-console/-/A-81114596',
        'unavailable element': (By.XPATH, '//*[@data-test="preorderSoldOutMessage"]'),
        'method': 'webdriver'
    },
    'Target': {
        'url': 'https://www.target.com/p/playstation-5-console/-/A-81114595',
        'unavailable element': (By.XPATH, '//*[@data-test="preorderSoldOutMessage"]'),
        'method': 'webdriver'
    },
    # 'Gamestop - digital': {
    #     'url': 'https://www.gamestop.com/video-games/playstation-5/consoles/products/playstation-5-digital-edition/225171.html',
    #     'unavailable element': (By.XPATH, '//span[@class="delivery-out-of-stock text-uppercase"]')
    # },
    # 'Gamestop': {
    #     'url': 'https://www.gamestop.com/video-games/playstation-5/consoles/products/playstation-5/11108140.html',
    #     'unavailable element': (By.XPATH, '//span[@class="delivery-out-of-stock text-uppercase"]')
    # },
    'Best Buy - digital': {
        'url': 'https://www.bestbuy.com/site/sony-playstation-5-digital-edition-console/6430161.p?skuId=6430161',
        'unavailable element': (By.XPATH, '//button[@class="btn btn-disabled btn-lg btn-block add-to-cart-button"]'),
        'out of stock text': 'Coming Soon',
        'method': 'get'
    },
    'Best Buy': {
        'url': 'https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149',
        'unavailable element': (By.XPATH, '//button[@class="btn btn-disabled btn-lg btn-block add-to-cart-button"]'),
        'out of stock text': 'Get in-stock alert',
        'method': 'get'
    },
    'Wal Mart': {
        'url': 'https://www.walmart.com/ip/PlayStation5-Console/363472942',
        'unavailable element': (By.XPATH, '//span[contains(text(),"Out of stock")]'),
        'out of stock text': 'Get in-stock alert',
        'method': 'get'
    },
    'Wal Mart - digital': {
        'url': 'https://www.walmart.com/ip/Sony-PlayStation-5-Digital-Edition/493824815',
        'unavailable element': (By.XPATH, '//span[contains(text(),"Out of stock")]'),
        'out of stock text': 'Get in-stock alert',
        'method': 'get'
    },
}


def setup():
    # Setup
    chrome_options = Options()
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--set-cookies')
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def ensure_is_unavailable(driver, obj):
    web_obj = WebDriverWait(driver, 15).until(EC.presence_of_element_located(obj))
    return web_obj


def check_pages():
    sold_out = []
    in_stock = []
    for page in pages:
        result = check_page(page_name=page)
        if len(result['sold_out']) >= 1:
            sold_out.append(result['sold_out'])
        if len(result['in_stock']) >= 1:
            in_stock.append(result['in_stock'])

    return in_stock


def check_page(page_name: str = None):
    sold_out = []
    in_stock = []
    selected_pages = pages[page_name]
    if selected_pages['method'] == 'get':
        result = requests.get(url=selected_pages['url'])
        status = result.status_code
        if status == 200:
            if selected_pages['out of stock text'] in result.text:
                sold_out.append(f'{page_name}: Sold Out')
            else:
                in_stock.append(f'{page_name}: POTENTIALLY IN STOCK AT {selected_pages["url"]}')
        else:
            pass
    else:
        driver = setup()
        try:
            driver.get(selected_pages['url'])
            time.sleep(2)
            ensure_is_unavailable(driver, selected_pages['unavailable element'])
            sold_out.append(f'{page_name}: Sold Out')
            driver.close()
        except:
            in_stock.append(f'{page_name}: POTENTIALLY IN STOCK AT {selected_pages["url"]}')
            driver.close()
    return {
        'sold_out': sold_out,
        'in_stock': in_stock
    }

# print(scrape_zoolert())
# in_stock = check_pages()
# for result in in_stock:
#     print(result)
