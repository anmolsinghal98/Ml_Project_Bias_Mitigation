# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import json
import matplotlib.pyplot as plt
import numpy as np
import pystan

baseline="""

data {
      int<lower=1> I; // number of products
      int<lower=1> N; // number of reviews
      int<lower=1> J; // number of reviewers
      vector<lower=0> [N] scores; // review scores vector
      int reviewerID[N]; // reviewer ID for each review
      int prodID[N]; // product ID for each review
}

parameters {
    vector [I] truescore;
    vector [J] reviewbias;
    real<lower=0> c;
    real<lower=0> d;
}

model {
    c ~ gamma(1,1);
    truescore ~ normal(3,1); // TODO: change hyperparameters for data reviewbias ~ normal(0, 1/c);
    for (i in 1:N) {
                scores[i] ~ normal(truescore[prodID[i]] + reviewbias[reviewerID[i]], 1);
                } 
    }

"""

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


rmap={}
pmap={}
rcount=1
pcount=1

for key in rusers.keys():
    rmap[key]=rcount
    rcount+=1

for key in rproducts.keys():
    pmap[key]=pcount
    pcount+=1


reviewer=[]
product=[]
ratings=[]
helpful=[]

for key in rusers.keys():
    for prod in rusers[key]:
        
        if prod['asin'] in rproducts:
            reviewer.append(rmap[key])
            product.append(pmap[prod['asin']])
            ratings.append(prod['overall'])
            helpful.append(prod['helpful'])

plt.hist(ratings, bins = [1,2,3,4,5,6])

print(helpful[0])

print(data[0])


base_data = {'I': 810, 'N': 6854, 'J':511, 'scores':ratings, 'reviewerID':reviewer, 'prodID':product}

sm = pystan.StanModel(model_code=baseline)

fit = sm.sampling(data=base_data, iter=1000, chains=4)

print(fit)

la = fit.extract(permuted=True)
