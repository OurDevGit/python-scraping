from selenium import webdriver
from datetime import datetime
from bs4 import BeautifulSoup
import csv, os, time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
import pandas as pd


def write_result(data):
    file_exists = os.path.isfile("output/result.csv")
    with open("output/result.csv", 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=',')
        if not file_exists:
            writer.writerow(('Date', 'Home team', 'Away team', 'Home Score', 'Away Score'))
        writer.writerow((data['Date'], data['Home_team'], data['Away_team'], data['Home_Score'], data['Away_Score']))   

def write_fixtures(data):
    file_exists = os.path.isfile("output/fixtures.csv")
    with open("output/fixtures.csv", 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=',')
        if not file_exists:
            writer.writerow(('Date', 'Home team', 'Away team'))
        writer.writerow((data['Date'], data['Home_team'], data['Away_team']))   

def write_standings(data):
    file_exists = os.path.isfile("output/standings.csv")
    with open("output/standings.csv", 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=',')
        if not file_exists:
            writer.writerow(('#', 'TEAM', 'MP', 'W', 'D', 'L', 'G', 'Pts'))
        writer.writerow((data['rank'], data['TEAM'], data['MP'], data['W'], data['D'], data['L'], data['G'], data['Pts']))                                                                            

def read_txt():
    with open('input.txt', 'r', encoding='utf-8-sig') as f:
        return f.readlines()

def main():
    list = read_txt()
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images":2}
    chromeOptions.add_experimental_option("prefs",prefs)
    chromeOptions.add_argument("--headless")
    browser = webdriver.Chrome(chrome_options=chromeOptions,executable_path="chromedriver")
    wait = ui.WebDriverWait(browser,60)
    i=0
    while i < len(list):
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
              # TEAM    MP  W   D   L   G   Pts
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
 //       df1 = pd.read_csv ('out/result.csv')   
 //       df2 = pd.read_csv ('out/fixtures.csv')   
 //       df3 = pd.read_csv ('out/standings.csv')   
        df1 = pd.read_csv ('output/result.csv')   
        df2 = pd.read_csv ('output/fixtures.csv')   
        df3 = pd.read_csv ('output/standings.csv') 
        writer = pd.ExcelWriter('output/' + soup.find('div', class_='teamHeader__name').text.strip() +'.xlsx', engine='xlsxwriter')
        df1.to_excel(writer, sheet_name='Results', index=False)
        df2.to_excel(writer, sheet_name='Fixtures', index=False)
        df3.to_excel(writer, sheet_name='Standings', index=False)
        writer.save() 
        os.remove('output/result.csv')          
        os.remove('output/fixtures.csv')          
        os.remove('output/standings.csv')          
        i+=1


    browser.quit()

if __name__ == '__main__':
    main()
