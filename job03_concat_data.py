# 데이터 수집 및 병합

import pandas as pd

# 사회, 문화 뉴스 데이터 로드
df = pd.read_csv('data/naver_headline_news_Social_ Culture.csv')
print(df.head())

# 경제 뉴스 데이터 로드
df_temp = pd.read_csv('data/naver_news_section_KYJe.csv')
print(df_temp.head())

# 데이터 병합
df = pd.concat([df, df_temp], ignore_index=True)
# 정치 뉴스 데이터 로드
df_temp = pd.read_csv('data/naver_news_section_KYJp.csv')
# 데이터 병합
df = pd.concat([df, df_temp], ignore_index=True)
# 세계, IT 뉴스 데이터 로드
df_temp = pd.read_csv('data/naver_news_section_PDY.csv')
df = pd.concat([df, df_temp], ignore_index=True)
# 최신 헤드라인 뉴스 데이터 로드
df_temp = pd.read_csv('data/naver_headline_news_20260605.csv')
df = pd.concat([df, df_temp], ignore_index=True)
# 데이터 정보 확인
df.info()
# 중복 데이터 제거
df = df.drop_duplicates()
# 카테고리별 데이터 개수 확인
print(df.category.value_counts())
# 결측치 확인
print(df.isnull().sum())
# 최종 데이터 정보 확인
df.info()
# 최종 데이터 CSV 저장
df.to_csv('data/news_titles.csv', index=False)