from urllib.request import urlopen, Request
import urllib
import bs4
import requests

def get_condition(dust):
    dust = int(dust[:-3])
    if dust <31:
        cond = "좋음"
    elif dust <81:
        cond  = "보통"
    elif dust <151:
        cond = "나쁨"
    else:
        cond = "매우나쁨"
    return cond

location = '서울'
enc_location = urllib.parse.quote(location + '+미세먼지')

url = 'https://finance.naver.com/item/main.nhn?code=005930'
req = Request(url)
page = urlopen(req)
html = page.read()
soup = bs4.BeautifulSoup(html,'html5lib')
micro_dust = soup.find_all('div', class_='wa')
print(micro_dust)
