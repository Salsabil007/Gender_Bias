import pandas as pd
import numpy as np
import ast

text = pd.read_csv("pred_title.csv")

text = text.drop_duplicates(subset=['doi','media','Title'])
print(len(text))
print(text['gender'].unique())


G = []
for ind in text.index:
    if text['gender'][ind] == 'male' or text['gender'][ind] == 'M' or text['gender'][ind] == 'm':
        G.append("Male")
    elif text['gender'][ind] == 'female' or text['gender'][ind] == 'F' or text['gender'][ind] == 'f':
        G.append("Female")

text['G'] = G

print("len of female in the entire dataset ",len(text[text['G'] == "Female"]), " and len of male in the entire dataset ",len(text[text['G'] == "Male"]))

a1 = text[text['title_pred_bin'] == 'C']
a2 = text[text['title_pred_bin'] == 'U']

print("proportion of title with uncertainty ",len(a2)/len(text))


a1f = a1[a1['G'] == "Female"]
a2f = a2[a2['G'] == "Female"]
a2m = a2[a2['G'] == "Male"]

print("propor of female in certain title group ",len(a1f)/len(a1)," prop of female in uncertain group ",len(a2f)/len(a2))

print("proportion of female in the entire set",len(text[text['G'] == "Female"])/len(text))


nf = text[text['G'] == "Female"]
nm = text[text['G'] == "Male"]

nfu = nf[nf['title_pred_bin'] == 'U']
nmu = nm[nm['title_pred_bin'] == 'U']

print("proportion of uncertain title for female ",len(nfu)/len(nf))
print("proportion of uncertain title for male ",len(nmu)/len(nm))

Cf = len(nf[nf['title_pred_nobin'] == 'C'])/len(nf)
Ef = len(nf[nf['title_pred_nobin'] == 'E'])/len(nf)
Nf = len(nf[nf['title_pred_nobin'] == 'N'])/len(nf)
Df = len(nf[nf['title_pred_nobin'] == 'D'])/len(nf)
If = len(nf[nf['title_pred_nobin'] == 'I'])/len(nf)
Uf = len(nf[nf['title_pred_nobin'] == 'U'])/len(nf)

print("for female, proportion of C: ", Cf, " E ",Ef," N ",Nf, " D ",Df," I ",If," U ",Uf)

Cm = len(nm[nm['title_pred_nobin'] == 'C'])/len(nm)
Em = len(nm[nm['title_pred_nobin'] == 'E'])/len(nm)
Nm = len(nm[nm['title_pred_nobin'] == 'N'])/len(nm)
Dm = len(nm[nm['title_pred_nobin'] == 'D'])/len(nm)
Im = len(nm[nm['title_pred_nobin'] == 'I'])/len(nm)
Um = len(nm[nm['title_pred_nobin'] == 'U'])/len(nm)

print("for male, proportion of C: ", Cm, " E ",Em," N ",Nm, " D ",Dm," I ",Im," U ",Um)

'''print(len(text)," male: ",len(nm)," female: ",len(nf))
print(nf['title_pred_nobin'].value_counts().reset_index())
print(nm['title_pred_nobin'].value_counts().reset_index())


print("c ",1386/1540," E ",144/len(nfu)," I ",3/len(nfu)," U ",3/len(nfu)," N ",3/len(nfu)," D ",1/len(nfu))
print("c ",3891/4316," E ",372/len(nmu)," I ",10/len(nmu)," U ",4/len(nmu)," N ",31/len(nmu)," D ",8/len(nmu))

print(a2['Title'])'''

