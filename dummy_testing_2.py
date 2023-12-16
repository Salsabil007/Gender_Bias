import asyncio
import aiohttp
import csv
import random
from bs4 import BeautifulSoup

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

import nltk
#https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-x86_64.sh

'''loaded_df = pd.read_json('news_post.json', orient='records')
print(len(loaded_df))

new_final_list = pd.read_csv("doi_news_final.csv")
#print(len(new_final_list[new_final_list['news_cnt'] > 0]))

merged = new_final_list.merge(loaded_df, on = 'doi', how = "inner")
print(len(merged))

def extract_id(dictionary_list):
    return [d.get('author', {}).get('name') for d in dictionary_list]

merged['media'] = merged['news'].apply(lambda x: extract_id(x))

def extract_url(dictionary_list):
    return [d.get('url') for d in dictionary_list]
merged['url'] = merged['news'].apply(lambda x: extract_url(x))

def extract_citid(dictionary_list):
    return [d.get('citation_ids') for d in dictionary_list]
merged['citation_ids'] = merged['news'].apply(lambda x: extract_citid(x))

print(merged.head(10))



# Explode the 'url', 'media' and 'citation_ids' columns
df_expanded = merged.explode(['url', 'citation_ids','media'])


df_expanded['doi'] = merged['doi'].repeat(merged['url'].str.len())
df_expanded['news_cnt'] = merged['news_cnt'].repeat(merged['url'].str.len())

# Reset the index
df_expanded.reset_index(drop=True, inplace=True)

df_expanded['cit_len'] = df_expanded['citation_ids'].apply(lambda x: len(set(x)))
#df_expanded.to_csv("url_doi_list.csv", index = False)

##extract the ones with only one citation, drop duplicates and keep the first
len_1 = df_expanded[df_expanded['cit_len'] == 1]
print(len(df_expanded))
print(df_expanded['doi'].nunique())
print(len(len_1))
print(len_1['doi'].nunique())

#len_1 = len_1.drop_duplicates(subset=['doi'],keep = 'first', ignore_index = True)
#print(len(len_1))

len_1 = len_1.drop(columns=['news_cnt','news','cit_len','citation_ids'], axis = 1)

##we applied this rules on the media of doi_media_for_databricks.csv during its generation. So no problem.
len_1['media'] = len_1['media'].str.strip()
len_1['media'] = len_1['media'].str.replace(r'\s+', '', regex=True)
len_1['media'] = len_1['media'].str.lower()
len_1['media'] = len_1['media'].str.replace(r'\.com$', '', regex=True)


##this block is useless as we didn't use this classification later.
df = pd.read_excel("media_by_me_2.xlsx", 'combined')
print(len(df))
#print(df.head(10))
df['media'] = df['media'].str.strip()
df['media'] = df['media'].str.replace(r'\s+', '', regex=True)
df['media'] = df['media'].str.lower()
df['media'] = df['media'].str.replace(r'\.com$', '', regex=True)
df = df.drop_duplicates()
df['is_top'] = 1
res = len_1.merge(df, on = 'media', how = 'left')
res.fillna({'is_top':0}, inplace=True)
res['is_top'] = res['is_top'].astype(float)
print(len(res))
#print(res.head(5))
print(res['media'].nunique())




res = res.sample(frac=1, random_state=1, ignore_index=True)
print(res.head(10))
res.to_csv("url_doi_list_len1.csv", index = False)'''

