#!/usr/bin/env python
# encoding=utf-8
# maintainer: fad

from PyQt4 import QtGui, QtCore

from common import F_Widget
from magasins import MagasinViewWidget
from report_period import ReportViewWidget
from exports import export_database_as_file
from alerteview import AlertViewWidget
from transfert import TransferttViewWidget
from produits import ProduitViewWidget
from chiks import ChiksViewWidget
from chickencoop import ChickenCoopViewWidget


class MenuBar(QtGui.QMenuBar, F_Widget):

    def __init__(self, parent=None, *args, **kwargs):
        QtGui.QMenuBar.__init__(self, parent, *args, **kwargs)

        #Menu File
        file_ = self.addMenu(_(u"&File"))
        # Export
        export = file_.addMenu(_(u"&Export data"))

        export.addAction(_(u"Backup Database"), self.goto_export_db)

        # Exit
        exit_ = QtGui.QAction(_(u"Exit"), self)
        exit_.setShortcut("Ctrl+Q")
        exit_.setToolTip(_("Exit the application"))
        self.connect(exit_, QtCore.SIGNAL("triggered()"), \
                                         self.parentWidget(), \
                                         QtCore.SLOT("close()"))
        file_.addAction(exit_)

        # Menu aller à
        goto_ = self.addMenu(_(u"&Go to"))

        #Gestion des stocks
        stock = goto_.addMenu(_(u"&Gestion de store"))

        # magasin
        store = QtGui.QAction(_(u"New store"), self)
        store.setShortcut("Ctrl+M")
        self.connect(store, QtCore.SIGNAL("triggered()"),
                                            self.goto_store)
        stock.addAction(store)
        # Produit
        Product = QtGui.QAction(_(u"New Product"), self)
        Product.setShortcut("Ctrl+S")
        self.connect(Product, QtCore.SIGNAL("triggered()"),
                                            self.goto_product)
        stock.addAction(Product)

        #Gestion des suivis
        followed = goto_.addMenu(_(u"&Followed"))

        # Poussinière
        Chiks = QtGui.QAction(_(u"New Chiks"), self)
        Chiks.setShortcut("Ctrl+C")
        self.connect(Chiks, QtCore.SIGNAL("triggered()"),
                                            self.goto_chiks)
        followed.addAction(Chiks)
        # Poulailler
        chickencoop = QtGui.QAction(_(u"New chickencoop"), self)
        chickencoop.setShortcut("Ctrl+E")
        self.connect(chickencoop, QtCore.SIGNAL("triggered()"),
                                            self.goto_chickencoop)
        followed.addAction(chickencoop)

        # alerte
        alerte = QtGui.QAction(_(u"Add alert"), self)
        alerte.setShortcut("Ctrl+A")
        self.connect(alerte, QtCore.SIGNAL("triggered()"),
                                            self.goto_editalerte)
        goto_.addAction(alerte)

        # Rapport periodique
        rap_p = QtGui.QAction(_(u"Periodic report"), self)
        rap_p.setShortcut("Ctrl+P")
        self.connect(rap_p, QtCore.SIGNAL("triggered()"),
                                            self.report_period)
        goto_.addAction(rap_p)

        # Rapport inventaire
        rap_inv = QtGui.QAction(_(u"Inventory"), self)
        rap_inv.setShortcut("Ctrl+I")
        self.connect(rap_inv, QtCore.SIGNAL("triggered()"),
                                            self.goto_inventaire)
        goto_.addAction(rap_inv)

        # Transfert
        transfert = QtGui.QAction(_(u"Transfert"), self)
        transfert.setShortcut("Ctrl+M")
        self.connect(transfert, QtCore.SIGNAL("triggered()"),
                                            self.goto__transfert_chiks)
        goto_.addAction(transfert)

        #Menu Aide
        help_ = self.addMenu(_(u"help"))
        help_.addAction(QtGui.QIcon('images/help.png'), _("help"),
                                    self.goto_help)
        help_.addAction(QtGui.QIcon('images/about.png'), _(u"About"),
                                    self.goto_about)

    #Inventaire
    def goto_editalerte(self):
        self.open_dialog(AlertViewWidget)

    #Inventaire
    def goto_inventaire(self):
        pass

    #Rapport periodique.
    def report_period(self):
         self.change_main_context(ReportViewWidget)

    def goto__transfert_chiks(self):
        self.change_main_context(TransferttViewWidget)

    def goto_store(self):
        self.change_main_context(MagasinViewWidget)

    #Produit
    def goto_product(self):
        self.change_main_context(ProduitViewWidget)

    def goto_chiks(self):
        self.change_main_context(ChiksViewWidget)

    def goto_chickencoop(self):
        self.change_main_context(ChickenCoopViewWidget)

    #Export the database.
    def goto_export_db(self):
        export_database_as_file()

    #Aide
    def goto_help(self):
        mbox = QtGui.QMessageBox.about(self, _(u"help"),
                                       _(u"Need Help"))
    #About
    def goto_about(self):
        mbox = QtGui.QMessageBox.about(self, _(u"About"),
                                       _(u"gestion de poulailler\n\n"
                                         u"Developpeur: Ibrahima Fadiga, Alou Dolo\n\n"
                                         u"© 2012 Fanga comp s.à.r.l\n"
                                         u"Bamako(Mali)\n"
                                         u"Tel: (223)76 43 38 90\n"
                                         u"E-mail: ibfadiga@gmail.com"))
