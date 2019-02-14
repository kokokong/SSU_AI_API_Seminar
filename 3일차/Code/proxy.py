from flask import Flask,jsonify,request,make_response
from urllib.request import urlopen, Request
import urllib
import bs4
import requests


app = Flask(__name__) 
app.secret_key = 'secret'

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

def ReturnWeather(paraM):
    location = paraM["city"]["value"]
    print(location)
    enc_location = urllib.parse.quote(location + '+날씨')

    url = 'https://search.naver.com/search.naver?ie=utf8&query='+ enc_location

    req = Request(url)
    page = urlopen(req)
    html = page.read()
    soup = bs4.BeautifulSoup(html,'html5lib')
    tmper = soup.find('p', class_='info_temperature').find('span', class_='todaytemp').text
    cast_txt = soup.find('ul', class_='info_list').find('p', class_='cast_txt').text
    w_cond = cast_txt[:2]; diff = cast_txt[4:-2]
    msg =  tmper + '도로 '+w_cond+"이며 "+diff+"습니다."
    
    return jsonify ({
            "version": "2.0",
            "resultCode": "OK",
            "output": {
                    "answer": msg
                }
            })


def Return_dust(paraM):
    location = paraM["city_for_dust"]["value"]
    print(location)
    enc_location = urllib.parse.quote(location + '+날씨')

    url = 'https://search.naver.com/search.naver?ie=utf8&query='+ enc_location

    req = Request(url)
    page = urlopen(req)
    html = page.read()
    soup = bs4.BeautifulSoup(html,'html5lib')
    #print('현재 ' + location + ' 날씨는 ' + soup.find('p', class_='info_temperature').find('span', class_='todaytemp').text + '도 입니다.')
    micro_dust = soup.find('dd', class_='lv2').find('span', class_='num').text
    m_cond = get_condition(micro_dust)

    s_micro_dust = soup.find('dd', class_='lv2').find('span', class_='num').text
    s_cond = get_condition(s_micro_dust)

    msg =  '미세먼지는 ' + micro_dust+'로 ' +m_cond + '이며, 초미세먼지는 '+s_micro_dust+'로 '+s_cond+'입니다.'
    print(msg)

    return jsonify ({
        "version": "2.0",
        "resultCode": "OK",
        "output": {
                    "answer_dust": msg
                }
            })

@app.route('/',methods=["POST"])
def foo():
    data = request.json
    print(data)
    actionName = data["action"]["actionName"]
    paraM = data["action"]["parameters"]
    print(actionName)
    print(paraM)
    if data["action"]["actionName"]=="answer.Dust":
        return Return_dust(paraM)

    elif data["action"]["actionName"]=="answer.weather":
        return ReturnWeather(paraM)

    return jsonify ({
        "version": "2.0",
        "resultCode": "OK",
        "output": {
                    "answer": "누구는 알지 못하는 질문이네요"
                }
        })

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=443)