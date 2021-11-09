# -*- coding: utf-8 -*-
"""

Script will work as a more thorough analysis and processing of the policies
data

@author: jis
"""
# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import nltk

from nltk.corpus import stopwords
# from nltk.stem.porter import PorterStemmer
# from nltk.tokenize import RegexpTokenizer
# from nltk.stem.snowball import SnowballStemmer
# from nltk.stem.wordnet import WordNetLemmatizer
import seaborn as sns
from wordcloud import WordCloud
import gensim
from gensim.models import Word2Vec, Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from sklearn.decomposition import PCA
# import snowballstemmer

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

import data_imports
# %% Downloads of stopwords and wordnet
# nltk.download('stopwords')

# nltk.download('wordnet')
# %%

policies_df = data_imports.policy_data_current()


policies_df['date'] = policies_df['date'].astype('datetime64[ns]')

# %%
# Getting all unique values from the columns after "policy" columns in the
# dataframe
for col in policies_df.columns[3:]:
    print(col, ": ", set(policies_df[col]))


# %%
# Fixin some of the inconsistencies such as lower case Y seen in
# previous cell.

# Replacing only single lowercase y to Y
policies_df.replace(to_replace=r'^y$', value="Y", regex=True, inplace=True)


# %%
# Finding which entry has a whitespace
print(
    policies_df[policies_df['Restrict/Close'].str.contains("\s", regex=True,
                                                           na=False)])


# %%
# Reading the policy from entry
list(policies_df["policy"]
     [policies_df['Restrict/Close'].str.contains("\s", regex=True, na=False)])

# %% [markdown]
# Policy doesnt provide enough info so will just fill with NaN in the meantime.

# %%
policies_df['Restrict/Close'].replace("\s", np.nan, inplace=True, regex=True)


# %%
# Re-verifying all unique values
for col in policies_df.columns[3:]:
    print(col, ": ", set(policies_df[col]))


# %%
# Dropping, if any, duplicates that are contained from the first 3 cols
policies_df.drop_duplicates(["date", "State", "policy"], inplace=True)


# %%
# Checking dups of only first 2 cols
policies_df[policies_df.duplicated(["date", "State"], keep=False)]

# %% [markdown]
# There seem to be multiple entries per date,state. Maybe merging them could
# be a good idea.

# %%
print(list(policies_df.columns[2:]))


# %%
print(policies_df.dtypes)


# %%
# Combining data between the date and state columns
# Inspired by
# https://stackoverflow.com/questions/14529838/apply-multiple-functions-to-multiple-groupby-columns

cols = list(policies_df.columns[2:])
dic = {}

for col in cols:
    # Changin datatype to string to avoid issues with nans
    policies_df = policies_df.astype({col: str})
    # Property of joining with commas for the agg
    dic[col] = ",".join

policies_df = policies_df.groupby(["date", "State"]).agg(dic).reset_index()





# %%
# Merging the combined data from before.
# This will make it so that if all are nans then place 0
# but if there is a Y then replace with 1
# this binary approach will make it usable when model
# def reducto(df):
#     dic = {}

#     cols = list(df.columns)[3:]  # Only the columns 4th and forward

#     for col in cols:
#         for val in df[col]:
#             val = val.strip()  # Remove any whitespaces
#             split = val.split(',')  # Split on comma
#             if len(split) > 1:
#                 if "Y" in split:
#                     dic[col] = 'Y'
#                 else:
#                     dic[col] = np.nan
#     return pd.Series(dic, index=cols, dtype=object)
    

    

# policies_df = policies_df.groupby(
#     ["date", "State", "policy"]).apply(reducto).reset_index()

# %%Vectorized method of previous block, more efficient

cols = list(policies_df.columns)[3:]  # Only the columns 4th and forward

for col in cols:

    policies_df[col] = policies_df[col].str.strip()
    
    filter_Y = policies_df[col].str.lower().str.contains('y')
    
    policies_df.loc[filter_Y, col] = 1
    
    policies_df.loc[np.logical_not(filter_Y), col] = 0

# %%
# Counting most common words, inspired by
# https://www.houseninetytwo.com/how-to-use-python-to-extract-keywords-from-sentance-in-dataframe/
common_words = pd.Series(
    ' '.join(policies_df['policy']).split()).value_counts()[:40]
# common_words


# %%
uncommon_words = pd.Series(
    ' '.join(policies_df['policy']).split()).value_counts()[-40:]
# uncommon_words


# %%
# Convert all policies lowercase for case sensitivity, as stopwords are
# lowercase
policies_df['policy'] = policies_df['policy'].str.lower()


# %%
# Stemming OR Lemmatizing words
#stemmer = SnowballStemmer("english")
lemma = nltk.wordnet.WordNetLemmatizer()


