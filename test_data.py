#!/usr/bin/env python
# encoding= utf-8
#maintainer : Fad

from datetime import datetime
from model import *

m = Magasin(name=u"magasin aliment", qte_maxi_stok=5000)
m.save()
p = Produit(libelle=u"poisson", unite="kg")
p.save()

print "produit", Produit.all()
print "magasin", Magasin.all()

sr = StockRapport()
sr.type_ = "poulailler"
sr.magasin = 1
sr.produit = 1
sr.qte_utilise = 50
sr.restant = 20
sr.date_rapp = datetime.now()
sr.registered_on = datetime.now()
sr.save()

print "rapport pour les stocks ",  StockRapport.all()
