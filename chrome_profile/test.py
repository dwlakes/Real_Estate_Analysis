import requests
from bs4 import BeautifulSoup
import json

# URL of the website
url = 'PUT_THE_URL_HERE'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all script tags
    script_tags = soup.find_all('script')

    # Search for the script containing the pins data
    pins_script = None
    for script in script_tags:
        if 'P2H.map_state' in script.text:
            pins_script = script.text
            break

    if pins_script:
        # Extracting the pins data using regex
        pins_data = re.search(r'pins:\s*(\{.*?\})\s*,', pins_script, re.DOTALL)

        if pins_data:
            pins_json = pins_data.group(1)
            # Parsing the pins data as JSON
            pins = json.loads(pins_json)
            # Accessing the 'pins' key to get the pins information
            pins_info = pins.get('pins', {})
            print(json.dumps(pins_info, indent=4))  # Print pins information in a readable format
        else:
            print("Pins data not found in the script.")
    else:
        print("Script containing pins data not found in the HTML document.")
else:
    print("Failed to retrieve the website. Status code:", response.status_code)
