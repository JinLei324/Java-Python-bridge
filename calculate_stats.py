#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import math
import numpy as np
import sklearn
import argparse

#parser = argparse.ArgumentParser(description='Linear Regression')
#parser.add_argument("--path")
#args=parser.parse_args()
file_path="a01.csv"

print(file_path)


# 1. import and clean the data
df=pd.read_csv(file_path)

df=df.iloc[1:]

df.columns=['t','se1','se2','se3','se4']

# convert str to number
def str_to_n(x):
    try:
        return float(x)
    except:
        return np.nan

for col in ['t','se1','se2','se3','se4']:
    df[col] = df[col].apply(str_to_n)

# first order lag
df=pd.concat([df, df.shift()], axis=1)

df.columns=['t','se1','se2','se3','se4','t2','l_se1','l_se2','l_se3','l_se4']

df=df.dropna()

df.drop(['t','t2'], axis=1, inplace=True)

# 1.1 4 R-squares
from sklearn.linear_model import LinearRegression

ols = LinearRegression().fit(df[['se2','se3','se4']], df['se1'])
r_sq_1 = ols.score(df[['se2','se3','se4']], df['se1'])

ols = LinearRegression().fit(df[['se1','se3','se4']], df['se2'])
r_sq_2 = ols.score(df[['se1','se3','se4']], df['se2'])

ols = LinearRegression().fit(df[['se2','se1','se4']], df['se3'])
r_sq_3 = ols.score(df[['se2','se1','se4']], df['se3'])

ols = LinearRegression().fit(df[['se2','se3','se1']], df['se4'])
r_sq_4 = ols.score(df[['se2','se3','se1']], df['se4'])

# 1.2 4 AR(1) coeffs
ols = LinearRegression().fit(df[['l_se1']], df['se1'])
ar_1=ols.coef_[0]

ols = LinearRegression().fit(df[['l_se2']], df['se2'])
ar_2=ols.coef_[0]

ols = LinearRegression().fit(df[['l_se3']], df['se3'])
ar_3=ols.coef_[0]

ols = LinearRegression().fit(df[['l_se4']], df['se4'])
ar_4=ols.coef_[0]

# 1.3 pairwise correlation
cor=df[['se1','se2','se3','se4']].corr(method ='pearson')

cor=cor.values

corr=[]
for i in range(1,4):
    for j in range(i):
        corr.append(cor[i][j])


# 1.4 average growth rate
df['g1']=df['se1']/df['l_se1']-1
df['g1']=df['g1'].replace([np.inf, -np.inf], np.nan)
df['g2']=df['se2']/df['l_se2']-1
df['g2']=df['g2'].replace([np.inf, -np.inf], np.nan)
df['g3']=df['se3']/df['l_se3']-1
df['g3']=df['g3'].replace([np.inf, -np.inf], np.nan)
df['g4']=df['se4']/df['l_se4']-1
df['g4']=df['g4'].replace([np.inf, -np.inf], np.nan)

g_mean=df[['g1','g2','g3','g4']].mean()

g_mean=g_mean.values.tolist()
for i in range(4):
    g_mean[i]=-1*g_mean[i]

# 1.5 mean of the series
mean=df[['se1','se2','se3','se4']].mean()

mean=mean.values.tolist()

std=df[['se1','se2','se3','se4']].std()
std=std.values.tolist()

cv=[]
for i in range(4):
    cv.append(std[i]/mean[i])

#return [r_sq_1, r_sq_2, r_sq_3, r_sq_4]+ [ar_1,ar_2, ar_3, ar_4]+ corr + g_mean + mean +std +cv
print ([r_sq_1, r_sq_2, r_sq_3, r_sq_4]+ [ar_1,ar_2, ar_3, ar_4]+ corr + g_mean + mean +std +cv)




