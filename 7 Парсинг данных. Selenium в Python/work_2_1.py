# Любая работа с JS на сайте со сбором данных, обсудим в конце вебинара

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

client = MongoClient('127.0.0.1', 27017)
db = client['db_mvideo']
mvideo_most_viewed_products = db.mvideo_most_viewed_products

service = Service('./chromedriver')
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(4)
driver.maximize_window()
driver.get('https://www.mvideo.ru/')

step = 0
while True:
    driver.execute_script(f"window.scrollTo(0, {step})")
    step += 200
    try:
        if driver.find_element(By.XPATH, "//h2[contains(text(), 'Самые просматриваемые')]"):
            break
    except:
        pass

names = [i.text for i in driver.find_elements(By.XPATH, ".//div[@class='product-mini-card__name ng-star-inserted']")]
prices = [int(i.text[0:i.text.find('₽')].replace(' ', '')) for i in driver.find_elements(By.XPATH, ".//div[@class='product-mini-card__price ng-star-inserted']")]
link = [i.get_attribute('href') for i in driver.find_elements(By.XPATH, ".//div[@class='product-mini-card__name ng-star-inserted']//a")]

most_viewed_products = {}
for i in range(0, len(names)):
    most_viewed_products = {
        '_id': link[i],
        'name': names[i],
        'price': prices[i],
        'link': link[i]}
    try:
        mvideo_most_viewed_products.insert_one(most_viewed_products)
    except DuplicateKeyError:
        print(f'товар {names[i]} уже есть в базе')
