#!/usr/local/bin/python3
# coding: utf-8

# import libraries
from bs4 import BeautifulSoup
import requests

# specify the url
quote_page = "https://www.marketwatch.com/investing/index/spx?mod=newsviewer_cl\
ick"

# query the website and return the html to the variable ‘page’
page = requests.get(quote_page)

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page.content, "html.parser")

#print(soup.prettify(formatter="html"))

# get the index price
price_box = soup.find("meta", attrs= {'name' : 'price'})
print("%s" % (price_box))
