# %%
import pandas as pd
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
import glob
import numpy as np
import matplotlib.pyplot as plt
import re
import nltk

#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
#nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer
import seaborn as sns
from wordcloud import WordCloud
#import snowballstemmer

# Importing, merging, and creating a column containing the state of policies.

# %%
policies_path = ".\\CCI_C-19_Policies\\data_tables\\policy_data\\table_data\\Current\\"
policies_files = glob.glob(policies_path + "*.csv")

content = [] #store contents from files

for filepath in policies_files:
    
    df = pd.read_csv(filepath, index_col=None)
    #Stripping the string to store the name of the file to a State column
    #State column should be the second column
    df.insert(1,"State", filepath.replace(policies_path,"").replace("_policy.csv",""))
    content.append(df)


policies_df = pd.concat(content)

# %%
# Getting all unique values from the columns after "policy" columns in the dataframe
for col in policies_df.columns[3:]:
    print(col,": ",set(policies_df[col]))


# %%
# Fixin some of the inconsistencies such as lower case Y seen in
# previous cell.

# Replacing only single lowercase y to Y
policies_df.replace(to_replace=r'^y$',value="Y",regex=True,inplace=True)


# %%
# Finding which entry has a whitespace
print(policies_df[policies_df['Restrict/Close'].str.contains("\s", regex=True, na=False)])


# %%
# Reading the policy from entry
list(policies_df["policy"][policies_df['Restrict/Close'].str.contains("\s", regex=True, na=False)])

# %% [markdown]
# Policy doesnt provide enough info so will just fill with NaN in the meantime.

# %%
policies_df['Restrict/Close'].replace("\s", np.nan ,inplace=True,regex=True)


# %%
# Re-verifying all unique values
for col in policies_df.columns[3:]:
    print(col,": ",set(policies_df[col]))


# %%
# Dropping, if any, duplicates that are contained from the first 3 cols
policies_df.drop_duplicates(["date","State","policy"], inplace=True)


# %%
# Checking dups of only first 2 cols
policies_df[policies_df.duplicated(["date","State"], keep= False)]

# %% [markdown]
# There seem to be multiple entries per date,state. Maybe merging them could be a good idea.

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

policies_df = policies_df.groupby(["date","State"]).agg(dic).reset_index()


# %%
#policies_df


# %%
# Merging the combined data from before.
# This will make it so that if all are nans then just leave nan
# but if there is a Y then replace with Y

def reducto(df):
    dic = {}
    
    cols = list(df.columns)[3:] #Only the columns 4th and forward
    
    for col in cols:
        for val in df[col]:
            val = val.strip()#Remove any whitespaces
            split = val.split(',')#Split on comma
            if len(split) > 1:
                if "Y" in split:
                    dic[col] = "Y"
                else:
                    dic[col] = np.nan
    return pd.Series(dic, index=cols, dtype = object)

policies_df = policies_df.groupby(["date","State","policy"]).apply(reducto).reset_index()  


# %%
# Counting most common words, inspired by
# https://www.houseninetytwo.com/how-to-use-python-to-extract-keywords-from-sentance-in-dataframe/
common_words = pd.Series(' '.join(policies_df['policy']).split()).value_counts()[:40]
# common_words


# %%
uncommon_words = pd.Series(' '.join(policies_df['policy']).split()).value_counts()[-40:]
# uncommon_words


# %%
# Convert all policies lowercase for case sensitivity, as stopwords are lowercase
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
    x = x.strip(",.;") #replace(",","").replace(".","").replace(";","")#removing commas,periods,semicolons
     
    #words = x.split(' ') #splitting words by space
    words = tokenizer.tokenize(x)# Splitting words by tokenization
    
    #Stripping words of extra whitespaces
    stripped_words = [word.strip() for word in words]
    
    unique_words = set(stripped_words) #This will only keep unique words/remove duplicate words
        
    unique_words_str = " ".join(unique_words) #Turning the list back to a string
    
    return unique_words_str
    
policies_df['policy'] = policies_df['policy'].apply(rem_dup)


# %%
#list of stop words (i can add more words if necesary)
stop_words = set(stopwords.words('english'))
# stop_words = stop_words.union([""]) #To add custom/extra words
#stop_words


# %%
# Remove useless words using the stop words
policies_df['policy'] = policies_df['policy'].apply(lambda x: ' '.join(item for item in x.split() if item not in stop_words))
#policies_df.head(50)


# %%
# Checking for other useless words to remove
def pointless(x):
    words = x.split(" ")
    keep = []
    
    for word in words:
        #if word has a lenght between...
        if len(word) < 3 and len(word) >= 1:
            continue #Ignore these words
        else:
            keep.append(word)
    return ' '.join(keep)
    
policies_df['policy'] = policies_df['policy'].apply(pointless)


# %%
# Removing special characters from words (hashtags, numbers etc.)

# def remove_special(x):
#     words = str(x).split(" ")
#     stripped = []
    
#     for word in words:
# #         print(word)
# #         print(re.sub(r'[^A-Za-z]+','',word))
        
#         if word != (re.sub(r'[^A-Za-z]+','',word)):
#             print(word)
#             print(re.sub(r'[^A-Za-z]+','',word))
#         #stripped.append(re.sub(r'A-Za-z]+','',word))

# policies_df['policy'].apply(remove_special)

# Not applying because the changes might be too altering.


# %%
# Adding a word count column
policies_df.insert(3, "word_count", policies_df['policy'].apply(lambda x: len(str(x).split(" "))))
policies_df


# %%
# Statistics of word count
policies_df.word_count.describe()


# %%
# Number of words and unique words
total_words = pd.Series(' '.join(policies_df['policy']).split())
print("Total wods: ",len(total_words))
print("Unique Words: ",len(set(total_words)))


# %%
# Creating a violinplot from wordcount
sns.violinplot(y = 'word_count',data = policies_df)


# %%
#refreshing most common words now that we removed stop words
word_frequency = pd.Series(' '.join(policies_df['policy']).split()).value_counts()
print("Common Words: ",word_frequency.head(15))
print("Uncommon Words: ",word_frequency.tail(15))


# %%
plt.figure(figsize=(15,4))
plt.xticks(rotation=90)
plt.bar(word_frequency.index[:100], word_frequency[:100])


# %%
plt.figure(figsize=(15,4))
plt.xticks(rotation=50)
plt.bar(word_frequency.index[-40:], word_frequency[-40:])


# %%
#Creating a wordcloud
wordcloud = WordCloud(width=1600,height=1600,collocations=False,background_color='black').generate(" ".join(total_words))
plt.figure(figsize=(20,20))
plt.imshow(wordcloud)


# %%
# Splitting into train,val,test

# %% [markdown]
# #### Policies Dictionary
# 
# No column dictionary was provided in the repository for these. Will make my own.
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
