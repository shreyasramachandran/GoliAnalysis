import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Calculating market competativeness

df0 = pd.read_csv('Market Pricing.csv')
# Remove null values 
df0 = df0[pd.notnull(df0['Rate'])]
df0 = df0[pd.notnull(df0['Menu Item'])]
df0.drop_duplicates(inplace=True)
df0 = df0.reset_index()
df0.drop(df0.columns[0],axis=1,inplace=True)


# To see which are the items similar in other resturants compared to goli
goli = df0[df0["Restaurant"] == "Goli"].drop("Restaurant",axis = 1)
goli.drop_duplicates("Menu Item",inplace=True)
goli = goli.reset_index()
goli.drop(goli.columns[0],axis=1,inplace=True)

# Remove goli from df0
df0 = df0[df0["Restaurant"] != "Goli"].drop("Restaurant",axis = 1)
df0 = df0.reset_index()
df0.drop(df0.columns[0],axis=1,inplace=True)



"""
temp = []
for (i,x) in enumerate(df0["Menu Item"]):
    if(("Chicken" in x) and ("Curry" in x)):
        temp.append((x,df0.loc[i,"Rate"]))

temp1 = set(df0["Restaurant"])
temp1.remove("Goli")

# Creating the entry rows in goli for 
goli = pd.concat([goli,pd.DataFrame(columns=temp1)],sort = False)
"""
"""
# Checking the average price of a resturant

k = df0.groupby('Restaurant')['Rate']\
    .agg({'Average': 'mean', 'Total': 'sum'})\
    .reset_index()

df0['Rate'].unique()
"""

# Remove the NOT FOUND ones and MRP ones(generally contain cold drinks and mineral water not much use in analysis)
df0 = df0[(df0["Rate"] != "NOT FOUND")]
df0 = df0.reset_index()
df0.drop(df0.columns[0],axis=1,inplace=True)

df0 = df0[(df0["Rate"] != "MRP")]
df0 = df0.reset_index()
df0.drop(df0.columns[0],axis=1,inplace=True)

# Take out the ones with "/" in rate, saperate them into entries, merge with the original dataset.
trial = []
index = []
for (i,x) in enumerate(df0["Rate"]):
    if(("/" in x)):
        trial.append(df0.loc[i])
        index.append(i)

df0.drop(df0.index[index],inplace=True)
df0 = df0.reset_index()
df0.drop(df0.columns[0],axis=1,inplace=True)

# Compare differnt price distributions
df0['Rate'] = df0['Rate'].apply(pd.to_numeric)
overall_price_dist = df0.groupby('Restaurant')['Rate']\
    .agg({'Average': 'mean', 'Total': 'sum' ,})\
    .reset_index()

menu_price_dist = df0.groupby('Menu Header')['Rate']\
    .agg({'Average': 'mean', 'Total': 'sum'})\
    .reset_index()
    
# take out the items similar to goli items. For our analysis we consider variations also to be of the 
# same group and full and half to be different
"""
Rules for taking out the similar items.
1. Consider the first two words of the goli item entry
2. If similar matches are found. Check for full or half word in goli item entry
3. If full or half is present in goli item entry then check for the words in the similar matches
4. Divide according to full and half if required
5. Now check the remaining entries. 
6. To label the remaining entries as full or half consider the price of rest of the similar matches
"""

rate_list = {}
#averageDishPrice = []
priceIndex = [] 
def splitWord(row):
    # print(type(float(row["Rate"])))
    rate_list.setdefault(row["Menu Item"].lower(),{})
    temp = row["Menu Item"].lower().split(' ')    
    tempList = []
    itemPrice = float(row["Rate"])
    dish = row["Menu Item"]
    for (i,x) in enumerate(df0["Menu Item"]):
        x = x.lower()
        if(len(temp)>1):
            if((temp[0] in x) and (temp[1] in x)):
                tempList.append((x,df0.loc[i,"Rate"]))
        else:
            if(temp[0] in x):
                tempList.append((x,df0.loc[i,"Rate"]))
    # Remove the full entries from half and vice versa
    if("full" in dish.lower()):
        tempList = [y for y in tempList if "half" not in y[0].lower()]
    if("half" in dish.lower()):
        tempList = [y for y in tempList if "full" not in y[0].lower()]
    if tempList:
        rate_list[dish] = tempList
    if(len(tempList) > 0):
        priceIndex.append((dish,sum(float(n)/itemPrice for _,n in tempList)/float(len(tempList))*100 ))
    else:
        priceIndex.append((dish,0))
    #averageDishPrice.append((row["Menu Item"],sum(n for _, n in tempList)/len(tempList),len(tempList)))
    return row

r = goli.apply(splitWord,axis=1)
dishPriceIndex = pd.DataFrame(priceIndex) 
dishPriceIndex.columns = ["Dish Name","Competative Market Price"]
dishPriceIndex["Market Price Change Relative to Goli"] =   dishPriceIndex["Competative Market Price"] - 100
dishPriceIndex.to_csv("Competative Dish Market Price.csv", sep='\t')



# Dishes to promote and remove
# Remove the goli entries from df0
df0 = pd.read_csv('Market Pricing.csv')
df0 = df0[df0["Restaurant"] != "Goli"]
df0 = df0.reset_index()
df0.drop(df0.columns[0],axis=1,inplace=True)

# Prepare a list of things famous in all resturants except goli
loved = df0["What people love here"].drop_duplicates()
loved.dropna(inplace=True)
loved = loved.reset_index()
loved.drop(loved.columns[0],axis=1,inplace=True)
lovedList = [] 
for x in loved["What people love here"]:
    temp = x.split(',')
    for y in temp:
        lovedList.append(y.lstrip().lower())
lovedList = list(set(lovedList))  

lovedL = lovedList
lis = []
for temp in lovedList:
    x = temp.split(" ")
    count = -1
    for y in lovedL:
        if(len(x) > 1):
            if((x[0] in y) and (x[1] in y)):
                count = count+1
        else:
            if(x[0] in y):
                count = count+1
    lis.append((temp,count))
lis = set(lis)
lis = list(lis)

lis = pd.DataFrame(lis)
lis.to_csv("lastSol.csv")

# list of things loved in goli
rspl = lambda x : x.lstrip().lower()
lovedGoli = list(map(rspl,goli["What people love here"][0].split(",")))

# To create a list of the items that
"""
common = [] 
for x in lovedList:
    temp = x.split(' ')
    for y in lovedGoli:
        if(len(temp)>1):
            if((temp[0] in y) and (temp[1] in y)):
                common.append(x)
        else:
            if((temp[0] in y)):
                common.append(x)
                
solution3 = list(set(lovedList) ^ set(common))
"""
common = [] 
for x in lovedGoli:
    temp = x.split(' ')
    for y in lovedList:
        if(len(temp)>1):
            if((temp[0] in y) and (temp[1] in y)):
                common.append(x)
        else:
            if((temp[0] in y)):
                common.append(x)
                
df2 = pd.read_csv('Customer Order Item Details.csv')
l = list(set(df2["Dish Name"]))
for x in l:
    if(x not in lovedGoli):
        temp = x.split(' ')
        for y in lovedList:
            if((temp[0] in y) and (temp[1] in y)):
                common.append(x)
            
                
solution3 = list(set(lovedGoli) ^ set(common))
solution3 = pd.DataFrame(solution3) 
solution3.columns = ["Dishes To Promote"]
solution3.to_csv("solution3.csv", sep='\t')
