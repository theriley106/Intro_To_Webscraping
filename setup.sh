sudo -H python -m ensurepip
cp -r dependencies/* .
python -m pip config set global.index-url https://artifactory.cloud.capitalone.com/artifactory/api/pypi/pypi-internalfacing/simple/
python -m pip install -r requirements.txt -t .
python -c 'import randomheaders;import bs4;import requests;import lxml;page = bs4.BeautifulSoup("<html></html>", "lxml");'