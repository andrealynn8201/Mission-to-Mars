# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pprint as pp

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# Featured Images

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


#line 1: read_html() specifically looks for tables, the 0 tells it to take the first one it finds.
#Line 2 specifies column names for the table
#Line 3 tells the df that the description is the index
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

# Converts a table to html
df.to_html()

# # Challenge Del 1

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)

# create a list for the hemisphere dictionaries to load into
hemispheres =[]

# loop through required images
for x in range(0,4):
    # find first link to the full images
    full_image_elem = browser.find_by_tag('h3')[x]
    full_image_elem.click()
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    # Find the relative image url
    img_url_rel = img_soup.find('img', class_='wide-image', id=False).get('src')
    # Use the base URL to create an absolute URL
    img_url = f'https://marshemispheres.com/{img_url_rel}'
    # Find the title of the image
    img_title = img_soup.find('h2', class_='title').text
    # Append the list with a dictionary of the url and title
    hemispheres.append({'img_url':img_url, 'title':img_title})
    # back up 1 page
    browser.back()


pp.pprint(hemispheres)

# 5. Quit the browser
browser.quit()