#Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

#Navigation
executable_path = {"executable_path": "chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)


def scrape():
    final_data = {}
    output = marsNews()
    final_data["mars_news"] = output[0]
    final_data["mars_paragraph"] = output[1]
    final_data["mars_image"] = marsImage()
    final_data["mars_weather"] = marsWeather()
    final_data["mars_facts"] = marsFacts()
    final_data["mars_hemisphere"] = marsHem()
    return final_data


#Nasa Mars News Requirement 1
def marsNews():
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    time.sleep(15)
    news_p = article.find("div", class_="article_teaser_body").text
    output = [news_title, news_p]
    return output


time.sleep(15)


#JPL images Requiremet 2
def marsImage():
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    image = soup.find('article', class_='carousel_item')['style'].split("'")[1]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    return featured_image_url


time.sleep(15)


#Mars Weather Scrape Requirement 3
def marsWeather():
    results = {}
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    soup = BeautifulSoup(browser.html, 'html.parser')
    #Latest tweet
    mars_weather = soup.find(
        'div', class_='js-tweet-text-container').text.split('\n')[1]
    results['mars_weather'] = mars_weather
    return mars_weather


time.sleep(15)


#Mars Facts
def marsFacts():
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    mars_data = pd.read_html(facts_url)
    mars_data = pd.DataFrame(mars_data[0])
    mars_facts = mars_data.to_html(header=False, index=False)
    print(mars_facts)
    return mars_facts


time.sleep(15)


#Mars Hemispheres
def marsHem():
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_hemisphere = []

    products = soup.find("div", class_="result-list")
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link
        browser.visit(image_link)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemisphere.append({"title": title, "img_url": image_url})
    return mars_hemisphere