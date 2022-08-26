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

# Head to the url, find the add-to-cart btn, and click it
# real URL: https://store.401games.ca/products/pokemon-ultra-premium-collection-charizard-pre-order
# test URL: https://store.401games.ca/collections/all/products/pokemon-astral-radiance-checklane-blister-bundle?variant=42511032156347

# as long as the add to cart btn is not available, keep trying
while True:
    try:
        wd.get("https://store.401games.ca/products/pokemon-ultra-premium-collection-charizard-pre-order")
        time.sleep(1)

        add_cart_btn = wd.find_element(By.XPATH, '//*[@id="AddToCart-product-template"]')
        add_cart_btn.click()
        time.sleep(1)

        cart_btn = wd.find_element(By.XPATH, '//*[@id="CartButton"]')
        cart_btn.click()
        time.sleep(1)

        checkout_btn = wd.find_element(By.XPATH, '//*[@id="shopify-section-cart-template"]/section/div/div/div/form/div[2]/div[2]/input[2]')
        checkout_btn.click()
        time.sleep(1)

        print("Item added to cart!")
        break
    except:
        print("Item not available...")



# login procedure
email_field = wd.find_element(By.XPATH, '//*[@id="CustomerEmail"]')
email_field.send_keys(os.getenv('EMAIL'))

time.sleep(random.uniform(0.1, 0.3))

pw_field = wd.find_element(By.XPATH, '//*[@id="CustomerPassword"]')
pw_field.send_keys(os.getenv('PASSWORD'))
time.sleep(0.1)

sign_in_btn = wd.find_element(By.XPATH, '/html/body/div[1]/main/section[2]/div/div/div[1]/form/div/p/input')
sign_in_btn.click()
time.sleep(1.5)

while True:
    try:
        # Express checkout with PayPal
        pp_btn = wd.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/div/div[2]/main/form/div[1]/div/div/div[1]/div[1]/div[2]')
        pp_btn.click()
        time.sleep(5)
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
    pp_email = wd.find_element(By.XPATH, '//*[@id="email"]')
    pp_email.clear()
    pp_email.send_keys(os.getenv("PP_EMAIL"))
except:
    time.sleep(20) # if we get to this point, it is most likely because PayPal saved login info, and is asking for a confirmation code

# PayPal has a few variations of the login prompts, so catch errors that could arise
try:
    next_btn = wd.find_element(By.XPATH, '//*[@id="btnNext"]')
    next_btn.click()
    time.sleep(0.5)

    login_w_pw_instead = wd.find_element(By.XPATH, '//*[@id="loginWithPasswordLink"]/a')
    login_w_pw_instead.click()
    time.sleep(0.5)

    pp_pw = wd.find_element(By.XPATH, '//*[@id="password"]')
    pp_pw.send_keys(os.getenv("PP_PW"))

    pp_login = wd.find_element(By.XPATH, '//*[@id="btnLogin"]')
    pp_login.click()

except:
    # if there's no nextBtn at the beginning, it means the password prompt is on the current page, so fill it and login
    pp_pw = wd.find_element(By.XPATH, '//*[@id="password"]')
    pp_pw.send_keys(os.getenv("PP_PW"))
    pp_login_btn = wd.find_element(By.XPATH, '//*[@id="btnLogin"]')
    pp_login_btn.click()

time.sleep(1)
pp_continue = wd.find_element(By.XPATH, '//*[@id="payment-submit-btn"]')
pp_continue.click()
time.sleep(5)

### Done with PayPal, back to main page
wd.switch_to.window(main_page)
time.sleep(0.5)

# choose shipping method
shipping_method = wd.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/div/div[2]/main/form/div[1]/div/div/div[1]/section/div/fieldset/div[2]/div[3]/label')
shipping_method.click()
time.sleep(0.1)

# head to the final checkout page
continue_payment_btn = wd.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/div/div[2]/main/form/div[1]/div/div/div[2]/div[1]/button')
continue_payment_btn.click()
time.sleep(2)

# Only for final transaction:
pay_now_btn = wd.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/div/div[2]/main/div/form/div[1]/div/div[2]/div[1]/button')
pay_now_btn.click()
print("Script has executed in " + str(int(time.time() - start)) + " seconds.")