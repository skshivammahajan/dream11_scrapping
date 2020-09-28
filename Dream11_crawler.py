import pickle
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

chrome=webdriver.Chrome(r"C:\Users\akanksha\Downloads\chromedriver_win32\\chromedriver.exe")

##chrome.get("https://www.dream11.com")
##try:
##    WebDriverWait(chrome, 100).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='matchCardMainTitle_7b586 matchCardMainTitleDesktop_83a22']")))
##finally:
##    pass
##
##pickle.dump(chrome.get_cookies(), open("cookie.txt","wb"))

team_list=[]
player_list=[]

cookies=pickle.load(open("cookie.txt","rb"))
chrome.get("https://www.dream11.com/login")
for cookie in cookies:
    chrome.add_cookie(cookie)

chrome.get('https://www.dream11.com/cricket/leaderboard/ipl/1027/14085/309112306')# URL of leaderboard of your chosen contest goes here..

# https://www.dream11.com/cricket/leaderboard/ipl/1027/14085/309112306?compare=false
# https://www.dream11.com/cricket/leaderboard/Dream11%20IPL/1551/22396/1517261029
res=chrome.execute_script("return document.documentElement.outerHTML")
page=bs(res,'lxml')
time.sleep(2)
# teams=page.findAll('div', attrs={'class':'leaderboard__players__user-information'})
teams=chrome.find_elements_by_xpath("//div[@class='playerUserName_1ac16']")
for team in teams:
    team_list.append(team.text)

# print(len(team_list[1:]))


time.sleep(2)
els=chrome.find_elements_by_xpath("//div[@class='js--leaderboard__players-container defaultUserRow_4d390 leaderboardPlayerContainer_4da24']")
for el in els:
    el.click()
    time.sleep(2)
    # players=chrome.find_elements_by_xpath("//div[@class='fieldPlayerTitle_75d21 awayTeamPlayerTitle_95944' or @class='fieldPlayerTitle_75d21 homeTeamPlayerTitle_c0c14']")
    players=chrome.find_elements_by_xpath("//div[@class='playerPoints_d4e06']")
    for player in players:
        player_list.append(player.text)


data=pd.DataFrame(zip(team_list, player_list[0::11] ,player_list[1::11],player_list[2::11],player_list[3::11],player_list[4::11],
                      player_list[5::11],player_list[6::11],player_list[7::11],player_list[8::11],player_list[9::11],player_list[10::11]),
                  columns=["TEAM","Pl-1","Pl-2","Pl-3","Pl-4","Pl-5","Pl-6","Pl-7","Pl-8","Pl-9","Pl-10","Pl-11"])
# import pdb;pdb.set_trace()

data.to_excel("DREAM11_Points.xlsx", index=False)
