#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fadiga


from PyQt4 import QtGui, QtCore

from gstockreports import G_reportViewWidget
from dashboard import DashbordViewWidget
from monitoring_chicks import PsRapportViewWidget
from menubar import MenuBar
from statusbar import GStatusBar
from data_helper import alerte
from showalerte import ShowAlViewWidget



class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.resize(1200, 650)
        self.setWindowTitle(u"Management chicken coop")
        self.setWindowIcon(QtGui.QIcon('images/eggs.ico'))

        self.toolbar2 = QtGui.QToolBar()
        self.toolbar2.setStyleSheet("color: rgb(255, 45, 8);")
        # self.toolbar2.setTabPosition(QtGui.QTabWidget.West)
        self.alerte, c = alerte()
        self.update()
        self.toolbar = QtGui.QToolBar()
        self.toolbar.setEnabled(True)
        self.toolbar.addAction(QtGui.QIcon('images/quiter.png'), \
                                                    _(u"Exit"), self.goto_exit)
        self.toolbar.addSeparator()
        self.toolbar.addAction(_(u"Dashboard"), self.accueil)
        self.toolbar.addSeparator()
        self.toolbar.addAction(_(u"Management reports"), \
                                                self.goto_gestion_rapport)
        self.toolbar.addSeparator()
        self.toolbar.addAction(_(u"Monitoring chiks"), \
                                                self.goto__suivi_chiks)
        self.addToolBar(self.toolbar)

        self.menubar = MenuBar(self)
        self.setMenuBar(self.menubar)
        self.statusbar = GStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.change_context(DashbordViewWidget)

        self.startTimer(10000)

    def timerEvent(self, event):
        al, c = alerte()
        if len(self.alerte) != len(al):
            self.update()

    def update(self):
        al, c = alerte()
        if len(al) != 0:
            self.toolbar2.addAction(QtGui.QIcon('images/war.png'),
                                    c, self.goto_alerte)
            self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolbar2)
        self.alerte, c = alerte()

    def goto_exit(self):
        self.close()

    def goto_alerte(self):
        self.setWindowTitle(u"Show alert")
        self.open_dialog(ShowAlViewWidget)

    def accueil(self):
        self.setWindowTitle(u"Home")
        self.change_context(DashbordViewWidget)

    def goto_gestion_rapport(self):
        self.setWindowTitle(_(u"Management Reports"))
        self.change_context(G_reportViewWidget)

    def goto__suivi_chiks(self):
        self.setWindowTitle(_(u"Monitoring chiks"))
        self.change_context(PsRapportViewWidget)


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

