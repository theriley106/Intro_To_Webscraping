import requests
import bs4
import utilities
import randomheaders

EBAY_URL = "https://www.amazon.com/s?k=textbook+edition+Pearson&i=stripbooks&ref=nb_sb_noss_2"
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
	for item in page.select(".aok-float-left"):
		price = extract_ebay_price(item)
		shipping = extract_ebay_shipping(item)
		if price != 0:
			return price + shipping
	return 0

if __name__ == '__main__':
	url = EBAY_URL
	res = requests.get(url, headers=randomheaders.LoadHeader())
	page = bs4.BeautifulSoup(res.text, 'lxml')
	for item in page.select(".aok-float-left"):
		for v in item.select(".a-carousel-card"):
			print(v)