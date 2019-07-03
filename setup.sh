curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
cp -r dependencies/* .
pip config set global.index-url https://artifactory.cloud.capitalone.com/artifactory/api/pypi/pypi-internalfacing/simple/
pip install lxml -t .
python -c 'import randomheaders;import bs4;import requests;import lxml;page = bs4.BeautifulSoup("<html></html>", "lxml");'