import pandas as pd
import numpy as np
import ast


text1 = pd.read_csv("pred1_test.csv", converters={'sentence': ast.literal_eval,'sent_pred': ast.literal_eval})
text2 = pd.read_csv("pred2_test.csv", converters={'sentence': ast.literal_eval,'sent_pred': ast.literal_eval})
text3 = pd.read_csv("pred3_test.csv", converters={'sentence': ast.literal_eval,'sent_pred': ast.literal_eval})

t = pd.concat([text1, text2], ignore_index=True)
text4 = pd.concat([t,text3], ignore_index= True)

#print(text.iloc[0]['new_text'])

text = text4.drop(columns = ['sentence'], axis = 1)
#text = text.drop_duplicates(subset = ['new_text'])

print(len(text))
#print(text.dtypes)
#print(len(text.iloc[0]['sentence']))
#print(len(text.iloc[0]['sent_pred']))

#print(text.iloc[0]['sent_pred'][0])
#print(text.iloc[0]['sentence'][4])

#print(text['gender'].unique())



total_cnt = []
uncertain = []
G = []
for ind in text.index:
    total_cnt.append(len(text['sent_pred'][ind]))
    sum = 0
    for i in text['sent_pred'][ind]:
        if i == 'U':
            sum += 1
    uncertain.append(sum)

    if text['gender'][ind] == 'male' or text['gender'][ind] == 'M' or text['gender'][ind] == 'm':
        G.append("Male")
    elif text['gender'][ind] == 'female' or text['gender'][ind] == 'F' or text['gender'][ind] == 'f':
        G.append("Female")

text['total_cnt'] = total_cnt
text['uncertain'] = uncertain
text['G'] = G
     
C,E,N,I,D,U = [],[],[],[],[],[]
for ind in text.index:
    
    c,e,n,ii,d,u = 0,0,0,0,0,0
    for i in text['sent_pred_nobin'][ind]:
        if i == 'U':
            u += 1
        elif i == 'C':
            c += 1
        elif i == 'E':
            e += 1
        elif i == 'D':
            d += 1
        elif i == 'I':
            ii += 1
        elif i == 'N':
            n += 1
    C.append(c)
    U.append(u)
    E.append(e)
    N.append(n)
    D.append(d)
    I.append(ii)

    

    
text['C'] = C
text['U'] = U
text['D'] = D
text['E'] = E
text['I'] = I
text['N'] = N



text = text.drop(columns = ['URL','new_text','word_count','gender','sent_pred','sent_pred_nobin'], axis = 1)

#print(text.head(5))



text['prop'] = text['uncertain']/text['total_cnt']

text = text[text['total_cnt'] >= 5]
text = text[text['total_cnt'] <= 120]
print(len(text))

f = text[text['G'] == "Female"]
m = text[text['G'] == "Male"]
#m = m.sample(n = len(f), replace = False, random_state=0)

print("mean proportion of uncertain sentence for the articles of female ",f['prop'].mean()," and male ", m['prop'].mean())
print("median proportion of uncertain sentence for the articles of female ",f['prop'].median()," and male", m['prop'].median())

#print(f['total_cnt'].mean()," ", m['total_cnt'].mean())
print(len(f)," ",len(m))

a = text[text['uncertain'] == 0]
print("proportion of article with certainty ",len(a)/len(text))

af = a[a['G'] == "Female"]
print("proportion of female in certain group ",len(af)/len(a))

a = text[text['uncertain'] > 0]
af = a[a['G'] == "Female"]
print("proportion of female in uncertain group ",len(af)/len(a))

f = f[f['uncertain'] > 0]
m = m[m['uncertain'] > 0]
print(len(f)," ",len(m))

f['U'] = f['U']/f['uncertain']
f['D'] = f['D']/f['uncertain']
f['N'] = f['N']/f['uncertain']
f['E'] = f['E']/f['uncertain']
f['I'] = f['I']/f['uncertain']


m['U'] = m['U']/m['uncertain']
m['D'] = m['D']/m['uncertain']
m['N'] = m['N']/m['uncertain']
m['E'] = m['E']/m['uncertain']
m['I'] = m['I']/m['uncertain']


print("male U ",m['U'].mean()," E ",m['E'].mean(), " D ",m['D'].mean()," N ",m['N'].mean()," I ",m['I'].mean())
print("female U ",f['U'].mean()," E ",f['E'].mean(), " D ",f['D'].mean()," N ",f['N'].mean()," I ",f['I'].mean())


print(text.dtypes)
text.to_csv("full_luci_reg.csv", index = False)