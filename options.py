#!/usr/bin/env python
from __future__ import division
import os
import requests
import io
import re
import operator
import urllib2
import time
from bs4 import BeautifulSoup

c_list=[]
oi_list=[]
vol_list=[]
call_oi_dic = {}
call_vol_dic = {}
put_oi_dic = {}
put_vol_dic = {}
call_oi_sorted = {}
today = time.strftime("%Y_%m_%d")
t_folder = time.strftime("%Y%m%d")
with open('snp500.txt') as f:
    for line in f:
        cname = line.split(',')
        c_list.append(cname[0])
f.close()

if not os.path.exists('data'):
        os.makedirs('data')
        
f_daily = os.path.join('./data/','Daily')        
fo = open('./data/%s' % today,'w+')
fo.write(today+"\n")

for fname in c_list:
    if not os.path.exists(os.path.join('./data/',fname)):
        os.makedirs(os.path.join('./data/',fname))

    file_path = os.path.join('./data/',fname)
    file_path_today = os.path.join(file_path,'stats.txt')
    url = 'http://www.optionetics.com/marketdata/Quote.aspx?symbol='+ fname +'&page=chain'
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    g_data = soup.find_all("tr")
    call_oi_total = 0
    call_vol_total = 0
    put_oi_total = 0
    put_vol_total = 0
    interest = []


    for item in g_data:
        try:
            call_oi = item.find_all("td")[1].text
            call_oi_num = re.findall("[0-9]+", call_oi)
            call_oi_total = call_oi_total + int(call_oi_num[0])
        except:
            pass
        try:
            put_oi = item.find_all("td")[11].text
            put_oi_num = re.findall("[0-9]+", put_oi)
            put_oi_total = put_oi_total + int(put_oi_num[0])
        except:
            pass
        try:
            call_vol = item.find_all("td")[2].text
            call_vol_num = re.findall("[0-9]+", call_vol)
            call_vol_total = call_vol_total + int(call_vol_num[0])
        except:
            pass
        try:
            put_vol = item.find_all("td")[10].text
            put_vol_num = re.findall("[0-9]+", put_vol)
            put_vol_total = put_vol_total + int(put_vol_num[0])
        except:
            pass

    call_oi_dic.update({fname:call_oi_total})
    call_vol_dic.update({fname:call_vol_total})
    put_oi_dic.update({fname:put_oi_total})
    put_vol_dic.update({fname:put_vol_total})
    if put_vol_total == 0:
        vol_ratio = 0
    else:
        vol_ratio = call_vol_total/put_vol_total
        
    if put_oi_total == 0:
        oi_ratio = 0
    else:
        oi_ratio = call_oi_total/put_oi_total
    
    try:
        print ("%s %d %d %d %d %.4f %.4f" % (fname, call_vol_total, call_oi_total, put_vol_total, put_oi_total, vol_ratio, oi_ratio))
        fo.write("%s %d %d %d %d %.4f %.4f\n" % (fname, call_vol_total, call_oi_total, put_vol_total, put_oi_total, vol_ratio, oi_ratio))
    except ZeroDivisionError:
        print ("WARNING: Invalid Equation")
    
    f = open(file_path_today,'a+')
    f.write("\n")
    f.write(today)
    f.write(" %d %d %d %d" % (call_vol_total, call_oi_total, put_vol_total, put_oi_total))
    f.close()

fo.close()

call_oi_sorted = sorted(call_oi_dic.items(), key=operator.itemgetter(1), reverse=True)
call_vol_sorted = sorted(call_vol_dic.items(), key=operator.itemgetter(1), reverse=True)
put_oi_sorted = sorted(put_oi_dic.items(), key=operator.itemgetter(1), reverse=True)
put_vol_sorted = sorted(put_vol_dic.items(), key=operator.itemgetter(1), reverse=True)

if not os.path.exists(os.path.join('./data/',t_folder)):
    os.makedirs(os.path.join('./data/',t_folder))

f_today = os.path.join('./data/',t_folder)

f=open('%s/call_vol.txt' % (f_today),'w')
f.write(time.strftime("%Y-%m-%d\n"))
for k, v in call_vol_sorted:
    f.write("%s %s\n" % (k,v))
f.close()
f=open('%s/put_vol.txt' % (f_today),'w')
f.write(time.strftime("%Y-%m-%d\n"))
for k, v in put_vol_sorted:
    f.write("%s %s\n" % (k,v))
f.close()
f=open('%s/call_oi.txt' % (f_today),'w')
f.write(time.strftime("%Y-%m-%d\n"))
for k, v in call_oi_sorted:
    f.write("%s %s\n" % (k,v))
f.close()
f=open('%s/put_oi.txt' % (f_today),'w')
f.write(time.strftime("%Y-%m-%d\n"))
for k, v in put_oi_sorted:
    f.write("%s %s\n" % (k,v))
f.close()

