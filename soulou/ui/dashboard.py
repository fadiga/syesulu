#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fadiga

from PyQt4 import QtGui

from common import F_Widget, F_PageTitle, F_TableWidget, F_BoxTitle
from tabpane import tabbox
from model import *


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

        self.title_alert = F_BoxTitle(_(u"Les alertes "))
        self.table_alert = AlertTableWidget(parent=self)
        table_alert.addWidget(self.title_alert) 
        table_alert.addWidget(self.table_alert)

        self.title_etat = F_BoxTitle(_(u"Les stocks actual"))
        self.table_etat = EtatTableWidget(parent=self)
        table_etat.addWidget(self.title_etat)
        table_etat.addWidget(self.table_etat)

        tab_widget = tabbox((table_etat, _(u"Etat")),
                            (table_alert, _(u"warning")))

        vbox.addWidget(self.title)
        vbox.addWidget(tab_widget)
        self.setLayout(vbox)


class EtatTableWidget(F_TableWidget):
    pass


class AlertTableWidget(F_TableWidget):

    def __init__(self, parent, *args, **kwargs):
        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)
        self.header = [_(u"Objets"), _(u"Date debut"), _('Date fin')
                      , _('Status')]
        self.set_data_for()
        self.refresh(True)

    def refresh_(self):
        """ """
        self._reset()
        self.set_data_for()
        self.refresh()

    def set_data_for(self):

        self.data = [(al.objets, al.date_debut.strftime(u'%x %Hh:%Mmn'), 
                      al.date_fin.strftime(u'%x %Hh:%Mmn'), al.status)
                                                    for al in Alerte.all()]

