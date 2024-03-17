from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from validate_email import validate_email
from webdriver_manager.chrome import ChromeDriverManager

import point2home_scraper


from time import sleep

# pages = 1

# browser = None

def init_browser():
    options = ChromeOptions()
    #options.add_argument("--headless=new")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(1) # wait time in seconds to allow loading of elements
    driver.set_window_position(-2000, 0)
    
    return driver

def main():
    
    point2home_scraper.start_scrape()
    

if __name__ == "__main__":
    main()
