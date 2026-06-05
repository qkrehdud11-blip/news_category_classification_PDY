from bs4 import BeautifulSoup       # HTML 문서 파싱용 라이브러리
import requests                     # 웹 페이지 요청
import re                           # 정규표현식 사용
import pandas as pd                 # 데이터프레임 생성 및 저장
import datetime                     # 날짜 및 시간 처리

# 뉴스 카테고리 목록
category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']
# 전체 기사 제목 저장용 데이터프레임
df_titles = pd.DataFrame()

# 카테고리별 뉴스 수집
for i in range(6):
    # 카테고리별 네이버 뉴스 URL 생성
    url = 'https://news.naver.com/section/10{}'.format(i)
    # 웹 페이지 요청
    resp = requests.get(url)
    # HTML 파싱
    soup = BeautifulSoup(resp.text, 'html.parser')
    # 기사 제목 태그 추출
    title_tag = soup.select('.sa_text_strong')
    # 추출된 태그 확인
    print(title_tag)
    # 제목 저장 리스트
    titles = []
    # 기사 제목 추출
    for title in title_tag:
        titles.append(title.text)
    # 추출 결과 확인
    print(titles)
    # 제목 데이터프레임 생성
    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    # 카테고리 컬럼 추가
    df_section_titles['category'] = category[i]
    # 전체 데이터프레임에 추가
    df_titles = pd.concat([df_titles, df_section_titles], ignore_index=True)

# 상위 데이터 확인
print(df_titles.head())
# 데이터 정보 확인
df_titles.info()
# 현재 날짜를 파일명에 추가하여 CSV 저장
df_titles.to_csv('./data/naver_headline_news_{}.csv'.format(
                datetime.datetime.now().strftime('%Y%m%d')), index=False)