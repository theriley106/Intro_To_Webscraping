import requests
import bs4
import randomheaders
import re

URL = "https://www.amazon.com/s/ref=nb_sb_ss_c_2_17?url=search-alias%3Dstripbooks&field-keywords={0}"
EXAMPLE_URL = "https://www.amazon.com/s?k=g&i=electronics&bbn=172282&rh=p_6%3AA2L77EE7U53NWQ%7CATVPDKIKX0DER&dc&qid=1562077809&rnid=303116011&ref=sr_nr_p_6_1"
SELECTOR = ".s-include-content-margin"
PRICE_CSS = ".a-spacing-top-mini .a-color-base"
TRADE_SELECTOR = ".a-text-normal .a-size-small .a-color-base"
PRIME_SELECTOR = ".a-icon-medium"
# This is the CSS selector for the Amazon Prime logo
NEW_PRICE_SELECTOR = ".a-spacing-top-small .a-text-normal"
# This is the CSS selector for new prices on Amazon

USED_NEW_PRICE_SELECTOR = ".a-spacing-top-mini .a-color-base"
# This is the used/new price selector

URL.format("biology+textbooks")

def extract_number(string):
	return [x for x in re.findall("([0-9]+\.[0-9][0-9]?)?", string) if len(x) > 2]

def is_prime_eligible(item):
	# This indicates that the item is prime eligible
	return len(item.select(PRIME_SELECTOR)) > 0

def get_used_price(item):
	usedPrice = item.select(USED_NEW_PRICE_SELECTOR)
	try:
		usedPrice = float(usedPrice[0].getText().replace("$", ""))
		return usedPrice
	except:
		return None

def get_amazon_prime_price(item):
	amazonPrice = item.select(NEW_PRICE_SELECTOR)
	try:
		return extract_number(amazonPrice[0].getText())
	except:
		return None


def create_url(keyword, page=1):
	return URL.format(keyword.replace(" ", "+")) + "&page={}".format(page)

def get_url(url):
	headers = randomheaders.LoadHeader()
	return requests.get(url, headers=headers)

def string_to_float(string):
	return float('.'.join(re.findall("\d+", string)))


if __name__ == '__main__':
	urlVal = create_url("Biology Textbooks")
	print(urlVal)
	res = get_url(urlVal)
	page = bs4.BeautifulSoup(res.text, 'lxml')
	print(page.title.string)
	selections = page.select(SELECTOR)
	for item in selections:
		try:
			if get_used_price(item) != None:
				print(get_amazon_prime_price(item))
			#priceVal = (string_to_float(item.select(PRICE_CSS)[0].getText()))
			#tradeVal = (string_to_float(item.select(TRADE_SELECTOR)[0].getText()))
			#print(tradeVal - priceVal)
		except Exception as exp:
			print(exp)
			pass
