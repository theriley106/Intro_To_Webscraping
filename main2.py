import requests
import bs4
import randomheaders
import re

URL = "https://www.amazon.com/s/ref=nb_sb_ss_c_2_17?url=search-alias%3Dstripbooks&field-keywords={0}"
SELECTOR = ".s-item-container"
PRICE_CSS = ".a-size-base.a-color-base"
TRADE_SELECTOR = ".a-text-normal .a-size-small .a-color-base"
URL.format("biology+textbooks")

def create_url(keyword, page=1):
	return URL.format(keyword.replace(" ", "+")) + "&page={}".format(page)

def get_url(url):
	headers = randomheaders.LoadHeader()
	return requests.get(url, headers=headers)

def string_to_float(string):
	return float('.'.join(re.findall("\d+", string)))


if __name__ == '__main__':
	urlVal = create_url("Biology Textbooks")
	res = get_url(urlVal)
	page = bs4.BeautifulSoup(res.text, 'lxml')
	print(page.title.string)
	selections = page.select(SELECTOR)
	for item in selections:
		try:
			priceVal = (string_to_float(item.select(PRICE_CSS)[0].getText()))
			tradeVal = (string_to_float(item.select(TRADE_SELECTOR)[0].getText()))
			print(tradeVal - priceVal)
		except Exception as exp:
			print(exp)
			pass
