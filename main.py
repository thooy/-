from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():

  url ='{"code":0,"msg":"操作成功","data":{"total":7,"sourceName":"墨迹天气","list":[{"city":"淮安","lastUpdateTime":"2022-08-22 16:55:08","date":"2022-08-22","weather":"阴","temp":38.0,"humidity":"78%","wind":"南风2级","pm25":19.0,"pm10":32.0,"low":25.0,"high":38.0,"airData":"42","airQuality":"优","dateLong":1661097600000,"weatherType":2,"windLevel":2,"province":"江苏"},{"city":"淮安","lastUpdateTime":"2022-08-22 16:11:00","date":"2022-08-23","weather":"大雨","humidity":"未知","wind":"东北风","pm25":0.0,"low":20.0,"high":26.0,"airData":"80","airQuality":"良","dateLong":1661184000000,"weatherType":9,"windLevel":1,"province":"江苏"},{"city":"淮安","lastUpdateTime":"2022-08-22 16:11:00","date":"2022-08-24","weather":"多云","humidity":"未知","wind":"东北风","pm25":0.0,"low":18.0,"high":28.0,"airData":"55","airQuality":"良","dateLong":1661270400000,"weatherType":1,"windLevel":1,"province":"江苏"},{"city":"淮安","lastUpdateTime":"2022-08-22 16:11:00","date":"2022-08-25","weather":"多云","humidity":"未知","wind":"东风","pm25":0.0,"low":21.0,"high":29.0,"airData":"55","airQuality":"良","dateLong":1661356800000,"weatherType":1,"windLevel":2,"province":"江苏"}],"logoUrl":"http://iflycar.hfdn.openstorage.cn/xfypicture/dev/logo/moji.png"}}'
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
