from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

url = 'https://www.otomoto.pl/'

options = Options()
service = Service('Lab006/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)

driver.get(url)

button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#onetrust-accept-btn-handler')))
button.click()

button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#__next > div > div > div > main > div.ooa-v3cvs3.e1j93m721 > article > article > fieldset > form > section.ooa-qmp9fa.e1wnr56l6 > div:nth-child(1) > div.ooa-jra37b > div > input')))
button.click()

element = driver.find_element(By.ID, "porsche")
element.click()

time.sleep(2)
button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#__next > div > div > div > main > div.ooa-v3cvs3.e1j93m721 > article > article > fieldset > form > section.ooa-f6jnp4.e1wnr56l2 > button.e1wnr56l4.e12bczjw0.ooa-1bmzle9')))
button.click()

button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#baxter-h-interstitial-inner-modal-container > div > div.baxter-interstitial-modal-footer > button')))
button.click()

for _ in range(100):
    driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)
    time.sleep(1)

time.sleep(5000)
driver.close()
