#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fad

import peewee

from datetime import date, datetime

dbh = peewee.SqliteDatabase("poulailler_base.db")


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
    magasin = peewee.ForeignKeyField(Magasin)
    produit = peewee.ForeignKeyField(Produit)
    qte_utilise = peewee.IntegerField(default=0)
    restant = peewee.IntegerField(default=0)
    date_rapp = peewee.DateTimeField(default=0)
    registered_on = datetime.now()

    def __unicode__(self):
        return (u"%(type_)s %(date_rapp)s %(produit)s: %(magasin)s") \
               % {'type_': self.type_, \
                'date_rapp': self.date_rapp.strftime('%F'), \
                'produit': self.produit, 'magasin': self.magasin}

    def save(self):
        """
        Calcul du restant en stock après une operation."""
        from util import raise_success, raise_error

        last_reports = StockRapport.filter(produit__libelle=self
                                           .produit.libelle,
                                           magasin__name=self.magasin.name,
                                           date_rapp__lt=self.date_rapp) \
                                    .order_by(('date_rapp','desc'))
        previous_remaining = 0
        self.restant = 0
        try:
            last_reports = last_reports.get()
        except:
            last_reports = None

        if last_reports == None and self.type_ == _(u"inout"):
            raise_error(_(u"error"), _(u"Il n'existe aucun %s dans le magasin %s") %
                                               (self.produit.libelle, self.magasin.name))
            return False
        if last_reports:
            previous_remaining = last_reports.restant
            if self.type_ == _(u"input"):
                self.restant = previous_remaining + self.qte_utilise
            if self.type_ == _(u"inout"):
                self.restant = previous_remaining - self.qte_utilise
                if self.restant < 0:
                    print  self.qte_utilise, previous_remaining
                    raise_error(_(u"error"), _(u"On peut pas utilisé %d puis qu'il ne reste que %d") %
                                               (self.qte_utilise, previous_remaining))
                    return False
        else:
            self.restant = self.qte_utilise
        super(StockRapport, self).save()
        raise_success(_(u"Confirmation"), _(u"Registered operation"))
        # ----------------------------------------------------------------#
        next_reports = StockRapport.filter(produit__libelle=self.produit.libelle,
                                      magasin__name=self.magasin.name,
                                      date__gt=self.date_rapp).order_by(('date_rapp', 'asc'))
        try:
            next_reports = next_reports.get()
        except:
            next_reports = None
        if next_reports:
            next_reports.save()

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


class ChickenCoop(BaseModel):
    """docstring for Poulalle"""

    TYPE_POUL = 0 # blank created
    TYPE_POUS = 1 # started edition
    TYPE= ((TYPE_POUL, u"poussinière"),
                (TYPE_POUS, u"poulailler"),)

    type_ = peewee.IntegerField(default=TYPE_POUS)
    num = peewee.IntegerField(default=0)
    nbr_sujet_maxi = peewee.IntegerField(default=0)
    date = peewee.DateTimeField(default=0)

    def __unicode__(self):
        return (u"%(type_)s %(num)s") % \
                {'type_': self.TYPE[self.type_][1], 'num': self.num}

    def full_name(self):
        return (u"%(type_)s %(num)s") % \
                {'type_': self.TYPE[self.type_][1], 'num': self.num}


class PsArrivage(BaseModel):
    """docstring for PsArrivage"""

    race = peewee.CharField(max_length=50)
    nb_total_chiks = peewee.IntegerField(default=0)
    arrival_date = peewee.DateTimeField(default=0)
    chicken_coop = peewee.ForeignKeyField(ChickenCoop)

    def __unicode__(self):
        return (u"%(nb_total_chiks)s %(arrival_date)s") % \
                {'nb_total_chiks': self.nb_total_chiks,
                 'arrival_date': self.arrival_date}


class PsRapport(BaseModel):
    """docstring for PsPoulalle"""

    chickencoop = peewee.ForeignKeyField(ChickenCoop, unique=True)
    nbb_death = peewee.IntegerField(default=0)
    remaining = peewee.IntegerField(default=0)
    nb_eggs = peewee.IntegerField(default=0)
    date_report = peewee.DateTimeField(default=0)
    weight = peewee.IntegerField(default=0)

    def __unicode__(self):
        return (u"%(chickencoop)s %(remaining)s %(date_report)s") % \
                {'chickencoop': self.chickencoop, 'remaining' : self.remaining,
                 'date_report': self.date_report}
