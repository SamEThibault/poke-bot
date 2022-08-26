import chromedriver_binary
import time
import os
import random

from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

# load .env variables, initialize Chrome driver and wait for it to load
load_dotenv()
wd = wd.Chrome()
wd.implicitly_wait(10)
start = time.time() # to analyze runtime

# store current window in variable for reference later
main_page = wd.current_window_handle

# find and click button @ specific xpath
def clickBtn(xpath):
    btn = wd.find_element(By.XPATH, xpath)
    btn.click()
    time.sleep(0.5)
    return

# find and send text to form @ specific xpath
def sendData(xpath, data):
    form = wd.find_element(By.XPATH, xpath)
    form.clear()
    form.send_keys(data)
    time.sleep(random.uniform(0.1, 0.2))
    return

print("*ENSURE THE FINAL CLICK FUNCTION CALL IS UNCOMMENTED BEFORE USING THIS SCRIPT FOR A REAL DROP*")
# Head to the url, find the add-to-cart btn, and click it
url = input("Enter an item URL: ")

# as long as the add to cart btn is not available, keep trying
count = 0
while True:
    try:
        wd.get(url)
        count += 1
        if count == 30:
            res = input("Would you like to keep searching? (Y/N)")
            if res == "N" or res == "n":
                quit()
        time.sleep(1)
        clickBtn('//*[@id="AddToCart-product-template"]')
        clickBtn('//*[@id="CartButton"]')
        clickBtn('//*[@id="shopify-section-cart-template"]/section/div/div/div/form/div[2]/div[2]/input[2]')
        print("Item added to cart!")
        break
    except:
        print("Item not available...")

# login procedure
sendData('//*[@id="CustomerEmail"]', os.getenv('EMAIL'))
sendData('//*[@id="CustomerPassword"]', os.getenv('PASSWORD'))
clickBtn('/html/body/div[1]/main/section[2]/div/div/div[1]/form/div/p/input')

while True:
    try:
        # Express checkout with PayPal
        clickBtn('/html/body/div[1]/div/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/div/div[2]/main/form/div[1]/div/div/div[1]/div[1]/div[2]')
        time.sleep(4)
        break
    except:
        continue

# find all available window names, and head to the one that we're not currently on
for handle in wd.window_handles:
    if handle != main_page:
        pp_page = handle
wd.switch_to.window(pp_page)

# Paypal login procedure
try:
    sendData('//*[@id="email"]', os.getenv("PP_EMAIL") )
except:
    time.sleep(20) # if we get to this point, it is most likely because PayPal saved login info, and is asking for a confirmation code

# PayPal has a few variations of the login prompts, so try to send keys to elements, and handle exceptions if a variation of the page arises
try:
    clickBtn('//*[@id="btnNext"]')
    clickBtn('//*[@id="loginWithPasswordLink"]/a')
    sendData('//*[@id="password"]', os.getenv("PP_PW"))
    clickBtn('//*[@id="btnLogin"]')
except:
    # if there's no nextBtn at the beginning, it means the password prompt is on the current page, so fill it and login
    sendData('//*[@id="password"]', os.getenv("PP_PW"))
    clickBtn('//*[@id="btnLogin"]')

clickBtn('//*[@id="payment-submit-btn"]')
time.sleep(4)

### Done with PayPal, back to main page
wd.switch_to.window(main_page)
time.sleep(0.5)

# choose shipping method
clickBtn('/html/body/div[1]/div/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/div/div[2]/main/form/div[1]/div/div/div[1]/section/div/fieldset/div[2]/div[3]/label')

# head to the final checkout page
clickBtn('/html/body/div[1]/div/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/div/div[2]/main/form/div[1]/div/div/div[2]/div[1]/button')

# Only for final transaction:
# clickBtn('/html/body/div[1]/div[1]/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/div/div[2]/main/div/form/div[1]/div/div[2]/div[1]/button', wd)
print("Script has executed in " + str(int(time.time() - start)) + " seconds.")