from selenium import webdriver
from datetime import datetime
from bs4 import BeautifulSoup
import csv, os, time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
import pandas as pd


def write_summary(data):
    file_exists = os.path.isfile("result/summary.csv")
    with open("result/summary.csv", 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=',')
        if not file_exists:
            writer.writerow(('Date', 'Home team', 'Away team', 'Home Score', 'Away Score'))
        writer.writerow((data['Date'], data['Home_team'], data['Away_team'], data['Home_Score'], data['Away_Score']))   

def write_result(data):
    file_exists = os.path.isfile("result/result.csv")
    with open("result/result.csv", 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=',')
        if not file_exists:
            writer.writerow(('Date', 'Home team', 'Away team', 'Home Score', 'Away Score'))
        writer.writerow((data['Date'], data['Home_team'], data['Away_team'], data['Home_Score'], data['Away_Score']))   

def write_fixtures(data):
    file_exists = os.path.isfile("result/fixtures.csv")
    with open("result/fixtures.csv", 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=',')
        if not file_exists:
            writer.writerow(('Date', 'Home team', 'Away team'))
        writer.writerow((data['Date'], data['Home_team'], data['Away_team']))   

def write_standings(data):
    file_exists = os.path.isfile("result/standings.csv")
    with open("result/standings.csv", 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=',')
        if not file_exists:
            writer.writerow(('#', 'TEAM', 'MP', 'W', 'D', 'L', 'G', 'Pts'))
        writer.writerow((data['rank'], data['TEAM'], data['MP'], data['W'], data['D'], data['L'], data['G'], data['Pts']))  

def write_teams(data):
    file_exists = os.path.isfile("result/teams.csv")
    with open("result/teams.csv", 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=',')
        if not file_exists:
            writer.writerow(('TEAM', 'URL'))
        writer.writerow((data['TEAM'], data['url']))  

def write_archive(data):
    file_exists = os.path.isfile("result/archive.csv")
    with open("result/archive.csv", 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=',')
        if not file_exists:
            writer.writerow(('Season', 'Winner'))
        writer.writerow((data['Season'], data['Winner']))                                                                            

def read_txt():
    with open('input.txt', 'r', encoding='utf-8-sig') as f:
        return f.readlines()

