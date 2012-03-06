#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: alou

from datetime import datetime

from PyQt4 import QtGui, QtCore

from database import PsRapport, ChickenCoop
from common import (F_Widget, F_PageTitle, F_TableWidget, F_BoxTitle,
                    Button_save, FormatDate, IntLineEdit, FloatLineEdit)
from util import raise_error


class PsRapportViewWidget(F_Widget):
    """ Gestion de ps  """

    def __init__(self, parent=0, *args, **kwargs):
        super(PsRapportViewWidget, self).__init__(parent=parent,
                                                        *args, **kwargs)

        self.setWindowTitle(_(u"Monitoring"))
        vbox = QtGui.QVBoxLayout()
        self.title = F_PageTitle(_("Monitoring"))

        tablebox = QtGui.QVBoxLayout()
        tablebox.addWidget(F_BoxTitle(_(u"Table of monitored")))
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
            sentence = _(u"%(full_name)s") % {'full_name': op.full_name()}
            self.chicken_coop.addItem(sentence, QtCore.QVariant(op.id))

        butt = Button_save(_(u"Save"))
        editbox.addWidget(QtGui.QLabel((_(u"Date"))), 0, 0)
        editbox.addWidget(self.date_report, 1, 0)
        editbox.addWidget(QtGui.QLabel((_(u"Chicken coop"))), 0, 1)
        editbox.addWidget(self.chicken_coop, 1, 1)
        editbox.addWidget(QtGui.QLabel((_(u"Death"))), 0, 2)
        editbox.addWidget(self.nb_death, 1, 2)
        editbox.addWidget(QtGui.QLabel((_(u"Weight"))), 0, 3)
        editbox.addWidget(self.weight, 1, 3)
        editbox.addWidget(QtGui.QLabel((_(u"Number of eggs"))), 0, 4)
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
        print chicken_coop.id
        datetime_ = datetime(int(year), int(month), int(day), int(dt.hour),
                             int(dt.minute), int(dt.second),
                             int(dt.microsecond))

        if unicode(self.nb_death.text()) != "":
            ps = PsRapport()
            ps.nb_death = int(self.nb_death.text())
            ps.weight = int(self.weight.text())
            ps.nb_eggs = int(self.nb_eggs.text())
            ps.date_report = datetime_
            ps.psarrivage = chicken_coop.id
            ps.save()
            self.nb_death.clear()
            self.nb_eggs.clear()
            self.weight.clear()
            self.chiks_table.refresh_()
        else:
            raise_error(_("Error"), _(u"Give the number of the death"))


class ChiksTableWidget(F_TableWidget):

    def __init__(self, parent, *args, **kwargs):
        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)
        self.header = [_('Date'), _(u"Chicken coop"), _('Death'), \
                       _('Remaining'), _('Eggs'), _('Weight')]
        self.set_data_for()
        self.refresh(True)

    def refresh_(self):
        """ """
        self._reset()
        self.set_data_for()
        self.refresh()

    def set_data_for(self):

        self.data = [(ps.date_report, ps.psarrivage.chicken_coop.full_name(), \
                      ps.nb_death, ps.remaining, ps.nb_eggs, ps.weight) \
                      for ps in PsRapport.select() \
                                         .order_by(('date_report', 'desc'))]
