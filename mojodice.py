from time import sleep
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup as bs
import gspread
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from oauth2client.service_account import ServiceAccountCredentials
import os
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive.file']
creds = ServiceAccountCredentials.from_json_keyfile_name('automate-mojodice-785ba1611214.json', scope)
client = gspread.authorize(creds)
sheet_api = client.open("Mojodice Data")


chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--diable-deb-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options = chrome_options)


def run_forever():
    driver.get('https://mojodice.com/')
    element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//table"))
    )
    worksheet = sheet_api.worksheet(f"Mojodice data Store Room")
    winlose_list = worksheet.col_values(1)[1:50]
    gametime_list = worksheet.col_values(2)[1:50]
    gameid_list = worksheet.col_values(3)[1:50]
    betamount_list  = worksheet.col_values(4)[1:20]
    
    list_of_lists = worksheet.get_all_values()

    soup = bs(driver.page_source,'html.parser')
    table_rows = soup.find('table').find('tbody').findAll('tr')[1:]

    i = 1
    for row in table_rows[:25]:
        each_row = []
        winlose = row.findAll('td')[0].text.strip()
        gametime = row.findAll('td')[1].text.strip()
        gametime = gametime[:-5] +' '+ gametime[12:]
        gameid = row.findAll('td')[3].text.strip()
        betamount = row.findAll('td')[6].text.strip()
        if gameid in gameid_list:
            pass
        else:
            each_row.append(winlose)
            each_row.append(gametime)
            each_row.append(gameid)
            each_row.append(betamount)
    
        list_of_lists.insert(i,each_row)
        i = i + 1
    data= {}
    lists = []

    for listi in list_of_lists[1:]:
        if len(listi) == 0:
            pass
        else:
            win_lose = listi[0]
            game_time = listi[1]
            game_id = listi[2]
            game_bid = listi[3]
            data = {
                'Win/lose': win_lose,
                'Game Time': game_time,
                'Game ID': game_id,
                'Bid Amount': game_bid
            }
            lists.append(data)
    df = pd.DataFrame(lists).drop_duplicates(subset=['Win/lose','Game ID'], keep='last')
    win = df['Win/lose'].tolist()
    gt = df['Game Time'].tolist()
    gi = df['Game ID'].tolist()
    gb = df['Bid Amount'].tolist()

    new_list_of_lists = []
    for w,gtime,gid,bamount in zip(win,gt,gi,gb):
        each_lit = []
        each_lit.append(w)
        each_lit.append(gtime)
        each_lit.append(gid)
        each_lit.append(bamount)
        new_list_of_lists.append(each_lit)

    
    worksheet.update('A2:D300000', new_list_of_lists)

while True:
    run_forever()
    sleep(20)