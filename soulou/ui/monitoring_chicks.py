#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: alou

from datetime import datetime
from PyQt4 import QtGui, QtCore
from database import *
from common import (F_Widget, F_PageTitle, F_TableWidget, F_BoxTitle,
                    Button_save, FormatDate)
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

        self.race = QtGui.QLineEdit()
        self.nb_total_chiks = QtGui.QLineEdit()
        self.date_arriver = FormatDate(QtCore.QDate.currentDate())
        self.date_arriver.setFont(QtGui.QFont("Courier New", 10, True))

        #Combobox widget
        self.list_chicken_coop = ChickenCoop.all()
        self.chicken_coop = QtGui.QComboBox()
        for index in xrange(0, len(self.list_chicken_coop)):
            op = self.list_chicken_coop[index]
            sentence = _(u"%(libelle)s") % {'libelle': op.full_name()}
            self.chicken_coop.addItem(sentence, QtCore.QVariant(op.id))

        butt = Button_save(_(u"Save"))
        self.nb_total_chiks.setValidator(QtGui.QIntValidator())
        editbox.addWidget(QtGui.QLabel((_(u"Date"))), 0, 0)
        editbox.addWidget(self.date_arriver, 1, 0)
        editbox.addWidget(QtGui.QLabel((_(u"Poulailler"))), 0, 1)
        editbox.addWidget(self.chicken_coop, 1, 1)
        editbox.addWidget(QtGui.QLabel((_(u"Race"))), 0, 2)
        editbox.addWidget(self.race, 1, 2)
        editbox.addWidget(QtGui.QLabel((_(u"Nombre de sujet"))), 0, 3)
        editbox.addWidget(self.nb_total_chiks, 1, 3)
        editbox.addWidget(butt, 1, 4)

        butt.clicked.connect(self.add_chiks)

        formbox.addLayout(editbox)

        vbox.addLayout(formbox)
        vbox.addLayout(tablebox)
        self.setLayout(vbox)

    def add_chiks(self):
        ''' add operation '''

        date_ = self.date_arriver.text()
        day, month, year = date_.split('/')
        dt = datetime.now()
        chicken_coop = self.list_chicken_coop[self.chicken_coop.currentIndex()]
        datetime_ = datetime(int(year), int(month), int(day),
                             int(dt.hour), int(dt.minute), int(dt.second),
                             int(dt.microsecond))

        if unicode(self.nb_total_chiks.text()) != "":
            ps = PsArrivage()
            ps.race = unicode(self.race.text())
            ps.nb_total_chiks = int(self.nb_total_chiks.text())
            ps.arrival_date = datetime_
            ps.chicken_coop = chicken_coop
            ps.save()
            self.chiks_table.refresh_()
            raise_success(_(u"Confirmation"), _(u"Registered operation"))
        else:
            raise_error(_("Error"), _(u"Give the name of the store"))


class ChiksTableWidget(F_TableWidget):

    def __init__(self, parent, *args, **kwargs):
        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)
        self.header = [_(u"Poulailler"), _('Mort'), _('restant'), \
                       _('Oeufs'), _('Poids'), _('Date'), _('Date rapport')]
        self.set_data_for()
        self.refresh(True)

    def refresh_(self):
        """ """
        self._reset()
        self.set_data_for()
        self.refresh()

    def set_data_for(self):
        try:
            self.data = [(ps.race, ps.chicken_coop, \
            ps.nb_total_chiks, ps.arrival_date) for ps in PsRapport.all()]
        except:
            pass
