#!/usr/bin/env python
# encoding=utf-8
# maintainer: fad

from PyQt4 import QtGui, QtCore

from common import F_Widget


class MenuBar(QtGui.QMenuBar, F_Widget):

    def __init__(self, parent=None, *args, **kwargs):
        QtGui.QMenuBar.__init__(self, parent, *args, **kwargs)

        #Menu File
        file_ = self.addMenu(_(u"&File"))
        # Export
        export = file_.addMenu(_(u"&Export data"))

        export.addAction(_(u"Backup Database"), self.goto_export_db)

        export.addAction(_(u"In an Excel file"),\
                                        self.goto_export_excel)
        # Exit
        # Exit
        exit_ = QtGui.QAction(_(u"Exit"), self)
        exit_.setShortcut("Ctrl+Q")
        exit_.setToolTip(_("Quiter l'application"))
        self.connect(exit_, QtCore.SIGNAL("triggered()"), \
                                         self.parentWidget(), \
                                         QtCore.SLOT("close()"))
        file_.addAction(exit_)

        # Menu aller à
        goto_ = self.addMenu(_(u"&Go to"))

        # magasin
        magasin = QtGui.QAction(_(u"New store"), self)
        magasin.setShortcut("Ctrl+M")
        self.connect(magasin, QtCore.SIGNAL("triggered()"),
                                            self.addstore)
        goto_.addAction(magasin)

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
        #Menu Aide
        help_ = self.addMenu(_(u"help"))
        help_.addAction(QtGui.QIcon('images/help.png'), _("help"),
                                    self.goto_help)
        help_.addAction(QtGui.QIcon('images/about.png'), _(u"About"),
                                    self.goto_about)

    #Inventaire
    def goto_inventaire(self):
        passs

    #Rapport periodique.
    def report_period(self):
        passs

    def addstore(self):
        passs

    #Export the database.
    def goto_export_db(self):
        pass

    def goto_export_excel(self):
        pass

    #Aide
    def goto_help(self):
        mbox = QtGui.QMessageBox.about(self, _(u"help"),
                                       _(u"Besoin d'aide"))
    #About
    def goto_about(self):
        mbox = QtGui.QMessageBox.about(self, _(u"About"),
                                       _(u"G_stock gestion de stock\n\n"
                                         u"Developpeur: Ibrahima Fadiga, Alou Dolo\n\n"
                                         u"© 2012 Fanga comp s.à.r.l\n"
                                         u"Bamako(Mali)\n"
                                         u"Tel: (223)76 43 38 90\n"
                                         u"E-mail: ibfadiga@gmail.com"))