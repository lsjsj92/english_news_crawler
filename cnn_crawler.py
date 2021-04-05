import os
import lxml
import requests as r
import datetime as d
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from multiprocessing import Process

base_dir = os.path.dirname(os.path.abspath(__file__))

def set_driver(driver_path):
    '''chrome driver setting'''
    driver = webdriver.Chrome(driver_path)
    return driver

def save_data(q, href_list, title_list, date_list, content_list):
    '''data 저장'''
    pd.DataFrame({
        'href' : href_list,
        'title' : title_list,
        'date' : date_list,
        'content' : content_list
    }).to_csv(base_dir + f'/data/{q}.csv', index=False)

def crawling(q):
    '''crawler main
    query(search 키워드)에 따라서 muliprocess로 돌면서 data collect and save
    '''
    href_list, title_list, date_list, content_list = [], [], [], []
    flag_is_first = True
    driver_path = base_dir + '/driver/chromedriver'
    driver = set_driver(driver_path)
    url = f"https://edition.cnn.com/search/?size=10&q={q}&page="
    for i in range(1, 3):
        # 처음일 때와 아닐 때 url 값이 바뀌어서 flag를 이용해 변환
        if flag_is_first == True:
            url = url + str(i)
            flag_is_first = False
        else:
            # 첫 페이지가 아닐 때는 뒤에 &from=10이 붙음
            url = url + str(i) + "&from=10"
        driver.get(url)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        div_list = soup.findAll("div", {"class":"cnn-search__result-contents"})
        for d in div_list:
            try:
                # 제목, 링크, 콘텐츠, 날짜 값 저장
                href = d.find("h3", {"class":"cnn-search__result-headline"}).find('a').attrs['href']
                title = d.find("h3", {"class":"cnn-search__result-headline"}).find('a').text.strip()
                date = d.find("div", {"class" : "cnn-search__result-publish-date"}).findAll('span')[1].text.strip()
                content = d.find("div", {"class":"cnn-search__result-body"}).text.strip()
                href_list.append(href)
                title_list.append(title)
                date_list.append(date)
                content_list.append(content)
            except:
                continue
        url = url[:-1]
        # 약간의 시간차를 둠
        time.sleep(2)
    save_data(q, href_list, title_list, date_list, content_list)
    # end of driver
    driver.close()

def start(search_list):
    jobs = []
    for query in search_list:
        proc = Process(target=crawling, args=(query, ))
        jobs.append(proc)
        proc.start()
    # 모든 multi가 돌아갈 때까지 기다릴 수 있도록 join
    for p in jobs:
        p.join()

if __name__ == "__main__":
    search_list = []
    with open(base_dir + '/data/search_list.txt', 'r') as f:
        for line in f:
            search_list.append(line.rstrip('\n'))
    start(search_list)
    
    # 개선사항
        # 1. .env나 argument로 파라미터 받을 수 있도록 변경할 수도 있음
        # 2. class 객체화?
        # 3. input 개수가 만약 4개 이상이면, 4개씩 쪼개서 프로세스 돌리도록 -> 지금은 내가 원하는 것만 받아서 4개뿐임

