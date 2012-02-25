#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fadiga

import sys

from PyQt4 import QtGui, QtCore

from model import *
from gstockreports import G_reportViewWidget
from dashboard import DashbordViewWidget
from magasins import MagasinViewWidget
from produits import ProduitViewWidget
from menubar import MenuBar
from statusbar import GStatusBar


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.resize(900, 650)
        self.setWindowTitle(u"Gestion du poulailer")
        self.setWindowIcon(QtGui.QIcon('images/mali.png'))

        self.toolbar = QtGui.QToolBar()
        self.toolbar.addAction(QtGui.QIcon('images/quiter.png'), \
                                                    _(u"Exit"), self.goto_exit)
        self.toolbar.addSeparator()
        self.toolbar.addAction(_(u"Dashboard"), self.accueil)
        self.toolbar.addSeparator()
        self.toolbar.addAction(_(u"Produit"), self.goto_produit)
        self.toolbar.addSeparator()
        self.toolbar.addAction(_(u"Management reports"), \
                                                self.goto_gestion_rapport)
        self.addToolBar(self.toolbar)

        self.menubar = MenuBar(self)
        self.setMenuBar(self.menubar)
        self.statusbar = GStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.change_context(DashbordViewWidget)

    def goto_exit(self):
        self.close()

    def accueil(self):
        self.setWindowTitle(u"Accueil")
        self.change_context(DashbordViewWidget)

    def goto_produit(self):
        self.setWindowTitle(_(u"Products"))
        self.change_context(ProduitViewWidget)
        
    def goto_gestion_rapport(self):
        self.setWindowTitle(_(u"Management Reports"))
        self.change_context(G_reportViewWidget)


    def change_context(self, context_widget, *args, **kwargs):

        # instanciate context
        self.view_widget = context_widget(parent=self, *args, **kwargs)

        # attach context to window
        self.setCentralWidget(self.view_widget)

    def open_dialog(self, dialog, modal=False, *args, **kwargs):
        d = dialog(parent=self, *args, **kwargs)
        d.setModal(modal)
        d.setWindowOpacity(0.97)
        d.exec_()

    # def open_Dock(self, dock, modal=False, *args, **kwargs):
    #     d = dock(parent=self, *args, **kwargs)
    #     d.setModal(modal)
    #     d.exec_()
