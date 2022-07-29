from unittest import result
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup as bs
import pprint
import re #文字列のパターンで検索できる
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import difflib
import matplotlib.pyplot as plt
import datetime
import numpy as np
import schedule
from matplotlib import animation
from time import sleep

def rate_graph():
    url = "https://jp.investing.com/rates-bonds/world-government-bonds"

    dt_now = datetime.datetime.now() 
    r = requests.get(url)
    time.sleep(1)

    soup = bs(r.text, "html.parser")


    Country_10years_dict_result_now = {
        "Canada": 0,
        "America": 0,
        "Australia": 0,
        "New Zealand": 0,
        "Germany": 0,
        "France": 0,
        "England": 0,
        "Turkey": 0,
        "Japan": 0,
    }
    Country_10years_dict_result_1hourago = {
        "Canada": 0,
        "America": 0,
        "Australia": 0,
        "New Zealand": 0,
        "Germany": 0,
        "France": 0,
        "England": 0,
        "Turkey": 0,
        "Japan": 0,
    }
    Country_10years_dict_difference ={
        "Canada": 0,
        "America": 0,
        "Australia": 0,
        "New Zealand": 0,
        "Germany": 0,
        "France": 0,
        "England": 0,
        "Turkey": 0,
        "Japan": 0,
    }

    Country_10years_dict = {   #redBgが更新時？
        "Canada" :"pid-25275-last",
        "America": "pid-23705-last",
        "Australia": "pid-23878-last",
        "New Zealand": "pid-42410-last",
        "Germany": "pid-23693-last",
        "France": "pid-23778-last",
        "England": "pid-23673-last",
        "Turkey":  "pid-24037-last",
        "Japan":  "pid-23901-last",
    }

    Country_10years_dict_rate = {}




    print("rate_graph")
    # 10年のタグの中身を辞書化
    for key_a, value_a in Country_10years_dict.items():
        f = soup.find("td", class_=value_a)
        d = f.contents[0] #タグの中身のみ表示
        Country_10years_dict_result_now[key_a]=d
        #一時間前の値と現在の値の差分を計算して辞書化
        for difference in (Country_10years_dict_result_1hourago.keys() | Country_10years_dict_result_now.keys()):

            num_1 = float(Country_10years_dict_result_1hourago.get(difference))
            num_2 = float(Country_10years_dict_result_now.get(difference))
        
            total = num_2 - num_1
            Country_10years_dict_difference[difference]=total
    #それぞれの国と日本の差分を計算して辞書化
    for key_a, value_a in Country_10years_dict_difference.items():
        
        num_1 = float(Country_10years_dict_difference.get(key_a))
        num_2 = float(Country_10years_dict_difference.get("Japan"))
        result_a = num_1 - num_2
        if result_a == 0:
            pass
        else:
            Country_10years_dict_rate[key_a]=(round(result_a, 7))
    print(Country_10years_dict_rate)
    #Country_10years_dict_rateをグラフに


    fig, ax = plt.subplots()
    xs = []
    ys = []

    for i, d in Country_10years_dict_rate.items():
        

        xs.append(i)
        ys.append(d)
    
        
        ax.set_xlim(-1, 10)
        ax.set_ylim(-10, 30)
        ax.plot(xs, ys)
        
        plt.text(i, d, d) 
        plt.title('RATE')
        dt_now = datetime.datetime.now()  
        dirname = r"D:\python project\portforio\interest rate comparison\graf_image"
        filename = dirname + dt_now.strftime('%Y%m%d_%H%M%S') + '.png'
        plt.savefig(filename)


schedule.every(10).seconds.do(rate_graph) 


while True:
    schedule.run_pending()
    time.sleep(1)











 