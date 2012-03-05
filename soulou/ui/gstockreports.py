#!usr/bin/env python
# -*- coding: utf-8 -*-
#maintainer: Fadiga


from datetime import datetime

from PyQt4 import QtGui, QtCore

from model import *
from common import (F_Widget, F_PageTitle, F_TableWidget,
                    F_BoxTitle, Button_add, Button_save, FormatDate,
                    IntLineEdit)
from util import raise_success, raise_error, formatted_number
from magasins import MagasinViewWidget
from produits import ProduitViewWidget


class G_reportViewWidget(F_Widget):

    def __init__(self, parent=0, *args, **kwargs):
        super(G_reportViewWidget, self).__init__(parent=parent,\
                                                        *args, **kwargs)
        self.setWindowTitle(_(u"Management reports"))
        vbox = QtGui.QVBoxLayout()

        tablebox = QtGui.QVBoxLayout()
        tablebox.addWidget(F_BoxTitle(_(u"Table rapports")))
        self.table_op = StockRapTableWidget(parent=self)
        tablebox.addWidget(self.table_op)

        formbox = QtGui.QVBoxLayout()
        editbox = QtGui.QGridLayout()

        self.qte_utilise = IntLineEdit()
        self.qte_utilise.setDragEnabled(True)

        self.date_ = FormatDate(QtCore.QDate.currentDate())
        self.date_.setFont(QtGui.QFont("Courier New", 10, True))

        self.time = QtGui.QDateTimeEdit(QtCore.QTime.currentTime())

        self.liste_type = [_(u"input"), _(u"inout")]
        #Combobox widget
        self.box_type = QtGui.QComboBox()
        for index in self.liste_type:
            self.box_type.addItem(u'%(type)s' % {'type': index})
        #Combobox widget
        self.liste_magasin = Magasin.all()
        self.box_mag = QtGui.QComboBox()
        for index in xrange(0, len(self.liste_magasin)):
            op = self.liste_magasin[index]
            sentence = u"%(name)s" % {'name': op.name}
            self.box_mag.addItem(sentence, QtCore.QVariant(op.id))
        #Combobox widget
        self.liste_produit = Produit.all()
        self.box_prod = QtGui.QComboBox()
        for index in xrange(0, len(self.liste_produit)):
            op = self.liste_produit[index]
            sentence = _(u"%(libelle)s") % {'libelle': op.libelle}
            self.box_prod.addItem(sentence, QtCore.QVariant(op.id))
            
        editbox.addWidget(QtGui.QLabel(_(u"Type")), 0, 0)
        editbox.addWidget(self.box_type, 1, 0)
        editbox.addWidget(QtGui.QLabel(_(u"Store")), 0, 1)
        editbox.addWidget(self.box_mag, 1, 1)
        editbox.addWidget(QtGui.QLabel(_(u"Product")), 0, 2)
        editbox.addWidget(self.box_prod, 1, 2)
        editbox.addWidget(QtGui.QLabel((_(u"Quantite utilise"))), 0, 3)
        editbox.addWidget(self.qte_utilise, 1, 3)
        editbox.addWidget(QtGui.QLabel((_(u"Date"))), 0, 4)
        editbox.addWidget(self.date_, 1, 4)
        butt = Button_save(_(u"Save"))
        butt.clicked.connect(self.add_operation)
        editbox.addWidget(butt, 1, 5)
    
        formbox.addLayout(editbox)
        editbox.setColumnStretch(7, 2)

        vbox.addLayout(formbox)
        vbox.addLayout(tablebox)
        self.setLayout(vbox)

    def refresh(self):
        self.table_op.refresh()

    def add_operation(self):
        ''' add operation '''
        type_ = self.liste_type[self.box_type.currentIndex()]
        magasin = self.liste_magasin[self.box_mag.currentIndex()]
        produit = self.liste_produit[self.box_prod.currentIndex()]
        qte_utilise = self.qte_utilise.text()
        date_ = self.date_.text()
        day, month, year = date_.split('/')
        dt = datetime.now()
        datetime_ = datetime(int(year), int(month), int(day),
                             int(dt.hour), int(dt.minute), int(dt.second),
                             int(dt.microsecond))

        if unicode(self.qte_utilise.text()) != "":
            strap = StockRapport()
            strap.type_ = unicode(type_)
            strap.magasin = magasin
            strap.produit = produit
            strap.qte_utilise = int(qte_utilise)
            strap.date_rapp = datetime_
            strap.restant = 0
            strap.save()
            self.qte_utilise.clear()
            self.table_op.refresh_()
        else:
            raise_error(_(u"error"), _(u"Donnez le nbre de carton"))


class StockRapTableWidget(F_TableWidget):
    """ """

    def __init__(self, parent, *args, **kwargs):
        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)
        self.header = [_(u"Type"), _(u"Store"), _(u"Product"), \
                       _(u"Quantite"), _(u"Remaining"), \
                       _(u"Date")]
        self.set_data_for()
        self.refresh(True)

    def refresh_(self):
        """ """
        self._reset()
        self.set_data_for()
        self.refresh()

    def set_data_for(self):
        self.data = [(rap.type_, rap.magasin, rap.produit,
                        formatted_number(rap.qte_utilise),
                        formatted_number(rap.restant),
                        rap.date_rapp.strftime(u'%x %Hh:%Mmn')) \
                        for rap in StockRapport.select().order_by(('date_rapp', 'desc'))]

    def _item_for_data(self, row, column, data, context=None):
        if column == 0 and self.data[row][0] == _("input"):
            return QtGui.QTableWidgetItem(QtGui.QIcon("images/in.ico"),
                                                      u"")
        if column == 0 and self.data[row][0] == _("inout"):
            return QtGui.QTableWidgetItem(QtGui.QIcon("images/out.ico"),
                                                      u"")

        return super(StockRapTableWidget, self)\
                                            ._item_for_data(row, column, \
                                                        data, context)
