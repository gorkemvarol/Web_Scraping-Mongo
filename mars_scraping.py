from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
import pymongo
import os
from config import chromedriver_path


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path":chromedriver_path}
    
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    print("hello")
    browser = init_browser()
    
    #### NASA Mars News : Visit redplanetscience.com
    url = 'http://redplanetscience.com/'
    browser.visit(url)

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve the latest news title and paragraph
    news_title = soup.find_all('div', class_='content_title')[0].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text

    # Use Beautiful Soup's find() method to navigate and retrieve attributes

    print(f'Title: {news_title}')
    print('-----------')
    print(f'Para: {news_p}') 
    ###

    #### JPL Mars Space Images - Visir spaceimages-mars.com
    # Mars Image to be scraped
    img_url = 'http://spaceimages-mars.com'
    featured_image_url = 'http://spaceimages-mars.com/image/featured/mars3.jpg'
    browser.visit(featured_image_url)

    # HTML object
    html = browser.html
    # Parse HTML
    featured_image_soup = BeautifulSoup(html, 'html.parser')
    # Retrieve featured image link
    relative_image_path = featured_image_soup.find_all('img')[0]["src"]
    featured_image = relative_image_path
    print(featured_image)
    ###

    ### Mars Facts
    url = 'https://galaxyfacts-mars.com'
    tables = pd.read_html(url)
    df = tables[0]
    new_header = df.iloc[0] #grab the first row for the header
    df = df[1:] #take the data less the header row
    df.columns = new_header #set the header row as the df header

    df.rename(columns = {'Mars - Earth Comparison':'Description'}, inplace = True)
    df.head()
    html_table = df.to_html()
    html_table.replace('\n', '')
    print(html_table)
    ###
    
    ### Mars Hemispheres 
    img_url = 'http://marshemispheres.com/'
    featured_image_url = 'https://marshemispheres.com/images/39d3266553462198bd2fbc4d18fbed17_cerberus_enhanced.tif_thumb.png'
    browser.visit(img_url)

    # HTML object
    html = browser.html
    # Parse HTML
    soup = BeautifulSoup(html, 'html.parser')
    relative_image_paths = soup.find_all('img', class_='thumb')
    titles = soup.find_all('div', class_='description')
    # featured_image = relative_image_path

    hemisphere_image_urls=[]

    for x in range(len(relative_image_paths)):
        hemisphere_image_urls.append({ "tile": titles[x].h3.text,"img_ulr":img_url+relative_image_paths[x]['src']})

    print(hemisphere_image_urls)


    #### Mars Dictionary  
    mars_dict = {
        'Title': news_title,
        "Para": news_p,
        "mars_facts": html_table,
        "featured_Image": featured_image,
        "hemisphere_images": hemisphere_image_urls
    }
    browser.quit()
    return mars_dict  

if __name__ == "__main__":
    scrape()