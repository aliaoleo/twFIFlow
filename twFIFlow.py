#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 10:20:24 2018

@author: hh
"""

import requests
from io import StringIO
import pandas as pd
import datetime as date
import os
from pandas.tseries.offsets import BDay
import matplotlib.pyplot as plt

#date = '20180102'
#r = requests.get('http://www.twse.com.tw/fund/T86?response=csv&date='+date+'&selectType=ALLBUT0999')#
#df = pd.read_csv(StringIO(r.text), header=1).dropna(how='all', axis=1).dropna(how='any')
#df



def crawl_legal_person(date):
    
    # 將時間物件變成字串：'20180102'
    datestr = date.strftime('%Y%m%d')

    # 下載三大法人資料
    try

        r = requests.get('http://www.tse.com.tw/fund/T86?response=csv&date='+datestr+'&selectType=ALLBUT0999')
    except:
        return None
    # 製作三大法人的DataFrame
    try:
        df = pd.read_csv(StringIO(r.text), header=1).dropna(how='all', axis=1).dropna(how='any')
    except:
        return None
    
    # 微調整（為了配合資料庫的格式）
    # 刪除逗點
    
    df = df.astype(str).apply(lambda s: s.str.replace(',',''))
    # 刪除「證券代號」中的「"」和「=」
    df['stock_id'] = df['證券代號'].str.replace('=','').str.replace('"','')
    # 刪除「證券代號」這個欄位
    df = df.drop(['證券代號'], axis=1)
    # 設定index
    df['date'] = date
    #    original columns ['外陸資買進股數(不含外資自營商)', '外陸資賣出股數(不含外資自營商)', '外陸資買賣超股數(不含外資自營商)','外資自營商買進股數', '外資自營商賣出股數', '外資自營商買賣超股數', '投信買進股數', '投信賣出股數','投信買賣超股數', '自營商買賣超股數', '自營商買進股數(自行買賣)', '自營商賣出股數(自行買賣)','自營商買賣超股數(自行買賣)', '自營商買進股數(避險)', '自營商賣出股數(避險)', '自營商買賣超股數(避險)','三大法人買賣超股數']
    df = df.rename(columns = {'證券名稱':'stock name','外陸資買進股數(不含外資自營商)':'FFI Buy', '外陸資賣出股數(不含外資自營商)':'FFI Sell', '外陸資買賣超股數(不含外資自營商)':'FFI Net Buy'})
    df.sort_values(['FFI Net Buy'],ascending=False,inplace = True) 
    df = df.set_index(['stock_id', 'stock name','date'])
#    df.columns = ['FFI Buy', 'FFI Sell', 'FFI Net Buy',
#       'FFI Prop Buy', 'FFI Prop Sell', 'FFI Prop Net Buy', 'SITE Buy', 'SITE Sell',
#       'SITE Net Bu', 'Prop Net Buy', 'Prop Disc Buy', 'Prop Disc Sell',
#       'Prop Disc Net Buy', 'Prop Hedge Buy', 'Prop Hedge Sell', 'Prop Hedge Net Buy',
#       'Summary']
#   將dataframe的型態轉成數字
    return df.apply(lambda s: pd.to_numeric(s, errors='coerce')).dropna(how='all', axis=1)


#day = date.date.today()-date.timedelta(days = 1)
#df1 = crawl_legal_person(day)
#df1.sort_values(['FFI Net Buy'],ascending=False,inplace = True)
#df1.head(10)

day = date.date.today()
#dayrange = [day - date.timedelta(x) for x in range(0,5)]
dayrange = [day - BDay(x) for x in range(1,30)]

df1 = pd.DataFrame()
idx = pd.IndexSlice

for day in dayrange:
    if crawl_legal_person(day) is None:
        pass
    else:
        df = crawl_legal_person(day) 
        df.to_csv('/Users/hh/Documents/PythonWorkspace/@current/TWSE/legal/' + day.strftime('%Y%m%d') + '.csv', sep='\t')
#        df.to_csv('\\Mac\\Home\\Documents\\PythonWorkspace\\@current\\TWSE\\legal\\' + day.strftime('%Y%m%d') + '.csv', sep='\t')
        df1 = df1.append(df)
        df_stock = df1.loc[idx['2330',:,:],:]
        
        plot(df_stock)
        plt.show()
        df_stock
        
        
        

