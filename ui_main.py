# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitledFkRidX.ui'
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


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1240, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1080, 560))
        MainWindow.setMaximumSize(QSize(1240, 600))
        self.editFolderList = QAction(MainWindow)
        self.editFolderList.setObjectName(u"editFolderList")
        self.actionPhotoReport = QAction(MainWindow)
        self.actionPhotoReport.setObjectName(u"actionPhotoReport")
        self.actionDiagrams = QAction(MainWindow)
        self.actionDiagrams.setObjectName(u"actionDiagrams")
        self.actionAlbumReport = QAction(MainWindow)
        self.actionAlbumReport.setObjectName(u"actionAlbumReport")
        self.actionPhotoesListReport = QAction(MainWindow)
        self.actionPhotoesListReport.setObjectName(u"actionPhotoesListReport")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.buttonLoadAll = QPushButton(self.centralwidget)
        self.buttonLoadAll.setObjectName(u"buttonLoadAll")
        self.buttonLoadAll.setGeometry(QRect(260, 20, 71, 28))
        self.buttonLoadFavorite = QPushButton(self.centralwidget)
        self.buttonLoadFavorite.setObjectName(u"buttonLoadFavorite")
        self.buttonLoadFavorite.setGeometry(QRect(330, 20, 71, 28))
        self.buttonToggleSearch = QPushButton(self.centralwidget)
        self.buttonToggleSearch.setObjectName(u"buttonToggleSearch")
        self.buttonToggleSearch.setGeometry(QRect(0, 270, 16, 28))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(710, 50, 331, 271))
        self.label_4.setLayoutDirection(Qt.LeftToRight)
        self.label_4.setScaledContents(False)
        self.label_4.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(710, 350, 330, 191))
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_7 = QLabel(self.widget)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 2, 0, 1, 1)

        self.buttonAddToFav = QPushButton(self.widget)
        self.buttonAddToFav.setObjectName(u"buttonAddToFav")

        self.gridLayout.addWidget(self.buttonAddToFav, 5, 0, 1, 2)

        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)

        self.label_6 = QLabel(self.widget)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 1)

        self.label_8 = QLabel(self.widget)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 3, 0, 1, 1)

        self.label_9 = QLabel(self.widget)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 4, 0, 1, 1)

        self.stackedDate = QStackedWidget(self.widget)
        self.stackedDate.setObjectName(u"stackedDate")
        self.watchDate = QWidget()
        self.watchDate.setObjectName(u"watchDate")
        self.labelDate = QLabel(self.watchDate)
        self.labelDate.setObjectName(u"labelDate")
        self.labelDate.setGeometry(QRect(0, 0, 261, 31))
        self.stackedDate.addWidget(self.watchDate)
        self.editDate = QWidget()
        self.editDate.setObjectName(u"editDate")
        self.dateTimeEdit = QDateTimeEdit(self.editDate)
        self.dateTimeEdit.setObjectName(u"dateTimeEdit")
        self.dateTimeEdit.setGeometry(QRect(0, 0, 261, 31))
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.dateTimeEdit.sizePolicy().hasHeightForWidth())
        self.dateTimeEdit.setSizePolicy(sizePolicy1)
        self.dateTimeEdit.setLayoutDirection(Qt.LeftToRight)
        self.dateTimeEdit.setAutoFillBackground(False)
        self.stackedDate.addWidget(self.editDate)

        self.gridLayout.addWidget(self.stackedDate, 0, 1, 1, 1)

        self.stackedDescription = QStackedWidget(self.widget)
        self.stackedDescription.setObjectName(u"stackedDescription")
        self.watchDescription = QWidget()
        self.watchDescription.setObjectName(u"watchDescription")
        self.labelDescription = QLabel(self.watchDescription)
        self.labelDescription.setObjectName(u"labelDescription")
        self.labelDescription.setGeometry(QRect(0, -5, 260, 31))
        self.stackedDescription.addWidget(self.watchDescription)
        self.editDescription = QWidget()
        self.editDescription.setObjectName(u"editDescription")
        self.textEditDescription = QTextEdit(self.editDescription)
        self.textEditDescription.setObjectName(u"textEditDescription")
        self.textEditDescription.setGeometry(QRect(0, 0, 261, 31))
        self.stackedDescription.addWidget(self.editDescription)

        self.gridLayout.addWidget(self.stackedDescription, 4, 1, 1, 1)

        self.stackedLocation = QStackedWidget(self.widget)
        self.stackedLocation.setObjectName(u"stackedLocation")
        self.watchLocation = QWidget()
        self.watchLocation.setObjectName(u"watchLocation")
        self.labelLocation = QLabel(self.watchLocation)
        self.labelLocation.setObjectName(u"labelLocation")
        self.labelLocation.setGeometry(QRect(0, -5, 261, 31))
        self.stackedLocation.addWidget(self.watchLocation)
        self.editLocation = QWidget()
        self.editLocation.setObjectName(u"editLocation")
        self.textEditLocation = QTextEdit(self.editLocation)
        self.textEditLocation.setObjectName(u"textEditLocation")
        self.textEditLocation.setGeometry(QRect(0, 10, 221, 21))
        self.stackedLocation.addWidget(self.editLocation)

        self.gridLayout.addWidget(self.stackedLocation, 1, 1, 1, 1)

        self.stackedPeople = QStackedWidget(self.widget)
        self.stackedPeople.setObjectName(u"stackedPeople")
        self.watchPeople = QWidget()
        self.watchPeople.setObjectName(u"watchPeople")
        self.labelPeople = QLabel(self.watchPeople)
        self.labelPeople.setObjectName(u"labelPeople")
        self.labelPeople.setGeometry(QRect(0, -5, 261, 31))
        self.stackedPeople.addWidget(self.watchPeople)
        self.editPeople = QWidget()
        self.editPeople.setObjectName(u"editPeople")
        self.textEditPeople = QTextEdit(self.editPeople)
        self.textEditPeople.setObjectName(u"textEditPeople")
        self.textEditPeople.setGeometry(QRect(0, 0, 251, 31))
        self.stackedPeople.addWidget(self.editPeople)

        self.gridLayout.addWidget(self.stackedPeople, 2, 1, 1, 1)

        self.stackedTags = QStackedWidget(self.widget)
        self.stackedTags.setObjectName(u"stackedTags")
        self.watchTags = QWidget()
        self.watchTags.setObjectName(u"watchTags")
        self.labelTags = QLabel(self.watchTags)
        self.labelTags.setObjectName(u"labelTags")
        self.labelTags.setGeometry(QRect(0, 0, 260, 31))
        self.stackedTags.addWidget(self.watchTags)
        self.editTags = QWidget()
        self.editTags.setObjectName(u"editTags")
        self.textEditTags = QTextEdit(self.editTags)
        self.textEditTags.setObjectName(u"textEditTags")
        self.textEditTags.setGeometry(QRect(0, 0, 251, 21))
        self.stackedTags.addWidget(self.editTags)

        self.gridLayout.addWidget(self.stackedTags, 3, 1, 1, 1)

        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(20, 90, 671, 451))
        sizePolicy1.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy1)
        self.listWidget.setBaseSize(QSize(0, 0))
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(21, 51, 669, 31))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.textEdit = QTextEdit(self.horizontalLayoutWidget)
        self.textEdit.setObjectName(u"textEdit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.textEdit)

        self.buttonFilterTags = QPushButton(self.horizontalLayoutWidget)
        self.buttonFilterTags.setObjectName(u"buttonFilterTags")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(1)
        sizePolicy3.setHeightForWidth(self.buttonFilterTags.sizePolicy().hasHeightForWidth())
        self.buttonFilterTags.setSizePolicy(sizePolicy3)

        self.horizontalLayout.addWidget(self.buttonFilterTags)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1240, 26))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName(u"menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockSearch = QDockWidget(MainWindow)
        self.dockSearch.setObjectName(u"dockSearch")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.dockSearch.sizePolicy().hasHeightForWidth())
        self.dockSearch.setSizePolicy(sizePolicy4)
        self.dockSearch.setMinimumSize(QSize(164, 40))
        self.dockSearch.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.widget1 = QWidget(self.dockWidgetContents)
        self.widget1.setObjectName(u"widget1")
        self.widget1.setGeometry(QRect(20, 20, 141, 131))
        self.verticalLayout = QVBoxLayout(self.widget1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.widget1)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.label_2 = QLabel(self.widget1)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.dateEdit = QDateEdit(self.widget1)
        self.dateEdit.setObjectName(u"dateEdit")

        self.verticalLayout.addWidget(self.dateEdit)

        self.label_3 = QLabel(self.widget1)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.dateEdit_2 = QDateEdit(self.widget1)
        self.dateEdit_2.setObjectName(u"dateEdit_2")

        self.verticalLayout.addWidget(self.dateEdit_2)

        self.widget2 = QWidget(self.dockWidgetContents)
        self.widget2.setObjectName(u"widget2")
        self.widget2.setGeometry(QRect(20, 190, 141, 261))
        self.verticalLayout_2 = QVBoxLayout(self.widget2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.comboBox = QComboBox(self.widget2)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setEnabled(True)

        self.verticalLayout_2.addWidget(self.comboBox)

        self.comboBox_2 = QComboBox(self.widget2)
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.verticalLayout_2.addWidget(self.comboBox_2)

        self.comboBox_3 = QComboBox(self.widget2)
        self.comboBox_3.setObjectName(u"comboBox_3")

        self.verticalLayout_2.addWidget(self.comboBox_3)

        self.comboBox_4 = QComboBox(self.widget2)
        self.comboBox_4.setObjectName(u"comboBox_4")

        self.verticalLayout_2.addWidget(self.comboBox_4)

        self.comboBox_5 = QComboBox(self.widget2)
        self.comboBox_5.setObjectName(u"comboBox_5")

        self.verticalLayout_2.addWidget(self.comboBox_5)

        self.buttonFilterAll = QPushButton(self.dockWidgetContents)
        self.buttonFilterAll.setObjectName(u"buttonFilterAll")
        self.buttonFilterAll.setGeometry(QRect(20, 460, 141, 31))
        self.buttonResetFilters = QPushButton(self.dockWidgetContents)
        self.buttonResetFilters.setObjectName(u"buttonResetFilters")
        self.buttonResetFilters.setGeometry(QRect(20, 490, 141, 28))
        self.label_10 = QLabel(self.dockWidgetContents)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(20, 170, 55, 16))
        self.dockSearch.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.LeftDockWidgetArea, self.dockSearch)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menu.addAction(self.editFolderList)
        self.menu_2.addAction(self.actionPhotoReport)
        self.menu_2.addAction(self.actionPhotoesListReport)
        self.menu_2.addAction(self.actionAlbumReport)
        self.menu_2.addAction(self.actionDiagrams)

        self.retranslateUi(MainWindow)

        self.stackedDate.setCurrentIndex(0)
        self.stackedDescription.setCurrentIndex(0)
        self.stackedLocation.setCurrentIndex(0)
        self.stackedPeople.setCurrentIndex(0)
        self.stackedTags.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u0424\u043e\u0442\u043e\u0430\u043b\u044c\u0431\u043e\u043c\u041f\u0420\u041e", None))
        self.editFolderList.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u043f\u0430\u043f\u043a\u0438 \u0434\u043b\u044f \u043f\u0440\u043e\u0441\u043c\u043e\u0442\u0440\u0430", None))
        self.actionPhotoReport.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u0447\u0451\u0442 \u043f\u043e \u0432\u044b\u0431\u0440\u0430\u043d\u043d\u043e\u0439 \u0444\u043e\u0442\u043e\u0433\u0440\u0430\u0444\u0438\u0438", None))
        self.actionDiagrams.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043a\u0430\u0437\u0430\u0442\u044c \u0433\u0440\u0430\u0444\u0438\u043a\u0438", None))
        self.actionAlbumReport.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u0447\u0451\u0442 \u0441 \u043e\u0431\u0449\u0435\u0439 \u0441\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u043e\u0439 \u0444\u043e\u0442\u043e\u0430\u043b\u044c\u0431\u043e\u043c\u0430", None))
        self.actionPhotoesListReport.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u0447\u0451\u0442 \u043f\u043e \u0441\u043f\u0438\u0441\u043a\u0443 \u0444\u043e\u0442\u043e\u0433\u0440\u0430\u0444\u0438\u0439", None))
        self.buttonLoadAll.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0441\u0435 \u0444\u043e\u0442\u043e", None))
        self.buttonLoadFavorite.setText(QCoreApplication.translate("MainWindow", u"\u0418\u0437\u0431\u0440\u0430\u043d\u043d\u043e\u0435", None))
        self.buttonToggleSearch.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u0437\u0434\u0435\u0441\u044c \u0431\u0443\u0434\u0435\u0442 \u043e\u0442\u043e\u0431\u0440\u0430\u0436\u0430\u0442\u044c\u0441\u044f \u043f\u0440\u0435\u0434\u043f\u0440\u043e\u0441\u043c\u043e\u0442\u0440 \u0444\u043e\u0442\u043e\u0433\u0440\u0430\u0444\u0438\u0438", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u041b\u0438\u0446\u0430:", None))
        self.buttonAddToFav.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0432 \u0438\u0437\u0431\u0440\u0430\u043d\u043d\u043e\u0435", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u0414\u0430\u0442\u0430:", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u041c\u0435\u0441\u0442\u043e:", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0435\u0433\u0438:", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435:", None))
        self.labelDate.setText("")
        self.labelDescription.setText("")
        self.labelLocation.setText("")
        self.labelPeople.setText("")
        self.labelTags.setText("")
        self.textEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.textEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0438\u0441\u043a\u0430\u0442\u044c \u043f\u043e \u0442\u0435\u0433\u0430\u043c", None))
        self.buttonFilterTags.setText(QCoreApplication.translate("MainWindow", u"\u0418\u0441\u043a\u0430\u0442\u044c", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u0439\u043b", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0430", None))
        self.dockSearch.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u0420\u0430\u0441\u0448\u0438\u0440\u0435\u043d\u043d\u044b\u0439 \u043f\u043e\u0438\u0441\u043a", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0435\u0440\u0438\u043e\u0434", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u043e\u0442:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u0434\u043e:", None))
        self.buttonFilterAll.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.buttonResetFilters.setText(QCoreApplication.translate("MainWindow", u"\u0441\u0431\u0440\u043e\u0441\u0438\u0442\u044c \u0444\u0438\u043b\u044c\u0442\u0440\u044b", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"\u041b\u0438\u0446\u0430:", None))
    # retranslateUi

