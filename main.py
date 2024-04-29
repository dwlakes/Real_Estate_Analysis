from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from validate_email import validate_email
from webdriver_manager.chrome import ChromeDriverManager

import threading

import point2home_scraper
import realtor_scraper
import properstar_scraper


from time import sleep

# pages = 1

# browser = None

def init_browser():
    options = ChromeOptions()
    #options.add_argument("--headless=new")
    service = Service(ChromeDriverManager().install())
    #driver = webdriver.Chrome(service=service, options=options)
    #options.add_argument(r'--user-data-dir=~/Library/Application Support/Google/Chrome/') #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
    #options.add_argument(r'--profile-directory=~/Library/Application Support/Google/Chrome/Profile 3') #e.g. Profile 3
    #options.add_argument('--disk-cache-dir=')
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(1) # wait time in seconds to allow loading of elements
   # driver.set_window_position(-2000, 0)
    
    return driver

def main():
    # thread1 = threading.Thread(target=point2home_scraper.start_scrape)
    # thread2 = threading.Thread(target=realtor_scraper.start_scrape)
    # thread3 = threading.Thread(target=properstar_scraper.start_scrape)

    # thread1.start()
    # thread2.start()
    # thread3.start()

    # thread1.join()
    # thread2.join()
    # thread3.join()
    point2home_scraper.start_scrape()
    realtor_scraper.start_scrape()
    properstar_scraper.start_scrape()

    print("all threads done")
       

if __name__ == "__main__":
    main()
