import csv
import re

import clean_currency
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from validate_email import validate_email
from webdriver_manager.chrome import ChromeDriverManager



from time import sleep

pages = 1

browser = None

countries = {#"Brazil": "br",
                 #"Colombia":"co",
                #  "Costa Rica": "cr",
                #  "Dominican Republic": "do",
                #  "Honduras":"hn",
                #  "Nicaragua": "ni",
                 #"Mexico": "mx",
                 #"Guatemala": "gt",
                "Puerto-Rico": "pr"}

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

def load_next_page(country):
    global browser, pages
    # dealing with captcha 
    browser.quit()
    browser = init_browser()
    pages += 1

    get_property_info(country)

def check_for_next_page(country):
    global pages

    try:
        next_page_links = browser.find_element(By.CLASS_NAME, "ant-pagination-next")
        aria_disabled_value = next_page_links.get_attribute('aria-disabled')
        print("aria-disabled value:", aria_disabled_value)

        if aria_disabled_value == "false":
            print("Next page link found")
            load_next_page(country)
        else:
            print("No more pages")
            pages = 1
    except NoSuchElementException:
        print("No next page link found. Exiting...")
        pages +=1
        get_property_info(country)

   
def get_listings(key):
    global pages, browser

    value = countries[key]

    if pages == 1:
        url = f'https://www.realtor.com/international/{value}/'
    else:
        url = f'https://www.realtor.com/international/{value}/p{pages}'
    browser.get(url)
    
    listings = browser.find_elements(By.CLASS_NAME, "sc-1dun5hk-0")

    return listings

def get_property_info(country):

    print(f'Starting page {pages} for {country}')
    
    listings = get_listings(country)
    sleep(10)
    
    #Open the CSV file in write mode
    with open(f'./data/{country}_property_info.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the header row
        # if pages <2:
        #     writer.writerow(['Listing ID', 'Bedrooms', 'Bathrooms', 'Lot Size', 'House Size', 'Property Type', 'Price', 'Country', 'Source'])
    #print(listings)    
        for i in listings:
            # # Find the price within each <li> element
            # price = i.find_element(By.CLASS_NAME, "price")
            beds = ""
            baths = ""
            lot_size = ""
            house_size = ""
            prop_type = ""
            price = ""

            try:
                features_element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "features")))
                features = features_element.get_attribute('innerHTML')
                soup = BeautifulSoup(features, 'html.parser')
            except StaleElementReferenceException:
                # If element is stale, refresh the listings and try again
                listings = get_listings(country)
                continue

            

            #print(f'Beds: {bedroom_element_digit.text.strip()}')

            try:
                regex_pattern = r'(\d+)/?$'
                href_element = i.find_element(By.CSS_SELECTOR,"a")  # You can use other locators too
                # Get the href attribute value
                href_value = href_element.get_attribute("href")
                match = re.findall(regex_pattern, href_value)
                
                #print(href_value)
                #print(match)
                if match:
                    listing_id = match[0]
                    #print(listing_id)
                else:
                    #print("No digits found in the link.")
                    pass

            
            except:
                #print("failed first time")
                continue
            
            try:
                bedroom_div = soup.find('img', alt="bedrooms").parent

                # Get the next sibling which contains the digit
                beds = bedroom_div.get_text(strip=True)

                # You can add similar code to extract other features like bathrooms, lot size, etc.

                #print("Bedrooms: ", beds)
            except:
                #print(listing_id, " has no bed information")
                pass
            
            try:
                bathroom_div = soup.find('img', alt="bathroom").parent

                # Get the next sibling which contains the digit
                baths = bathroom_div.get_text(strip=True)

                # You can add similar code to extract other features like bathrooms, lot size, etc.

                #print("Bathrooms: ", baths)
            except:
                #print(listing_id, " has no bathroom information")
                pass
            
            try:
                lot_size_div = soup.find('img', alt="landSize").parent

                # Get the next sibling which contains the digit
                lot_size = lot_size_div.get_text(strip=True)

                # You can add similar code to extract other features like bathrooms, lot size, etc.

                #print("Lot size: ", lot_size)
            except:
                #print(listing_id, " has no lot size information")
                pass

            try:
                house_size_div = soup.find('img', alt="buildingSize").parent

                # Get the next sibling which contains the digit
                house_size = house_size_div.get_text(strip=True)

                # You can add similar code to extract other features like bathrooms, lot size, etc.

                #print("House size: ", house_size)
            except:
                #print(listing_id, " has no house size information")
                pass

            try:
                prop_type = i.find_element(By.CLASS_NAME, "property-type").text
                #print("Prop type: ", prop_type)
            except:
                #print(listing_id, " has no property-type information")
                pass
            
            try:
                price = i.find_element(By.CLASS_NAME, "displayConsumerPrice").text
                price = clean_currency.clean_currency(price)
                #print(f'Price: {price}')
            except:
                #print(listing_id, " has no price information")
                pass
            writer.writerow([listing_id, beds, baths, lot_size, house_size, prop_type, price, country, 'realtor.com'])

        #print(i.text)
        #print("\n")

    sleep(5)
    file.close()
    check_for_next_page(country)
 
    browser.quit()

def start_scrape():

    global browser, countries

    browser = init_browser()
    print("started")

    try:
        for key in countries:
            browser = init_browser()
            print(f'Begin scraping for {key}')
            get_property_info(key)
    except KeyboardInterrupt:
        # Close the browser if the program is interrupted
        browser.quit()
        exit()  # Exit the program


start_scrape()