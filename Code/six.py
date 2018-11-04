import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from sklearn.externals.six import StringIO
from sklearn import preprocessing
from sklearn import cluster, tree, decomposition

df0 = pd.read_csv('Market Pricing.csv')
df1 = pd.read_csv('Customer Bill Detail.csv')
df2 = pd.read_csv('Customer Order Item Details.csv')

for (i,x) in enumerate(df1['Customer ID']):
    if(x == "UnKnown"):
        df1.at[i,'Customer ID'] = np.nan

for (i,x) in enumerate(df2['Customer ID']):
    if(x == "UnKnown"):
        df2.at[i,'Customer ID'] = np.nan

df0.isnull().sum()
df1.isnull().sum()
df2.isnull().sum()

df1 = df1[(df1['Subtotal']>0)]
df1 = df1[(df1['Total Bill']>0)]

df0.drop_duplicates(inplace=True)
df1.drop_duplicates(inplace=True)
df2.drop_duplicates(inplace=True)

# Remove null customer values for now
df1 = df1[pd.notnull(df1['Customer ID'])]
df2 = df2[pd.notnull(df2['Customer ID'])]

# Taking out the goli dataset from d01
df0 = df0[df0["Restaurant"] == "Goli"].drop("Restaurant",axis = 1)
df0 = df0.reset_index()
df0.drop(df0.columns[0],axis=1,inplace=True)

# Resetting all index

df0 = df0.reset_index()
df0.drop(df0.columns[0],axis=1,inplace=True)
df1 = df1.reset_index()
df1.drop(df1.columns[0],axis=1,inplace=True)
df2 = df2.reset_index()
df2.drop(df2.columns[0],axis=1,inplace=True)

loved = df0["What people love here"][0].replace(" ", "").split(',')
df0.drop("What people love here",axis=1,inplace=True)
df0["Menu Header"].unique()

for (i,x) in enumerate(df2["Dish Name"]):
    if(x == "Aloo Muttor"): df2.loc[i, "Dish Name"] = "Aloo Matar"
    if(x == "Bread Omlette"):df2.loc[i, "Dish Name"] = "Bread Omlatte"
    if(x == "Butter Nan"):df2.loc[i, "Dish Name"] = "Butter Naan"
    if(x == "Butter nan"):df2.loc[i, "Dish Name"] = "Butter Naan"
    if(x == "Lachchha Paratha"):df2.loc[i, "Dish Name"] = "Laccha Paratha"
    if(x == "Punjabi Salad"):df2.loc[i, "Dish Name"] = "Panjabi Salad"
    if(x == "Chicken Leg Afgani 2 pc"):df2.loc[i, "Dish Name"] = "Chicken Leg Afgani [2 Pieces]"
    if(x == "Chicken Leg Malai 2 pc"):df2.loc[i, "Dish Name"] = "Chicken Leg Malai [2 Pieces]"
    if(x == "Chicken Lollypop (6 pc)"):df2.loc[i, "Dish Name"] = "Chicken Lollipop [6 Pieces]"
    if(x == "Chicken Lollypop (6 pc)"):df2.loc[i, "Dish Name"] = "Dal Tadka"
    if(x == "Bhindi masala"):df2.loc[i, "Dish Name"] = "Bhindi Masala"
    if(x == "Dal tadhka"):df2.loc[i, "Dish Name"] = "Dal Tadka"
    if(x == "Garlic Nan"):df2.loc[i, "Dish Name"] = "Garlic Naan"
    if(x == "Muttor Paneer"):df2.loc[i, "Dish Name"] = "Matar Paneer"
    if(x == "Mutton Bati"):df2.loc[i, "Dish Name"] = "Mutton Boti"
    if(x == "Omlette"):df2.loc[i, "Dish Name"] = "Omlatte"
    if(x == "Muttor Pulav"):df2.loc[i, "Dish Name"] = "Matar Pulav"
    if(x == "Plain nan"):df2.loc[i, "Dish Name"] = "Plain Naan"
    if(x == "Veg pulav"):df2.loc[i, "Dish Name"] = "Veg Pulav"

# Merging df2 and df1 based on bill number 
# Merginf df2 and df0 based on dish name
df2 = pd.merge(df1, df2, on='Bill Number', how='right')
df0 = df0.rename(columns={"Menu Item" : "Dish Name"})
df2 = pd.merge(df0, df2, on='Dish Name', how='right')
# Drop duplicate columns
df2 = df2.drop(["Customer ID_y","Date_y"],axis =1)
df2 = df2.rename(columns={"Customer ID_x" : "Customer ID","Date_x" : "Date"})

# Creating a fav here column 
df2["FavouriteHere"] = np.nan
for (i,x) in enumerate(df2["Dish Name"]):
    if(x.replace(" ", "") in loved): 
        df2.loc[i,"FavouriteHere"] = 1
    else: 
        df2.loc[i,"FavouriteHere"] = 0
df2["Total On Food"] = df2["Subtotal"] + df2["Discount"]

# Some more preprocessing to fill up the rate column
df2['Rate'] = df2['Rate'].apply(pd.to_numeric)
df2["Subtotal"] = df2["Subtotal"].apply(pd.to_numeric)
df2["Discount"] = df2["Discount"].apply(pd.to_numeric)
df2["Total On Food"] = df2["Total On Food"].apply(pd.to_numeric)

def priceComp(row):
    for i in range(1,26):
        if((row["Dish Name"]+" (QTY-" + str(i) + ".000)") == row["Dish Details"]):
            row["Rate"] = row["Total On Food"]/i
            break
    return row
