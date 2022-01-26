from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--diable-deb-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options = chrome_options)


driver.get('https://mojodice.com/')

element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//table"))
)

print(driver.find_element_by_xpath("((//table/tbody/tr)[2]/td)[2]"))
print(driver.page_source)