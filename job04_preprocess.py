# ================================================================================================
# 뉴스 제목 분류 모델 학습용 데이터 전처리
# ================================================================================================

# ------------------------------------------------------------------------------------------------
# 1. 라이브러리 import
# ------------------------------------------------------------------------------------------------
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

# ------------------------------------------------------------------------------------------------
# 2. 데이터 로드 및 기본 확인
# ------------------------------------------------------------------------------------------------
df = pd.read_csv('./data/news_titles.csv')

df.info()                           # 데이터 정보 확인
print(df.head(30))                  # 데이터 샘플 확인
print(df.category.value_counts())   # 카테고리별 개수 확인

# ------------------------------------------------------------------------------------------------
# 3. 입력 데이터와 정답 데이터 분리
# ------------------------------------------------------------------------------------------------
X = df.titles                                   # 입력 데이터(제목)
Y = df.category                                 # 정답 데이터(카테고리)

# print(X[0])
#
# okt = Okt()                                   # 형태소 분석기 생성
#
# okt_x = okt.morphs(X[0])                      # 첫 번째 제목 형태소 분석
# print(okt_x)
#
# okt_x_stem = okt.morphs(X[0], stem=True)      # 어간 추출 적용
# print(okt_x_stem)
#
# komoran = Komoran()
# komoran_x = komoran.morphs(X[0])
# print(komoran_x)

# ------------------------------------------------------------------------------------------------
# 4. 정답 라벨 인코딩
# ------------------------------------------------------------------------------------------------
encoder = LabelEncoder()
labeled_y = encoder.fit_transform(Y)

print(labeled_y[:5])

label = encoder.classes_
print(label)

with open('./data/encoder.pkl', 'wb') as f:     # 라벨 이름 저장
    pickle.dump(label, f)
onehot_y = to_categorical(labeled_y)            # 정답 데이터를 원-핫 인코딩으로 변환
print(onehot_y[:5])

# 자연어 처리 예제
# cleaned_x = re.sub('[^가-힇]', ' ', X[0])
# print(X[0])
# print(cleaned_x)

# ------------------------------------------------------------------------------------------------
# 5. 뉴스 제목 형태소 분석 및 정제
# ------------------------------------------------------------------------------------------------
okt = Okt()
X = list(X)

for i in range(len(X)):
    X[i] = re.sub('[^가-힇]', ' ', X[i])         # 한글을 제외한 문자는 공백으로 변경
    X[i] = okt.morphs(X[i], stem=True)                      # 형태소 분석 및 어간 추출
    if i % 1000 == 0:                                       # 전처리 진행 상황 출력
        print(i)

print(X[:5])

# 의미가 적은 한 글자 형태소 제거
for idx, sentence in enumerate(X[:5]):
    words = []
    for word in sentence:
        if len(word) > 1:
            words.append(word)
    X[idx] = ' '.join(words)
print(X[:5])

# ------------------------------------------------------------------------------------------------
# 6. 텍스트 토큰화
# ------------------------------------------------------------------------------------------------
tokenizer = Tokenizer()
tokenizer.fit_on_texts(X)                       # 단어 사전 생성
tokened_x = tokenizer.texts_to_sequences(X)     # 텍스트를 숫자 시퀀스로 변환
print(tokened_x)
wordsize = len(tokenizer.word_index) + 1        # 전체 단어 개수 계산
print(wordsize)

# ------------------------------------------------------------------------------------------------
# 7. 문장 최대 길이 확인 및 토크나이저 저장
# ------------------------------------------------------------------------------------------------
max = 0
for sentence in tokened_x:
    if max < len(sentence):
        max = len(sentence)
print(max)
with open('./data/tokenizer_max{}.pkl'.format(max), 'wb') as f:
    pickle.dump(tokenizer, f)

# ------------------------------------------------------------------------------------------------
# 8. 패딩 처리
# ------------------------------------------------------------------------------------------------
x_pad = pad_sequences(tokened_x, maxlen=max)
print(x_pad[:5])

# ------------------------------------------------------------------------------------------------
# 9. 학습 데이터와 테스트 데이터 분리
# ------------------------------------------------------------------------------------------------
x_train, x_test, y_train, y_test = train_test_split(
    x_pad, onehot_y, test_size=0.1)

print(x_train.shape, y_train.shape)
print(x_test.shape, y_test.shape)

# ------------------------------------------------------------------------------------------------
# 10. 전처리 데이터 저장
# ------------------------------------------------------------------------------------------------
np.save('./data/x_train.npy', x_train)
np.save('./data/y_train.npy', y_train)
np.save('./data/x_test.npy', x_test)
np.save('./data/y_test.npy', y_test)