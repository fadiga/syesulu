#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fadiga

from PyQt4 import QtGui
from PyQt4 import QtCore

from common import (F_Widget, F_BoxTitle, Button_save,
                    FormatDate, FormLabel)
from util import raise_success
from model import Alerte
from data_helper import format_date

class AlertViewWidget(QtGui.QDialog, F_Widget):
    def __init__(self, parent, *args, **kwargs):
        QtGui.QDialog.__init__(self, parent, *args, **kwargs)
        self.setWindowTitle(_(u"Alerts"))

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(F_BoxTitle(_(u"Create Alert")))
        self.objets = QtGui.QTextEdit()
        self.date_a = FormatDate(QtCore.QDate.currentDate())

        vbox = QtGui.QVBoxLayout()
        # Grid
        gridbox = QtGui.QGridLayout()
        gridbox.addWidget(FormLabel(_(u"Objets")), 0, 0)
        gridbox.addWidget(self.objets, 0, 1)
        gridbox.addWidget(FormLabel(_(u"On date")), 1, 0)
        gridbox.addWidget(self.date_a, 1, 1)
        gridbox.setColumnStretch(3, 3)
        butt = Button_save(_(u"Records the change"))
        butt.clicked.connect(self.save_alerte)
        cancel_but = Button_save(_(u"Cancel"))
        cancel_but.clicked.connect(self.cancel)
        gridbox.addWidget(butt, 3, 0)
        gridbox.addWidget(cancel_but, 3, 1)

        vbox.addLayout(gridbox)
        self.setLayout(vbox)

    def cancel(self):
        self.close()

    def save_alerte(self):
        alt = Alerte()
        alt.objets = unicode(self.objets.toPlainText())
        alt.date_a = format_date(self.date_a.text())
        alt.save()
 
        self.cancel()
        raise_success(_(u"Confirmation"), _(u"The store has been changing"))
