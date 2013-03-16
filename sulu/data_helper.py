#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fadiga

from datetime import datetime, timedelta

from model import Alerte

def format_date(dat):
    dat = str(dat)
    day, month, year = dat.split('/')
    return '-'.join([year, month, day])
 
def alerte():
    list_al , msg = [], ""
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
                msg += "%d jr(s) pour: %s " % (dat, al.objets)

    return list_al, msg


def update_alert(chickencoop_type):
    """ Active les alerte 
        params: le type de chickencoop"""

    if chickencoop_type == 0:
        """A lancer après quand les poussins arrive dans les Poussinières"""

        list_al = [("periode de transfere des poussins dans les poulaillers", make_date(4))]

    if chickencoop_type == 1:
        """A lancer après le transfere
         dans les poulaillers"""

        list_al = [("periode de reforme", make_date(76)),
                   ("phage ponde est arrive", make_date(14)),
                   ("le nettoyage des poulaillers apres la periode de reforme", make_date(77)),
                   ("Il est temps de faire une commande de nouveau poussins", make_date(75)),]
    save_al(list_al)


def save_al(list_):
    """Enregistrer les alertes qui sont dans la liste"""
    for el in list_:
        try:
            al = Alerte.filter(objets=el[0]).get()
        except:
            al = Alerte()
        al.objets = unicode(el[0])
        al.date_a = el[1]
        al.status = True
        al.save()

def make_date(nbr_week):
    """return une date"""
    return datetime.now() + timedelta(nbr_week * 7)


