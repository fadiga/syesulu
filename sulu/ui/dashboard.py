#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fadiga

from PyQt4 import QtGui

from common import F_Widget, F_PageTitle, F_TableWidget, F_BoxTitle
from tabpane import tabbox
from model import Alerte


class DashbordViewWidget(F_Widget):
    """ Shows the home page  """

    def __init__(self, parent=0, *args, **kwargs):
        super(DashbordViewWidget, self).__init__(parent=parent,
                                                        *args, **kwargs)

        self.setWindowTitle(_(u"Dashboard"))
        vbox = QtGui.QVBoxLayout()
        box_left = QtGui.QHBoxLayout()
        box_rigth = QtGui.QHBoxLayout()
        table_etat = QtGui.QVBoxLayout()
        table_alert = QtGui.QVBoxLayout()

        self.title = F_PageTitle(_("Dashboard"))

        self.title_alert = F_BoxTitle(_(u"Alerts"))
        self.table_alert = AlertTableWidget(parent=self)
        table_alert.addWidget(self.title_alert)
        table_alert.addWidget(self.table_alert)

        self.title_etat = F_BoxTitle(_(u"Current stocks"))
        self.table_etat = EtatTableWidget(parent=self)
        table_etat.addWidget(self.title_etat)
        table_etat.addWidget(self.table_etat)

        tab_widget = tabbox((table_etat, _(u"Status")),
                            (table_alert, _(u"Warning")))

        vbox.addWidget(self.title)
        vbox.addWidget(tab_widget)
        self.setLayout(vbox)
        

class EtatTableWidget(F_TableWidget):
    def __init__(self, parent, *args, **kwargs):
        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)
        self.header = [_(u""), _(u""), _("")]
        self.set_data_for()
        self.refresh(True)

    def refresh_(self):
        """ """
        self._reset()
        self.set_data_for()
        self.refresh()

    def set_data_for(self):
        self.data = [(al.objets, al.date_a, al.status) \
                                                  for al in Alerte.all()]


class AlertTableWidget(F_TableWidget):

    def __init__(self, parent, *args, **kwargs):
        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)
        self.header = [_(u"Objets"), _(u"Date d'alerte"), _("Status")]
        self.set_data_for()
        self.refresh(True)

    def refresh_(self):
        """ """
        self._reset()
        self.set_data_for()
        self.refresh()

    def set_data_for(self):
        self.data = [(al.objets, al.date_a, al.status) \
                                                  for al in Alerte.all()]

    def _item_for_data(self, row, column, data, context=None):
        if column == 2 and self.data[row][2] == 0:
            return QtGui.QTableWidgetItem(QtGui.QIcon("images/tick.ico"),
                                                      u"")
        if column == 2 and self.data[row][2] == 1:
            return QtGui.QTableWidgetItem(QtGui.QIcon("images/star.ico"),
                                                      u"")

        return super(AlertTableWidget, self)._item_for_data(row, column,
                                                            data, context)
