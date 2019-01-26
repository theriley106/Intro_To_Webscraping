import requests
import bs4
import RandomHeaders

URL_FORMAT = "https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dstripbooks&field-keywords={}"
SECTION_CSS = ".a-fixed-left-grid-inner"
TEXTBOOK_CSS = ".a-text-normal .a-size-small .a-color-base"
PRICE_CSS = ".a-size-base.a-color-base"

def gen_url(keyword, page=1):
	# This generates the URL from a keyword and page number
	url = URL_FORMAT.format(keyword.replace(" ", "+"))
	# Would convert "Biology Textbooks" into "Biology+Textbooks" - proper URL encoding
	if page > 1:
		# You don't want to add the page parameter for pages == 1
		url += '&page={}'.format(page)
	return url

def grab_site(url):
	# Pulls the site
	headers = RandomHeaders.LoadHeader()
	# This is a non-Python user agent, which prevents Amazon from blocking the request
	return requests.get(url, headers=headers)

def convert_string_to_float(stringVal):
	# Turns function would turn $41.11 into 41.11
	# You could also just use regex
	# float("".join(re.findall("\d+", stringVal))
	try:
		price = stringVal.replace("$", "")
		price = float(price)
		return price
	except:
		return None


if __name__ == '__main__':
	keyWord = raw_input("Keyword: ")
	# This is the keyword you input into the search box on Amazon
	url = gen_url(keyWord)
	# This calls the generate URL function for that keyword
	res = grab_site(url)
	# This calls the grab URL function
	page = bs4.BeautifulSoup(res.text, 'lxml')
	# This converts it into a Beautiful Soup Object
	print page.title.string
	# This prints the URL of the page | to verify the URL was correct
	pageNumbers = int(page.select(".pagnDisabled")[0].getText())
	# Gets the total amount of page numbers for this search result
	for i in range(2,pageNumbers+1):
		# Goes from the second page onward
		# Keep in mind that URL was originally generated with the default param of 1
		try:
			# Try/Except for presentation purposes - ideally you would have better exception handling...
			for section in page.select(SECTION_CSS):
				# Goes through each item box on the Amazon page
				priceVal = section.select(PRICE_CSS)
				# This grabs the used/new price value
				tradeInPrice = section.select(TEXTBOOK_CSS)
				# This grabs the trade in price on Amazon
				if len(priceVal) == 0 or len(tradeInPrice) == 0:
					# This means that either the trade in price or the actual price were not not
					# IE Item is not trade in eligible or is out of stock
					continue
					# Continue will "Continue" to the next item on the page
				priceVal = priceVal[0].getText()
				# This convert the price value HTML markup into a human-readable string
				tradeInPrice = tradeInPrice[0].getText()
				# This convert the trade in price HTML markup into a human-readable string
				priceVal = convert_string_to_float(priceVal)
				# Turns $41.11 into 41.11
				tradeInPrice = convert_string_to_float(tradeInPrice)
				# Turns $41.11 into 41.11
				if priceVal == None or tradeInPrice == None:
					# convert_string_to_float returns None if the conversion failed
					# IE: It tries convert a single price that == "$43.13/$12.45"
					continue
					# Continue will "Continue" to the next item on the page
				profit = tradeInPrice - priceVal
				# Calculate the "Profit" for this item by subtracting trade in value by the price
				print("Price: {} | Trade In Price: {} | Profit: {}".format(priceVal, tradeInPrice, profit))
				# Prints it to the Console - you could do whatever you want with this data: store it, make a purchase, etc.
			url = gen_url(keyWord, i)
			# This generate a new url with the new page number
			res = grab_site(url)
			# Grabs the new page and save the HTML to res
			page = bs4.BeautifulSoup(res.text, 'lxml')
			# Converts the new page into a beautiful soup object
			print("{} | Page: {}".format(page.title.string, i))
			# Prints the page title and page number to the console
		except:
			pass
