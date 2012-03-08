#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fadiga

from datetime import datetime 

from model import Alerte

def format_date(dat):
    dat = str(dat)
    day, month, year = dat.split('/')
    return '-'.join([year, month, day])
 
def alerte():
    list_al , msg = [], "Il vous reste que "
    min_nbr_day = 0
    max_nbr_day = 4
    try:
        alerte = Alerte.get()
    except:
        alerte = None

    if alerte:
        for al in Alerte.filter(status=True):
            dat = (al.date_a - datetime.now()).days
            if dat <= max_nbr_day and dat >= min_nbr_day:
                list_al.append(al)  
                msg += "%d jr(s) pour faire: %s " % (dat, al.objets)

    return list_al, msg
