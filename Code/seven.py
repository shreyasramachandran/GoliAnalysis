import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import itertools

df0 = pd.read_csv('Market Pricing.csv')
df1 = pd.read_csv('Customer Bill Detail.csv')
df2 = pd.read_csv('Customer Order Item Details.csv')

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

def completeMenuHeader(row):
    for (i,x) in enumerate(df0["Dish Name"]):
        if(row["Dish Name"].lower() in x.lower()):
            row["Menu Header"] = df0.loc[i,"Menu Header"]
    return row

# Keep only the relevant ones for combos

df2.drop(['Rate', 'Type', 'Date','Discount', 'Subtotal', 'Delivery Amt', 'Total Bill', 'Channel','Customer ID', 'Dish Details','Total On Food'],inplace=True,axis = 1)

r = df2.apply(completeMenuHeader,axis = 1)
r.to_csv("sol5.csv")  
# Made some changes to the excel file reloading it
r = pd.read_csv("sol5.csv")
r.drop(r.columns[0],axis=1,inplace=True)

# Most sold and weakest
msw = df2.groupby('Dish Name')['Quantity']\
    .agg({'TotalOrderTimes': 'sum'})\
    .reset_index()\
    .sort_values(by='TotalOrderTimes')
# famous and non-famous combination

# According to Menu Header
    
mh = r.groupby('Menu Header')['Quantity']\
    .agg({'TotalOrderTimes': 'sum'})\
    .reset_index()\
    .sort_values(by='TotalOrderTimes')
# plot a graph here

bt = r.groupby('Bill Number')
r = r.reset_index()
r.drop(r.columns[0],axis=1,inplace=True)

# to calculate the most two dishes ordered together
dishes = r["Dish Name"].unique().tolist()
dishesCombo = itertools.combinations(dishes, 2)
combos = []    
for subset in dishesCombo:
    combos.append(subset)
combosList = []
for x in combos:
    count = 0
    for y in df1["Dish Details"]:
        if((x[0] in y) and (x[1] in y)):
            count = count+1
    combosList.append((x,count))
combosList = pd.DataFrame(combosList)

combosList.to_csv("comboList.csv") 