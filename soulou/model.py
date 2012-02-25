#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fad

import peewee

from datetime import date, datetime


dbh = peewee.SqliteDatabase("peewee.db")


class BaseModel(peewee.Model):

    class Meta:
        database = dbh

    @classmethod
    def all(cls):
        return list(cls.select())

class Magasin(BaseModel):
    name = peewee.CharField(max_length=100)
    qte_maxi_stok = peewee.IntegerField(default=0)

    def __unicode__(self):
        return (u"%(magasin)s") % {'magasin': self.name}


class Produit(BaseModel):
    """ """
    libelle = peewee.CharField(max_length=50)
    unite = peewee.CharField(max_length=50)

    def __unicode__(self):
        return (u"%(libelle)s (%(unite)s)" % \
                {'libelle': self.libelle, 'unite': self.unite})


class StockRapport(BaseModel):
    """ """
    type_ = peewee.CharField(max_length=50)
    magasin = peewee.ForeignKeyField(Magasin, unique=True)
    produit = peewee.ForeignKeyField(Produit, unique=True)
    qte_utilise = peewee.IntegerField(default=0)
    restant = peewee.IntegerField(default=0)
    date_rapp = peewee.DateTimeField(default=0)
    registered_on = datetime.now()

    def __unicode__(self):
        return (u"%(type_)s %(date_rapp)s %(produit)s: %(magasin)s") \
               % {'type_': self.type_, \
                'date_rapp': self.date_rapp.strftime('%F'), \
                'produit': self.produit, 'magasin': self.magasin}


class Alerte(BaseModel):
    """docstring for Alerte"""

    STATUS_ON = 0 # blank created
    STATUS_OFF = 1 # started edition
    STATUSES = ((STATUS_ON, u"Commencé"),
                (STATUS_OFF, u"fait"),)

    objets = peewee.TextField()
    date_debut = peewee.DateTimeField(default=0)
    date_fin = peewee.DateTimeField(default=0)
    status = peewee.IntegerField(default=STATUS_OFF)

    def __unicode__(self):
        return (u"%(alerte)s") % {'alerte': self.objets}


class Poulailler(BaseModel):
    """docstring for Poulalle"""

    TYPE_POUL = 0 # blank created
    TYPE_POUS = 1 # started edition
    TYPE= ((TYPE_POUS, u"poulailler"),
                (TYPE_POUL, u"poussinière"),)

    type_ = peewee.IntegerField(default=TYPE_POUS)
    num = peewee.IntegerField(default=0)
    nbr_sujet = peewee.IntegerField(default=0)
    stock_maxi = peewee.IntegerField(default=0)
    date = peewee.DateTimeField(default=0)

    def __unicode__(self):
        return (u"%(type_)s %(num)s") % \
                {'type_': self.type_, 'num': self.num}


class PsArrivage(BaseModel):
    """docstring for PsArrivage"""

    race = peewee.CharField(max_length=50)
    nbre_total_poussin = peewee.IntegerField(default=0)
    date_arriver = peewee.DateTimeField(default=0)
    poulailler = peewee.ForeignKeyField(Poulailler, unique=True)

    def __unicode__(self):
        return (u"%(nbre_total_poussin)s %(date_arriver)s") % \
                {'nbre_total_poussin': self.nbre_total_poussin,
                 'date_arriver': self.date_arriver}


class PsRapport(BaseModel):
    """docstring for PsPoulalle"""

    poulailler = peewee.ForeignKeyField(Poulailler, unique=True)
    nbr_mort = peewee.IntegerField(default=0)
    restant = peewee.IntegerField(default=0)
    nbr_oeuf = peewee.IntegerField(default=0)
    date_rapp = peewee.DateTimeField(default=0)
    poids = peewee.IntegerField(default=0)

    def __unicode__(self):
        return (u"%(poulailler)s %(restant)s %(date)s") % \
                {'poulailler': self.poulailler, 'restant' : self.restant,
                 'date': self.date}
