#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fad

import peewee

from datetime import date, datetime


DB_FILE = 'poulailler_base.db'
dbh = peewee.SqliteDatabase(DB_FILE)


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
        return (u"%(name)s") % {'name': self.name}


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
    date_rapp = peewee.DateTimeField(default=datetime.now())
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
            raise_error(_(u"error"), \
                        _(u"Il n'existe aucun %s dans le magasin %s") % \
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
                    raise_error(_(u"error"), _(u"On peut pas utilisé %d puis qu'il ne reste que %d") % \
                                       (self.qte_utilise, previous_remaining))
                    return False
        else:
            self.restant = self.qte_utilise
        super(StockRapport, self).save()
        raise_success(_(u"Confirmation"), _(u"Registered operation"))
        # ----------------------------------------------------------------#
        next_reports = StockRapport.filter(produit__libelle=self.produit \
                                .libelle, magasin__name=self.magasin.name, \
                        date__gt=self.date_rapp).order_by(('date_rapp', 'asc'))
        try:
            next_reports = next_reports.get()
        except:
            next_reports = None
        if next_reports:
            next_reports.save()


class Alerte(BaseModel):
    """docstring for Alerte"""

    objets = peewee.TextField()
    date_a = peewee.DateTimeField(default=datetime.today())
    status = peewee.BooleanField(default=True)

    def __unicode__(self):
        return (u"%(alerte)s %(date_a)s") % {u'alerte': self.objets,
                u'date_a': self.date_a}


class ChickenCoop(BaseModel):
    """docstring for Poulalle"""

    TYPE_POUL = 0 # blank created
    TYPE_POUS = 1 # started edition
    TYPE= ((TYPE_POUL, u"Poulailler"),
                (TYPE_POUS, u"Poussinière"),)

    EMPTY = 0 # blank created
    OCCUPY = 1 # started edition
    STATUS = ((EMPTY, u"Vide"),
                (OCCUPY, u"Occuper"),)

    type_ = peewee.IntegerField(default=TYPE_POUS)
    num = peewee.IntegerField(default=0)
    nbr_sujet_maxi = peewee.IntegerField(default=0)
    date = peewee.DateTimeField(default=datetime.now())
    status = peewee.IntegerField(default=EMPTY)

    def __unicode__(self):
        return (u"%(type_)s %(num)s") % \
                {u'type_': self.TYPE[self.type_][1], u'num': self.num}

    def full_name(self):
        return (u"%(type_)s %(num)s") % \
                {u'type_': self.TYPE[self.type_][1], u'num': self.num}


class PsArrivage(BaseModel):
    """docstring for PsArrivage"""

    NEW = 0 # blank created
    TRANSFERE = 1 # started edition
    REFORME = 2 # started edition
    STATUS = ((NEW, u"Nouveau"),
              (TRANSFERE, u"Transfert"),
              (REFORME, u"Reforme"),)

    race = peewee.CharField(max_length=50)
    nb_total_chiks = peewee.IntegerField(default=0)
    arrival_date = peewee.DateTimeField(default=datetime.now())
    chicken_coop = peewee.ForeignKeyField(ChickenCoop)
    status = peewee.IntegerField(default=NEW)

    def __unicode__(self):
        return (u"%(nb_total_chiks)s %(arrival_date)s") % \
                {'nb_total_chiks': self.nb_total_chiks,
                 'arrival_date': self.arrival_date}


class PsRapport(BaseModel):
    """docstring for PsPoulalle"""

    psarrivage = peewee.ForeignKeyField(PsArrivage)
    nb_death = peewee.IntegerField(default=0)
    remaining = peewee.IntegerField(default=0)
    nb_eggs = peewee.IntegerField(default=0)
    date_report = peewee.DateTimeField(default=datetime.now())
    weight = peewee.IntegerField(default=0)

    def save(self):
        """
        Calcul du restant en stock après une operation."""
        from util import raise_success, raise_error
        try:
            last_reports = PsRapport.filter(psarrivage__chicken_coop_id= \
                           self.psarrivage).order_by(('date_report', 'desc'))
        except:
            raise_error(_("Error"), _(u"Give the number of the death"))
        previous_remaining = 0
        self.remaining = 0
        try:
            last_report = last_reports.get()
        except:
            last_report = None

        if last_report:
            previous_remaining = last_report.remaining
            self.remaining = previous_remaining - self.nb_death
            if self.remaining < 0:
                raise_error(_(u"error"), \
                    _(u"On peut pas utilisé %d puis qu'il ne reste que %d") % \
                    (self.nb_death, previous_remaining))
                return False
        else:
            self.remaining = self.psarrivage.nb_total_chiks - self.nb_death

        super(PsRapport, self).save()
        raise_success(_(u"Confirmation"), _(u"Registered operation"))
        # ----------------------------------------------------------------#
        next_reports = PsRapport.filter(psarrivage=self.psarrivage, \
                                        date_report__gt=self.date_report) \
                                .order_by(('date_report', 'asc'))

        try:
            next_reports = next_reports.get()
        except:
            next_reports = None

        if next_reports:
            next_reports.save()

    def __unicode__(self):
        return (u" %(remaining)s %(date_report)s") % \
                {'psarrivage': self.psarrivage, 'remaining' : self.remaining,
                 'date_report': self.date_report}
