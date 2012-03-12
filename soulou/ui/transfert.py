#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: alou

from datetime import datetime

from PyQt4 import QtGui, QtCore

from database import PsRapport, ChickenCoop, PsArrivage
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

        formbox = QtGui.QVBoxLayout()
        editbox = QtGui.QGridLayout()
        l = 0

        editbox.addWidget(QtGui.QLabel((_(u"Date"))), 0, 0)
        editbox.addWidget(QtGui.QLabel((_(u"Chicken coop"))), 0, 1)
        editbox.addWidget(QtGui.QLabel((_(u"Status"))), 0, 2)
        editbox.addWidget(QtGui.QLabel((_(u"Number of chiks"))), 0, 3)

        self.list_data = []
        for chicken_coop in list(ChickenCoop.select()):
            print chicken_coop.full_name()
            id_ = chicken_coop.id
            print id_
            c = 0
            self.nb_chiks = IntLineEdit()
            self.num = FloatLineEdit()
            self.date_transfert = FormatDate(QtCore.QDate.currentDate())
            self.date_transfert.setFont(QtGui.QFont("Courier New", 10, True))

            #Combobox widget
            self.list_chicken_coop = list(ChickenCoop.select())
            #~ print self.list_chicken_coop
            self.chicken_coop = QtGui.QComboBox()
            for index in xrange(0, len(self.list_chicken_coop)):
                print index
                op = self.list_chicken_coop[index]
                sentence = _(u"%(libelle)s") % {'libelle': op.full_name()}
                self.chicken_coop.addItem(sentence, QtCore.QVariant(op.id))

            #Combobox widget
            self.list_transfert = ['Nouveau', 'Transfert', 'Reforme']
            self.transfert = QtGui.QComboBox()
            for index in self.list_transfert:
                self.transfert.addItem(u'%(type)s' % {'type': index})
            i = 0
            for ch in self.list_chicken_coop:
                i += 1
                print ch.id, 'toto'
                if ch.full_name() == chicken_coop.full_name():
                    idex =i
                    self.chicken_coop.setCurrentIndex(idex)
            try:
                ps = chicken_coop.chicken_coops.get()
                print ps, chicken_coop.id, 'dolo'
                self.transfert.setCurrentIndex(ps.status)
                pr = ps.psarrivages.get()
                print pr.remaining, 'alou'
                self.nb_chiks = IntLineEdit(str(pr.remaining))
            except:
                #~ raise
                self.nb_chiks = IntLineEdit(str(0))
                ps = None

            editbox.addWidget(self.date_transfert, l + 1, c)
            c += 1

            editbox.addWidget(self.chicken_coop, l +1 , c)
            c += 1

            editbox.addWidget(self.transfert, l +1, c)
            c += 1

            editbox.addWidget(self.nb_chiks, l+1, c)
            c += 1

            l += 1

            self.list_data.append((self.chicken_coop, self.date_transfert,\
                            self.transfert, self.nb_chiks, self.num))
        l += 1
        butt = Button_save(_(u"Tranfert"))
        editbox.addWidget(butt, l, c)
        butt.clicked.connect(self.add_transfert)

        formbox.addLayout(editbox)
        vbox.addLayout(formbox)
        self.setLayout(vbox)

    def add_transfert(self):
        ''' add operation '''

        for data in self.list_data:
            chicken_coop = data[0].currentIndex()
            date_ = data[1].text()
            day, month, year = date_.split('/')
            dt = datetime.now()
            #~ chicken_coop = self.list_chicken_coop[self.chicken_coop.currentIndex()]
            #~ print chicken_coop.id
            datetime_ = datetime(int(year), int(month), int(day), int(dt.hour),
                                 int(dt.minute), int(dt.second),
                                 int(dt.microsecond))
            transfert = data[2].currentIndex()
            nb_chiks = data[3].text()
            num = data[4].text()
            #~ print name, datetime_, transfert, nb_chiks, num
            try:
                ps = PsArrivage.get(id=data[6])
                ps.status = int(transfert)
                ps.nb_total_chiks -= int(nb_chiks)
                ps.save()

                chicken_coop = ChickenCoop.get(id=ps.chicken_coop_id)
                chicken_coop.status = 0
                chicken_coop.save()
            except:
                ps = None
            print ps

        #~ if unicode(self.nb_chiks.text()) != "":
            #~ ps = PsArrivage()
            #~ ps.race = int(self.nb_chiks.text())
            #~ ps.nb_total_chiks = int(self.num.text())
            #~ ps.arrival_date = datetime_
            #~ ps.chicken_coop = chicken_coop.id
            #~ ps.status = chicken_coop.id
            #~ ps.save()
            #~ self.nb_chiks.clear()
            #~ self.nb_eggs.clear()
            #~ self.num.clear()
            #~ self.tranfert_table.refresh_()
        #~ else:
            #~ raise_error(_("Error"), _(u"Give the number of the death"))


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
