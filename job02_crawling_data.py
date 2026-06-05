# 파일명은 naver_news_section.csv
# 컬럼명은 titles, category로 해주세요!
# 영재님이 정치, 경제
# 유정님이 사회, 문화
# 도영님이 세계, IT
# 다 되면 PR 부탁드립니다!!!


import pandas as pd                                                     # 데이터프레임 처리
from selenium import webdriver                                          # 웹 브라우저 제어
from selenium.webdriver.common.by import By                             # 요소 탐색
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import time                                                             # 대기 시간 설정

# 뉴스 카테고리 목록
category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']
# 전체 기사 저장용 데이터프레임
df_titles = pd.DataFrame()

# 크롬 옵션 설정
options = ChromeOptions()
options.add_argument('lang=ko_KR')
# 브라우저 창 숨김
options.add_argument('headless')

# 크롬 드라이버 실행
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# 더보기 버튼 XPath
button_xpath = '//*[@id="newsct"]/div[4]/div/div[2]/a'

# 도영 담당: World(104), IT(105)
for SECTION, CATEGORY in zip(range(4, 6), category[4:6]):
    # 카테고리 페이지 접속
    url = 'https://news.naver.com/section/10{}'.format(SECTION)
    driver.get(url)

    # 더보기 버튼 반복 클릭
    for i in range(30):
        driver.find_element(By.XPATH, button_xpath).click()
        time.sleep(0.5)

    # 기사 제목 저장 리스트
    titles = []

    # 기사 제목 수집
    for j in range(1, 180):
        for k in range(1, 7):
            try:
                title_xpath = '//*[@id="newsct"]/div[4]/div/div[1]/div[{}]/ul/li[{}]/div/div/div[2]/a/strong'.format(
                    j, k)
                title = driver.find_element(By.XPATH, title_xpath).text
                titles.append(title)
            except:
                print('error', j, k)

    # 카테고리별 데이터프레임 생성
    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    # 카테고리 컬럼 추가
    df_section_titles['category'] = CATEGORY
    # 전체 데이터프레임에 병합
    df_titles = pd.concat([df_titles, df_section_titles], ignore_index=True)

# 브라우저 종료
driver.quit()
# 데이터 확인
print(df_titles.head())
df_titles.info()
# CSV 파일 저장
df_titles.to_csv('./data/naver_news_section_PDY.csv', index=False)
