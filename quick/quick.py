# -*- coding: utf-8 -*-

import mechanize
import json
import codecs
from webhelpers.text import urlify
from bs4 import BeautifulSoup, Tag, NavigableString

styles = "p { padding: 0; margin: 0; margin-top: 0; margin-bottom: 0; padding-top: 0; padding-bottom: 0; font-family: arial; }"

# parse with beautifulsoup and return soup
#-----------------------------------------

def get_soup(email_file):

	f = open(email_file, 'r')
	soup = BeautifulSoup(f)

	return soup

# parse with beautifulsoup and return soup
#-----------------------------------------

def insert_styles(soup):

	style_tag = soup.new_tag("style")

	html = soup.find("html")
	html.insert(0, style_tag)
	style_tag.insert(0, styles)

	return soup

# center entire email by nesting it in a table
#-----------------------------------------------

def center_email(soup):

	# Get Elements of Email
	body = soup.body

	body['bgcolor'] = ""
	inner_table = body.find("table")
	inner_table['id'] = "inner"

	# create table to use later
	new_wrapper_table = soup.new_tag("table")
	new_wrapper_row = soup.new_tag("tr")
	new_wrapper_col = soup.new_tag("td")

	# give it attr
	new_wrapper_table['border'] = '0'
	new_wrapper_table['cellpadding'] = '0'
	new_wrapper_table['cellspacing'] = '0'
	new_wrapper_table['align'] = 'center'

	# insert new table and nest the original table inside
	body.insert(0, new_wrapper_table)
	new_wrapper_table.insert(0, new_wrapper_row)
	new_wrapper_row.insert(0, new_wrapper_col)
	new_wrapper_col.insert(0, inner_table)

	return soup



# strip all height attributes out of the email
#----------------------------------------------

def strip_heights(soup):

	tags = soup.find_all(True)
	for tag in tags:
		del tag["height"]

	return soup


# create nested tables and remove colspans
#-------------------------------------------

def remove_colspans(soup):

	# First remove the unnecessary attributes

	td = soup.find_all('td')
	for tag in td:
		del tag["colspan"]

	# Create our nested tables

	tbl = soup.find("table", {"id": "inner"})
	tblrow = tbl.find_all('tr')
	for i in tblrow:
		new = i.find_all('td')
		if len(new) > 1:
			for item in i.find_all('td'):
				item.extract()

			# create table
			intable = soup.new_tag("table")
			inrow = soup.new_tag("tr")
			incol = soup.new_tag("td")

			#attr
			intable['border'] = '0'
			intable['cellpadding'] = '0'
			intable['cellspacing'] = '0'

			i.insert(0, incol)
			incol.insert(0, intable)
			intable.insert(0, inrow)
			new.reverse()
			for item in new:
				inrow.insert(0, item)

	return soup

# insert necessary image styles for all img tags
#------------------------------------------------

def image_styles(soup):

	# Get images and add necessary styles

	img = soup.findAll('img')
	for i in img:
		i['style'] = "display: block; border: 0;"
		width = i['width']
		i.parent["width"] = width

	return soup

# make all styles inline
#-----------------------------

def inline_email(filename, html):
	# get the url global var
	inliner = 'http://inliner.cm/'

	# make ourselves a browser
	br = mechanize.Browser()
	br.set_handle_robots(False)
	#br.addheaders = [('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:24.0) Gecko/20100101 Firefox/24.0')]

	# open the inliner url and select the right form
	br.open(inliner)
	br.select_form(nr=0)

	# make the html from the file into a string
	html = str(html)

	# fill the text area
	br.form['code'] = html

	# submit and get json response
	resp = br.submit()
	un = json.loads(resp.read())

	# parse as html
	soup = BeautifulSoup(un['HTML'])

	# set up filename and content to write to file
	#title = soup.title.text
	content = soup.prettify()

	# write
	print "Writing to out.%s" % filename
	with codecs.open("out.%s" % filename, 'w', encoding='utf-8') as out:
		out.write(content)
