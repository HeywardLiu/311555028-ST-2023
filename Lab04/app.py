from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")

# Part 1
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)
time.sleep(5)
nycu_url = "https://www.nycu.edu.tw/"
driver.get(nycu_url)
driver.maximize_window()


# driver.find_element("link text", "新聞").click()
element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "新聞")))
element.click()


# # driver.find_element(By.CLASS_NAME, "su-post").click()
# element = WebDriverWait(driver, 5).until(
#     EC.element_to_be_clickable((By.CLASS_NAME, "su-post")))
# element.click()
# print(driver.current_url)
element = WebDriverWait(driver, 60).until(
    lambda d:d.find_elements(By.XPATH, "//a[contains(@href, 'https://www.nycu.edu.tw/news/')]") )[1]
element.click()


# post_title = driver.find_element(
#                 By.CLASS_NAME, "single-post-title.entry-title").text
element = WebDriverWait(driver, 5).until(
    lambda d: d.find_element(By.CLASS_NAME, "single-post-title.entry-title"))
post_title = element.text
print(post_title)

# paragraph_list = driver.find_elements(By.CLASS_NAME, "entry-content.clr")
paragraph_list = WebDriverWait(driver, 5).until(
    lambda d: d.find_element(By.CLASS_NAME, "entry-content.clr"))
print(paragraph_list.text)


# Google Serach id and Print title of the second result
driver.switch_to.new_window("google")
driver.get("https://www.google.com/")
driver.find_element(By.CLASS_NAME, "gLFyf").send_keys("311555028")
driver.find_element(By.CLASS_NAME, "gLFyf").send_keys(Keys.ENTER)
time.sleep(5)
print(driver.find_elements(By.CLASS_NAME, "LC20lb.MBeuO.DKV0Md")[1].text)
time.sleep(5)
driver.close()
