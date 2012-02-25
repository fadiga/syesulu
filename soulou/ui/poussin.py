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


class PoussinViewWidget(F_Widget):
    """ Gestion de ps  """

    def __init__(self, parent=0, *args, **kwargs):
        super(PoussinViewWidget, self).__init__(parent=parent,
                                                        *args, **kwargs)

        self.setWindowTitle(_(u"Poussin"))
        vbox = QtGui.QVBoxLayout()
        self.title = F_PageTitle(_("Poussin"))

        tablebox = QtGui.QVBoxLayout()
        tablebox.addWidget(F_BoxTitle(_(u"Table poussins")))
        self.poussin_table = PoussinTableWidget(parent=self)
        tablebox.addWidget(self.poussin_table)

        formbox = QtGui.QVBoxLayout()
        editbox = QtGui.QGridLayout()

        self.race = QtGui.QLineEdit()
        self.nbre_total_poussin = QtGui.QLineEdit()
        self.date_arriver = FormatDate(QtCore.QDate.currentDate())
        self.date_arriver.setFont(QtGui.QFont("Courier New", 10, True))

        #Combobox widget
        self.liste_poulailler = Poulailler.all()
        self.poulailler = QtGui.QComboBox()
        for index in xrange(0, len(self.liste_poulailler)):
            op = self.liste_poulailler[index]
            sentence = _(u"%(libelle)s") % {'libelle': op.full_name()}
            self.poulailler.addItem(sentence, QtCore.QVariant(op.id))

        butt = Button_save(_(u"Save"))
        self.nbre_total_poussin.setValidator(QtGui.QIntValidator())
        editbox.addWidget(QtGui.QLabel((_(u"Nombre de sujet"))), 0, 0)
        editbox.addWidget(self.nbre_total_poussin, 1, 0)
        editbox.addWidget(QtGui.QLabel((_(u"Poulailler"))), 0, 1)
        editbox.addWidget(self.poulailler, 1, 1)
        editbox.addWidget(QtGui.QLabel((_(u"Race"))), 0, 2)
        editbox.addWidget(self.race, 1, 2)
        editbox.addWidget(QtGui.QLabel((_(u"Date"))), 0, 3)
        editbox.addWidget(self.date_arriver, 1, 3)
        editbox.addWidget(butt, 1, 4)

        butt.clicked.connect(self.add_poussin)

        formbox.addLayout(editbox)

        vbox.addLayout(formbox)
        vbox.addLayout(tablebox)
        self.setLayout(vbox)

    def add_poussin(self):
        ''' add operation '''

        date_ = self.date_arriver.text()
        day, month, year = date_.split('/')
        dt = datetime.now()
        poulailler = self.liste_poulailler[self.poulailler.currentIndex()]
        datetime_ = datetime(int(year), int(month), int(day),
                             int(dt.hour), int(dt.minute), int(dt.second),
                             int(dt.microsecond))

        if unicode(self.nbre_total_poussin.text()) != "":
            ps = PsArrivage()
            ps.race = unicode(self.race.text())
            ps.nbre_total_poussin = int(self.nbre_total_poussin.text())
            ps.date_arriver = datetime_
            ps.poulailler = poulailler
            ps.save()
            self.poussin_table.refresh_()
            raise_success(_(u"Confirmation"), _(u"Registered operation"))
        else:
            raise_error(_("Error"), _(u"Give the name of the store"))


class PoussinTableWidget(F_TableWidget):

    def __init__(self, parent, *args, **kwargs):
        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)
        self.header = [_(u"Race"), _(u"Poulailler"), _('Nombre de sujet'), \
                       _('Date')]
        self.set_data_for()
        self.refresh(True)

    def refresh_(self):
        """ """
        self._reset()
        self.set_data_for()
        self.refresh()

    def set_data_for(self):
        try:
            self.data = [(ps.race, ps.poulailler, \
                      ps.nbre_total_poussin, ps.date_arriver) for ps in PsArrivage.all()]
        except:
            pass
