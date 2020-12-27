#將特定網站的表格寫為csv且不會開啟為亂碼
#cmd直接執行版


import csv,codecs
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.request import HTTPError
import datetime # 需要轉換時間格式以例計算
import time #邊戳邊休息 time.sleep(秒數)
from datetime import timedelta  # 需要timedelta模組，用以加減日期
import os # 需要新增檔案路徑的資料夾 (os.path.join)
import requests  # 需要爬取網頁

def crawler_form():
    try:
        html = urlopen(url)
    except HTTPError as e:
        print("not found")
    bsObj = BeautifulSoup(html,"html.parser")
    table = bsObj.findAll("table",{"id":"MyTable"})[0]
    if table is None:
        print("no table");
        exit(1)

    rows = table.findAll("tr")
    csvFile = open(fullfilename,'wt',newline='',encoding='utf-8-sig')
    writer = csv.writer(csvFile)

    try:
        for row in rows:
            csvRow = []
            for cell in row.findAll(['td','th']):
                csvRow.append(cell.get_text())
            writer.writerow(csvRow)
    finally:
        csvFile.close()

start=datetime.datetime(2020,8,31) #這是起始日期的前一天
path = 'C:\\Users\\USER\\Desktop\\testpy\\ccClub\\Mid-Project\\csv_test'


count = 1
for i in range(61):
    next_day = start + timedelta(count) 
    only_date = next_day.date()
    only_year = only_date.year
    only_month = only_date.month
    YYYY_mm = str(only_year) + '_' + str(only_month)
    if not os.path.exists(os.path.join(path, YYYY_mm)):
        os.makedirs(os.path.join(path, YYYY_mm))
        
    mypath = str(path) + '\\' + str(YYYY_mm)
    url = 'https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=466920&stname=%25E8%2587%25BA%25E5%258C%2597&datepicker=' + str(only_date)
    filename = '466920-' + str(only_date) + '.csv'
    print('正在輸出第['+ str(count) + ']個成果：' +  str(only_date))
    fullfilename = os.path.join(mypath, filename)
    crawler_form()
    
    print( '檔案' + str(filename) + '已輸出至路徑[' + mypath + ']!')
    count += 1
    time.sleep(6)
    
print('所有成果輸出完成')
os.system("pause")