# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'server_browser.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Server_browser(object):
    def setupUi(self, Server_browser):
        Server_browser.setObjectName(_fromUtf8("Server_browser"))
        Server_browser.resize(775, 602)
        self.centralWidget = QtGui.QWidget(Server_browser)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setMargin(11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.rabbitMQhost = QtGui.QGroupBox(self.centralWidget)
        self.rabbitMQhost.setObjectName(_fromUtf8("rabbitMQhost"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.rabbitMQhost)
        self.verticalLayout_3.setMargin(11)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.hostLineEdit = QtGui.QLineEdit(self.rabbitMQhost)
        self.hostLineEdit.setPlaceholderText(_fromUtf8(""))
        self.hostLineEdit.setObjectName(_fromUtf8("hostLineEdit"))
        self.verticalLayout_3.addWidget(self.hostLineEdit)
        self.brokerConnectButton = QtGui.QPushButton(self.rabbitMQhost)
        self.brokerConnectButton.setObjectName(_fromUtf8("brokerConnectButton"))
        self.verticalLayout_3.addWidget(self.brokerConnectButton)
        self.verticalLayout_2.addWidget(self.rabbitMQhost)
        self.serverGroupBox = QtGui.QGroupBox(self.centralWidget)
        self.serverGroupBox.setObjectName(_fromUtf8("serverGroupBox"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.serverGroupBox)
        self.verticalLayout_4.setMargin(11)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.serverListWidget = QtGui.QListWidget(self.serverGroupBox)
        self.serverListWidget.setObjectName(_fromUtf8("serverListWidget"))
        self.verticalLayout_4.addWidget(self.serverListWidget)
        self.serverConnectButton = QtGui.QPushButton(self.serverGroupBox)
        self.serverConnectButton.setObjectName(_fromUtf8("serverConnectButton"))
        self.verticalLayout_4.addWidget(self.serverConnectButton)
        self.verticalLayout_2.addWidget(self.serverGroupBox)
        self.gamesGroupBox = QtGui.QGroupBox(self.centralWidget)
        self.gamesGroupBox.setObjectName(_fromUtf8("gamesGroupBox"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.gamesGroupBox)
        self.verticalLayout_5.setMargin(11)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.gamesList = QtGui.QListWidget(self.gamesGroupBox)
        self.gamesList.setObjectName(_fromUtf8("gamesList"))
        self.verticalLayout_5.addWidget(self.gamesList)
        self.gameButtonLayout = QtGui.QHBoxLayout()
        self.gameButtonLayout.setMargin(11)
        self.gameButtonLayout.setSpacing(6)
        self.gameButtonLayout.setObjectName(_fromUtf8("gameButtonLayout"))
        self.joinGameButton = QtGui.QPushButton(self.gamesGroupBox)
        self.joinGameButton.setObjectName(_fromUtf8("joinGameButton"))
        self.gameButtonLayout.addWidget(self.joinGameButton)
        self.createGameButton = QtGui.QPushButton(self.gamesGroupBox)
        self.createGameButton.setObjectName(_fromUtf8("createGameButton"))
        self.gameButtonLayout.addWidget(self.createGameButton)
        self.verticalLayout_5.addLayout(self.gameButtonLayout)
        self.verticalLayout_2.addWidget(self.gamesGroupBox)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        Server_browser.setCentralWidget(self.centralWidget)
        self.connectionsStatus = QtGui.QStatusBar(Server_browser)
        self.connectionsStatus.setObjectName(_fromUtf8("connectionsStatus"))
        Server_browser.setStatusBar(self.connectionsStatus)

        self.retranslateUi(Server_browser)
        QtCore.QMetaObject.connectSlotsByName(Server_browser)

    def retranslateUi(self, Server_browser):
        Server_browser.setWindowTitle(_translate("Server_browser", "MainWindow", None))
        self.rabbitMQhost.setTitle(_translate("Server_browser", "rabbitMQ host", None))
        self.hostLineEdit.setText(_translate("Server_browser", "localhost", None))
        self.brokerConnectButton.setText(_translate("Server_browser", "connect to host", None))
        self.serverGroupBox.setTitle(_translate("Server_browser", "servers", None))
        self.serverConnectButton.setText(_translate("Server_browser", "Connect to game server", None))
        self.gamesGroupBox.setTitle(_translate("Server_browser", "games", None))
        self.joinGameButton.setText(_translate("Server_browser", "Join Game", None))
        self.createGameButton.setText(_translate("Server_browser", "Create Game", None))

