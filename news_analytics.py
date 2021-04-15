import os
import re
import pandas as pd
import numpy as np
import pandas.io.sql as psql
import psycopg2
import matplotlib.pyplot as plt

from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer, SnowballStemmer, WordNetLemmatizer

# Setup connection with DB
pg_auth = os.environ.get("PG_AUTH")

conn = psycopg2.connect(host="localhost",
                        user="postgres",
                        dbname="investment_db",
                        password=pg_auth)

cur = conn.cursor()
cur.execute("SELECT * FROM stock_price")
rows = cur.fetchall()

# Query data
df_downs = psql.read_sql('''select top_3_news from stock_price
                      where delta_price < 0''', conn)

df_ups = psql.read_sql('''select top_3_news from stock_price
                      where delta_price > 0''', conn)

df_ups['cleaned_news'] = [i[2:-2].split('","') for i in df_ups['top_3_news']]
df_downs['cleaned_news'] = [i[2:-2].split('","') for i in df_downs['top_3_news']]

def lambda_nltk_news(df):

    df.loc[:, 'cleaned_news'] = df['cleaned_news'].fillna('None')
    stop_words = stopwords.words('english')
    special_char = re.compile(r'[\W]')

    comment_words = ''
    all_news = []
    for index, news_list in enumerate(df['cleaned_news']):
        cleaned_news_list = []
        for news in news_list:
            word_tokens = word_tokenize(news)
            no_stops = [i for i in word_tokens if i.lower() not in stop_words]
            no_special_char = [special_char.sub('',i) for i in no_stops if special_char.sub('', i) != '']
            cleaned_news = " ".join(i.lower() for i in no_special_char)
            comment_words += " ".join(i.lower() for i in no_special_char)+" "
            cleaned_news_list.append(cleaned_news)
        all_news.append(cleaned_news_list)
    return all_news, comment_words

df_ups.loc[:,'cleaned_news'], word_cloud_ups = lambda_nltk_news(df_ups)
df_downs.loc[:,'cleaned_news'], word_cloud_downs = lambda_nltk_news(df_downs)


# # plot the WordCloud image - UPs
wordcloud_ups = WordCloud(width = 800, height = 800,
                background_color ='green',
                min_font_size = 10).generate(word_cloud_ups)

plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud_ups)
plt.axis("off")
plt.tight_layout(pad = 0)
plt.savefig('/Users/nikhilsawal/OneDrive/investment_portfolio/eda_plots/ups.png')
plt.show()

# plot the WordCloud image - DOWNs
wordcloud_downs = WordCloud(width = 800, height = 800,
  background_color ='red',
  min_font_size = 10).generate(word_cloud_downs)

plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud_downs)
plt.axis("off")
plt.tight_layout(pad = 0)
plt.savefig('/Users/nikhilsawal/OneDrive/investment_portfolio/eda_plots/downs.png')
plt.show()
