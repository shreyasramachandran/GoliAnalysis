import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.externals.six import StringIO
from sklearn import preprocessing
from sklearn import cluster, tree, decomposition
import itertools

# Loading the datasets
df0 = pd.read_csv('Market Pricing.csv')
df1 = pd.read_csv('Customer Bill Detail.csv')
df2 = pd.read_csv('Customer Order Item Details.csv')

# Taking out the goli dataset from d01

df0 = df0[df0["Restaurant"] == "Goli"].drop("Restaurant",axis = 1)
df0 = df0.reset_index()
df0.drop(df0.columns[0],axis=1,inplace=True)

# Replace Unknown will null

for (i,x) in enumerate(df1['Customer ID']):
    if(x == "UnKnown"):
        df1.at[i,'Customer ID'] = np.nan

for (i,x) in enumerate(df2['Customer ID']):
    if(x == "UnKnown"):
        df2.at[i,'Customer ID'] = np.nan
        
# Check for null values
df0.isnull().sum()
df1.isnull().sum()
df2.isnull().sum()


# Subtotal and total bill cannot be 0
df1 = df1[(df1['Subtotal']>0)]
df1 = df1[(df1['Total Bill']>0)]

# Drop Duplicates
df0.drop_duplicates(inplace=True)
df1.drop_duplicates(inplace=True)
df2.drop_duplicates(inplace=True)

# Checking if the number of bill entries and customerID match
df0.nunique()
df1.nunique()
df2.nunique()

# As we are performing customer Segmentation remove the Unknown Customers
df1 = df1[pd.notnull(df1['Customer ID'])]
df2 = df2[pd.notnull(df2['Customer ID'])]

# Data Preprocessing.df0
# Take out what people love at this retuarant
loved = df0["What people love here"][0].replace(" ", "").split(',')
df0.drop("What people love here",axis=1,inplace=True)
df0["Menu Header"].unique()
# index number 4,5,6,7,8,9 dishes have are there on two course menus. We keep only one
df0.drop(df0.index[[4,5,6,7,8,9]],inplace=True)
list(set(df0["Menu Item"]).intersection(set(df2["Dish Name"])))

df1.drop(["Date","Customer ID"],axis = 1,inplace=True)

df2 = pd.merge(df1, df2, on='Bill Number', how='right')

"""
# combining df2 and df1
df2["Type"] = np.nan
df2["Total Bill"] = np.nan
df2["Channel"] = np.nan

for x in df1["Bill Number"]:
    df2.loc[df2["Bill Number"] == x, "Channel"] = df1.loc[df1["Bill Number"] == x,"Channel"].values[0]
    df2.loc[df2["Bill Number"] == x, "Total Bill"] = df1.loc[df1["Bill Number"] == x,"Total Bill"].values[0]
    df2.loc[df2["Bill Number"] == x, "Type"] = df1.loc[df1["Bill Number"] == x,"Type"].values[0]
"""
  
# Creating new columns
# Total Times Ordered(count),publicHoliday,FavouriteHere
# df2.drop(["Bill Number"],axis=1,inplace=True)
df2 = df2.merge(df2.groupby('Dish Name')['Quantity'].agg(['count']).reset_index())
df2["FavouriteHere"] = np.nan
for (i,x) in enumerate(df2["Dish Name"]):
    if(x.replace(" ", "") in loved): 
        df2.loc[i,"FavouriteHere"] = 1
    else: 
        df2.loc[i,"FavouriteHere"] = 0
    
""" New Dataset """ 
#df2.to_csv("NewOCD.csv", sep='\t') 
#df2 = pd.read_csv('New1.csv',sep='\t')
#df2.drop(df2.columns[0], axis=1,inplace = True)
df0 = df0.reset_index()
df0.drop(df0.columns[0], axis=1,inplace = True)

# Items not in the menu provided by df0. Remove the entries
#list2 = []
#y = []
#for x in df0["Menu Item"]:
#    y.append(x.replace(" ", ""))
#for x in set(df2["Dish Name"]):
#        if(x.replace(" ", "") not in y):
#          list2.append(x)  

# Correcting certain entries
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

#q = set(df0["Menu Item"])
#df2["Price"] = np.nan
#df2["Menu Header"] = np.nan

for (i,x) in enumerate(df2["Dish Name"]):
    if(x in q): 
        df2.loc[i, "Price"] = df0.loc[df0["Menu Item"] == x,"Rate"].values[0]
        df2.loc[i, "Menu Header"] = df0.loc[df0["Menu Item"] == x,"Menu Header"].values[0]

