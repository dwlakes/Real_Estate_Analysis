from bs4 import BeautifulSoup

html = '''
<div class="sc-1dun5hk-0">
    <div class="features">
        <div class="feature-item">
            <img src="img.png" alt="bedrooms">
            "4"
        </div>
    </div>
</div>
'''

# Parse the HTML
soup = BeautifulSoup(html, 'html.parser')

# Find the element with alt="bedrooms"
bedroom_element = soup.find('img', alt='bedrooms')

# Get the text after the image tag
bedroom_text = bedroom_element.find_next_sibling()

print(bedroom_text)  # Output: 4
