#!usr/bin/env python
# -*- coding: utf-8 -*-
#maintainer: Fad


from datetime import datetime
from PyQt4 import QtGui, QtCore

from model import *
from common import (F_Widget, F_PageTitle, F_TableWidget,
                    F_BoxTitle, Button_save)
from util import raise_success, raise_error


class ProduitViewWidget(F_Widget):

    def __init__(self, produit="", parent=0, *args, **kwargs):
        super(ProduitViewWidget, self).__init__(parent=parent,\
                                                        *args, **kwargs)
        self.setWindowTitle(_(u"Products"))
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(F_PageTitle(_(u"The list of products")))

        tablebox = QtGui.QVBoxLayout()
        tablebox.addWidget(F_PageTitle(_(u"Table products")))
        self.table_op = ProduitTableWidget(parent=self)
        tablebox.addWidget(self.table_op)

        self.libelle = QtGui.QLineEdit()
        self.unite = QtGui.QLineEdit()

        formbox = QtGui.QVBoxLayout()
        editbox = QtGui.QGridLayout()
        formbox.addWidget(F_BoxTitle(_(u"Add product")))

        editbox.addWidget(QtGui.QLabel((_(u"Designation"))), 0, 0)
        editbox.addWidget(self.libelle, 1, 0)
        editbox.addWidget(QtGui.QLabel((_(u"Number of rooms"))), 0, 1)
        editbox.addWidget(self.unite, 1, 1)
        butt = Button_save(_(u"Save"))
        butt.clicked.connect(self.add_operation)
        editbox.addWidget(butt, 1, 2)

        formbox.addLayout(editbox)
        vbox.addLayout(formbox)
        vbox.addLayout(tablebox)
        self.setLayout(vbox)

    def add_operation(self):
        ''' add operation '''
        if unicode(self.libelle.text()) != "":
            if unicode(self.unite.text()) != "":
                produit = Produit()
                produit.libelle = unicode(self.libelle.text())
                produit.unite = unicode(self.unite.text())
                produit.save()
                self.libelle.clear()
                self.unite.clear()
                self.table_op.refresh_()
                raise_success(_(u"Confirmation"), _(u"The product %s "
                              u" was recorded") % produit.libelle)
            else:
                raise_error(_(u"error"), \
                            _(u"Give the room number in the box"))
        else:
            raise_error(_(u"Error"), _(u"Give the name of the product"))


class ProduitTableWidget(F_TableWidget):

    def __init__(self, parent, *args, **kwargs):
        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)
        self.header = [_(u"Designation"), _(u"Unite")]
        self.set_data_for()
        self.refresh(True)

    def refresh_(self):
        """ """
        self._reset()
        self.set_data_for()
        self.refresh()

    def set_data_for(self):
        self.data = [(prod.libelle, prod.unite) \
                                    for prod in Produit.all()]
