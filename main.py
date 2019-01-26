import requests
import bs4

URL_FORMAT = "https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dstripbooks&field-keywords={}"
SECTION_CSS = ".a-fixed-left-grid-inner"
TEXTBOOK_CSS = ".a-text-normal .a-size-small .a-color-base"
PRICE_CSS = ".a-size-base.a-color-base"

def gen_url(keyword):
	return URL_FORMAT.format(keyword.replace(" ", "+"))

def grab_site(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	return requests.get(url, headers=headers)

def convert_string_to_float(stringVal):
	if '$' in stringVal and '.' in stringVal:
		price = stringVal.replace("$", "")
		try:
			price = float(price)
			return price
		except:
			return None


if __name__ == '__main__':
	url = gen_url("Biology Textbooks")
	#raw_input(url)
	res = grab_site(url)
	page = bs4.BeautifulSoup(res.text, 'lxml')
	print page.title.string
	for section in page.select(SECTION_CSS):
		priceVal = section.select(PRICE_CSS)
		tradeInPrice = section.select(TEXTBOOK_CSS)
		if len(priceVal) == 0 or len(tradeInPrice) == 0:
			continue
		priceVal = priceVal[0].getText()
		tradeInPrice = tradeInPrice[0].getText()
		if priceVal == None or tradeInPrice == None:
			continue
		priceVal = convert_string_to_float(priceVal)
		tradeInPrice = convert_string_to_float(tradeInPrice)
		print("Price: {}".format(priceVal))
		print("Trade In Price: {}".format(tradeInPrice))
	#print [0].getText()
	#
	#page = bs4.BeautifulSoup(res.text, 'lxml')


