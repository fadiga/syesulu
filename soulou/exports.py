#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fadiga

import os
import shutil
from datetime import datetime

from PyQt4 import QtGui, QtCore

import model
from util import raise_success, raise_error


def export_database_as_file():
    destination = QtGui.QFileDialog.getSaveFileName(QtGui.QWidget(),
                                    _(u"Sauvegarder la base de Donnée."),
                                      u"%s.db" % datetime.now()\
                                                .strftime(u'%x-%Hh%M'),
                                    "*.db")
    if not destination:
        return None

    try:
        shutil.copyfile(model.DB_FILE, destination)
        raise_success(u"Les données ont été exportées correctement.",
                      u"Conservez ce fichier précieusement car il "
                      u"contient toutes vos données.\n"
                      u"Exportez vos données régulièrement.")
    except IOError:
        raise_error(u"La base de données n'a pas pu être exportée.",
                    u"Vérifiez le chemin de destination puis re-essayez.\n\n"
                    u"Demandez de l'aide si le problème persiste.")