# Prices which are known from the excel sheet but not filled due to glitch  

df2 = df2.apply(priceComp,axis = 1)

df2.loc[df2["Dish Name"] == "Tandoori Roti","Rate"] = 12
df2.loc[df2["Dish Name"] == "Butter Naan","Rate"] = 25
df2.loc[df2["Dish Name"] == "Bati","Rate"] = 30
df2.loc[df2["Dish Name"] == "Benjo","Rate"] = 50
df2.loc[df2["Dish Name"] == "rajma rice","Rate"] = 100
df2.loc[df2["Dish Name"] == "Tea","Rate"] = 10

#df2.to_csv("NewBeginning.csv") 
#df2 = pd.read_csv("NewBeginning.csv")
#df2.drop(df2.columns[0], axis=1,inplace = True)

def completeMenuHeader(row):
    for (i,x) in enumerate(df0["Dish Name"]):
        if(row["Dish Name"].lower() in x.lower()):
            row["Menu Header"] = df0.loc[i,"Menu Header"]
    return row

df2 = df2.apply(completeMenuHeader,axis = 1)

# Analysis for revenue increse

df2.groupby("Menu Header")["Rate"].agg({"Total amount spent":"sum"})
x = df2.groupby("Dish Name")["Quantity"].agg({"Total amount spent":"sum"})
x = df2.groupby("Channel")["Quantity"].agg({"Total amount spent":"sum"})


df2["month"] = np.nan
def month(row):
    row["month"] = row["Date"].split('-')[1]
    return row
    
df2 = df2.apply(month,axis = 1)

r = df2[df2["month"] != '09']
x = r.groupby(["Dish Name","month"])["Quantity"].agg({"Total times bought":"sum"}).reset_index().groupby("Dish Name")["Total times bought"].agg({"sum":"sum"}).reset_index().sort_values(by='sum')
x.to_csv("sol4")

r = df2[df2["month"] == '08']
x = df2.groupby("Channel")["Total Bill"].agg({"Total amount spent":"sum"})


# Customer Segmentation start
# Remove the unnecessary columns

df2.drop(['Rate', 'Date', 'Subtotal'],inplace=True,axis = 1)
df2.drop(['Total On Food'],inplace=True,axis = 1)
df2.loc[df2["Channel"]=="-","Channel"] = "Store"
df2.drop(["Bill Number"],axis = 1,inplace=True)
df2.drop(["Dish Details"],axis = 1,inplace=True)
df2 = df2.dropna()
df2 = df2.reset_index()
df2.drop(df2.columns[0],axis=1,inplace=True)



# encoding
EncodingScheme = pd.DataFrame()
encoding_schemes = []
from sklearn import preprocessing
for x in df2.columns:
    if((type(df2[x][0]) != np.int64 and (x != "Customer ID")) and (x != "Discount" and x!="Delivery Amt" and x!= "Total Bill")):
        le = preprocessing.LabelEncoder()
        df2[x] = le.fit_transform(df2['Menu Header'].astype(str))
        encoding_schemes.append((df2[x],le.classes_))
# Based on spending amount

customerGroupsSpend =df2.groupby(['Customer ID','Dish Name','Type',])['Quantity'].agg({'Total per Customer':'sum'}).reset_index().dropna(axis=0)
customerGroupsSpend= pd.merge(df2,customerGroupsSpend,on='Customer ID',how='left')

customerGroupsSpendStd = customerGroupsSpend.copy()
for i in customerGroupsSpendStd.columns:
    if(i != "Customer ID"):
        customerGroupsSpendStd[i] = preprocessing.scale(customerGroupsSpendStd[i])

num_col = ['Type','Dish Name','Total per Customer']

from sklearn.cluster import KMeans
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
    kmeans.fit(customerGroupsSpendStd[num_col])
    wcss.append(kmeans.inertia_)
plt.plot(range(1, 11), wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

# based on elbow method we take number of clusters as 8 for total bill and 
# 5 for segmentation according to dish type. have to check and see

km = cluster.KMeans(n_clusters=5, max_iter=300, random_state=None)
customerGroupsSpendStd['cluster'] = km.fit_predict(customerGroupsSpendStd[num_col])

# Principle component analysis

pca = decomposition.PCA(n_components=2, whiten=True)
pca.fit(customerGroupsSpend[num_col])
customerGroupsSpendStd['x'] = pca.fit_transform(customerGroupsSpendStd[num_col])[:, 0]
customerGroupsSpendStd['y'] = pca.fit_transform(customerGroupsSpendStd[num_col])[:, 1]
plt.scatter(customerGroupsSpendStd['x'], customerGroupsSpendStd['y'], c=customerGroupsSpendStd['cluster'])
plt.show()
# Customer groups according to total bill

 customerGroupsSpendStd[['Customer ID','cluster']].to_csv("sol6part1.csv")
# Convert to python style
 

# Customer Segmentation new method
import datetime as dt
NOW = dt.datetime(2018,9,22)
df2['Date'] = pd.to_datetime(df2['Date'])

df1 = df1[["Total Bill","Bill Number"]]
df2 = pd.merge(df1, df2, on='Bill Number', how='right')
df2 = df2[["Date","Bill Number","Total Bill","Customer ID"]]
df2.isnull().sum()
df2.nunique()
# Calculating based RFM metric
# RECENCY (R): Days since last purchase. This is the number of days between the present day and today
temp = df2.groupby("Customer ID")["Date"].agg({'Recency': lambda x: (NOW - x.max()).days})
temp.nunique()
