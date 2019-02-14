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
enc_location = urllib.parse.quote(location + '+날씨')

url = 'https://search.naver.com/search.naver?ie=utf8&query='+ enc_location

req = Request(url)
page = urlopen(req)
html = page.read()
soup = bs4.BeautifulSoup(html,'html5lib')
tmper = soup.find('p', class_='info_temperature').find('span', class_='todaytemp').text
cast_txt = soup.find('ul', class_='info_list').find('p', class_='cast_txt').text
w_cond = cast_txt[:2]; diff = cast_txt[4:-2]
msg = ' 날씨는 ' + tmper + '도로 '+w_cond+"이며 "+diff+"습니다."
print(msg)
"""
#print('현재 ' + location + ' 날씨는 ' + soup.find('p', class_='info_temperature').find('span', class_='todaytemp').text + '도 입니다.')
micro_dust = soup.find('dd', class_='lv2').find('span', class_='num').text
m_cond = get_condition(micro_dust)

s_micro_dust = soup.find('dd', class_='lv2').find('span', class_='num').text
s_cond = get_condition(s_micro_dust)

print('현재 ' + location + ' 미세먼지는 ' + micro_dust+'로 '+m_cond + '이며, 초미세먼지는 '+s_micro_dust+'로 '+s_cond+'입니다.')

r = requests.post('http://ubuntu.hanukoon.com:3000/', json={
    "version": "2.0",
    "action": {
        "actionName": "getSchool",
        "parameters": {
            "scname": {
                "type": "SCHOOL_NAME",
                "value": "은여울중학교"
            }
        }
    },
})
print(r.text)
#"""