'''
##part1
res = pd.read_csv("url_doi_list_len1.csv")
print(len(res))
print(res.dtypes)

r1 = pd.read_csv("doi_list_news.csv") #https://docs.google.com/spreadsheets/d/1KbihhMaKQCYtCgrBJeqviPAEO2X5vR8LDGaMCsOC8co/edit#gid=0 list doi US cor_au generated doi with gender
r1 = r1.drop(columns=['year','news_cnt'], axis = 1)
print(len(r1))
print(r1.dtypes)

final = res.merge(r1, on = ['doi'],how = 'inner')
print(len(final))
final.to_csv("doi_list_for_text_with_gender.csv", index = False)
'''
'''
import asyncio
from newspaper import Article, ArticleException
import csv
import random
import socket


async def fetch_article_data(session, url, min_delay=3, max_delay=10):
    delay = random.uniform(min_delay, max_delay)
    await asyncio.sleep(delay)

    if not isinstance(url, str) or not url.startswith(("http://", "https://")):
        print(f"Invalid URL: {url}")
        return None, None, None

    try:

        async with session.get(url) as response:
            if response.status == 404:
                print(f"404 Error for URL: {url}")
                return None, None, None
        
        # Download and process the article
            article = Article(url, language="en")
            article.download()
            article.parse()
            article.nlp()

            try:
                article.download()
                article.parse()
                article.nlp()
            except Exception as e:
                print(f"Error processing article from {url}: {e}")
                return None, None, None
            
            return article.title, article.text, article.keywords
        
    except ArticleException as e:
        print(f"Article download error for URL {url}: {e}")
        return None, None, None
    
    except (aiohttp.ClientConnectorError, socket.gaierror,asyncio.exceptions.TimeoutError, aiohttp.client_exceptions.TooManyRedirects, aiohttp.client_exceptions.ServerDisconnectedError,aiohttp.client_exceptions.ClientOSError) as e:
        print(f"Connection error for URL {url}: {e}")
        return None, None, None

async def main():
    n = 900+191 + 150 + 317 + 500 + 500 + 62 + 217 +140 + 500 + 179 + 14 +300 + 147 + 300 + 500 + 500 + 500 + 500 ##oct 22: n = 900+191+150 + 316 + 500 + 500 + 62 + 217 + 140 +500 + 179+14 + 300 + 147+300+500+500+500+500
    print("n ",n)
    res = pd.read_csv("doi_list_for_text_with_gender.csv")
    
    #res = res.head(n)
    #data = res.drop_duplicates(subset=['media'],keep = 'first', ignore_index = True)

    data = res.tail(res.shape[0]-n)
    data = data.head(585)
    #data = data.dropna(subset = ['url'])
    print("len of data after dropping na ",len(data))

    doi = data['doi']
    media = data['media']
    urls = data['url']
    gen = data['gender']
    output_file = "newstext_new_us_2.csv"

    ##save the undone ones
    m,dd,ur,gg = [],[],[],[]

    dic = {}
    
    async with aiohttp.ClientSession() as session:
        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["URL", "Title", "Text", "Keywords", 'doi','media','gender'])  # Write header
            cnt = 1
            for url,d,med,g in zip(urls,doi,media,gen):
                if med in dic:
                    print(med," is already done")
                    m.append(med)
                    ur.append(url)
                    dd.append(d)
                    gg.append(g)

                    sv = pd.DataFrame()
                    sv['media'] = m
                    sv['doi'] = dd 
                    sv['url'] = ur
                    sv['gender'] = gg
                    sv.to_csv("uncalled_new_us_links2.csv", index = False)
                    cnt += 1
                    continue
                title, text, keywords = await fetch_article_data(session, url)
                if text is not None:
                    csv_writer.writerow([url, title, text, keywords,d,med,g])
                    dic[med] = 1
                #print(f"Processed: {url}")
                print(cnt)
                cnt += 1
                
                
                # Add a delay between requests
                await asyncio.sleep(10)  # Adjust the delay as needed

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

'''
'''d1 = pd.read_csv("newstext_new_us_2.csv")
d2 = pd.read_csv("newstext_new_us_1.csv")

d2 = pd.concat([d2, d1], ignore_index=True)
d2.to_csv("newstext_new_us_1.csv", index = False)'''

'''d1 = pd.read_csv("uncalled_new_us_links2.csv")
d2 = pd.read_csv("uncalled_new_us_links1.csv")

d2 = pd.concat([d2, d1], ignore_index=True)
d2.to_csv("uncalled_new_us_links1.csv", index = False)'''


'''data = pd.read_csv("newstext_new_us_1.csv") ##us_1 has 2447 unique data
print(data.dtypes)
print(len(data))
data = data.drop_duplicates()
print(len(data))'''
