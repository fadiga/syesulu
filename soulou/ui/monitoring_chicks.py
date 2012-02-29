#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: alou

from datetime import datetime
from PyQt4 import QtGui, QtCore
from database import *
from common import (F_Widget, F_PageTitle, F_TableWidget, F_BoxTitle,
                    Button_save, FormatDate, IntLineEdit, FloatLineEdit)
from util import raise_success, raise_error
from tabpane import tabbox


class PsRapportViewWidget(F_Widget):
    """ Gestion de ps  """

    def __init__(self, parent=0, *args, **kwargs):
        super(PsRapportViewWidget, self).__init__(parent=parent,
                                                        *args, **kwargs)

        self.setWindowTitle(_(u"suivi"))
        vbox = QtGui.QVBoxLayout()
        self.title = F_PageTitle(_("suivi"))

        tablebox = QtGui.QVBoxLayout()
        tablebox.addWidget(F_BoxTitle(_(u"Table suivi")))
        self.chiks_table = ChiksTableWidget(parent=self)
        tablebox.addWidget(self.chiks_table)

        formbox = QtGui.QVBoxLayout()
        editbox = QtGui.QGridLayout()

        self.nb_death = IntLineEdit()
        self.nb_eggs = IntLineEdit()
        self.weight = FloatLineEdit()
        self.date_report = FormatDate(QtCore.QDate.currentDate())
        self.date_report.setFont(QtGui.QFont("Courier New", 10, True))

        #Combobox widget
        self.list_chicken_coop = ChickenCoop.all()
        self.chicken_coop = QtGui.QComboBox()
        for index in xrange(0, len(self.list_chicken_coop)):
            op = self.list_chicken_coop[index]
            sentence = _(u"%(libelle)s") % {'libelle': op.full_name()}
            self.chicken_coop.addItem(sentence, QtCore.QVariant(op.id))

        butt = Button_save(_(u"Save"))
        #~ self.nb_total_chiks.setValidator(QtGui.QIntValidator())
        editbox.addWidget(QtGui.QLabel((_(u"Date"))), 0, 0)
        editbox.addWidget(self.date_report, 1, 0)
        editbox.addWidget(QtGui.QLabel((_(u"Poulailler"))), 0, 1)
        editbox.addWidget(self.chicken_coop, 1, 1)
        editbox.addWidget(QtGui.QLabel((_(u"Mort"))), 0, 2)
        editbox.addWidget(self.nb_death, 1, 2)
        editbox.addWidget(QtGui.QLabel((_(u"Poids"))), 0, 3)
        editbox.addWidget(self.weight, 1, 3)
        editbox.addWidget(QtGui.QLabel((_(u"Nombre d'oeufs"))), 0, 4)
        editbox.addWidget(self.nb_eggs, 1, 4)
        editbox.addWidget(butt, 1, 5)

        butt.clicked.connect(self.add_chiks)

        formbox.addLayout(editbox)

        vbox.addLayout(formbox)
        vbox.addLayout(tablebox)
        self.setLayout(vbox)

    def add_chiks(self):
        ''' add operation '''

        date_ = self.date_report.text()
        day, month, year = date_.split('/')
        dt = datetime.now()
        chicken_coop = self.list_chicken_coop[self.chicken_coop.currentIndex()]
        datetime_ = datetime(int(year), int(month), int(day),
                             int(dt.hour), int(dt.minute), int(dt.second),
                             int(dt.microsecond))

        if unicode(self.nb_death.text()) != "":
            ps = PsRapport()
            ps.nb_death = int(self.nb_death.text())
            ps.nb_eggs = int(self.nb_eggs.text())
            ps.date_report = datetime_
            ps.chickencoop = chicken_coop
            ps.save()
            self.chiks_table.refresh_()
            raise_success(_(u"Confirmation"), _(u"Registered operation"))
        else:
            raise_error(_("Error"), _(u"Give the name of the store"))


class ChiksTableWidget(F_TableWidget):

    def __init__(self, parent, *args, **kwargs):
        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)
        self.header = [_(u"Poulailler"), _('Mort'), _('restant'), \
                       _('Oeufs'), _('Poids'), _('Date rapport')]
        self.set_data_for()
        self.refresh(True)

    def refresh_(self):
        """ """
        self._reset()
        self.set_data_for()
        self.refresh()

    def set_data_for(self):

        self.data = [(ps.chickencoop.full_name(), ps.nb_death, ps.remaining, \
        ps.nb_eggs, ps.date_report) for ps in PsRapport.all()]

