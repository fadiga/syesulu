#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: alou

from PyQt4 import QtGui, QtCore

from database import Poulailler
from common import (F_Widget, F_PageTitle, F_TableWidget, F_BoxTitle,
                    Button_save)
from util import raise_success, raise_error


class PoulaillerViewWidget(F_Widget):
    """ Gestion de pasin  """

    def __init__(self, parent=0, *args, **kwargs):
        super(PoulaillerViewWidget, self).__init__(parent=parent,
                                                        *args, **kwargs)

        self.setWindowTitle(_(u"Poulailler"))
        vbox = QtGui.QVBoxLayout()
        self.title = F_PageTitle(_("Poulailler"))

        tablebox = QtGui.QVBoxLayout()
        tablebox.addWidget(F_BoxTitle(_(u"Table Poulailler")))
        self.poussin_table = PoulaillerTableWidget(parent=self)
        tablebox.addWidget(self.poussin_table)

        formbox = QtGui.QVBoxLayout()
        editbox = QtGui.QGridLayout()
        butt = Button_save(_(u"Save"))


        liste_type = [u"poulailler", u"poussinière"]
        #Combobox widget
        self.type_ = QtGui.QComboBox()
        for index in liste_type:
            self.type_.addItem(u'%(type)s' % {'type': index})

        self.num = QtGui.QLineEdit()
        self.nbr_sujet = QtGui.QLineEdit()
        self.stock_maxi = QtGui.QLineEdit()
        self.date = QtGui.QDateEdit()
        self.num.setValidator(QtGui.QIntValidator())
        editbox.addWidget(QtGui.QLabel((_(u"Type"))), 0, 0)
        editbox.addWidget(self.type_, 1, 0)
        editbox.addWidget(QtGui.QLabel((_(u"Number"))), 0, 1)
        editbox.addWidget(self.num, 1, 1)
        editbox.addWidget(QtGui.QLabel((_(u"Number sujet"))), 0, 2)
        editbox.addWidget(self.nbr_sujet, 1, 2)
        editbox.addWidget(QtGui.QLabel((_(u"Max"))), 0, 3)
        editbox.addWidget(self.stock_maxi, 1, 3)
        editbox.addWidget(QtGui.QLabel((_(u"Date"))), 0, 4)
        editbox.addWidget(self.date, 1, 4)

        editbox.addWidget(butt, 1, 5)

        butt.clicked.connect(self.add_poulailler)
        editbox.addWidget(butt, 1, 2)

        formbox.addLayout(editbox)

        vbox.addLayout(formbox)
        vbox.addLayout(tablebox)
        self.setLayout(vbox)

    def add_poulailler(self):
        ''' add operation '''
        if unicode(self.num.text()) != "":
            poussin = Poulailler()
            poussin.type_ = int(self.type_.currentIndex())
            poussin.num = int(self.num.text())
            poussin.nbr_sujet = int(self.nbr_sujet.text())
            poussin.stock_maxi = int(self.stock_maxi.text())
            poussin.date = self.date.text()
            poussin.save()
            self.poussin_table.refresh_()
            raise_success(_(u"Confirmation"), _(u"Registered operation"))
        else:
            raise_error(_("Error"), _(u"Give the name of the store"))


class PoulaillerTableWidget(F_TableWidget):

    def __init__(self, parent, *args, **kwargs):
        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)
        self.header = [_(u"Nom"), _(u"Nombre de sujet"), _('Max'), _('Date')]
        self.set_data_for()
        self.refresh(True)

    def refresh_(self):
        """ """
        self._reset()
        self.set_data_for()
        self.refresh()

    def set_data_for(self):
        self.data = [(p.__unicode__(), p.nbr_sujet,\
                      p.stock_maxi,p.date) for p in Poulailler.all()]
