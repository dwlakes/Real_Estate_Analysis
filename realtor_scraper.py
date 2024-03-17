import main
import csv
import re

import clean_currency
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup



from time import sleep

pages = 1

browser = None

countries = {"Brazil": "br",
                 "Colombia":"co",
                 "Costa Rica": "cr",
                 "Dominican Republic": "do",
                 "Honduras":"hn",
                 "Nicaragua": "ni",
                 "Mexico": "mx",
                 "Guatemala": "gt"}

def load_next_page(country):
    global browser, pages
    # dealing with captcha 
    browser.quit()
    browser = main.init_browser()
    pages += 1

    get_property_info(country)

def check_for_next_page(country):
    global pages

    next_page_links = browser.find_elements(By.CLASS_NAME, "pager-next")
    
    if next_page_links:
        print("Next page link found")
        load_next_page(country)
    else:
        print("No more pages")
        pages = 1


        
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
    # Open the CSV file in write mode
    # with open(f'./data/{country}_property_info.csv', mode='a', newline='', encoding='utf-8') as file:
    #     writer = csv.writer(file)
        
    #     # Write the header row
    #     if pages <2:
    #         writer.writerow(['Listing ID', 'Bedrooms', 'Bathrooms', 'Lot Size', 'House Size', 'Property Type', 'Price', 'Country'])
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

        features = (i.find_element(By.CLASS_NAME, "features").get_attribute('innerHTML'))

        soup = BeautifulSoup(features, 'html.parser')

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
                print(listing_id)
            else:
                print("No digits found in the link.")

        
        except:
            #print("failed first time")
            continue
        
        # try:
        #     bedroom_div = soup.find('img', alt="bedrooms").parent

        #     # Get the next sibling which contains the digit
        #     next_sibling = bedroom_div.find_next_sibling()
        #     beds = next_sibling.get_text(strip=True)

        #     # You can add similar code to extract other features like bathrooms, lot size, etc.

        #     print("Bedrooms:", beds)
        # except:
        #     print(listing_id, " has no bed information")
        #     pass
        
        # try:
        #     baths = i.find_element(By.CLASS_NAME, "ic-baths").text
        # except:
        #     #print(listing_id, " has no baths information")
        #     pass
        
        # try:
        #     lot_size = i.find_element(By.CLASS_NAME, "ic-lotsize").text
        # except:
        #     #print(listing_id, " has no lot size information")
        #     pass

        # try:
        #     house_size = i.find_element(By.CLASS_NAME, "ic-sqft").text, " sqft"
        # except:
        #     #print(listing_id, " has no house size information")
        #     pass

        # try:
        #     prop_type = i.find_element(By.CLASS_NAME, "property-type").text
        # except:
        #     #print(listing_id, " has no property-type information")
        #     pass
        
        try:
            price = i.find_element(By.CLASS_NAME, "price").text
            price = clean_currency.clean_currency(price)
        except:
            #print(listing_id, " has no price information")
            pass
        #writer.writerow([listing_id, beds, baths, lot_size, house_size, prop_type, price, country])

        #print(i.text)
        print("\n")

    sleep(5)
    #file.close()
    check_for_next_page(country)
 
    browser.quit()

def start_scrape():

    global browser, countries

    browser =  main.init_browser()
    print("started")
    get_property_info("Brazil")


    # try:
    #     for key in countries:
    #         browser =  main.init_browser()
    #         print(f'Begin scraping for {key}')
    #         get_property_info(key)
    # except KeyboardInterrupt:
    #     # Close the browser if the program is interrupted
    #     browser.quit()
    #     exit()  # Exit the program


start_scrape()