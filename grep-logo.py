from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import urllib.parse
import time
import requests
import pandas as pd


# Replace 'path_to_chromedriver' with the actual path to your chromedriver executable
driver = webdriver.Chrome()


def retrieve_image(vendor: str):
    # Navigate to Google's homepage
    driver.get("https://images.google.com")
    # Find the search bar element and type your query
    # search_box = driver.find_element_by_name("q")
    search_box = driver.find_element(by=By.ID, value='APjFqb')
    search_query = f"{vendor} logo ext:png"
    search_box.send_keys(search_query)
    # Press 'Enter' to perform the search
    search_box.send_keys(Keys.RETURN)
    # Wait for the search results to load
    time.sleep(3)  # You can adjust the wait time based on your internet speed
    # Extract the search results
    files = []
    l = driver.find_elements(by=By.CSS_SELECTOR, value="a.FRuiCf.islib.nfEiy")
    for cnt in range(0, 4):
        l[cnt].click()
        files.append(urllib.parse.unquote(
            l[cnt].get_attribute("href").split("&")[0].replace("https://www.google.com/imgres?imgurl=", "")))
    for c in range(0, len(files)):
        response = requests.get(files[c])
        with open(f"images/{vendor}_{c}.jpg", "wb") as f:
            f.write(response.content)


df = pd.read_csv("vendors.csv")
vendors = df['Vendors'].tolist()

for v in vendors:
    retrieve_image(v)

# Close the browser
driver.quit()

