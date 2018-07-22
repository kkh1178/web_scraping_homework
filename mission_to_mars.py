
import time
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime

import tweepy
import pandas as pd
import json
import os

TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
# mars_data = {
#     "news": "Scientists with NASA's Mars orbiters have been waiting years for an event like the current Mars global dust storm.",
#     "Featured Image": "https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA07137_ip.jpg",
#     "weather": "Sol 2108 (2018-07-12), Sunny, high -24C/-11F, low -65C/-84F, pressure at 8.06 hPa, daylight 05:19-17:27",
#     "Hemispheres": [
#         {
#             "title": "Cerberus Hemisphere Enhanced",
#             "url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg",
#         },
#         {
#             "title": "Schiaparelli Hemisphere Enhanced",
#             "url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg",
#         },
#         {
#             "title": "Syrtis Major Hemisphere Enhanced",
#             "url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg",
#         },
#         {
#             "title": "Valles Marineris Hemisphere Enhanced",
#             "url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg",
#         },
#     ],
# }


def get_data():
    return mars_data


def scrape():

    mars = {}
    # coding: utf-8

    # # Mission to Mars

    # In this assignment, you will build a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page. The following outlines what you need to do.
    #
    #

    # In[1]:

    # Step 1 - Scraping
    # Complete your initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.
    #
    # Create a Jupyter Notebook file called mission_to_mars.ipynb and use this to complete all of your scraping and analysis tasks. The following outlines what you need to scrape.

    # In[2]:

    # Initialize browser
    def init_browser():
        # @NOTE: Replace the path with your actual path to the chromedriver
        executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
        return Browser("chrome", **executable_path, headless=False)

    # In[3]:

    # Initialize browser
    browser = init_browser()

    # ### NASA Mars News

    # In[8]:

    # Visit the NASA Mars news site
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(3)

    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # In[9]:

    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text.
    # Assign the text to variables that you can reference later.
    news = soup.select(".grid_layout .list_text")[0]
    # news

    # In[10]:

    # article title
    news.a.text

    # In[11]:

    # article text

    #  max_temp = forecast_today.find("span", class_="temp-max").text
    text = news.find("div", class_="article_teaser_body").text
    mars["news"] = text

    # ### JPL Mars Space Images - Featured Image

    # In[12]:

    # Initialize browser
    # browser = init_browser()

    # In[16]:

    # Visit the url for JPL Featured Space Image here.
    url2 = "https://www.jpl.nasa.gov/spaceimages/index.php?category=Mars"
    # Use splinter to navigate the site and find the image url for the current Featured Mars Image
    # and assign the url string to a variable called featured_image_url.
    browser.visit(url2)
    time.sleep(3)

    # In[17]:

    button = browser.find_by_id("full_image")
    button.click()

    # In[18]:

    time.sleep(3)
    # Scrape page into soup
    html2 = browser.html
    soup2 = BeautifulSoup(html2, "html.parser")
    # soup2

    # In[19]:

    # Use splinter to navigate the site and find the image url for the current Featured Mars
    # Image and assign the url string to a variable called featured_image_url.
    pic_url = soup2.select(".fancybox-image")[0]["src"]

    pic_url

    # In[20]:

    # Make sure to save a complete url string for this image.
    featured_image_url = "https://www.jpl.nasa.gov" + pic_url
    featured_image_url
    mars["Featured Image"] = featured_image_url

    # ### Mars Weather

    # In[21]:

    # Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the
    # page. Save the tweet text for the weather report as a variable called mars_weather.

    # In[22]:

    # In[23]:

    # Setup Tweepy API Authentication
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    # In[24]:

    # target_user = "MarsWxReport"

    # tweet = api.user_timeline(target_user, count=1)
    # tweet = tweet[0]

    # In[25]:

    # mars_weather = tweet["text"]
    # mars_weather

    # In[33]:

    # Unfortunately, the last tweet that this user has is a retweet of something not related to Mars weather so I'm going
    # to have to scrape twitter and not use the twitter API.

    twitter_url = "https://twitter.com/MarsWxReport"
    browser.visit(twitter_url)
    time.sleep(3)
    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # In[39]:

    mars_weather_tweet = soup.find(
        "div", attrs={"class": "tweet", "data-screen-name": "MarsWxReport"}
    )
    mars_weather_tweet

    tweet = mars_weather_tweet.find(
        "p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"
    ).text

    mars["weather"] = tweet

    # ### Mars Facts

    # In[26]:

    # Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including
    # Diameter, Mass, etc.
    # Use Pandas to convert the data to a HTML table string.

    url = "https://space-facts.com/mars/"

    table = pd.read_html(url)[0]
    mars["table"] = table.to_html()

    # In[27]:

    # type(table)

    # ### Mars Hemispheres

    # In[28]:

    # Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
    # browser = init_browser()

    hemis_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(hemis_url)
    time.sleep(3)
    # In[29]:

    # Scrape page into soup
    html = browser.html
    soup3 = BeautifulSoup(html, "html.parser")

    # In[30]:

    # isolate the class
    soup3.select(".description")[3].a["href"]

    # In[31]:

    # Loop to pull out the partial urls
    hemispheres = []

    for i in range(4):
        hemi = soup3.select(".description")[i].a["href"]
        # print(hemi)
        hemispheres.append(hemi)

    # In[32]:

    # Loop to add the partial URL to the original and append it to a list
    image_url = []
    for h in hemispheres:
        image = "https://astrogeology.usgs.gov" + h
        image_url.append(image)
        # print(image)

    # In[34]:

    # loop to go to each of the URLs and scrape it for the full images uand the title
    hemi_url = []
    hemi_title = []
    for url in image_url:
        #     browser = init_browser()
        browser.visit(url)
        time.sleep(3)
        # Scrape page into soup
        html = browser.html
        soup4 = BeautifulSoup(html, "html.parser")
        href = soup4.select(".downloads")[0].a["href"]
        hemi_url.append(href)
        title = soup4.find("h2", class_="title").text
        hemi_title.append(title)

    # In[35]:

    # hemi_url

    # In[36]:

    # Creating a list of dictionaries with my lists of urls and image titles.
    hemisphere_info = []

    for i in range(4):
        hemisphere_info.append({"title": hemi_title[i], "url": hemi_url[i]})

    mars["Hemispheres"] = hemisphere_info

    # In[ ]:

    # look at the costa rica page
    # put all of the data you scraped into a dictionary

    browser.quit()
    return mars


if __name__ == "__main__":
    data = scrape()
    print(data)
