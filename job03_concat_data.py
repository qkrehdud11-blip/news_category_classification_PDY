# data 수집

import pandas as pd
df = pd.read_csv('data/naver_headline_news_Social_ Culture.csv')
print(df.head())

df_temp = pd.read_csv('data/naver_news_section_KYJe.csv')
print(df_temp.head())

df = pd.concat([df, df_temp], ignore_index=True)
df_temp = pd.read_csv('data/naver_news_section_KYJp.csv')

df = pd.concat([df, df_temp], ignore_index=True)
df_temp = pd.read_csv('data/naver_news_section_PDY.csv')
df = pd.concat([df, df_temp], ignore_index=True)
df_temp = pd.read_csv('data/naver_headline_news_20260605.csv')
df = pd.concat([df, df_temp], ignore_index=True)
df.info()
df = df.drop_duplicates()
print(df.category.value_counts())
print(df.isnull().sum())
df.info()
df.to_csv('data/news_titles.csv', index=False)