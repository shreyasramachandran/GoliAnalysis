import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df1 = pd.read_csv('Customer Bill Detail.csv')
df2 = pd.read_csv('Customer Order Item Details.csv')

# Replace Unknown will null

for (i,x) in enumerate(df1['Customer ID']):
    if(x == "UnKnown"):
        df1.at[i,'Customer ID'] = np.nan

for (i,x) in enumerate(df2['Customer ID']):
    if(x == "UnKnown"):
        df2.at[i,'Customer ID'] = np.nan

df1.isnull().sum()
df2.isnull().sum()

# As we are performing customer segmentation no need for UnKnown values in CustomerID

df1 = df1[pd.notnull(df1['Customer ID'])]
df2 = df2[pd.notnull(df2['Customer ID'])]

df1.nunique()
df1.min()

df2.nunique()
df2.min()

# Subtotal and total bill cannot be 0
df1 = df1[(df1['Subtotal']>0)]
df1 = df1[(df1['Total Bill']>0)]

# Drop Duplicates, if any
df1.drop_duplicates(inplace=True)
df2.drop_duplicates(inplace=True)

# Customer Segmentation begin.
# By the amount they spend
# Total amount already includes Discount,Subtotal,Delivery Amt so remove the three
# No need for channel as home delivery already includes that
df1.drop(['Discount','Subtotal','Delivery Amt','Channel'],axis = 1, inplace = True)

# Merge df1 and df2 
df2["Type"] = np.nan
df2["Total Bill"] = np.nan

for x in df1["Bill Number"]:
    df2.loc[df2["Bill Number"] == x, "Channel"] = df1.loc[df1["Bill Number"] == x,"Channel"].values[0]
    df2.loc[df2["Bill Number"] == x, "Total Bill"] = df1.loc[df1["Bill Number"] == x,"Total Bill"].values[0]
    df2.loc[df2["Bill Number"] == x, "Type"] = df1.loc[df1["Bill Number"] == x,"Type"].values[0]
    
# df2.to_csv("New.csv", sep='\t')
df2 = pd.read_csv('New.csv',sep='\t')
df2.drop(df2.columns[0], axis=1,inplace = True)


# now recency is calculated relative. So we compare the min date with 01-06-2018(Starting date)

EncodingScheme = pd.DataFrame()
# Encoding the data and storing the encoding scheme
from sklearn import preprocessing
for x in df2.columns:
    if(type(df2[x][0]) != np.int64):
        le = preprocessing.LabelEncoder()
        df2[x] = le.fit_transform(df2[x])
        # EncodingScheme[x] = le.classes_
    

# Customer Segmentation according to grouping
dish_group = {}
unique_dishes = df2["Dish Name"].unique()
for x in unique_dishes:
    CusWhoOrdered = df2.loc[df2["Dish Name"] == x,"Customer ID"]
    TotalTimesOrdered =  df2.loc[df2["Dish Name"] == x,"Quantity"].sum()
    dish_group.setdefault(x,{})
    dish_group[x].update({'CustomerID': CusWhoOrdered , 'TotalTimesOrdered': TotalTimesOrdered})

X = df2.iloc[:, [3, 4]].values


# New Method
df0 = pd.read_csv('Market Pricing.csv')
# Take out the goli resturant entries
df0 = df0[df0["Restaurant"] == "Goli"].drop("Restaurant",axis = 1)

df0.drop_duplicates(inplace=True)
df0["Menu Item"].nunique()
df2["Dish Name"].nunique()

l = pd.crosstab(df2['Dish Name'], df2['Quantity'])
df2.groupby('Dish Name')['Quantity'].sum()
df2 = df2.merge(df2.groupby('Dish Name')['Quantity'].agg(['count']).reset_index())

# comparing different dishes

k=df2.groupby('Dish Name')['Quantity']\
    .agg({'AverageOrderTimes': 'mean', 'TotalOrderTimes': 'sum'})\
    .reset_index()\
    .sort_values(by='AverageOrderTimes')
    
df2.drop(["Bill Number","Customer ID"],axis = 1,inplace=True)
df2.drop(["count"],axis = 1,inplace=True)

from sklearn.externals.six import StringIO
from sklearn import preprocessing
from sklearn import cluster, tree, decomposition

km = cluster.KMeans(n_clusters=3, max_iter=300, random_state=None)
df2['cluster'] = km.fit_predict(df2)

