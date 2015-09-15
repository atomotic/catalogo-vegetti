#!/usr/bin/env python

import sys
import requests
import requests_cache
import unicodecsv
from bs4 import BeautifulSoup

if len(sys.argv) < 2:
    sys.exit('Usage: %s capital-letter' % sys.argv[0])
letter = sys.argv[1]

BASE_URL = "http://www.fantascienza.com/catalogo/autori"

output_file = "{}/{}.csv".format("./authors", letter )
output_csv = open(output_file, 'w')
csv = unicodecsv.writer(output_csv, encoding='utf-8', delimiter=';', quoting=unicodecsv.QUOTE_ALL)

start_url = "{}/{}".format(BASE_URL, letter)
requests_cache.install_cache('demo_cache')
html_doc = requests.get(start_url).content

doc = BeautifulSoup(html_doc, 'html.parser')

def last_page():
	pages = doc.find('div',  {'class': 'paginazione'})
	try:
		p = [page for page in pages.find_all('a')]
		return p[-2].text
	except AttributeError:
		return 1

def pages_url(last_page):
	return ["{}/?p={}".format(start_url,p) for p in range(1, (int(last_page)+1))]

print "scraping {}".format(letter)

for page in pages_url(last_page()):
	html = requests.get(page).content
	doc = BeautifulSoup(html, 'html.parser')
	authors = doc.find_all("dt")

	for author in authors:
		nilf =  author["id"]
		link = author.a["href"]
		name = author.a.text
		csv.writerow([nilf, name, link])
		# print u"{} - {} - {}".format(nilf, link, name)

output_csv.close()