sudo -H python -m ensurepip
cp -r dependencies/* .
mkdir -p ~/.pip
cat > ~/.pip/pip.conf << EOF
[global]
timeout = 60
index-url = https://artifactory.cloud.capitalone.com/artifactory/api/pypi/pypi-internalfacing/simple
EOF
python -m pip install -r requirements.txt -t .
python -c 'import randomheaders;import bs4;import requests;import lxml;page = bs4.BeautifulSoup("<html></html>", "lxml");'