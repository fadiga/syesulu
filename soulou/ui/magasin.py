#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: alou

from PyQt4 import QtGui

from common import F_Widget, F_PageTitle, F_TableWidget, F_BoxTitle
from tabpane import tabbox


class MagasinViewWidget(F_Widget):
    """ Gestion de magasin  """

    def __init__(self, parent=0, *args, **kwargs):
        super(MagasinViewWidget, self).__init__(parent=parent,
                                                        *args, **kwargs)

        self.setWindowTitle(_(u"Magasin"))
        vbox = QtGui.QVBoxLayout()
        box_left = QtGui.QHBoxLayout()
        box_rigth = QtGui.QHBoxLayout()
        table_etat = QtGui.QVBoxLayout()
        self.title = F_PageTitle(_("Magasin"))

        self.title_etat = F_BoxTitle(_(u"Magasin"))

        self.table_etat = EtatTableWidget(parent=self)
        vbox.addWidget(self.title)
        table_etat.addWidget(self.title_etat)
        table_etat.addWidget(self.table_etat)

        tab_widget = tabbox((table_etat, _(u"Magasini")))

        vbox.addWidget(tab_widget)
        self.setLayout(vbox)


class EtatTableWidget(F_TableWidget):

    pass
