#!/usr/bin/env python
# encoding=utf-8
# Autor: Fadiga

from model import (Magasin, Produit, StockRapport, ChickenCoop,
                   PsArrivage, Alerte, PsRapport)


def setup(drop_tables=False):
    """ create tables if not exist """

    did_create = False

    for model in [Magasin, Produit, StockRapport, ChickenCoop,
                  PsArrivage, Alerte, PsRapport]:
        if drop_tables:
            model.drop_table()
        if not model.table_exists():
            model.create_table()
            did_create = True

setup()
