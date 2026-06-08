# ================================================================================================
# 네이버 뉴스 카테고리별 기사 제목 수집
# ================================================================================================

# 파일명 : naver_news_section.csv
# 컬럼명 : titles, category
#
# 도영님 : Politics, Economic, Social, Culture, World, IT
#
# 작업 완료 후 PR 진행

# ------------------------------------------------------------------------------------------------
# 1. 라이브러리 import
# ------------------------------------------------------------------------------------------------
import pandas as pd                                                     # 데이터프레임 처리
from selenium import webdriver                                          # 웹 브라우저 제어
from selenium.webdriver.common.by import By                             # 요소 탐색
from selenium.webdriver.chrome.service import Service as ChromeService  # 크롬 드라이버 서비스 설정
from selenium.webdriver.chrome.options import Options as ChromeOptions  # 크롬 실행 옵션 설정
from webdriver_manager.chrome import ChromeDriverManager                # 크롬 드라이버 자동 설치
import time                                                             # 대기 시간 설정

# ------------------------------------------------------------------------------------------------
# 2. 기본 설정
# ------------------------------------------------------------------------------------------------
category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']     # 뉴스 카테고리 목록
df_titles = pd.DataFrame()                                                  # 전체 기사 저장용 데이터프레임

# ------------------------------------------------------------------------------------------------
# 3. 크롬 드라이버 설정
# ------------------------------------------------------------------------------------------------
options = ChromeOptions()
options.add_argument('lang=ko_KR')          # 한국어 환경 설정
options.add_argument('headless')            # 브라우저 창 숨김

# 크롬 드라이버 실행
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


# ------------------------------------------------------------------------------------------------
# 4. 뉴스 페이지 정보 설정
# ------------------------------------------------------------------------------------------------
# button_xpath = '//*[@id="newsct"]/div[4]/div/div[2]/a'              # 더보기 버튼 XPath

# ------------------------------------------------------------------------------------------------
# 5. 뉴스 제목 수집
# ------------------------------------------------------------------------------------------------
# 도영 담당:Politics(100), Economic(101), Social(102), Culture(103) World(104), IT(105)
for SECTION, CATEGORY in zip(range(0, 6), category[0:6]):
    # 카테고리 페이지 접속
    url = 'https://news.naver.com/section/10{}'.format(SECTION)
    driver.get(url)

    # 더보기 버튼 반복 클릭
    if SECTION == 1:
        div_num = 5
    else:
        div_num = 4

    button_xpath = f'//*[@id="newsct"]/div[{div_num}]/div/div[2]/a'

    for i in range(30):
        try:
            driver.find_element(By.XPATH, button_xpath).click()
            time.sleep(0.5)
        except:
            print('더보기 종료:', CATEGORY)
            break

    # 기사 제목 저장 리스트
    titles = []

    # 기사 제목 수집
    for j in range(1, 180):
        for k in range(1, 7):
            try:
                title_xpath = '//*[@id="newsct"]/div[{}]/div/div[1]/div[{}]/ul/li[{}]/div/div/div[2]/a/strong'.format(
                    div_num, j, k)
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

# ------------------------------------------------------------------------------------------------
# 6. 수집 종료
# ------------------------------------------------------------------------------------------------
# 브라우저 종료
driver.quit()

# ------------------------------------------------------------------------------------------------
# 7. 데이터 확인
# ------------------------------------------------------------------------------------------------
print(df_titles.head())
df_titles.info()

# ------------------------------------------------------------------------------------------------
# 8. CSV 파일 저장
# ------------------------------------------------------------------------------------------------
df_titles.to_csv('./data/naver_news_section_PDY_260608_1050.csv', index=False)
