# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frame.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from algotides.interfaces.widgets import CustomListWidget


class Ui_WalletFrame(object):
    def setupUi(self, WalletFrame):
        if not WalletFrame.objectName():
            WalletFrame.setObjectName(u"WalletFrame")
        WalletFrame.resize(874, 366)
        self.horizontalLayout = QHBoxLayout(WalletFrame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.listWidget = CustomListWidget(WalletFrame)
        self.listWidget.setObjectName(u"listWidget")

        self.horizontalLayout.addWidget(self.listWidget)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButton_Manage = QPushButton(WalletFrame)
        self.pushButton_Manage.setObjectName(u"pushButton_Manage")
        self.pushButton_Manage.setEnabled(False)

        self.verticalLayout.addWidget(self.pushButton_Manage)

        self.pushButton_LockUnlock = QPushButton(WalletFrame)
        self.pushButton_LockUnlock.setObjectName(u"pushButton_LockUnlock")
        self.pushButton_LockUnlock.setEnabled(False)

        self.verticalLayout.addWidget(self.pushButton_LockUnlock)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.pushButton_Rename = QPushButton(WalletFrame)
        self.pushButton_Rename.setObjectName(u"pushButton_Rename")
        self.pushButton_Rename.setEnabled(False)

        self.verticalLayout.addWidget(self.pushButton_Rename)

        self.pushButton_NewImport = QPushButton(WalletFrame)
        self.pushButton_NewImport.setObjectName(u"pushButton_NewImport")
        self.pushButton_NewImport.setEnabled(False)

        self.verticalLayout.addWidget(self.pushButton_NewImport)

        self.pushButton_Export = QPushButton(WalletFrame)
        self.pushButton_Export.setObjectName(u"pushButton_Export")
        self.pushButton_Export.setEnabled(False)

        self.verticalLayout.addWidget(self.pushButton_Export)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(WalletFrame)

        self.pushButton_Manage.setDefault(False)


        QMetaObject.connectSlotsByName(WalletFrame)
    # setupUi

    def retranslateUi(self, WalletFrame):
        WalletFrame.setWindowTitle(QCoreApplication.translate("WalletFrame", u"Frame", None))
        self.pushButton_Manage.setText(QCoreApplication.translate("WalletFrame", u"Manage\n"
"Addresses", None))
        self.pushButton_LockUnlock.setText(QCoreApplication.translate("WalletFrame", u"Lock/Unlock", None))
        self.pushButton_Rename.setText(QCoreApplication.translate("WalletFrame", u"Rename", None))
        self.pushButton_NewImport.setText(QCoreApplication.translate("WalletFrame", u"New/Import", None))
        self.pushButton_Export.setText(QCoreApplication.translate("WalletFrame", u"Export", None))
    # retranslateUi

