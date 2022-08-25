from selenium import webdriver as wd
from selenium.webdriver.common.by import By
import chromedriver_binary
import time
import random

url = input("Enter the URL of the item: ")

wd = wd.Chrome()
wd.implicitly_wait(10)

# Head to the url, find the add-to-cart btn, and click it
wd.get(url)
add_cart_btn = wd.find_element(By.XPATH, '//*[@id="add-to-cart-button"]')
add_cart_btn.click()

# now view cart, head to checkout page, use element.send_keys() method to populate card/billing info, and press checkout
# also ensure that when filling in fields, add a time.sleep(random.range(5.0, 15.0)) to prevent site bans