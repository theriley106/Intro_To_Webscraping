import requests
import bs4
import utilities

EBAY_URL = "https://www.ebay.com/sch/i.html?_from=R40&_nkw={0}+&_sacat=0&LH_TitleDesc=0&_sop=15&rt=nc&LH_BIN=1"
# 0 -> ISBN

def extract_ebay_shipping(item):
	try:
		prices = utilities.extract_number(item.select(".s-item__logisticsCost")[0].getText())
		return prices[0]
	except:
		return 0

def extract_ebay_price(item):
	try:
		prices = utilities.extract_number(item.select(".s-item__price")[0].getText())
		return prices[0]
	except:
		return 0

def get_price_from_ebay(isbn):
	url = EBAY_URL.format(isbn)
	res = requests.get(url)
	page = bs4.BeautifulSoup(res.text, 'lxml')
	for item in page.select(".s-item__details"):
		price = extract_ebay_price(item)
		shipping = extract_ebay_shipping(item)
		if price != 0:
			return price + shipping
	return 0

if __name__ == '__main__':
	print(get_price_from_ebay("0545596270"))