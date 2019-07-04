import re
import os
import csv
from complete import *

SAVE_TO = "results.csv"

def extract_number(string):
	# This extracts prices from strings
	return [round(float(x), 2) for x in re.findall("([0-9]+\.[0-9][0-9]?)?", string) if len(x) > 2]

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
		return float(extract_number(amazonPrice[0].getText())[0])
	except:
		return None

def string_to_float(string):
	return float('.'.join(re.findall("\d+", string)))

def is_good_deal(usedPrice, newPrice):
	#print(((newPrice - usedPrice) / newPrice))
	return 100*((newPrice - usedPrice) / newPrice) > 30

def print_result(title, isbn, ebayPrice, tradeInValue, profit, success):
	if success:
		print("\n*****[ PROFITABLE BOOK FOUND ]*****")
	else:
		print("\n[ UNPROFITABLE BOOK FOUND ]")
	print("TITLE: {}".format(title))
	print("ISBN: {}".format(isbn))
	print("EBAY PRICE: {}".format(round(ebayPrice,2)))
	print("TRADE IN PRICE: {}".format(tradeInValue))
	print("PROFIT: {}\n".format(round(profit,2)))

def save_result(title, isbn, ebayPrice, tradeInValue, profit, success):
	if os.path.exists(SAVE_TO) == False:
		with open(SAVE_TO, 'w') as myfile:
			wr = csv.writer(myfile)
			wr.writerow(["Title", "ISBN", "Ebay Price", "Trade In Value", "Profit"])
	with open(SAVE_TO, 'a') as myfile:
		wr = csv.writer(myfile)
		wr.writerow([title, isbn, round(ebayPrice, 2), tradeInValue, round(profit,2)])
