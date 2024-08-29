import pandas as pd
import numpy as np

data = pd.read_csv("individual_sentence.csv")
print("for total data")
print(len(data))

#data = data.head(450000)
print(data['doi'].nunique())

print(data['post_id'].nunique(), " unique posts")
xx = data.drop_duplicates()
print(len(xx))




data3 = pd.read_csv("sentiment_pred_sh_1.csv")
print("for prediction data")
print(len(data3), " length ")
print(data3['post_id'].nunique(), " unique")
xx = data3.drop_duplicates()
print(len(xx))
#data3 = data3.tail(5000)
#print(data3.head(3066))

#print(data3['negative'].mean()," ",data3['neutral'].mean()," ",data3['positive'].mean())

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