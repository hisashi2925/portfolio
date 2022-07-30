from asyncore import read
from gettext import find
import json
from traceback import print_tb
import pandas as pd
from bs4 import BeautifulSoup as bs
import urllib.request as req
import os.path
import time
import requests
import re
import numpy as np

#URLを取得してtextに変換
url = "http://line.userlocal.jp/"
r = requests.get(url)
time.sleep(1)

soup = bs(r.text, "html.parser")

#都道府県URLを取得して辞書化
Prefectures_dict = {}

#serch_prefectures = [elem["href"] for elem in soup.find("li", class_="pref-name").find_all("a")] #解説

for i in soup.find_all("li", class_="pref-name"): #解説
    a_tag = i.contents[1] #<からカウント？　https://qiita.com/kuni007/items/eb490db75548acf611fc aタグで取り出し
    tag_name = a_tag.contents[0] #タグから県名取り出し
    href_get = a_tag.get("href") #タグからURL取り出し
    href_rename = "http://line.userlocal.jp" + href_get 
    Prefectures_dict[tag_name]=href_rename #辞書追加

#データ収集
columns_list = ["県URL", "県名", "アカウントURL", "アカウント名", "友だち数"]
account_url = []
account_name = []
friend_number = []
#アカウントurl アカウント名　取得
find_name_list = []
find_Prefectures_list = []
#県名・URLリスト
prefectures_names = []
prefectures_url = []

for i, j in Prefectures_dict.items():
    get = requests.get(j)
    url_soup = bs(get.text, "html.parser")
    find_name = url_soup.find_all("td", class_="name")
    find_friends = url_soup.find_all("td", class_="friends")
    for k in find_name:
        a_tag = k.contents[1]
        tag_name = (a_tag.contents[0]).replace("\u3000", "") #空白を削除
        href_get = a_tag.get("href")
        account_name.append(tag_name) 
        account_url.append(href_get) 
        prefectures_names.append(i)
        prefectures_url.append(j)

    for l in find_friends:
        friend_number_get = l.contents[0]
        friend_number.append(friend_number_get)

#DataFrame作成
df = pd.DataFrame(columns=columns_list)
#df["URL"] = url
df["県URL"] = prefectures_url
df["県名"] = prefectures_names
df["アカウントURL"] = account_url
df["アカウント名"] = account_name
df["友だち数"] = friend_number

print(df)