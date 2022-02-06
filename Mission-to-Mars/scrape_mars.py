import pandas as pd
import requests
import json
import collections
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
from bson import json_util
from bson.json_util import dumps
from pymongo import MongoClient

def scrape_data():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    data = {
        "news" : scrape_news(browser),
        "feature" : scrape_feature(browser),
        "facts" : scrape_facts(),
        "hemispheres" : scrape_images(browser)
    }
    browser.quit()
    return data

def scrape_news(browser):
    url = "https://redplanetscience.com/"
    browser.visit(url)
    soup = bs(browser.html,"html.parser")

    results = soup.find_all("div", class_= "list_text")
    news_list = []
    news_dict = {}
    for result in results:
        try:
            #news_title.append(result.find("div", class_ = "content_title").text)
            news_title = result.find("div", class_ = "content_title").text
            news_dict["tit"] = news_title
            #news_desc.append(result.find("div", class_ = "article_teaser_body").text)
            news_desc = result.find("div", class_ = "article_teaser_body").text
            news_dict["desc"] = news_desc
            #news_date.append(result.find("div", class_ = "list_date").text)
            news_date = result.find("div", class_ = "list_date").text
            news_dict["date"] = news_date
            dictionary = news_dict.copy()
            news_list.append(dictionary)
        except AttributeError as e:
            print(e)
    return news_list

def scrape_feature(browser):
    img_url = "https://spaceimages-mars.com/"
    browser.visit(img_url)
    img_soup = bs(browser.html,"html.parser")
    img_results = img_soup.find("img", class_ = "headerimage")["src"]
    featured_image_url = f"{img_url}{img_results}"
    #feature_dict = {"featured_image_url": featured_image_url}
    return featured_image_url

def scrape_facts():
    facts_url = "https://galaxyfacts-mars.com/"
    facts_table = pd.read_html(facts_url)
    mars_df = facts_table[0]
    header = mars_df.loc[0]
    clean_mars_df = mars_df[1:]
    clean_mars_df.columns = header
    clean_mars_df = clean_mars_df.set_index(clean_mars_df.columns[0])
    facts_html = clean_mars_df.to_html(classes="table-primary")
    return facts_html

def scrape_images(browser):
    astro_url = "https://marshemispheres.com/"
    browser.visit(astro_url)
    astro_soup = bs(browser.html,"html.parser")
    astro_html = astro_soup.find_all(class_="itemLink product-item")
    html_list = []
    img_urls = []
    hemi_dict = {}
    for a in astro_html:
        html = a["href"]
        if html not in html_list:
            html_list.append(html)
    for html in html_list:
        try:
            hemi_url = f"{astro_url}{html}"
            response = requests.get(hemi_url)
            response_soup = bs(response.text, "html.parser")
            #print(response_soup.prettify())
            hemi_img = response_soup.find("img", class_ = "wide-image")["src"]
            hemi_img_url = f"{astro_url}{hemi_img}"
            hemi_dict["img_url"] = hemi_img_url
            hemi_title = response_soup.find("h2", class_="title").text
            hemi_dict["img_tit"] = hemi_title
            dictionary = hemi_dict.copy()
            img_urls.append(dictionary)
            #print(astro_dict)
        except TypeError as e:
            print(html, e)
    return img_urls
if __name__ == "__main__" :
    print(scrape_data())
