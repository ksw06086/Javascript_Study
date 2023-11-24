import sys, os
import urllib3
import pprint

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from common import *
from openpyxl import load_workbook
import pandas as pd

urllib3.disable_warnings()

FULL_PAGE = len(sys.argv)==2 and sys.argv[1]=='full'

load_wb = load_workbook(r"C:\이미지 저작권 침해_채증_231121.xlsx")
load_ws = load_wb['1차']
data = load_ws.values
columns = next(data)[0:]
f = pd.DataFrame(data, columns=columns)

driver = chrome_driver()

data_list = []

def get_datas():
    datas = []
    for i, url in enumerate(f['URL']):
        # print(f"{i} {url} {number}")
        datas.append(url)
    return datas

def start_crawling(link):
    if('naver' in link):
        soup = requests_bs(link.replace('//blog', '//m.blog'))
        a = soup.select_one('p.se_date')
        if(a != None):
            data_list.append(a.get_text().strip())
            print(a.get_text().strip())

print("blog 크롤링 시작")
#* dh: 드라마
for data in get_datas():
    start_crawling(data)
print("blog 크롤링 끝")