def main():
    folder_exists = os.path.isdir("result")
    if not folder_exists:
        os.makedirs('result')
    list = read_txt()
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images":2}
    chromeOptions.add_experimental_option("prefs",prefs)
    browser = webdriver.Chrome(chrome_options=chromeOptions,executable_path="chromedriver")
    wait = ui.WebDriverWait(browser,60)
    i=0
    while i < len(list):
        browser.get(list[i].strip())
        wait.until(lambda browser: browser.find_element_by_css_selector('body div'))
        soup = BeautifulSoup(browser.page_source, "lxml")
        events = soup.find_all('div', class_='event__match')
        for event in events:
            try:
                Date = event.find('div', class_='event__time').text.strip()
            except:
                Date = event.find('div', class_='event__stage').text.strip()
            Home_team = event.find('div', class_='event__participant--home').text.strip()
            Away_team = event.find('div', class_='event__participant--away').text.strip()
            try:
                event__scores = event.find('div', class_='event__scores').text.strip()
                Home_Score = event__scores.split('-')[0].strip()
                Away_Score = event__scores.split('-')[1].strip()
            except:
                Home_Score = ""
                Away_Score = ""
            data = {
                'Date': Date,
                'Home_team': Home_team,
                'Away_team': Away_team,
                'Home_Score': Home_Score,
                'Away_Score': Away_Score,
            }
            write_summary(data)
        browser.get(list[i].strip()+"results/")
        wait.until(lambda browser: browser.find_element_by_css_selector('body div'))
        soup = BeautifulSoup(browser.page_source, "lxml")
        events = soup.find_all('div', class_='event__match')
        for event in events:
            Date = event.find('div', class_='event__time').text.strip()
            Home_team = event.find('div', class_='event__participant--home').text.strip()
            Away_team = event.find('div', class_='event__participant--away').text.strip()
            event__scores = event.find('div', class_='event__scores').text.strip()
            Home_Score = event__scores.split('-')[0].strip()
            Away_Score = event__scores.split('-')[1].strip()
            data = {
                'Date': Date,
                'Home_team': Home_team,
                'Away_team': Away_team,
                'Home_Score': Home_Score,
                'Away_Score': Away_Score,
            }
            write_result(data)
        browser.get(list[i].strip()+"fixtures/")
        wait.until(lambda browser: browser.find_element_by_css_selector('body div'))
        soup = BeautifulSoup(browser.page_source, "lxml")
        events = soup.find_all('div', class_='event__match')
        for event in events:
            Date = event.find('div', class_='event__time').text.strip()
            Home_team = event.find('div', class_='event__participant--home').text.strip()
            Away_team = event.find('div', class_='event__participant--away').text.strip()
            data = {
                'Date': Date,
                'Home_team': Home_team,
                'Away_team': Away_team,
            }
            write_fixtures(data)
        browser.get(list[i].strip()+"standings/")
        wait.until(lambda browser: browser.find_element_by_css_selector('body div.table__row'))
        soup = BeautifulSoup(browser.page_source, "lxml")
        events = soup.find_all('div', class_='table__row')
        for event in events:
            rank = event.find('div', class_='table__cell--rank').text.replace('.','').strip()
            TEAM = event.find('div', class_='table__cell--participant_name').find('span', class_='team_name_span').text.strip()
            MP = event.find('div', class_='table__cell--matches_played').text.strip()
            W = event.find('div', class_='table__cell--wins_regular').text.strip()
            D = event.find('div', class_='table__cell--draws').text.strip()
            L = event.find('div', class_='table__cell--losses_regular').text.strip()
            G = event.find('div', class_='table__cell--goals').text.strip()
            Pts = event.find('div', class_='table__cell--points').text.strip()
            data = {
                'rank': rank,
                'TEAM': TEAM,
                'MP': MP,
                'W': W,
                'D': D,
                'L': L,
                'G': G,
                'Pts': Pts,
            }
            write_standings(data)
        browser.get(list[i].strip()+"teams/")
        wait.until(lambda browser: browser.find_element_by_css_selector('body div#tournament-page-participants'))
        soup = BeautifulSoup(browser.page_source, "lxml")
        events = soup.find('div', id='tournament-page-participants').find_all('a', class_='leagueTable__team')
        for event in events:
            TEAM = event.text.strip()
            URL = "https://www.flashscore.com.au" + event.get('href')
            data = {
                'TEAM': TEAM,
                'url': URL,
            }
            write_teams(data)
        browser.get(list[i].strip()+"archive/")
        wait.until(lambda browser: browser.find_element_by_css_selector('body div#tournament-page-archiv'))
        soup = BeautifulSoup(browser.page_source, "lxml")
        events = soup.find('div', id='tournament-page-archiv').find_all('div', class_='profileTable__row--background')
        for event in events:
            Season = event.find('div', class_='leagueTable__seasonName').text.strip()
            try:
                Winner = event.find('div', class_='leagueTable__winner').text.strip()
            except:
                Winner = ""
            data = {
                'Season': Season,
                'Winner': Winner,
            }
            write_archive(data)      
        i+=1
    df1 = pd.read_csv ('result/summary.csv')   
    df2 = pd.read_csv ('result/result.csv')   
    df3 = pd.read_csv ('result/fixtures.csv')   
    df4 = pd.read_csv ('result/standings.csv')   
    df5 = pd.read_csv ('result/teams.csv')   
    df6 = pd.read_csv ('result/archive.csv')   
    writer = pd.ExcelWriter("result/" + 'all.xlsx', engine='xlsxwriter')
    # writer = pd.ExcelWriter("result/"+soup.find('div', class_='teamHeader__name').text.strip() +'.xlsx', engine='xlsxwriter')
    df1.to_excel(writer, sheet_name='Summary', index=False)
    df2.to_excel(writer, sheet_name='Results', index=False)
    df3.to_excel(writer, sheet_name='Fixtures', index=False)
    df4.to_excel(writer, sheet_name='Standings', index=False)
    df5.to_excel(writer, sheet_name='Teams', index=False)
    df6.to_excel(writer, sheet_name='Archive', index=False)
    writer.save() 
    os.remove('result/summary.csv')          
    os.remove('result/result.csv')          
    os.remove('result/fixtures.csv')          
    os.remove('result/standings.csv')          
    os.remove('result/teams.csv')          
    os.remove('result/archive.csv')    


    browser.quit()

if __name__ == '__main__':
    main()
