#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: alou

from datetime import datetime
from PyQt4 import QtGui, QtCore

from database import ChickenCoop
from common import (F_Widget, F_PageTitle, F_TableWidget, F_BoxTitle,
                    Button_save, FormatDate, IntLineEdit)
from util import raise_success, raise_error


class ChickenCoopViewWidget(F_Widget):
    """ Gestion de pasin  """

    def __init__(self, parent=0, *args, **kwargs):
        super(ChickenCoopViewWidget, self).__init__(parent=parent,
                                                        *args, **kwargs)

        self.setWindowTitle(_(u"Chicken Coop"))
        vbox = QtGui.QVBoxLayout()
        self.title = F_PageTitle(_("Chicken Coop"))

        tablebox = QtGui.QVBoxLayout()
        tablebox.addWidget(F_BoxTitle(_(u"Table Chicken Coop")))
        self.poussin_table = ChickenCoopTableWidget(parent=self)
        tablebox.addWidget(self.poussin_table)

        formbox = QtGui.QVBoxLayout()
        editbox = QtGui.QGridLayout()
        butt = Button_save(_(u"Save"))


        liste_type = [u"chicken coop", u"poussinière"]
        #Combobox widget
        self.type_ = QtGui.QComboBox()
        for index in liste_type:
            self.type_.addItem(u'%(type)s' % {'type': index})

        self.num = IntLineEdit()
        self.nbr_sujet = IntLineEdit()
        self.nbr_sujet_maxi = IntLineEdit()
        self.date = FormatDate(QtCore.QDate.currentDate())
        self.date.setFont(QtGui.QFont("Courier New", 10, True))

        self.num.setValidator(QtGui.QIntValidator())
        editbox.addWidget(QtGui.QLabel((_(u"Type"))), 0, 0)
        editbox.addWidget(self.type_, 1, 0)
        editbox.addWidget(QtGui.QLabel((_(u"Number of chicken coop"))), 0, 1)
        editbox.addWidget(self.num, 1, 1)
        editbox.addWidget(QtGui.QLabel((_(u"Max"))), 0, 2)
        editbox.addWidget(self.nbr_sujet_maxi, 1, 2)
        editbox.addWidget(QtGui.QLabel((_(u"Date"))), 0, 3)
        editbox.addWidget(self.date, 1, 3)

        editbox.addWidget(butt, 1, 4)

        butt.clicked.connect(self.add_chickencoop)
        editbox.addWidget(butt, 1, 2)

        formbox.addLayout(editbox)

        vbox.addLayout(formbox)
        vbox.addLayout(tablebox)
        self.setLayout(vbox)

    def add_chickencoop(self):
        ''' add operation '''
        date_ = self.date.text()
        day, month, year = date_.split('/')
        dt = datetime.now()
        datetime_ = datetime(int(year), int(month), int(day),
                             int(dt.hour), int(dt.minute), int(dt.second),
                             int(dt.microsecond))
        if unicode(self.num.text()) != "":
            poussin = ChickenCoop()
            poussin.type_ = int(self.type_.currentIndex())
            poussin.num = int(self.num.text())
            poussin.nbr_sujet_maxi = int(self.nbr_sujet_maxi.text())
            poussin.date = datetime_
            poussin.save()
            self.poussin_table.refresh_()
            raise_success(_(u"Confirmation"), _(u"Registered operation"))
        else:
            raise_error(_("Error"), _(u"Give the name of the store"))


class ChickenCoopTableWidget(F_TableWidget):

    def __init__(self, parent, *args, **kwargs):
        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)
        self.header = [_(u"Nom"), _(u"Max"), _('Date')]
        self.set_data_for()
        self.refresh(True)

    def refresh_(self):
        """ """
        self._reset()
        self.set_data_for()
        self.refresh()

    def set_data_for(self):
        self.data = [(p.__unicode__(), p.nbr_sujet_maxi,
                      p.date) for p in ChickenCoop.all()]
