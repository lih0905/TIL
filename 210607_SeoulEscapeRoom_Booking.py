"""
서울이스케이프룸 강남 1호점의 7월말까지 예약 목록을 스크레이핑하는 코드
페이지가 특정 날짜를 선택하면 자동으로 리스트가 로딩되는 형태로 되어 있어 팬텀js를 이용하여 스크레이핑함
목표는 '유럽횡단 야간열차'와 '화성탐사선의 임무' 예약 취소된 내역을 찾는 것!
"""

import urllib.request as req
import time
import datetime
import warnings
warnings.filterwarnings('ignore')

from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd


class Scraper:
    def __init__(self, url='https://www.seoul-escape.com/reservation/'):
        self.url = url
        self.driver = webdriver.PhantomJS('/workspace/test/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        self.source_today = BeautifulSoup(self.driver.page_source, 'html.parser')

    def get_available_days(self, source):
        """
        이번 달에 예약가능한 날짜를 리스트로 반환
        """
        self.driver.find_element_by_css_selector('input#reserve_date').click()
        bs = BeautifulSoup(self.driver.page_source, 'html.parser')
        days = bs.select('div.datepicker-days td')
        after_days = [t.text for t in days if t['class'] == ['day']]
        return after_days
    
    def get_source_of_desired_day(self, day):
        """
        선택된 날짜의 페이지 소스 코드를 BeautifulSoup으로 파싱한 결과를 반환
        """
        self.driver.find_element_by_css_selector('input#reserve_date').click()
        self.driver.implicitly_wait(1) # seconds
        # 달력에 이전달/다음달의 날짜로 인해 두번 떠있는 날짜들은 이번달의 날짜만 가져옴
        if int(day) <= 15:
            self.driver.find_element_by_css_selector('div.datepicker-days > table.table-condensed').find_elements_by_xpath(f'//td[text()="{day}"]')[0].click()
        else:
            self.driver.find_element_by_css_selector('div.datepicker-days > table.table-condensed').find_elements_by_xpath(f'//td[text()="{day}"]')[-1].click()
        self.driver.implicitly_wait(5) # seconds
        return BeautifulSoup(self.driver.page_source, 'html.parser')        
        
    def scrape_book_list(self, source):
        """
        페이지 소스 코드를 입력으로 받아서 예약 목록을 다음과 같은 형태로 반환
        ['일시', '시작시간', '소요시간', '제목', '예약가능인원', '예약상태'] 
        """
        # 소스 코드에서 날짜 확인
        year, month, day = map(int, source.select_one('input#reserve_date')['placeholder'].split("/"))
        date = datetime.date(year, month, day).strftime('%Y-%m-%d')

        book_list = []
        for table in source.select('tr.ng-scope'):
            table_list = table.select('td.ng-binding')
            book_status = table_list[-1].text.strip()
            book_list.append((date, table_list[1].text.strip(), table_list[2].text.strip(), \
                              table_list[3].text.strip(), table_list[4].text.strip(), \
                              book_status))
        return book_list
    
    def scrape(self):
        """
        스크레이핑 수행하는 메인 함수
        결과는 Pandas Dataframe으로 반환
        """
        result = list()
        result += self.scrape_book_list(self.source_today)
        
        available_days_this_month = self.get_available_days(self.source_today)
        for day in available_days_this_month:
            source = self.get_source_of_desired_day(day)
            result += self.scrape_book_list(source)
        
        month = list(map(int, source.select_one('input#reserve_date')['placeholder'].split("/")))[1]
        if month == 6: # 6월이면 7월도 추가로 스크랩
            # 다음달로 변경
            self.driver.find_element_by_css_selector('input#reserve_date').click()
            self.driver.implicitly_wait(1) # seconds
            self.driver.find_element_by_css_selector('div.datepicker-days > table.table-condensed').find_elements_by_xpath('//td[text()="1"]')[-1].click()
            self.driver.implicitly_wait(5) # seconds
            
            source = BeautifulSoup(self.driver.page_source, 'html.parser')    
            # 7월 스크랩
            for day in range(1, 32):
                source = self.get_source_of_desired_day(day)
                result += self.scrape_book_list(source)
        
        columns = ['일시', '시작시간', '소요시간', '제목', '예약가능인원', '예약상태']
        df = pd.DataFrame(result, columns=columns)
        return df
    
    def show_available_list(self, df, title):
        return df[(df['제목']==title) & (df['예약상태']!='예약완료')]
    
if __name__ == '__main__':
    print("스크레이핑을 시작합니다.")
    scraper = Scraper()
    result = scraper.scrape()
    print("스크레이핑이 완료되었습니다.")
    print(result.head())
    result.to_csv('Data/Escape.csv', index=False)
    
    for title in ['유럽횡단 야간열차', '화성탐사선의 임무', '죽음을 부르는 재즈바']:
        if len(result[result['제목']==title]['예약상태'].unique()) > 1:
            print(f"{title} 열림!")
            print(result[(result['제목']==title) & (result['예약상태']!='예약완료')])
        else:
            print(f"{title}는 모두 예약 완료입니다.")
        
    