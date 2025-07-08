# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerGXGWmk.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PyQt5.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(502, 419)
        self.listWidget = QListWidget(Dialog)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(40, 50, 411, 211))
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(40, 20, 131, 16))
        self.buttonAdd = QPushButton(Dialog)
        self.buttonAdd.setObjectName(u"buttonAdd")
        self.buttonAdd.setGeometry(QRect(40, 290, 411, 28))
        self.buttonRemove = QPushButton(Dialog)
        self.buttonRemove.setObjectName(u"buttonRemove")
        self.buttonRemove.setGeometry(QRect(40, 330, 411, 28))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u0422\u0435\u043a\u0443\u0449\u0438\u0435 \u043f\u0430\u043f\u043a\u0438:", None))
        self.buttonAdd.setText(QCoreApplication.translate("Dialog", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043f\u0430\u043f\u043a\u0443 \u0432 \u0431\u0430\u0437\u0443", None))
        self.buttonRemove.setText(QCoreApplication.translate("Dialog", u"\u0423\u0431\u0440\u0430\u0442\u044c \u043f\u0430\u043f\u043a\u0443 \u0438\u0437 \u0431\u0430\u0437\u044b", None))
    # retranslateUi

