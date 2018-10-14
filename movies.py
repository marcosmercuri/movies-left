from bs4 import BeautifulSoup
from lxml import html
import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import re

options = Options()
options.set_headless(headless=True)
driver = webdriver.Firefox(firefox_options=options)
driver.get("https://www.imdb.com/registration/signin")

driver.find_element_by_xpath('//span[text()="Sign in with IMDb"]').click()

username = input('Username: ')
driver.find_element_by_id("ap_email").send_keys(username)
password = getpass.getpass('Password:')
driver.find_element_by_id("ap_password").send_keys(password)
driver.find_element_by_id("signInSubmit").click()

driver.get('http://www.imdb.com/chart/top')
driver.find_element_by_id("hide-seen-top-250").click()
html_full_page = driver.page_source

soup = BeautifulSoup(html_full_page, "lxml")

movie_list_container = soup.find("div", {"class": "lister"})

print("Getting all movies")
movies = []
for movie_tr in movie_list_container.table.tbody.findChildren('tr'):
    if movie_tr.has_attr('style') is False or movie_tr['style'] != "display: none;":
    	link = movie_tr.findChildren('td')[1].a.attrs['href']
    	year = movie_tr.findChildren('td')[1].span.string
    	title = movie_tr.findChildren('td')[1].a.string
    	m = re.search('/title/(.*?)/', link)
    	cleanLink = m.group(1)
    	imdb_rating = movie_tr.findChildren('td')[2].strong.get('title')
    	movie = { 'title': title, 'link': cleanLink, 'imdb_rating': imdb_rating, 'year': year}
    	movies.append(movie)

for movie in movies:
	driver.get("https://www.imdb.com/title/"+movie['link'])
	# time.sleep(1) May or may not be needed
	element = driver.find_element_by_xpath('//time')
	movie['duration'] = element.text
	print("{: <35} {: <8} {: <10} {: <25}".format(movie['title'], movie['year'], movie['duration'], movie['imdb_rating']))


driver.quit()