def lemmatizing(x):

    words = str(x).split(" ")
    lemd = []

    for word in words:
        lemd.append(lemma.lemmatize(word))

    return " ".join(lemd)


policies_df['policy'] = policies_df['policy'].apply(lemmatizing)


# %%
# Remove duplicate words within the same row, or cell.
tokenizer = nltk.WordPunctTokenizer()


def rem_dup(x):
    #removing commas,periods,semicolons

    x = x.strip(",.;")

    # words = x.split(' ') #splitting words by space
    words = tokenizer.tokenize(x)  # Splitting words by tokenization

    # Stripping words of extra whitespaces
    stripped_words = [word.strip() for word in words]

    # This will only keep unique words/remove duplicate words
    # unique_words = set(stripped_words)
    unique_words = stripped_words # Disabled to test with dups
    
    # Turning the list back to a string
    unique_words_str = " ".join(unique_words)

    return unique_words_str


policies_df['policy'] = policies_df['policy'].apply(rem_dup)


# %%
# list of stop words (i can add more words if necesary)
stop_words = set(stopwords.words('english'))
# stop_words = stop_words.union([""]) #To add custom/extra words
# stop_words


# %%
# Remove useless words using the stop words
policies_df['policy'] = policies_df['policy'].apply(
    lambda x: ' '.join(item for item in x.split() if item not in stop_words))
# policies_df.head(50)


# %%
# Checking for other useless words to remove
def pointless(x):
    words = x.split(" ")
    keep = []

    for word in words:
        # if word has a lenght between...
        if len(word) < 3 and len(word) >= 1:
            continue  # Ignore these words
        else:
            keep.append(word)
    return ' '.join(keep)


policies_df['policy'] = policies_df['policy'].apply(pointless)


# %% Removing special characters from words (hashtags, numbers etc.)


def remove_special(x):
    words = str(x).split(" ")
    stripped = []

    for word in words:
        
        subed_word = re.sub(r'[^A-Za-z]+','',word)
        
        if word != (subed_word):
            print(word)
            print(subed_word)
        
        # Making sure the word has a nelght before appending
        if len(subed_word) == 0:
            pass
        else:
            stripped.append(subed_word)
        
    return ' '.join(stripped)

policies_df['policy'] = policies_df['policy'].apply(remove_special)




# %%
# Adding a word count column
policies_df.insert(3, "word_count", policies_df['policy'].apply(
    lambda x: len(str(x).split(" "))))
policies_df


# %%
# Statistics of word count
policies_df.word_count.describe()


# %%
# Number of words and unique words
total_words = pd.Series(' '.join(policies_df['policy']).split())
print("Total wods: ", len(total_words))
print("Unique Words: ", len(set(total_words)))


# %%
# Creating a violinplot from wordcount
sns.violinplot(y='word_count', data=policies_df)


# %%
# refreshing most common words now that we removed stop words
word_frequency = pd.Series(
    ' '.join(policies_df['policy']).split()).value_counts()
print("Common Words: ", word_frequency.head(15))
print("Uncommon Words: ", word_frequency.tail(15))


# %%
plt.figure(figsize=(15, 4))
plt.xticks(rotation=90)
plt.bar(word_frequency.index[:100], word_frequency[:100])


# %%
plt.figure(figsize=(15, 4))
plt.xticks(rotation=50)
plt.bar(word_frequency.index[-40:], word_frequency[-40:])


# %%
# Creating a wordcloud
wordcloud = WordCloud(width=1600, height=1600, collocations=False,
                      background_color='black').generate(" ".join(total_words))
plt.figure(figsize=(20, 20))
plt.imshow(wordcloud)
plt.show()
# %% Begining vectorization of words

# card_docs = [TaggedDocument(doc.split(' '),[i])
#              for i, doc in enumerate(policies_df.policy)]

# model = Doc2Vec(vector_size=64, min_count=1,epochs=20, window= 2, workers=6)

# model.build_vocab(card_docs)

# model.train(card_docs, total_examples=model.corpus_count, epochs=model.epochs)
# # %%
# card2vec = [model.infer_vector((policies_df['policy'][i].split(' ')))
#             for i in range(0, len(policies_df['policy']))]


# # %%

# corpus = [] # Contains list of cells in policy column

# [corpus.append(doc.split(" ")) for doc in policies_df.policy]

# model = Word2Vec(corpus)

# X = list(model.wv.index_to_key)

# # %%
# print(model.wv.most_similar('death'))

# # %%

# model = Word2Vec(corpus, min_count=1, vector_size=300, workers=6)
# print(model.wv.similarity('death','vaccine'))
# print(model.wv.doesnt_match('covid'))
# print(model.wv.most_similar('distancing'))
# %% TFIDF

