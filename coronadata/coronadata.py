from asyncore import read
import json
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request as req
import os.path
import urllib
#URLからjsonをダウンロード
url = "https://opendata.corona.go.jp/api/Covid19JapanAll"
savename = "D:\python project\portforio\coronadata\coronadata.json"



#存在しない場合jsonを保存
if not os.path.exists(savename):
    req.urlretrieve(url, 'D:\python project\portforio\coronadata.json')

#jsonファイルをエンコードして読み込み
encoding_coronadata = open(savename, 'r', encoding="utf-8")
read_coronadata = json.load(encoding_coronadata)



#jsonファイルを整形してカラム名を変更しcsvで保存
parse_coronadata = pd.json_normalize(read_coronadata, record_path="itemList")
rename_coronadata = parse_coronadata.rename(columns={"date": "日付", "name_jp": "県名", "npatients": "入院患者数"})
rename_coronadata.to_csv(r"D:\python project\portforio\coronadata\rename_coronadata.csv", index=False)