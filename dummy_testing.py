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
#nltk.download('punkt')

##part1
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

len_1['media'] = len_1['media'].str.strip()
len_1['media'] = len_1['media'].str.replace(r'\s+', '', regex=True)
len_1['media'] = len_1['media'].str.lower()
len_1['media'] = len_1['media'].str.replace(r'\.com$', '', regex=True)



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











##part 2
'''
async def fetch_url_with_random_delay(session, url, min_delay=3, max_delay=10):
    delay = random.uniform(min_delay, max_delay)
    await asyncio.sleep(delay)
    async with session.get(url) as response:
        return await response.text()

async def main():

    data = pd.read_csv("url_doi_list_len1.csv")
    data = data.head(5)

    doi = data['doi']
    media = data['media']
    urls = data['url']
    #urls = ['https://www.huffpost.com/entry/black-holes-white-holes-explode_n_5597006',
    #       'https://qz.com/india/1229007/abhas-mitra-the-indian-physicist-who-contested-stephen-hawkings-theory-about-black-holes']  # List of your 10,000 URLs
       # List of values for the new column
    max_concurrent_requests = 5  # Limit concurrent requests
    output_file = "newstext_1.csv"  # CSV file to store data

    async with aiohttp.ClientSession() as session, asyncio.Semaphore(max_concurrent_requests) as sem:
        tasks = [fetch_url_with_random_delay(session, url) for url in urls]
        pages = await asyncio.gather(*tasks)

    # Process and extract data using Beautiful Soup, then save to CSV
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["URL", "NewsText", "doi","media"])  # Write header
        cnt = 1

        for url, page, d,med in zip(urls, pages, doi, media):
            #soup = BeautifulSoup(page, 'html.parser')
            # Extract news text and other relevant information
            
            
            soup = BeautifulSoup(page, 'html.parser') 

            #s = soup.find('div', class_='main-content')
            if soup is None or len(soup) == 0:
                continue
            data = '' 
            #print(soup)


            #for data in soup.find_all("p"): 
            #    ss = data.get_text() 
        

            ss = ""
            for data in soup.find_all("p"): 
                s = data.get_text() 
                #print(s)
                ss = ss + s +"\n"

            news_text = ss
            csv_writer.writerow([url, news_text, d,med])

            print("count ",cnt)
            cnt += 1
            #if cnt == 2:
            #    break


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())'''


'''
#first time
n = 3000
res = pd.read_csv("url_doi_list_len1.csv")
res = res.head(n)
print(res.tail(5))
res = res.drop_duplicates(subset=['media'],keep = 'first', ignore_index = True)
print(len(res))'''

'''#rest
n = 3000 
res = pd.read_csv("url_doi_list_len1.csv")
res = res.tail(res.shape[0]-n)
res = res.head(3000)
print(res.head(5))
res = res.drop_duplicates(subset=['media'],keep = 'first', ignore_index = True)
print(len(res))'''




import asyncio
from newspaper import Article, ArticleException
import csv
import random


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

async def main():
    n = 8+34+76+13 + 4 + 47 ##done with 8 + 34+76+13 + 4 + 47, last saved in newstext_4, merged it with newstext_3 and saved in newstext_3. 
    #Aug 28. create new uncalled_links2.csv file, merged it with uncalled_links1.csv and saved it in uncalled_links1.csv. Aug 29.
    res = pd.read_csv("url_doi_list_len1.csv")
    
    #res = res.head(n)
    #data = res.drop_duplicates(subset=['media'],keep = 'first', ignore_index = True)

    data = res.tail(res.shape[0]-n)
    data = data.head(1000)

    doi = data['doi']
    media = data['media']
    urls = data['url']
    output_file = "newstext_4.csv"

    ##save the undone ones
    m,dd,ur = [],[],[]

    dic = {}
    
    async with aiohttp.ClientSession() as session:
        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["URL", "Title", "Text", "Keywords", 'doi','media'])  # Write header
            cnt = 1
            for url,d,med in zip(urls,doi,media):
                if med in dic:
                    print(med," is already done")
                    m.append(med)
                    ur.append(url)
                    dd.append(d)

                    sv = pd.DataFrame()
                    sv['media'] = m
                    sv['doi'] = dd 
                    sv['url'] = ur
                    sv.to_csv("uncalled_links2.csv", index = False)
                    continue
                title, text, keywords = await fetch_article_data(session, url)
                if text is not None:
                    csv_writer.writerow([url, title, text, keywords,d,med])
                    dic[med] = 1
                #print(f"Processed: {url}")
                print(cnt)
                cnt += 1
                
                
                # Add a delay between requests
                await asyncio.sleep(10)  # Adjust the delay as needed

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


'''d1 = pd.read_csv("newstext_4.csv")
d2 = pd.read_csv("newstext_3.csv")

d2 = pd.concat([d2, d1], ignore_index=True)
d2.to_csv("newstext_3.csv")'''

'''d1 = pd.read_csv("uncalled_links2.csv")
d2 = pd.read_csv("uncalled_links1.csv")

d2 = pd.concat([d2, d1], ignore_index=True)
d2.to_csv("uncalled_links1.csv")'''