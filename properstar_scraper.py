import csv
import re

import clean_currency
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from validate_email import validate_email
from webdriver_manager.chrome import ChromeDriverManager



from time import sleep

pages = 1

browser = None

countries = {#"brazil": "br",
#                  "colombia":"co",
#                  "costa-rica": "cr",
#                  "dominican-republic": "do",
#                  "honduras":"hn",
#                  "nicaragua": "ni",
#                  "mexico": "mx",
#                  "guatemala": "gt",
                 "puerto-rico": "pr"}

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

    next_page_links = browser.find_elements(By.CLASS_NAME, "page-link.next.disabled")

    try:

        if not next_page_links:
            print("Next page link found")
            load_next_page(country)
        else:
            print("No more pages")
            pages = 1
    except TimeoutException:
            print("Timed out, going to next page")
            pages +=1
            get_property_info(country)

   
def get_listings(key):
    global pages, browser

    value = countries[key]

    if pages == 1:
        url = f'https://www.properstar.com/{key}/buy'
    else:
        url = f'https://www.properstar.com/{key}/buy?p={pages}'
    browser.get(url)
    try:
        container = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "items-list-small")))
        listings = container.find_elements(By.CSS_SELECTOR, ".item-adaptive.card-full, .item-adaptive.card-extended")
    except StaleElementReferenceException:
        print("Encountered StaleElementReferenceException. Retrying...")
        listings = get_listings(key)  # Retry getting listings recursively
 

    return listings

def get_property_info(country):

    global pages

    print(f'Starting page {pages} for {country}')
    
    listings = get_listings(country)
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

            house_type_pattern = r'^(.*?)\s•'  # Match anything before the first bullet
            rooms_pattern = r'•\s(\d+)\sroom\(s\)'  # Match the number of rooms
            beds_pattern = r'•\s(\d+)\sbed\.'  # Match the number of bedrooms
            bath_pattern = r'•\s(\d+)\sbath\.'  # Match the number of bathrooms
            area_pattern = r'•\s(\d+)\s(m²|sq m)'  # Match the area in square meters
            
            try:
                regex_pattern = r'(\d+)/?$'
                href_element = i.find_element(By.CSS_SELECTOR,"a")  # You can use other locators too
                # Get the href attribute value
                href_value = href_element.get_attribute("href")
                match = re.findall(regex_pattern, href_value)
                
                # print(href_value)
                # print(match)
                if match:
                    listing_id = match[0]
                    #print(listing_id)
                else:
                    #print("No digits found in the link.")
                    pass
            except:
                    print("failed first time")
                    continue

            try:
                features_element = WebDriverWait(i, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "item-highlights")))
                features = features_element.get_attribute('innerHTML')
                #print(features)
                soup = BeautifulSoup(features, 'html.parser')
            except StaleElementReferenceException:
                # If element is stale, refresh the listings and try again
                listings = get_listings(country)
                continue
            except NoSuchElementException:
                print("Element with class 'features' not found. Skipping...")
                continue 
            except TimeoutException:
                print("Timed out, going to next page")
                pages +=1
                get_property_info(country)


            # Find matches using regex
            house_type_match = re.search(house_type_pattern, features)
            rooms_match = re.search(rooms_pattern, features)
            beds_match = re.search(beds_pattern, features)
            bath_match = re.search(bath_pattern, features)
            area_match = re.search(area_pattern, features)

            # Extract information if matches are found
            prop_type = house_type_match.group(1).strip() if house_type_match else ""
            #rooms = int(rooms_match.group(1)) if rooms_match else None
            beds = int(beds_match.group(1)) if beds_match else ""
            baths = int(bath_match.group(1)) if bath_match else ""
            house_size = float(float(area_match.group(1)) * 10.7639) if area_match else ""

            if house_size != "":
                house_size = str(house_size) + " ft sqr"

            # print(f'Prop type: {prop_type}')
            # print(f'Beds: {beds}')
            # print(f'Baths: {baths}')
            # print(f'House size: {house_size}')   

            
                
            try:
                price = i.find_element(By.CLASS_NAME, "listing-price-main").text
                price = price.replace('$', '')
                #print(f'Price: {price}')
            except:
                #print(listing_id, " has no price information")
                pass
            writer.writerow([listing_id, beds, baths, lot_size, house_size, prop_type, price, country, 'properstar.com'])

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
            browser =  init_browser()
            print(f'Begin scraping for {key}')
            get_property_info(key)
    except KeyboardInterrupt:
        # Close the browser if the program is interrupted
        browser.quit()
        exit()  # Exit the program


start_scrape()