# corpus = list(policies_df.policy)



# #countvectorizer = CountVectorizer(analyzer='word',stop_words='english')

# tfidfvectorizer = TfidfVectorizer(analyzer='word',stop_words='english',min_df = 8)

# #count_wm = countvectorizer.fit_transform(corpus)
# tfidf_wm = tfidfvectorizer.fit_transform(corpus)

# #count_tokens = countvectorizer.get_feature_names_out()

# tfidf_tokens = tfidfvectorizer.get_feature_names_out()

# # Renaming some of the tokens
# tfidf_tokens[tfidf_tokens == 'date'] = 'DATE'
# tfidf_tokens[tfidf_tokens == 'policy'] = 'POLICY'

# #print(count_tokens,tfidf_tokens)

# #df_countvect = pd.DataFrame(data =count_wm.toarray(),columns=count_tokens)

# df_tfidfvect = pd.DataFrame(data =tfidf_wm.toarray(),columns=tfidf_tokens)

# %% Word 2 vec

# corpus = [doc.split(" ") for doc in policies_df.policy]

# model = Word2Vec(corpus, min_count=1, vector_size=4)

# model.save('model.bin')

# model = gensim.models.KeyedVectors.load_word2vec_format('model.bin',binary=True)
# %% Check what state has the most policies
# test = policies_df.groupby('State')['word_count'].sum().sort_values()
# New York has the highest word count folloder by connnecticut and colorado.
# This means they are the top contenders for using tfidf for training.

# %% Normalizing values

# %% Doing a PCA to reduce to 3 components

# pca = PCA() 
# principal_components = pca.fit_transform(df_tfidfvect)

# %%

# sns.lineplot(x=np.arange(1,len(pca.explained_variance_ratio_)+1),
#              y=np.cumsum(pca.explained_variance_ratio_))
# plt.title('PCA of TFIDF data (Total info held after X amount of components)')
# plt.ylabel('Explained Variance Sum')
# plt.xlabel('Principal Components')
# plt.plot()

# %% TFIDF per state

def to_tfidf(x):
    
    x = x.reset_index(drop=True)
    
    corpus = x.policy
    
    # countvectorizer = CountVectorizer(analyzer='word',stop_words='english', min_df = 8)
    tfidfvectorizer = TfidfVectorizer(analyzer='word',stop_words='english',min_df = 8)
    
    
    # count_wm = countvectorizer.fit_transform(corpus)
    tfidf_wm = tfidfvectorizer.fit_transform(corpus)

    
    # count_tokens = countvectorizer.get_feature_names_out()
    tfidf_tokens = tfidfvectorizer.get_feature_names_out()

    # # Renaming some of the tokens
    
    # count_tokens[count_tokens == 'date'] = 'DATE'
    # count_tokens[count_tokens == 'policy'] = 'POLICY'
    
    tfidf_tokens[tfidf_tokens == 'date'] = 'DATE'
    tfidf_tokens[tfidf_tokens == 'policy'] = 'POLICY'
    
    
    # df_countvect = pd.DataFrame(data =count_wm.toarray(),columns=count_tokens)
    
    tfidf_df= pd.DataFrame(data = tfidf_wm.toarray(),columns = tfidf_tokens)
    
    # new_x = pd.concat([x,df_countvect],axis=1)
    new_x = pd.concat([x,tfidf_df],axis=1)
    
    
    
    return new_x

policies_df = policies_df.groupby('State').apply(to_tfidf).reset_index(drop=True)


# %% Concattenating

# policies_df[tfidf_tokens] = df_tfidfvect



# policies_df = pd.concat([policies_df,df_tfidfvect], axis=1)
# policies_df = pd.concat([policies_df, pd.DataFrame(principal_components)], axis = 1)




# %%
policies_df.to_csv('.\\policies_cleaned.csv')


# %% Policies Dictionary
# 
#
# No column dictionary was provided in the repository for these.
#
# Making my own
#
# **The following are the primary cols**
#
# date: date it occured
#
# State: string of State
#
# policy: string of actions taken by the state
#
# **The rest are just booleans, of which are mostly either Y or nan**
#
# Restrict/Close: Closure of unesential businesses?
#
# Opening (State): Opened the state to foreigners?
#
# Deferring to County: ?
#
# Testing: Covid testing began?
#
# Education: Physical attendance of education again?
#
# Health/Medical: ?
#
# Emergency Level: ?
#
# Transportation: Public transportation??
#
# Budget: ?
#
# Social Distancing: Social distancing was active?
#
# Other: ?
#
# Vaccine: Vaccines were active?
#
# Opening (County): ?
