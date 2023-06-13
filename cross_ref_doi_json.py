from crossref.restful import Works
from crossref.restful import Journals
import requests
import json
import math
import pandas as pd
import numpy as np

'''def get_data(msg,issn):
    url = "https://api.crossref.org/journals/"+issn+"/works?select=DOI,published&cursor=*&mailto=support@crossref.org"
    res = requests.get(url)
    if res.status_code == 200:
        result = res.json()
        print(result['message']['total-results'])
        cnt = math.ceil(result['message']['total-results']/1000)
        print(cnt)
        
        a = "*"
        for i in range(cnt):
            url = "https://api.crossref.org/journals/"+issn+"/works?select=DOI,published&rows=1000&cursor="+a+"&mailto=support@crossref.org"
            res = requests.get(url)
            if res.status_code != 200:
                print("ohh no")
                return msg
            
            result = res.json()
            
            
            if 'message' in result:
                result['message']['issn'] = str(issn)
                msg.append(result['message'])

                if 'next-cursor' in result['message']:
                    a = result['message']['next-cursor']
                else:
                    return msg
                

            else:
                return msg

    else:
        return msg
    return msg


data = pd.read_csv("top_25_single_issn.csv")
doi = []
#data2 = data.drop_duplicates(subset=['journal'],keep="first")


n = 5500
data = data.tail(data.shape[0]-n)
#data = data.head(500)

#print(data.tail(5))

issn = data['issn']
print("len of issn ",len(issn))

#exit(0)
#print("issn ",issn)


#remove = pd.read_csv("issn_doi.csv")
#remove = remove['issn'].unique()
#issn2 = [i for i in issn if i not in remove]

#print(len(issn))
#print(len(res))
#print(data['issn'].nunique())
#issn = res
#print(issn2)

count = 0
for i in issn:
    print("issn ",i)
    doi = get_data(doi,i)
    
    print("count ",count)
    count += 1
with open("doi_issn_json_6k2.json", "w") as outfile:
    json.dump(doi, outfile)'''


with open('doi_issn_json_6k2.json', 'r') as openfile:
 
    # Reading from json file
    dx1 = json.load(openfile)

doi,issn,yr = [],[],[]

for i in dx1:
    #dx[0]['items'][0]['DOI']
    if 'items' in i:
        #print(i['items'])
        for j in i['items']:
            if 'published' in j:
                if 'date-parts' in j['published']:
                    if j['published']['date-parts'][0][0] < 2018:
                        continue

            if 'DOI' in j:
                doi.append(j['DOI'])
                if 'published' in j:
                    if 'date-parts' in j['published']:
                        yr.append(j['published']['date-parts'][0][0])
                    else:
                        yr.append(0)
                else:
                    yr.append(0)
                if 'issn' in i:
                    issn.append(i['issn'])
                else:
                    issn.append(0)
            else:
                continue
                
dummy = pd.DataFrame()
dummy['doi'] = doi
dummy['issn'] = issn
dummy['yr'] = yr
#dummy = dummy[dummy['yr'] >= 2018]

dummy.to_csv("doi_6k2_from_json.csv", index = False)