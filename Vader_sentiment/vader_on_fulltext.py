from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np
import ast

def sentiment_scores(sentence):
 
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()
 
    # polarity_scores method of SentimentIntensityAnalyzer
    # object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)
     
    #print("Overall sentiment dictionary is : ", sentiment_dict)
    #print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
    #print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
    #print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")
    return sentiment_dict['pos'], sentiment_dict['neg'], sentiment_dict['neu'], sentiment_dict['compound']



text = pd.read_csv("interim_test.csv", converters={'sentence': ast.literal_eval})
print(len(text))

total_cnt = []
for ind in text.index:
    total_cnt.append(len(text['sentence'][ind]))
text['total_cnt'] = total_cnt
text = text[text['total_cnt'] >= 1]
print(len(text))

pos, neg, com, neu = [],[],[],[]


for ind in text.index:
    l1,l2,l3,l4 = [],[],[],[]
    print(text['URL'][ind])
    for i in text['sentence'][ind]:
        #print("%%sent ",i)
        a,b,c,d = sentiment_scores(i)
        l1.append(a)
        l2.append(b)
        l3.append(c)
        l4.append(d)

    pos.append(np.average(l1))
    neg.append(np.average(l2))
    neu.append(np.average(l3))
    com.append(np.average(l4))


text['positive'] = pos
text['negative'] = neg
text['neutral'] = neu
text['compound'] = com
text.to_csv("vader_pred_fulltext.csv", index = False)




