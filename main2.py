import requests
import bs4
import randomheaders
import utilities
import re
import traceback

URL = "https://www.amazon.com/s?k={0}&i=stripbooks&ref=nb_sb_noss_2"
#EXAMPLE_URL = "https://www.amazon.com/s?k=textbook+edition+Pearson&i=stripbooks&ref=nb_sb_noss_2"
SELECTOR = ".s-include-content-margin"
PRICE_CSS = ".a-spacing-top-mini .a-color-base"
TRADE_SELECTOR = ".a-text-normal .a-size-small .a-color-base"
PRIME_SELECTOR = ".a-icon-medium"
# This is the CSS selector for the Amazon Prime logo
NEW_PRICE_SELECTOR = ".a-spacing-top-small .a-text-normal"
# This is the CSS selector for new prices on Amazon

USED_NEW_PRICE_SELECTOR = ".a-spacing-top-mini .a-color-base"
# This is the used/new price selector
TITLE_SELECTOR = ".a-size-medium"
TRADE_IN_SELECTOR = "#tradeInButton_tradeInValue"

ISBN_SELECTOR = "#isbn_feature_div .a-color-base"
EBAY_URL = "https://www.ebay.com/sch/i.html?_from=R40&_nkw={0}+&_sacat=0&LH_TitleDesc=0&_sop=15&rt=nc&LH_BIN=1"
EBAY_ITEM_SELECTOR = ".s-item__details"

def create_url(keyword, page=1):
	return URL.format(keyword.replace(" ", "+")) + "&page={}".format(page)

def get_url(url):
	headers = randomheaders.LoadHeader()
	return requests.get(url, headers=headers)

def extract_ebay_shipping(item):
	# This extracts the eBay shipping price CSS selector for the first item on a search page
	try:
		return utilities.extract_number(item.select(".s-item__logisticsCost")[0].getText())[0]
	except:
		return 0

def extract_ebay_price(item):
	# This extracts the eBay selling price CSS selector for the first item on a search page
	try:
		return utilities.extract_number(item.select(".s-item__price")[0].getText())[0]
	except:
		return 0

def get_price_from_ebay(isbn):
	# This extracts the selling price (selling+shipping) from eBay for a given ISBN
	url = EBAY_URL.format(isbn)
	# Creates the eBay URL
	res = get_url(url)
	# Makes a network request to get the page
	print("\nCHECKING: {}".format(url))
	print("TITLE: ISBN #{}\n".format(isbn))
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
	try:
		return str(item.select(".s-line-clamp-2")[0]).partition("/dp/")[2].partition('/')[0]
	except:
		return None

def get_isbn(page):
	try:
		return page.select(ISBN_SELECTOR)[3].getText().strip()
	except:
		return None

def get_used_price(item):
	usedPrice = item.select(USED_NEW_PRICE_SELECTOR)
	try:
		usedPrice = float(usedPrice[0].getText().replace("$", ""))
		return usedPrice
	except:
		return None

def get_trade_in_value(page):
	isbn = get_isbn(page)
	tradeIn = page.select(TRADE_IN_SELECTOR)
	if len(tradeIn) == 0:
		return 0
	else:
		return utilities.extract_number(tradeIn[0].getText())[0]

def extract_title(item):
	return item.select(TITLE_SELECTOR)[0].getText()

def download_item_page(asinNumber):
	url = "https://www.amazon.com/dp/" + asinNumber
	res = get_url(url)
	print("\nCHECKING: {}".format(url))
	print("TITLE: ASIN #{}\n".format(asinNumber))
	return bs4.BeautifulSoup(res.text, 'lxml')

def check_for_arbitrage(item):
	usedPrice = get_used_price(item)
	#print(extract_dp(item))
	asinNumber = extract_dp(item)
	# This is the ASIN number from Amazon
	page = download_item_page(asinNumber)
	# Downloads the item page
	#print(page.title.string)
	tradeInValue = get_trade_in_value(page)
	# Trade In Value
	isbn = get_isbn(page)
	#print(tradeInValue)
	#print(isbn)
	if tradeInValue != 0 and isbn != None:
		ebayPrice = get_price_from_ebay(isbn)
		title = extract_title(item)
		profit = tradeInValue - ebayPrice
		if ebayPrice != 0 and profit > 0:
			print("*****[ PROFITABLE BOOK FOUND ]*****")
			print("TITLE: {}".format(title))
			print("ISBN: {}".format(isbn))
			print("EBAY PRICE: {}".format(ebayPrice))
			print("TRADE IN PRICE: {}".format(tradeInValue))
			print("PROFIT: {}\n".format(profit))
		else:
			print("[ UNPROFITABLE BOOK FOUND ]")
			print("TITLE: {}".format(title))
			print("ISBN: {}".format(isbn))
			print("EBAY PRICE: {}".format(ebayPrice))
			print("TRADE IN PRICE: {}".format(tradeInValue))
			print("PROFIT: {}\n".format(profit))



#print("ISBN: {}".format(isbn))
if __name__ == '__main__':
	for i in range(1,10):
		urlVal = create_url("textbook edition pearson", i)
		#print("CHECKING: {}\n".format(urlVal))
		res = get_url(urlVal)
		page = bs4.BeautifulSoup(res.text, 'lxml')
		print("\nCHECKING: {}".format(urlVal))
		print("TITLE: {}\n".format(page.title.string))
		selections = page.select(SELECTOR)
		for item in selections:
			try:
				check_for_arbitrage(item)
			except Exception as exp:
				traceback.print_exc()
				pass
