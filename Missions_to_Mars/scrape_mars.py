# Import Modules/Dependecies 
from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import requests 

# Initialize browser
def init_browser(): 
    # Replace the path with your actual path to the chromedriver

    #Mac Users
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

    #Windows Users
    #exec_path = {'executable_path': '/app/.chromedriver/bin/chromedriver'}
    #return Browser('chrome', headless=True, **exec_path)

# Create Mission to Mars global dictionary that can be imported into Mongo
mars_info = {}

# NASA Mars News
def scrape_mars_news():
    try: 

        # Initialize browser 
        browser = init_browser()

        # url for Nasa news
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        # HTML Object
        html_news = browser.html

        # Parse with Beautiful Soup
        news_soup = BeautifulSoup(html_news, 'html.parser')
        
        # Collect the latest News Title and Paragraph Text
        # Assign the text to variables that you can reference later

        # news_title = news_soup.find('div', class_='content_title').find('a').text
        # news_p = news_soup.find('div', class_='article_teaser_body').text
        news_title = news_soup.find('li',class_="slide").find('div',class_="content_title").text
        news_p = news_soup.find('li',class_="slide").find('div',class_="article_teaser_body").text
        
        # Dictionary entry from MARS NEWS
        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_p

        return mars_info

    finally:

        browser.quit()

# JPL Mars Space Images - Featured Image
def scrape_mars_image():

    try: 

        # Initialize browser 
        browser = init_browser()

        # url for JPL Featured Space Image
        url_image='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url_image)

        # HTML Object 
        html_img = browser.html

        # Parse with Beautiful Soup
        image_soup = BeautifulSoup(html_img, 'html.parser')
        
        #Find the image url for the current Featured Mars Image and assign the url string to a variable
        #Make sure to find the image url to the full size .jpg image.
        img = image_soup.find(class_="button fancybox")["data-fancybox-href"]
        featured_image_url = "https://www.jpl.nasa.gov/" + img

        # Dictionary entry from FEATURED IMAGE
        mars_info['featured_image_url'] = featured_image_url 
        
        return mars_info
    
    finally:

        browser.quit()

        

# Mars Weather
def scrape_mars_weather():

    try: 

        # Initialize browser 
        browser = init_browser()

        # Visit the Mars Weather twitter account
        url_weather='https://twitter.com/marswxreport?lang=en'
        browser.visit(url_weather)

        # HTML Object 
        html_weather = browser.html

        # Parse with Beautiful Soup
        weather_soup = BeautifulSoup(html_weather, 'html.parser')
        
        weather_tweet=weather_soup.find_all('ol', class_='stream-items')
        for rec in weather_tweet:
            mars_weather = rec.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
            if 'InSight' in rec:
                break
            else:
                continue
        mars_weather = mars_weather.split('pic')[0]
        mars_weather = mars_weather.replace('\n', ' ')
        mars_info['mars_weather'] = mars_weather

    
    finally:

        browser.quit()


# Mars Facts
def scrape_mars_facts():

    # Visit the Mars Facts webpage
    url_mars_facts='https://space-facts.com/mars/'
    
    # Use the read_html function in Pandas to automatically scrape tabular data
    mars_facts_table = pd.read_html(url_mars_facts)
    mars_facts_df = pd.DataFrame(mars_facts_table[0])

    #Assign Column Names
    mars_facts_df.columns = ['Description','Value']

    #Set Index
    mars_facts_df = mars_facts_df.set_index('Description')
    mars_facts_df     

    # Use to_html method to generate HTML tables
    mars_html_table = mars_facts_df.to_html(header=True, index=True)
    # Dictionary entry from MARS FACTS
    mars_info['mars_facts'] = mars_html_table

    return mars_info


# Mars Hemispheres


def scrape_mars_hemispheres():

    try: 

        # Initialize browser 
        browser = init_browser()

        # url for hemisphers
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        # HTML Object
        html_hemispheres = browser.html

        # Parse with Beautiful Soup
        soup = BeautifulSoup(html_hemispheres, 'html.parser')

        # Retreive 
        items = soup.find_all('div', class_='item')

        # Create a list
        hiu = []

        # Store the main_ul 
        hemispheres_main_url = 'https://astrogeology.usgs.gov' 

        # Loop through the items previously stored
        for i in items: 
            # Store title
            title = i.find('h3').text
            
            # Store link that leads to full image website
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
            # Visit the link that contains the full image website 
            browser.visit(hemispheres_main_url + partial_img_url)
            
            # HTML Object of individual hemisphere information website 
            partial_img_html = browser.html
            
            # Parse HTML with Beautiful Soup for every individual hemisphere information website 
            soup = BeautifulSoup( partial_img_html, 'html.parser')
            
            # Retrieve full image source 
            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
            # Append the retreived information into a list of dictionaries 
            hiu.append({"title" : title, "img_url" : img_url})

        mars_info['hiu'] = hiu

        
        # Return mars_data dictionary 

        return mars_info
    finally:

        browser.quit()