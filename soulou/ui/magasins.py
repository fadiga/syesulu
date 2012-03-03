#!usr/bin/env python
# -*- coding: utf-8 -*-
#maintainer: Fad


from datetime import datetime
from PyQt4 import QtGui, QtCore

from database import *
from common import (F_Widget, F_PageTitle, F_TableWidget, F_BoxTitle,
                    Button_save, IntLineEdit)
from util import raise_success, raise_error


class MagasinViewWidget(F_Widget):

    def __init__(self, magasin="", parent=0, *args, **kwargs):
        super(MagasinViewWidget, self).__init__(parent=parent,
                                                *args, **kwargs)
        self.setWindowTitle(_(u"Stores"))
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(F_PageTitle(_(u"The list of stores")))

        tablebox = QtGui.QVBoxLayout()
        tablebox.addWidget(F_BoxTitle(_(u"Table stores")))
        self.stori_table = MagasinTableWidget(parent=self)
        tablebox.addWidget(self.stori_table)

        formbox = QtGui.QVBoxLayout()
        editbox = QtGui.QGridLayout()

        self.name = QtGui.QLineEdit()
        self.qte_maxi_stok = IntLineEdit()

        editbox.addWidget(QtGui.QLabel((_(u"Name"))), 0, 0)
        editbox.addWidget(self.name, 1, 0)
        editbox.addWidget(QtGui.QLabel((_(u"Max quantity"))), 0, 1)
        editbox.addWidget(self.qte_maxi_stok, 1, 1)
        editbox.setColumnStretch(0, 2)
        editbox.setColumnStretch(3, 2)
        butt = Button_save(_(u"Save"))
        butt.clicked.connect(self.add_operation)
        editbox.addWidget(butt, 1, 2)

        formbox.addLayout(editbox)

        vbox.addLayout(formbox)
        vbox.addLayout(tablebox)
        self.setLayout(vbox)

    def add_operation(self):
        ''' add operation '''

        if unicode(self.name.text()) != "":
            magasin = Magasin()
            magasin.name = unicode(self.name.text())
            magasin.qte_maxi_stok = int(self.qte_maxi_stok.text())
            magasin.save()
            self.name.clear()
            self.qte_maxi_stok.clear()
            self.stori_table.refresh_()
            raise_success(_(u"Confirmation"), _(u"Registered operation"))
        else:
            raise_error(_("Error"), _(u"Give the name of the store"))


class MagasinTableWidget(F_TableWidget):

    def __init__(self, parent, *args, **kwargs):
        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)
        self.header = [_(u"Name"), _(u"Quantity max")]
        self.set_data_for()
        self.refresh(True)

    def refresh_(self):
        """ """
        self._reset()
        self.set_data_for()
        self.refresh()

    def set_data_for(self):
        self.data = [(mag.name, mag.qte_maxi_stok) for mag in Magasin.all()]



