# Scrapping aggregated Linkedin data using Python
This repository uses Python's Selenium [package](https://selenium-python.readthedocs.io/) to scrap data off of LinkedIn and export it into a csv file. This project scraps select aggregate alumini data (e.g. summary counts) from all eight Ivy League universities' Linkedin page. This would allow users, for example, identify the top industries or companies a majority of Ivy League graduates work for. However, the foundational code can have many other applications. 

As such, this is an introductory repository to help Python users learn about the basics of (a) webscraping, (b) using "for" loops for parsimonious code, and (c) working with / exporting nested dictionaries. This repository uses Google Chrome (and correspondingly [chromedriver](https://chromedriver.chromium.org/)) to complete its task. 

## How to use this repository
This repository contains two files:

1. **Parameters**: Where you can define and store your parameters:
  + College names and urls
  + LinkedIn username and password. This part is necessary if you want to automatically log-in to LinkedIn and do not want your crendetials displayed in the main code.  
2. **Scraping**: Running this script competes the main portions of the task. 
  + Uses Python (Selenium) to control and direct Chrome to target web site(s).
  + Loops over each universities' LinkedIn page
  + Downloads page_source HTML code into Python as text
  + Uses xpath location to identify and store target data/information on each website
  + Exports dictionaries of stored data into a CSV file
