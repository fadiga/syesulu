#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: alou

from datetime import datetime

from PyQt4 import QtGui, QtCore

from database import PsRapport, ChickenCoop
from common import (F_Widget, F_PageTitle, F_TableWidget, F_BoxTitle,
                    Button_save, FormatDate, IntLineEdit, FloatLineEdit)
from util import raise_error

class TransferttViewWidget(F_Widget):

    def __init__(self, parent=0, *args, **kwargs):
        super(TransferttViewWidget, self).__init__(parent=parent,
                                                        *args, **kwargs)

        self.setWindowTitle(_(u"Transfert"))
        vbox = QtGui.QVBoxLayout()
        self.title = F_PageTitle(_("Transfert"))

        tablebox = QtGui.QVBoxLayout()
        tablebox.addWidget(F_BoxTitle(_(u"Table of transfert")))
        self.tranfert_table = TransfertTableWidget(parent=self)
        tablebox.addWidget(self.tranfert_table)

        formbox = QtGui.QVBoxLayout()
        editbox = QtGui.QGridLayout()

        self.nb_chiks = IntLineEdit()
        self.num = FloatLineEdit()
        self.date_transfert = FormatDate(QtCore.QDate.currentDate())
        self.date_transfert.setFont(QtGui.QFont("Courier New", 10, True))

        #Combobox widget
        self.list_chicken_coop = list(ChickenCoop.select().filter(type_=0))
        self.chicken_coop = QtGui.QComboBox()
        for index in xrange(0, len(self.list_chicken_coop)):
            op = self.list_chicken_coop[index]
            sentence = _(u"%(full_name)s") % {'full_name': op.full_name()}
            self.chicken_coop.addItem(sentence, QtCore.QVariant(op.id))

        butt = Button_save(_(u"Tranfert"))
        editbox.addWidget(QtGui.QLabel((_(u"Date"))), 0, 0)
        editbox.addWidget(self.date_transfert, 1, 0)
        editbox.addWidget(QtGui.QLabel((_(u"Chicken coop"))), 0, 1)
        editbox.addWidget(self.chicken_coop, 1, 1)
        editbox.addWidget(QtGui.QLabel((_(u"Number of chiks"))), 0, 2)
        editbox.addWidget(self.nb_chiks, 1, 2)
        editbox.addWidget(QtGui.QLabel((_(u"Nombre"))), 0, 3)
        editbox.addWidget(self.num, 1, 3)
        editbox.addWidget(butt, 1, 4)

        butt.clicked.connect(self.add_chiks)

        formbox.addLayout(editbox)

        vbox.addLayout(formbox)
        vbox.addLayout(tablebox)
        self.setLayout(vbox)

    def add_chiks(self):
        ''' add operation '''

        date_ = self.date_transfert.text()
        day, month, year = date_.split('/')
        dt = datetime.now()
        chicken_coop = self.list_chicken_coop[self.chicken_coop.currentIndex()]
        print chicken_coop.id
        datetime_ = datetime(int(year), int(month), int(day), int(dt.hour),
                             int(dt.minute), int(dt.second),
                             int(dt.microsecond))

        if unicode(self.nb_chiks.text()) != "":
            ps = PsRapport()
            ps.nb_chiks = int(self.nb_chiks.text())
            ps.num = int(self.num.text())
            ps.date_transfert = datetime_
            ps.psarrivage = chicken_coop.id
            ps.save()
            self.nb_chiks.clear()
            self.nb_eggs.clear()
            self.num.clear()
            self.tranfert_table.refresh_()
        else:
            raise_error(_("Error"), _(u"Give the number of the death"))


class TransfertTableWidget(F_TableWidget):

    def __init__(self, parent, *args, **kwargs):
        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)
        self.header = [_('Date'), _(u"Chicken coop"), _('Death'), \
                       _('Remaining'), _('Eggs'), _('num')]
        #~ self.set_data_for()
        self.refresh(True)

    def refresh_(self):
        """ """
        self._reset()
        self.set_data_for()
        self.refresh()

    def set_data_for(self):

        self.data = [(ps.date_transfert, ps.psarrivage.chicken_coop.full_name(), \
                      ps.nb_chiks, ps.remaining, ps.num) \
                      for ps in PsRapport.select() \
                                         .order_by(('date_transfert', 'desc'))]
