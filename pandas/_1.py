import pandas as pd
import numpy as np

datafile = pd.read_csv('crime_20221231.csv', encoding='ms949')
num_data = datafile.to_numpy() # 데이터프레임을 넘파이배열로

apart_data = num_data[:, 2].copy() #범죄 종류별 아파트에서 발생한 수 (38, 1)
apart_data = apart_data.reshape(38,) #(38,) 형태로 reshape

mask_most_apart = apart_data == np.max(apart_data) #아파트에서 가장 많이 발생한 수의 범죄를 불리안 인덱싱으로 찾기
most_apart = num_data[mask_most_apart,1] # mask를 이용해 num_data에서 찾기

print(most_apart)

mask_most = num_data == np.max(num_data[:, 3:])
mask_row_most = np.sum(mask_most, 1) #row * column에서 같은 순번의 column끼리 sum == 같은 row의 데이터 sum -> row 수 만큼의 데이터
mask_column_most = np.sum(mask_most, 0) #row * column에서 같은 순번의 row끼리 sum == 같은 column의 데이터 sum -> column 수 만큼의 데이터

print(mask_column_most)
print(mask_row_most)

mask_row_most = mask_row_most==1

print(num_data[mask_row_most,1])
# 6, 33

