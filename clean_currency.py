import requests
import re
from bs4 import BeautifulSoup

def convert_currency(money):
    currency_type = "".join(re.findall(r'\b[A-Za-z]{3}\b', money))
    dollar_amount = "".join(re.findall(r'\d+', money))
    print(f'Needs to convert {dollar_amount} {currency_type} to USD')

    url = f'https://www.x-rates.com/calculator/?from={currency_type}&to=USD&amount={dollar_amount}'

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find("span", class_="ccOutputRslt")
    return (results.text)
    #refined = soup.find_all("b")
    #print(results)
    


def clean_currency(money):

    if "USD" not in money:
       cleaned_money = convert_currency(money)
    else:
        cleaned_money = money
    cleaned_money = re.sub('[a-zA-Z|$]', '', cleaned_money)
    #print(f'Cleaned money: {cleaned_money}')

    #print(cleaned_money)

    return cleaned_money

