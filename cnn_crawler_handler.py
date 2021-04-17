import os
import lxml
import requests as r
import datetime as d
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from multiprocessing import Process

class CNNcrawler:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

    def set_driver(self, driver_path):
        '''chrome driver setting'''
        driver = webdriver.Chrome(driver_path)
        return driver

    def save_data(self, q, href_list, title_list, date_list, content_list):
        '''data 저장'''
        pd.DataFrame({
            'href' : href_list,
            'title' : title_list,
            'date' : date_list,
            'content' : content_list
        }).to_csv(self.base_dir + f'/data/{q}.csv', index=False)

    def crawling(self, q):
        '''crawler main
        query(search 키워드)에 따라서 muliprocess로 돌면서 data collect and save
        '''
        href_list, title_list, date_list, content_list = [], [], [], []
        flag_is_first = True
        driver_path = self.base_dir + '/driver/chromedriver'
        driver = self.set_driver(driver_path)
        url = f"https://edition.cnn.com/search/?size=10&q={q}&page="
        # 아래 range를 변형해서 더 많은 데이터를 수집할 수 있음
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
        self.save_data(q, href_list, title_list, date_list, content_list)
        # end of driver
        driver.close()

    def start(self, search_list):
        jobs = []
        for query in search_list:
            proc = Process(target=self.crawling, args=(query, ))
            jobs.append(proc)
            proc.start()
        # 모든 multi가 돌아갈 때까지 기다릴 수 있도록 join
        for p in jobs:
            p.join()
