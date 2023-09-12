#!/usr/bin/env python
# coding=utf-8

import pandas as pd
import time

start = time.time()
with open('/media/hyz/dwarfcave/data/gaiaDR3/ms/gaiasource_path.list','r') as _list:
    path = _list.readlines()
    for _,_line in enumerate(path):
        _p = _line.strip()
        print("reading:%s ==> "%_,_p)
        _d    = pd.read_csv(_p,comment='#',usecols=['ra','dec','phot_g_mean_mag','phot_rp_mean_mag','phot_bp_mean_mag'])
        _d['phot_all_mean_mag'] = _d[['phot_g_mean_mag','phot_rp_mean_mag','phot_bp_mean_mag']].mean(axis=1)  # calculate mean of 3 band. obtain all objects
        _d = _d.fillna(0).to_numpy()
        if (_+1)%10 == 0:
            print('reading time:%s ==> %02f'%(_+1,time.time()-start))
