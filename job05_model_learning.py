# ================================================================================================
# 뉴스 제목 카테고리 분류 모델 학습
# ================================================================================================

# ------------------------------------------------------------------------------------------------
# 1. 라이브러리 import
# ------------------------------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from keras.models import *
from keras.layers import *

# ------------------------------------------------------------------------------------------------
# 2. 전처리 데이터 로드
# ------------------------------------------------------------------------------------------------
x_train = np.load('data/x_train.npy', allow_pickle=True)
y_train = np.load('data/y_train.npy', allow_pickle=True)
x_test = np.load('data/x_test.npy', allow_pickle=True)
y_test = np.load('data/y_test.npy', allow_pickle=True)
print(x_train.shape, y_train.shape, x_test.shape, y_test.shape)             # 데이터 크기 확인

# ------------------------------------------------------------------------------------------------
# 3. 모델 생성
# ------------------------------------------------------------------------------------------------
model = Sequential()
model.add(Embedding(9677, 300))                                # 단어 임베딩
model.build(input_shape=(None, 32))                                               # 입력 크기 설정
model.add(Conv1D(32, 5, padding='same', activation='relu'))       # 특징 추출을 위한 1차원 CNN
model.add(MaxPooling1D(1))                                                        # 특징 맵 유지
model.add(LSTM(128, activation='tanh', return_sequences=True))              # 첫 번째 LSTM 계층
model.add(Dropout(0.2))
model.add(LSTM(64, activation='tanh', return_sequences=True))               # 두 번째 LSTM 계층
model.add(Dropout(0.2))
model.add(LSTM(64,activation='tanh'))                                       # 세 번째 LSTM 계층
model.add(Dropout(0.2))
model.add(Flatten())                                                              # 완전연결층 입력을 위한 평탄화
model.add(Dense(64, activation='relu'))                                      # 은닉층
model.add(Dense(6, activation='softmax'))                                    # 출력층 (6개 카테고리)
model.summary()                                                                    # 모델 구조 출력

# ------------------------------------------------------------------------------------------------
# 4. 모델 컴파일
# ------------------------------------------------------------------------------------------------
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# ------------------------------------------------------------------------------------------------
# 5. 모델 학습
# ------------------------------------------------------------------------------------------------
fit_hist = model.fit(x_train, y_train, batch_size=128, epochs=10, validation_data=(x_test, y_test), verbose=1)

# ------------------------------------------------------------------------------------------------
# 6. 모델 평가
# ------------------------------------------------------------------------------------------------
score = model.evaluate(x_test, y_test, verbose=0)

# ------------------------------------------------------------------------------------------------
# 7. 모델 저장
# ------------------------------------------------------------------------------------------------
print('Final Test loss:', score[0])

# ------------------------------------------------------------------------------------------------
# 8. 학습 결과 시각화
# ------------------------------------------------------------------------------------------------
print('Final Test accuracy:', score[1])
model.save('./models/news_section_classifier{}.h5'.format(score[1]))
plt.plot(fit_hist.history['val_accuracy'], label='val accuracy')
plt.plot(fit_hist.history['accuracy'], label='train accuracy')
plt.legend(loc='lower right')
plt.show()