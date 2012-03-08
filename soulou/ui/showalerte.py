#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fadiga

from PyQt4 import QtGui
from PyQt4 import QtCore

from common import (F_Widget, F_BoxTitle, Button, Button_save,
                    F_TableWidget)
from data_helper import alerte
from model import Alerte


class ShowAlViewWidget(QtGui.QDialog, F_Widget):

    def __init__(self, parent, *args, **kwargs):
        
        QtGui.QDialog.__init__(self, parent, *args, **kwargs)
        self.setWindowTitle(_(u"Alertes"))

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(F_BoxTitle(_(u"Créer une Alerte")))
        tablebox = QtGui.QVBoxLayout()
        self.al_table = AlTableWidget(parent=self)
        tablebox.addWidget(self.al_table)

        vbox = QtGui.QVBoxLayout()
        # Grid
        gridbox = QtGui.QGridLayout()
        butt = Button_save(_(u"Records the change"))
        butt.clicked.connect(self.update_alerte)
        cancel_but = Button(_(u"Cancel"))
        cancel_but.clicked.connect(self.cancel)
        gridbox.addWidget(butt, 3, 0)
        gridbox.addWidget(cancel_but, 3, 1)

        vbox.addLayout(tablebox)
        vbox.addLayout(gridbox)
        self.setLayout(vbox)

    def cancel(self):
        self.close()

    def update_alerte(self):
        self.al_table.saveTableItems()
        self.cancel()


class AlTableWidget(F_TableWidget):
    """ """

    def __init__(self, parent, *args, **kwargs):

        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)

        self.header = [_(u"Executer"), _(u"objets"), _(u"date d'alerte"), ""]

        self.set_data_for()
        self.refresh(True)

    def _item_for_data(self, row, column, data, context=None):
        if column == 0:
            # create check box as our editor.
            editor = QtGui.QCheckBox()
            return editor
        return super(AlTableWidget, self) \
                     ._item_for_data(row, column, data, context)


    def saveTableItems(self):
        n = self.rowCount()
        for i in range(n):
            item = self.cellWidget(i, 0)
            if item.checkState() == QtCore.Qt.Checked:                
                alert = Alerte.filter(id=self.data[i][3]).get()
                alert.status = False
                alert.save()


    def set_data_for(self, *args):
        alert, c = alerte()
        self.data = [("", al.objets, al.date_a, al.id) for al in alert]
