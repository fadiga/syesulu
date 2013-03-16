#!/usr/bin/env python
# -*- coding: utf-8 -*-
#maintainer : Fad

from model import Alerte
from data_helper import make_date, save_al


list_alert = [(u"periode de transfere des poussins dans les poulaillers", make_date(4)),
       (u"periode de reforme", make_date(80)),
       ("phage ponde est arrive", make_date(18)),
       (u"le nettoyage des poulaillers apres la periode de reforme", make_date(81)),
       (u"Il est temps de faire une commande de nouveau poussins", make_date(79)),]

save_al(list_alert)
print "Les alertes",  Alerte.all()
