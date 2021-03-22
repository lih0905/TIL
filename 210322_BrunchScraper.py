"""
태그 생성 모델을 위해 브런치 데이터를 스크레이핑하는 함수 작성
매일의 추천 포스트와 키워드별 신규 포스트를 스크레이핑한다.
"""

import datetime as dt
import re 
import json

from bs4 import BeautifulSoup
import requests
import pandas as pd

# 스크레이퍼 함수 정의
def brunch_scraper(url: str, kind: str, date: str) -> dict:
    text = requests.get(url)
    soup = BeautifulSoup(text.content, 'html.parser')
    scraped = dict()
    
    texts = [h4.get_text().replace('\xa0',' ') for h4 in soup.find_all('h4')]
    texts = '\n'.join(texts)
    
    if texts == '':
        texts = []
        for p in soup.find_all('p'):
            try:
                if p['class'] == ['wrap_item', 'item_type_text']:
                    texts.append(p.text.replace('\xa0',' '))
            except:
                pass
        texts = '\n'.join(texts)
    
    scraped['date'] = date
    scraped['link'] = url
    scraped['kind'] = kind
    scraped['title'] = soup.find_all('tiara-page')[0]['data-tiara-name']
    scraped['text'] = texts
    scraped['tag'] = soup.find_all('tiara-page')[0]['data-tiara-tags']
    
    return scraped

if __name__ == '__main__':
    
    date = dt.date.today().strftime('%Y%m%d')
    
    # 추천글 스크레이핑
    url = 'https://brunch.co.kr/'
    text = requests.get(url)
    soup = BeautifulSoup(text.content, 'html.parser')

    recommended_links = []
    for link in soup.find_all('a'):
        try:
            if link['data-tiara-layer'] == "recommended_article":
                if link['href'].startswith('/@@'):
                    recommended_links.append(f"https://brunch.co.kr{link['href']}")
        except:
            pass
    
    recommended_texts = [brunch_scraper(url, kind='recommended', date=date) for url in recommended_links]
    
    # 키워드별 스크레이핑
    keywords = ['지구한바퀴_세계여행', '그림·웹툰', '시사·이슈', 'IT_트렌드', '사진·촬영',
                '취향저격_영화_리뷰', '오늘은_이런_책', '뮤직_인사이드', '글쓰기_코치', '직장인_현실_조언',
                '스타트업_경험담', '육아_이야기', '요리·레시피', '건강·운동', '멘탈_관리_심리_탐구',
                '디자인_스토리', '문화·예술', '건축·설계', '인문학·철학', '쉽게_읽는_역사',
                '우리집_반려동물', '멋진_캘리그래피', '사랑·이별', '감성_에세이']
    
    article_texts = []
    for keyword in keywords:exi
        keyword_url = f'https://brunch.co.kr/keyword/{keyword}?q=g'
        text = requests.get(keyword_url)
        
        # 정규식으로 글쓴이ID와 글번호를 따옴
        article_list = list(set(re.findall('userId":"([\w+]+)","articleNo":([\w+]+)', text.text)))
        article_urls = [f'https://brunch.co.kr/@@{article[0]}/{article[1]}' for article in article_list]
        
        article_texts += [brunch_scraper(url, kind=keyword, date=date) for url in article_urls]
    
    result_texts = recommended_texts + article_texts
    print(f"오늘의 스크랩 수는 {len(result_texts)}개입니다.")
    
    filename = f"Brunch/Articles_{date}.json"
    with open(filename, 'w') as f:
        json.dump(result_texts, f)
    print(f"오늘의 스크랩이 완료되었습니다. 파일은 {filename}으로 저장하였습니다.")