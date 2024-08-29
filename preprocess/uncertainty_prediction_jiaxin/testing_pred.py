import pandas as pd
import numpy as np

data = pd.read_csv("individual_sentence.csv")
print("for total data")
print(len(data))
print(data['doi'].nunique())

print(data['post_id'].nunique())
xx = data.drop_duplicates()
print(len(xx))




data3 = pd.read_csv("jiaxin_pred_sh_1.csv")
print("for prediction data")
print(len(data3))
print(data3['doi'].nunique())
print(data3['post_id'].nunique())
xx = data3.drop_duplicates()
print(len(xx))

'''
data2 = pd.read_csv("jiaxin_prediction_1.csv")
print("for part1 data")
print(len(data2))
print(data2['post_id'].nunique())

d = pd.concat([data2, data3], ignore_index=True)
print("for concatenated data")
print(len(d))
print(d['post_id'].nunique())


x1 = set(data['post_id'])
x2 = set(d['post_id'])

print(x1.difference(x2))
print(len(x1.difference(x2)))'''