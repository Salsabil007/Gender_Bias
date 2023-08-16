from hmac import new
from importlib.resources import contents
import os
import shutil
from typing import final
from crossref.restful import Works
from crossref.restful import Journals
import requests
import json
import math
import pandas as pd
import numpy as np
import re
import collections


'''def convert_to_list_of_dictionaries(data):
    dictionaries = []
    for dictionary in data.split("\n"):
        dictionary = re.sub(r"\s+", "", dictionary)
        dictionary = json.loads(dictionary)
        dictionaries.append(dictionary)
    return dictionaries

def extract_data(subfolders,doi,news_cnt):
    
    with open(os.getcwd()+'/copy_file/'+subfolders, "r") as f:
        data = f.read()

    new_data = re.sub(r"\s+$", "", data)
    dictionaries = convert_to_list_of_dictionaries(new_data)
    print(len(dictionaries))
    
    for j in dictionaries:
        if 'citation' in j:
            if 'doi' in j['citation']:
                if 'posts' in j and isinstance(j['posts'], dict):
                    if 'news' in j['posts']:
                        news_cnt.append(j['posts']['news'])
                        doi.append(j['citation']['doi'])
    return doi,news_cnt
    


subfolder_dir = os.getcwd()+'/copy_file'

# List all the folders in the sunfolder directory
subfolders = os.listdir(subfolder_dir)
#print(len(subfolders))

cnt = 1
doi,news_cnt = [],[]
for i in subfolders:
    doi,news_cnt = extract_data(i,doi,news_cnt)
    print("cnt ",cnt)
    if cnt % 5000 == 0:
        d = pd.DataFrame()
        d['doi'] = doi
        d['news'] = news_cnt
        d.to_json('news_post.json', orient='records')
    cnt += 1


    #%%%%%%%%%%%%%%%
    #if cnt == 10:
    #    break
        
    
    
d = pd.DataFrame()
d['doi'] = doi
d['news'] = news_cnt
d.to_json('news_post.json', orient='records')'''



###part 2
loaded_df = pd.read_json('news_post.json', orient='records')
print(len(loaded_df))

new_final_list = pd.read_csv("doi_news_final.csv")
#print(len(new_final_list[new_final_list['news_cnt'] > 0]))

merged = new_final_list.merge(loaded_df, on = 'doi', how = "inner")
print("len of merged ",len(merged))
print("len of unique in merged ",merged['doi'].nunique())

##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  //testing 
#merged = merged.head(10)





#print(loaded_df.iloc[0]['news'])


def extract_id(dictionary_list):
    return [d.get('author', {}).get('name') for d in dictionary_list]
# Apply the function to the 'Data' column
merged['author'] = merged['news'].apply(lambda x: extract_id(x))



merged= merged.drop(columns = ['news'], axis = 1)
new = merged.explode('author', ignore_index=True)
#print(new)
new.to_csv("doi_news_name.csv", index = False)







'''def extract_url(dictionary_list):
    return [d.get('url') for d in dictionary_list]
merged['url'] = merged['news'].apply(lambda x: extract_url(x))

def extract_citid(dictionary_list):
    return [d.get('citation_ids') for d in dictionary_list]
merged['citation_ids'] = merged['news'].apply(lambda x: extract_citid(x))

merged['len_citation'] = merged['citation_ids'].apply(lambda x: len(x))'''

dd = pd.read_csv("doi_news_name.csv")
print(len(dd))
print(dd['doi'].nunique())