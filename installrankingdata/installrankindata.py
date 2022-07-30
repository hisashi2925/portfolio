from asyncore import read
from gettext import find
import json
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


columns_list = ["URL", "県URL", "県名", "アカウントURL", "アカウント名", "友だち数"]
account_url = {}
account_name = {}
friend_number = {}


#アカウントurl アカウント名　取得


find_name_list = []
find_Prefectures_list = []
for i in Prefectures_dict.values():
    
    
    get = requests.get(i)
    url_soup = bs(get.text, "html.parser")
    find_name = url_soup.find_all("td", class_="name")
    find_Prefectures = url_soup.find_all(class_="page-nav") ###ページの県名を取得してif?
    for i in find_Prefectures:
        a_tag = (i.contents[2]).replace(">", "")
        b_tag = a_tag.strip()
        find_Prefectures_list.append(b_tag)
     
    for i in find_name:
        a_tag = i.contents[1]
        tag_name = (a_tag.contents[0]).replace("\u3000", "") #空白を削除
        href_get = a_tag.get("href")

        account_name.append(tag_name) 
        account_url.append(href_get) 
    
#友だち数 取得

for i in Prefectures_dict.values():
    
    
    get = requests.get(i)
    url_soup = bs(get.text, "html.parser")
    find_friends = url_soup.find_all("td", class_="friends")
    

    for i in find_friends:
        friend_number_get = i.contents[0]
        friend_number.append(friend_number_get)

#DataFrame作成

df = pd.DataFrame(columns=columns_list)
df["URL"] = url
df["県URL"] = Prefectures_dict.values()
df["県名"] = Prefectures_dict.keys()
df["アカウントURL"] = account_url
df["アカウント名"] = account_name
df["友だち数"] = friend_number

print(df)