one = list(set( df2[df2['Price']]["Dish Name"] ) )
two = list(set(df0["Menu Item"]))

three = list(set(one) - set(two))
# Search for three entries in two. and pick out a list of two entries similar to three

df2['Price'] = df2['Price'].apply(pd.to_numeric)
df2["Subtotal"] = df2["Subtotal"].apply(pd.to_numeric)

def priceComp(row):
    for i in range(1,26):
        if((row["Dish Name"]+" (QTY-" + str(i) + ".000)") == row["Dish Details"]):
            row["Price"] = row["Subtotal"]/i
            break"
    return row

temp = df2.loc[:,["Dish Name","Price"]]
temp.dropna(inplace = True)
temp.drop_duplicates("Dish Name",inplace = True)

"""
# Get a list of all half/full entries
f = list(df0["Menu Item"])
hf = []
for x in f: 
    if(("half" in x.lower()) or ("full" in x.lower())):
        hf.append(x)
hf = list(set(f)-set(hf))
"""
def pc(row):
    a = row["Dish Name"]
    if((a in list(temp["Dish Name"])) and (a in hf)):
        row["Price"] = temp[temp["Dish Name"] == a]["Price"].values[0]    
    return row


df2 = df2.apply(priceComp,axis = 1)
df2.isnull().sum()


temp = df2.loc[:,["Dish Name","Price"]]
temp.dropna(inplace = True)
temp = set(temp["Dish Name"])
temp = list(temp)
three = list(set(one) - set(temp))

temp2 = df2[pd.notnull(df2['Price'])].drop_duplicates("Dish Name")
temp2 = temp2.reset_index()
temp2.drop(temp2.columns[0],axis=1,inplace=True)
temp3List = []

for (i,x) in enumerate(temp2["Dish Name"]):
    if(("maggi" in x) or("water" in x) or ("Paratha" in x) or("Roti" in x)):
        temp3List.append((x,temp2.loc[i, "Price"]))

temp4List= []
def smc(row):
    if(np.isnan(row["Price"])):
        for x in temp3List:
            if(row["Dish Name"] in x[0]):
                row["Price"] = x[1]
    return row           
df2 = df2.apply(smc,axis = 1)

r = pd.merge(df2,df2.groupby('Bill Number')['Quantity'].agg(['count']).reset_index(),on='Bill Number', how='left')
r = r[r["count_y"] != 1]
r.drop(r.columns[0],axis=1,inplace=True)
r.isnull().sum()

def allEntries(entry = []):
    similarEnt = [];
    for x in entry:
        for (i,y) in enumerate(df0["Menu Item"]):
            if(x[0] in y):
                similarEnt.append((y,df0.loc[i,"Rate"],x[1]))
    return similarEnt

r = r.reset_index()
r = r.drop('index',axis =1)

for x in set(r["Bill Number"]):
    entries = r[r["Bill Number"] == 20083935920]
    entries = entries.reset_index()
    entries = entries.drop('index',axis =1)
    subtotal = r[r["Bill Number"] == 20083935920]["Subtotal"].values[0]
    items = r[r["Bill Number"] == 20083935920].loc[:,["Dish Name","Quantity"]]
    number = r[r["Bill Number"] == 20083935920]["count_y"].values[0]
    for (i,y) in enumerate(entries["Price"]):
        if(not np.isnan(y)):
            number = number - 1
            subtotal = subtotal - (int(entries.loc[i,"Quantity"]) * int(entries.loc[i,"Price"]))
            dish = entries.loc[i,"Dish Name"]
            items = items[items["Dish Name"] != dish]
    items = items.values.tolist()
    se = allEntries(items)
    combinations = itertools.combinations(se, number)  
    subs = []    
    # Append those according to the quantity of the items
    for subset in combinations:
        subs.append(subset)
    # Now calculate which subset sum is closest to subtotal
    # closest = subs[0]
    closeness = 10000
    for z in subs: 
        temp = abs(subtotal - sum(int((zx[1])*int(zx[2])) for zx in z))
        if(temp < closeness):
            closest = z
            closeness = temp
    print((x,closest))

# df2.to_csv("df234.csv")
# r.to_csv("r.csv")  
    
k = []    
for (i,x) in enumerate(df2["Price"]):
    if(np.isnan(x)):
        k.append(df2.loc[i,"Dish Name"])
k = pd.DataFrame(k)
k= k.drop_duplicates()
        
    

df2 = df2.reset_index()
df2.drop(df2.columns[0],axis=1,inplace=True)