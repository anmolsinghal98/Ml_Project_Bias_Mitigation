# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import json
import matplotlib.pyplot as plt
import numpy as np

path='reviews_Amazon_Instant_Video_5.json'

data=[]
for line in open(path,'r'):
    data.append(json.loads(line))

products={}
for d in data:
    if d['asin'] not in products:
        
        products[d['asin']] = [d]
    
    else:
        
        products[d['asin']].append(d)
        
users={}
for d in data:
    
    if d['reviewerID'] not in users:
        
        users[d['reviewerID']] = [d]
    
    else:
        
        users[d['reviewerID']].append(d)

print('No of reviews',len(data))   
print('No of reviewers',len(users))  
print('No. of products reviewed',len(products.keys()))

count1=0
rusers={}
for key in users.keys():
    
    if len(users[key])>10:
        pr=[]
        diff=0
        for i in users[key]:
            if i['asin'] not in pr:
                pr.append(i['asin'])
            else:
                diff+=1
        if(len(users[key])-diff>10):
            count1+=1
            rusers[key]=users[key]
                
print('No of users with more than 10 reviews',count1)

count2=0
rproducts={}
for key in products.keys():
    
    if len(products[key])>10:
        ur=[]
        diff=0
        for i in products[key]:
            if i['reviewerID'] not in ur:
                ur.append(i['reviewerID'])
            else:
                diff+=1
        if(len(products[key])-diff>10):
            count2+=1
            rproducts[key]=products[key]


print('No of products with more than 10 reviews',count2)

print("Reduced users",len(rusers))
print("Reduced products",len(rproducts))

A=[]
ratings=[]
for key in rusers.keys():
    for prod in rusers[key]:
        
        if prod['asin'] in rproducts:
            A.append([key,prod['asin']])
            ratings.append(prod['overall'])

plt.hist(ratings, bins = 5)

print(len(A))



print(data[0])