# 전처리
import pickle                                                       # 객체 저장 및 로드
import pandas as pd                                                 # 데이터 처리
import numpy as np                                                  # 수치 계산
from sklearn.model_selection import train_test_split                # 학습/테스트 데이터 분리
from konlpy.tag import Okt, Komoran                                 # 형태소 분석기
from sklearn.preprocessing import LabelEncoder                      # 문자열 라벨 인코딩
from keras.utils import to_categorical                              # 원-핫 인코딩
from tensorflow.keras.preprocessing.sequence import pad_sequences   # 문장 길이 맞춤
from tensorflow.keras.preprocessing.text import Tokenizer           # 텍스트 토큰화
import re                                                           # 정규표현식

# 뉴스 데이터 로드
df = pd.read_csv('./data/news_titles.csv')
# 데이터 정보 확인
df.info()
# 데이터 샘플 확인
print(df.head(30))
# 카테고리별 개수 확인
print(df.category.value_counts())

# 입력 데이터(제목)
X = df.titles
# 정답 데이터(카테고리)
Y = df.category

# 형태소 분석기 생성
okt = Okt()
# 첫 번째 제목 형태소 분석
okt_x = okt.morphs(X[0])
# 형태소 분석 결과 확인
print(okt_x)
