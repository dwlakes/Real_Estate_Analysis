import main
import csv

import clean_currency
from selenium.webdriver.common.by import By


from time import sleep

pages = 10

browser = None

countries = {#"Brazil": "BR",
                 #"Colombia":"CO",
                 #"Costa Rica": "CR",
                 #"Dominican Republic": "DO",
                #  "Honduras":"HN",
                #  "Nicaragua": "NI",
                #  "Mexico": "MX",
                 "Venezuela": "VE",
                 "Guatemala": "GT"}

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
        url = f'https://www.point2homes.com/{value}/Real-Estate-Listings.html'
    else:
        url = f'https://www.point2homes.com/{value}/Real-Estate-Listings.html?SelectedView=listings&page={pages}'
    browser.get(url)
    listing_container = browser.find_element(By.CLASS_NAME, "listings")
    listings = listing_container.find_elements(By.CSS_SELECTOR, "li[data-order]")

    return listings

def get_property_info(country):

    print(f'Starting page {pages} for {country}')
    
    listings = get_listings(country)
    # Open the CSV file in write mode
    with open(f'./data/{country}_property_info.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the header row
        if pages <2:
            writer.writerow(['Listing ID', 'Bedrooms', 'Bathrooms', 'Lot Size', 'House Size', 'Property Type', 'Price', 'Country'])
        
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
                listing_id = i.find_element(By.CSS_SELECTOR, ".item-cnt").get_attribute("id").replace(" ", "")
            except:
                #print("failed first time")
                continue
            #print(listing_id)
            
            try:
                beds =  i.find_element(By.CLASS_NAME, "ic-beds").text
            except:
                #print(listing_id, " has no bed information")
                pass
            
            try:
                baths = i.find_element(By.CLASS_NAME, "ic-baths").text
            except:
                #print(listing_id, " has no baths information")
                pass
            
            try:
                lot_size = i.find_element(By.CLASS_NAME, "ic-lotsize").text
            except:
                #print(listing_id, " has no lot size information")
                pass

            try:
                house_size = i.find_element(By.CLASS_NAME, "ic-sqft").text, " sqft"
            except:
                #print(listing_id, " has no house size information")
                pass

            try:
                prop_type = i.find_element(By.CLASS_NAME, "property-type").text
            except:
                #print(listing_id, " has no property-type information")
                pass
            
            try:
                price = i.find_element(By.CLASS_NAME, "price").text
                price = clean_currency.clean_currency(price)
            except:
                #print(listing_id, " has no price information")
                pass
            writer.writerow([listing_id, beds, baths, lot_size, house_size, prop_type, price, country])

            #print(i.text)
            #print("\n")

        sleep(5)
        file.close()
        check_for_next_page(country)
 
    browser.quit()

def start_scrape():

    global browser, countries

    try:
        for key in countries:
            browser =  main.init_browser()
            print(f'Begin scraping for {key}')
            get_property_info(key)
    except KeyboardInterrupt:
        # Close the browser if the program is interrupted
        browser.quit()
        exit()  # Exit the program
        