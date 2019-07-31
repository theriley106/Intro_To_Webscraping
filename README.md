# Intro_To_Webscraping

Finding Arbitrage Opportunities in the Amazon Textbook Trade-In Program.

My Introduction to Web Scraping talk at Capital One.

## Instructions

### Install Dependencies

```bash
$ pip install -r requirements.txt
```

### Find eBay -> Amazon Trade-In Arbitrage Opportunities

```bash
$ python complete.py
Pulling: https://www.amazon.com/s?k=textbook+edition+pearson&i=stripbooks&ref=nb_sb_noss_2&page=1
Pulling: https://www.amazon.com/dp/0134082575
9780134082578
Pulling: https://www.amazon.com/dp/0134093410
0134093410
Pulling: https://www.amazon.com/dp/0131421131
0131421131
Pulling: https://www.amazon.com/dp/0321927044
0321927044
Pulling: https://www.amazon.com/dp/0134497163
0134497163
Pulling: https://www.ebay.com/sch/i.html?_from=R40&_nkw=0134497163+&_sacat=0&LH_TitleDesc=0&_sop=15&rt=nc&LH_BIN=1

*****[ PROFITABLE BOOK FOUND ]*****
TITLE: Statistics for Business: Decision Making and Analysis (3rd Edition)
ISBN: 0134497163
EBAY PRICE: 37.98
TRADE IN PRICE: 65.52
PROFIT: 27.54

Pulling: https://www.amazon.com/dp/013449251X
013449251X
Pulling: https://www.amazon.com/dp/0134257014
9780134257013
Pulling: https://www.ebay.com/sch/i.html?_from=R40&_nkw=9780134257013+&_sacat=0&LH_TitleDesc=0&_sop=15&rt=nc&LH_BIN=1
...

```