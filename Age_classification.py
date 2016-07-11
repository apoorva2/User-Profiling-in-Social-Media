import pandas as pd
import csv
from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import train_test_split
from sklearn.metrics import mean_squared_error
import random
from sklearn.ensemble import RandomForestClassifier
from math import sqrt
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


# read profile data into dataframe
data1 = pd.read_csv("C:\\Users\\swetha Ch\\Desktop\\FacebookDataTCSS555Project\\TCSS555\\Train\\profile\\profile.csv", index_col=0)
# read LIWC data into a DataFrame
data2 = pd.read_csv('C:\\Users\\swetha Ch\\Desktop\\FacebookDataTCSS555Project\\TCSS555\\LIWC.csv', index_col=1)

merged = pd.merge(left=data1,right=data2, how='left',left_on='userid',right_on= 'userId')

print(merged.head(5))
ageCat = 0
for i in range(len(merged)):
    #print(merged.iloc[i].age)
    a=merged.iloc[i].age
    if a <=24:
        ageCat = 1
    elif a >= 25 and a <=34:
        ageCat = 2
    elif a >= 35 and a <=49:
        ageCat = 3
    elif a >= 50 :
        ageCat = 4
    else: print ("invalid age group")
        #print ("ageCat", ageCat)
    merged.loc[i,'age'] = ageCat
    #print(merged.iloc[i].age)

merged_train, merged_test = train_test_split(merged, test_size = 0.2)
print(len(merged_train),len(merged_test))
#merged.to_csv("C:\\Users\\swetha Ch\\Desktop\\FacebookDataTCSS555Project\\TCSS555\\output.csv", index=False)

feature_cols = ['WC', 'WPS', 'Sixltr', 'Dic', 'Numerals', 'funct', 'pronoun', 'ppron', 'i', 'we', 'you', 'shehe', 'they', 'ipron', 'article', 'verb', 'auxverb', 'past', 'present', 'future', 'adverb', 'preps', 'conj', 'negate', 'quant', 'number', 'swear', 'social', 'family', 'friend', 'humans', 'affect', 'posemo', 'negemo', 'anx', 'anger', 'sad', 'cogmech', 'insight', 'cause', 'discrep', 'tentat', 'certain', 'inhib', 'incl', 'excl', 'percept', 'see', 'hear', 'feel', 'bio', 'body', 'health', 'sexual', 'ingest', 'relativ', 'motion', 'space', 'time', 'work', 'achieve', 'leisure', 'home', 'money', 'relig', 'death', 'assent', 'nonfl', 'filler', 'Period', 'Comma', 'Colon', 'SemiC', 'QMark', 'Exclam', 'Dash', 'Quote', 'Apostro', 'Parenth', 'OtherP', 'AllPct']

target_age = merged_train.age
train = merged_train[feature_cols]
target_gen = merged_train.gender

rf = RandomForestClassifier(n_estimators=100)
rf.fit(train, target_age)

test = merged_test[feature_cols]
prediction = []
actual = []

for i in range(len(merged_test)):
    x = rf.predict(test.iloc[i])
    prediction.append(x)
    y = merged_test.iloc[i].age
    actual.append(y)

pscore = metrics.accuracy_score(actual, prediction)
print('accuracy_age', pscore)

rf.fit(train, target_gen)

test = merged_test[feature_cols]
prediction = []
actual = []

for i in range(len(merged_test)):
    x = rf.predict(test.iloc[i])
    prediction.append(x)
    y = merged_test.iloc[i].gender
    actual.append(y)

pscore = metrics.accuracy_score(actual, prediction)
print('accuracy_gen', pscore)