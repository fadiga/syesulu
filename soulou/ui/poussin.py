#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: alou

from PyQt4 import QtGui
from database import *
from common import (F_Widget, F_PageTitle, F_TableWidget, F_BoxTitle,
                    Button_save)
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
        self.date_arriver = QtGui.QDateEdit()

        liste_type = [p.__unicode__() for p in Poulailler.all()]
        self.poulailler = QtGui.QComboBox()
        for index in liste_type:
            self.poulailler.addItem(u'%(type)s' % {'type': index})

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

        if unicode(self.nbre_total_poussin.text()) != "":
            ps = PsArrivage()
            ps.race = unicode(self.race.text())
            ps.nbre_total_poussin = int(self.nbre_total_poussin.text())
            ps.date_arriver = 800
            print self.poulailler.currentIndex()
            ps.poulailler = 1
            ps.save()
            self.poussin_table.refresh_()
            raise_success(_(u"Confirmation"), _(u"Registered operation"))
        else:
            raise_error(_("Error"), _(u"Give the name of the store"))


class PoussinTableWidget(F_TableWidget):

    def __init__(self, parent, *args, **kwargs):
        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)
        self.header = [_(u"Nombre de sujet"), _(u"Poulailler"), _('Race'), \
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
            self.data = [(ps.race, ps.nbre_total_poussin, ps.date_arriver, \
                      ps.poulailler) for ps in PsArrivage.all()]
        except:
            pass
