# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

# define function
def scrape_all():
    # Initiate headless driver for deployment
    # headless was set as False so we could see the scraping in action.
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
                                                                    
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemisphere_data(),
        "last_modified": dt.datetime.now()
    }
   # Stop webdriver and return data
    browser.quit()
    return data

# Define function
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    # try.except error handling
    try:
 
        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    return news_title,news_p

# ### Featured Images
# define function
def featured_image(browser):
    # Visit URL 
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:

        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

        # Use the base URL to create an absolute URL
        img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    except AttributeError:
        return None
    return img_url

# define function for mars facts
def mars_facts():
    try:
        #line 1: read_html() specifically looks for tables, the 0 tells it to take the first one it finds.
        #Line 2 specifies column names for the table
        #Line 3 tells the df that the description is the index
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Converts a table to html and returns
    return df.to_html()

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())

def hemisphere_data():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars/'
    browser.visit(url)

    # create a list for the hemisphere dictionaries to load into
    hemispheres =[]
    try:
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
            img_url = f'https://astrogeology.usgs.gov/{img_url_rel}'
            # Find the title of the image
            img_title = img_soup.find('h2', class_='title').text
            # Append the list with a dictionary of the url and title
            hemispheres.append({'img_url':img_url, 'title':img_title})
            # back up 1 page
            browser.back()
        
        browser.quit()
        return hemispheres
    except:
        return None


