from importlib.resources import contents
import os
import shutil
from crossref.restful import Works
from crossref.restful import Journals
import requests
import json
import math
import pandas as pd
import numpy as np
import re
import collections

##part 1: extract the data files from the data dump folder (/RDAP-Export-14-11-2022/keys). Inside keys, there are around 793782 folders each having a txt file with 51 doi records. 
##I extract the files with each folder and place them into a single (/copy_file) folder for convenience.
'''
# Set the path to the folder containing the sunfolders
subfolder_dir = os.getcwd()+'/RDAP-Export-14-11-2022/keys'

# Set the path to the folder where you want to copy the files
destination_dir = os.getcwd()+'/copy_file'




cnt = 1
for subfolder_path, subfolders, files in os.walk(subfolder_dir):
    for file in files:
        #print(file)
        if file.endswith(".txt"):
            txt_file_path = os.path.join(subfolder_path, file)
            shutil.copy(txt_file_path, destination_dir)
        
  '''  


##step 2: I pick each of the txt files inside the /copy_file folder and for each record, if it has a doi, I extract the doi, pubdate,posts_count and save that in a folder.
'''def convert_to_list_of_dictionaries(data):
    dictionaries = []
    for dictionary in data.split("\n"):
        dictionary = re.sub(r"\s+", "", dictionary)
        dictionary = json.loads(dictionary)
        dictionaries.append(dictionary)
    return dictionaries

def extract_data(subfolders,doi,pubdate,news_cnt):
    
    with open(os.getcwd()+'/copy_file/'+subfolders, "r") as f:
        data = f.read()

    new_data = re.sub(r"\s+$", "", data)
    dictionaries = convert_to_list_of_dictionaries(new_data)
    print(len(dictionaries))
    
    for j in dictionaries:
        if 'citation' in j:
            if 'doi' in j['citation']:
                doi.append(j['citation']['doi'])
                if 'pubdate' in j['citation']:
                    pubdate.append(j['citation']['pubdate'])
                else:
                    pubdate.append("NO")
                if 'counts' in j and isinstance(j['counts'], dict):
                    if 'news' in j['counts']:
                        if 'posts_count' in j['counts']['news']:
                            news_cnt.append(j['counts']['news']['posts_count'])
                        else:
                            news_cnt.append(0)
                    else:
                        news_cnt.append(0)
                else:
                    news_cnt.append(0)
                
            else:
                continue
        else:
            continue
    return doi, pubdate,news_cnt
    


subfolder_dir = os.getcwd()+'/copy_file'

# List all the folders in the sunfolder directory
subfolders = os.listdir(subfolder_dir)
#print(len(subfolders))

cnt = 1
doi, pubdate,news_cnt = [],[],[]
for i in subfolders:
    doi, pubdate,news_cnt = extract_data(i,doi, pubdate,news_cnt)
    print("cnt ",cnt)
    if cnt % 5000 == 0:
        d = pd.DataFrame()
        d['doi'] = doi
        d['pubdate'] = pubdate
        d['news_cnt'] = news_cnt
        d.to_csv("interim.csv", index = False)
    cnt += 1
        
    
    
d = pd.DataFrame()
d['doi'] = doi
d['pubdate'] = pubdate
d['news_cnt'] = news_cnt
d.to_csv("interim.csv", index = False)'''


## once I have the dois and news count of all data dump (though data dump had 40M records, I found dois for 34M), I merged it with the previously extracted dois
## in "total_doi_crossref.csv" to get the issn and year. We got 4M match dois. However, the dois that are not matched, we can assume those to have no media counts.
data = pd.read_csv("interim.csv")
print(len(data))
print(data['doi'].nunique())
data = data.drop_duplicates(subset=['doi'],keep="first")
print(len(data))
#print(data.tail(5))


new = pd.read_csv("total_doi_crossref.csv")
print(len(new))

joined = new.merge(data,on=['doi'],how='left')
print(len(joined))

#print(len(joined[joined['news_cnt']>0]))
#print(joined.dtypes)