#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fadiga

import time

from datetime import date, timedelta, datetime

from model import Alerte

def format_date(dat):
    dat = str(dat)
    day, month, year = dat.split('/')
    return '-'.join([year, month, day])
 
def alerte():
    list_al = []

    try:
        alerte = Alerte.get()
    except:
        alerte = None
    if alerte:
        for al in Alerte.filter(status=True):
            if al.date_fin <= datetime.now():
                    list_al.append(al)
    return list_al
