import requests
import bs4
import randomheaders
import utilities
import re
import traceback

## AMAZON STUFF

AMAZON_URL = "https://www.amazon.com/s?k={0}&i=stripbooks&ref=nb_sb_noss_2"
PRIME_SELECTOR = ".a-icon-medium"
NEW_PRICE_SELECTOR = ".a-spacing-top-small .a-text-normal"
TITLE_SELECTOR = ".a-size-medium"
TRADE_IN_SELECTOR = "#tradeInButton_tradeInValue"
USED_NEW_PRICE_SELECTOR = ".a-spacing-top-mini .a-color-base"
ISBN_SELECTOR = "#isbn_feature_div .a-color-base"
TRADE_SELECTOR = ".a-text-normal .a-size-small .a-color-base"
SELECTOR = ".s-include-content-margin"
PRICE_CSS = ".a-spacing-top-mini .a-color-base"

## EBAY STUFF

EBAY_URL = "https://www.ebay.com/sch/i.html?_from=R40&_nkw={0}+&_sacat=0&LH_TitleDesc=0&_sop=15&rt=nc&LH_BIN=1"
EBAY_ITEM_SELECTOR = ".s-item__details"
EBAY_SHIPPING_SELECTOR = ".s-item__logisticsCost"
EBAY_PRICE_SELECTOR = ".s-item__price"

def create_amazon_url(keyword, page=1):
	# This generates valid Amazon URLs given a search query
	return AMAZON_URL.format(keyword.replace(" ", "+")) + "&page={}".format(page)

def get_url(url):
	# This is the function to make the network request to Amazon
	for i in range(3):
		try:
			headers = randomheaders.LoadHeader()
			print("Pulling: {}".format(url))
			return requests.get(url, headers=headers, timeout=5)
		except:
			print("Failed Network Request | Retrying")

def extract_ebay_shipping(item):
	# This extracts the eBay shipping price CSS selector for the first item on a search page
	try:
		return utilities.extract_number(item.select(EBAY_SHIPPING_SELECTOR)[0].getText())[0]
	except:
		return 0

def extract_ebay_price(item):
	# This extracts the eBay selling price CSS selector for the first item on a search page
	try:
		return utilities.extract_number(item.select(EBAY_PRICE_SELECTOR)[0].getText())[0]
	except:
		return 0

def get_price_from_ebay(isbn):
	# This extracts the selling price (selling+shipping) from eBay for a given ISBN
	url = EBAY_URL.format(isbn)
	# Creates the eBay URL
	res = get_url(url)
	# Makes a network request to get the page
	page = bs4.BeautifulSoup(res.text, 'lxml')
	for item in page.select(EBAY_ITEM_SELECTOR):
		price = extract_ebay_price(item)
		# This is the price on the page
		shipping = extract_ebay_shipping(item)
		# This is the price on the page
		if price != 0:
			return round(price + shipping, 2)
	return 0

def extract_dp(item):
	# This extract the Amazon ASIN Number from an item page | This is an internal identifier for the book
	try:
		return str(item.select(".s-line-clamp-2")[0]).partition("/dp/")[2].partition('/')[0]
	except:
		return None

def get_isbn(page):
	# This extracts the ISBN from an item page | This is an external identifier for the book
	try:
		return page.select(ISBN_SELECTOR)[3].getText().strip()
	except:
		return None

def get_used_price(item):
	# This extracts the used price from an Amazon Search page (Generally 16 used prices are on each page)
	try:
		usedPrice = item.select(USED_NEW_PRICE_SELECTOR)
		usedPrice = float(usedPrice[0].getText().replace("$", ""))
		return usedPrice
	except:
		return None

def get_trade_in_value(page):
	# This extracts the trade in value from an item page
	isbn = get_isbn(page)
	tradeIn = page.select(TRADE_IN_SELECTOR)
	if len(tradeIn) == 0:
		return 0
	else:
		return utilities.extract_number(tradeIn[0].getText())[0]

def extract_title(item):
	# This extracts the item title from a search page
	return item.select(TITLE_SELECTOR)[0].getText()

def download_item_page(asinNumber):
	# This downloads the page for a given ASIN number | IE the item page
	url = "https://www.amazon.com/dp/" + asinNumber
	res = get_url(url)
	return bs4.BeautifulSoup(res.text, 'lxml')

def check_for_arbitrage(item):
	# This function checks to see if an item object could be a potential arbitrage opportunity
	usedPrice = get_used_price(item)
	#print(extract_dp(item))
	asinNumber = extract_dp(item)
	# This is the ASIN number from Amazon
	if len(asinNumber) > 0:
		page = download_item_page(asinNumber)
		# Downloads the item page
		#print(page.title.string)
		tradeInValue = get_trade_in_value(page)
		# Trade In Value
		isbn = get_isbn(page)
		#print(tradeInValue)
		#print(isbn)
		print(isbn)
		if tradeInValue != 0 and isbn != None:
			ebayPrice = get_price_from_ebay(isbn)
			title = extract_title(item)
			profit = tradeInValue - ebayPrice
			if ebayPrice != 0 and profit > 0:
				utilities.print_result(title, isbn, ebayPrice, tradeInValue, profit, True)
				utilities.save_result(title, isbn, ebayPrice, tradeInValue, profit, True)
			else:
				
				utilities.print_result(title, isbn, ebayPrice, tradeInValue, profit, False)
				utilities.save_result(title, isbn, ebayPrice, tradeInValue, profit, False)

if __name__ == '__main__':
	for i in range(1,10):
		# Goes from page 1 -> 9
		urlVal = create_amazon_url("textbook edition pearson", i)
		# Creates an Amazon URL for the search query "Textbook edition pearson"
		res = get_url(urlVal)
		# Makes a network request to grab that URL
		page = bs4.BeautifulSoup(res.text, 'lxml')
		# Page is a BS4 object that allows us to parse the HTML
		searchResults = page.select(SELECTOR)
		for item in searchResults:
			try:
				check_for_arbitrage(item)
			except Exception as exp:
				traceback.print_exc()
				pass
