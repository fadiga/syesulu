#!/usr/bin/env python
# -*- coding: utf-8 -*-
#maintainer : Fad

from datetime import datetime, timedelta
from model import Alerte

def make_date(nbr_week):
    """return une date"""
    return datetime.now() + timedelta(nbr_week * 7)

def save_al(list_):
    """Enregistrer les alertes qui sont dans la liste"""
    for el in list_alert:
        al = Alerte()
        al.objets = unicode(el[0])
        al.date_a = el[1]
        al.status = True
        print al
        al.save()


list_alert = [(u"periode de transfere des poussins dans les poulaillers", make_date(4)),
       (u"periode de reforme", make_date(80)),
       ("phage ponde est arrive", make_date(18)),
       (u"le nettoyage des poulaillers apres la periode de reforme", make_date(81)),
       (u"Il est temps de faire une commande de nouveau poussins", make_date(79)),]

save_al(list_alert)
print "Les alertes",  Alerte.all()
