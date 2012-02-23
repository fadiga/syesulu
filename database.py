#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fad

from datetime import date, datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import mapper, relationship
from sqlalchemy import Table, Column, Integer, String, \
                       MetaData, ForeignKey, DateTime, Unicode

DB_FILE = 'base_ferme.db'

engine = create_engine('sqlite:///%s' % DB_FILE, echo=False)
Session = sessionmaker(bind=engine)
session = Session()

metadata = MetaData()

magasins_table = Table('magasin', metadata,
                       Column('id', Integer, primary_key=True),
                       Column('name', Unicode(20)),
                       Column('adresse', Unicode(100)),)

produits_table = Table('produit', metadata,
                       Column('id', Integer, primary_key=True),
                       Column('nbr_piece', Integer),
                       Column('libelle', Unicode(100)),)

stock_rapports_table = Table('rapport', metadata,
                            Column('id', Integer, primary_key=True),
                            Column('magasin_id', Integer,
                                    ForeignKey('magasin.id')),
                            Column('produit_id', Integer,
                                    ForeignKey('produit.id')),
                            Column('nbr_carton', Integer),
                            Column('restant', Integer),
                            Column('date_rapp', DateTime),
                            Column('registered_on',
                                    DateTime, nullable=True),
                            Column('type_', Unicode(20)),)


alertes_table = Table('alerte', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('arrivage_id', Integer,
                                  ForeignKey('arrivage.id')),
                      Column('objets', Unicode(100)),
                      Column('date_debut', DateTime),
                      Column('date_fin', DateTime),
                      Column('status', Integer),)

poulalles_table = Table('poulalle', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('type', Unicode(20)),
                        Column('num', Integer),
                        Column('stock_maxi', Integer),)

ps_arrivages_table = Table('arrivage', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('race', Unicode(20)),
                        Column('nbre_total_poussin', Integer),
                        Column('date_arriver', DateTime),
                        Column('status', Unicode(20)),)

ps_rapports_table = Table('ps_rapport', metadata,
                          Column('id', Integer, primary_key=True),
                          Column('poulalle_id', Integer,
                                  ForeignKey('poulalle.id')),
                          Column('arrivage_id', Integer,
                                  ForeignKey('arrivage.id')),
                          Column('nbr_mort', Integer),
                          Column('restant', Integer),
                          Column('nbr_oeuf', Integer),
                          Column('date_rapp', DateTime),
                          Column('registered_on',
                                  DateTime, nullable=True),
                          Column('poids', Unicode(20)),)

metadata.create_all(engine)


class Magasin(object):
    def __init__(self, name, adresse=None):
        self.name = name
        self.adresse = adresse

    def __repr__(self):
        return (u"Magasin (%(magasin)s)") % {'magasin': self.name}

    def __unicode__(self):
        return (u"%(magasin)s") % {'magasin': self.name}


class Produit(object):
    def __init__(self, libelle, nbr_piece):
        self.nbr_piece = nbr_piece
        self.libelle = libelle

    def __repr__(self):
        return (u"Produit(%(libelle)s %(nbr_piece)s)" % \
                                            {'libelle': self.libelle,\
                                            'nbr_piece': self.nbr_piece})

    def __unicode__(self):
        return (u"%(libelle)s (%(nbr_piece)sp/c)" % {'libelle': self.libelle,\
                                              'nbr_piece': self.nbr_piece})


class StockRapport(object):
    def __init__(self, type_, nbr_carton, date_rapp, remaining=0, \
                                        magasin=None, produit=None):
        self.type_ = type_
        self.magasin = magasin
        self.produit = produit
        self.nbr_carton = nbr_carton
        self.restant = remaining
        self.date_rapp = date_rapp
        self.registered_on = datetime.now()

    def __repr__(self):
        return ("StockRapport('%(type_)s', '%(magasin)s', '%(produit)s', \
                '%(nbr_carton)s, '%(date_rapp)s')") % {'type_': self.type_, \
                'date_rapp': self.date_rapp, 'nbr_carton': self.nbr_carton, \
                'magasin': self.magasin, 'produit': self.produit}

    def __unicode__(self):
        return (u"%(type_)s %(date_rapp)s %(produit)s: %(magasin)s") \
               % {'type_': self.type_, \
                'date_rapp': self.date_rapp.strftime('%F'), \
                'produit': self.produit, 'magasin': self.magasin}


class Alerte(object):
    """docstring for Alerte"""

    def __init__(self, objets, date_debut, date_fin, status):
        self.objets = objets
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.status = status

    def __repr__(self):
        return (u"Alerte (%(alerte)s)") % {'alerte': self.objets}

    def __unicode__(self):
        return (u"%(alerte)s") % {'alerte': self.objets}


class Poulalles(object):
    """docstring for Poulalle"""

    def __init__(self, type_, num, stock_maxi):

        self.type_ = type_
        self.num = num
        self.stock_maxi = stock_maxi

    def __repr__(self):
        return (u"Poulalle(%(type_)s %(num)s") % \
                 {'type_': self.type_, 'num': self.num}

    def __unicode__(self):
        return (u"%(type_)s %(num)s") % \
                {'type_': self.type_, 'num': self.num}


class PsArrivage(object):
    """docstring for PsArrivage"""

    def __init__(self, race, nbre_total_poussin, date_arriver, status):

        self.race = race
        self.nbre_total_poussin = nbre_total_poussin
        self.date_arriver = date_arriver
        self.status = status

    def __repr__(self):
        return (u"PsArrivage(%(nbre_total_poussin)s %(date_arriver)s") % \
                 {'nbre_total_poussin': self.nbre_total_poussin,
                  'date_arriver': self.date_arriver}

    def __unicode__(self):
        return (u"%(nbre_total_poussin)s %(date_arriver)s") % \
                {'nbre_total_poussin': self.nbre_total_poussin,
                 'date_arriver': self.date_arriver}


class PsRapport(object):
    """docstring for PsPoulalle"""
    def __init__(self, poulalle_id, nbr_mort, restant, nbr_oeuf,
                 date_rapp, poids):
        self.poulalle_id = poulalle_id
        self.nbr_mort = nbr_mort
        self.restant = restant
        self.nbr_oeuf = nbr_oeuf
        self.date_rapp = date_rapp
        self.poids = poids

    def __repr__(self):
        return (u"PsRapport(%(poulalle)s %(restant)s %(date)s") % \
                {'poulalle': self.poulalle, 'restant': self.restant,
                 'date': self.date}

    def __unicode__(self):
        return (u"%(poulalle)s %(restant)s %(date)s") % \
                {'poulalle': self.poulalle, 'restant' : self.restant,
                 'date': self.date}

mapper(Produit, produits_table, properties={
    'rapports': relationship(StockRapport, backref='produit'),
})
mapper(Magasin, magasins_table, properties={
    'rapports': relationship(StockRapport, backref='magasin'),
    })
mapper(StockRapport, stock_rapports_table)
mapper(Alerte, alertes_table)
mapper(Poulalles, poulalles_table)
mapper(PsArrivage, ps_arrivages_table)
mapper(PsRapport, ps_rapports_table)
