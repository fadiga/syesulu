#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fadiga

from PyQt4 import QtGui
from PyQt4 import QtCore

from common import (F_Widget, F_BoxTitle, Button_save,
                    FormatDate, FormLabel)
from util import raise_error, raise_success
from model import *


class AlertViewWidget(QtGui.QDialog, F_Widget):
    def __init__(self, parent, *args, **kwargs):
        QtGui.QDialog.__init__(self, parent, *args, **kwargs)
        self.setWindowTitle(_(u"Alertes"))

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(F_BoxTitle(_(u"Créer une Alerte")))
        self.object = QtGui.QLineEdit()
        self.on_date = FormatDate(QtCore.QDate(date.today().year, 01, 01))
        self.end_date = FormatDate(QtCore.QDate.currentDate())

        vbox = QtGui.QVBoxLayout()
        # Grid
        gridbox = QtGui.QGridLayout()
        gridbox.addWidget(FormLabel(_(u"Object")), 0, 0)
        gridbox.addWidget(self.object, 1, 0)
        gridbox.addWidget(FormLabel(_(u"On date")), 1, 1)
        gridbox.addWidget(self.on_date, 1, 2)
        gridbox.addWidget(FormLabel(_(u"End date")), 2, 1)
        gridbox.addWidget(self.end_date, 2, 2)
        gridbox.addWidget(FormLabel(""), 2, 3)
        gridbox.setColumnStretch(3, 5)
        butt = Button_save(_(u"Records the change"))
        butt.clicked.connect(self.save_alerte)
        cancel_but = Button_save(_(u"Cancel"))
        cancel_but.clicked.connect(self.cancel)
        gridbox.addWidget(butt, 4, 1)
        gridbox.addWidget(cancel_but, 4, 2)

        vbox.addLayout(gridbox)
        self.setLayout(vbox)

    def cancel(self):
        self.close()

    def save_alerte(self):

        self.cancel()
        raise_success(_(u"Confirmation"), _(u"The store has been changing"))
