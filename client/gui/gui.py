# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(775, 602)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.textEdit = QtGui.QTextEdit(self.centralWidget)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.horizontalLayout.addWidget(self.textEdit)
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
        self.horizontalLayout.setStretch(0, 5)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.groupBox = QtGui.QGroupBox(self.centralWidget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setMargin(11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.attackButton = QtGui.QPushButton(self.groupBox)
        self.attackButton.setObjectName(_fromUtf8("attackButton"))
        self.horizontalLayout_2.addWidget(self.attackButton)
        self.y_coordsComboBox = QtGui.QComboBox(self.groupBox)
        self.y_coordsComboBox.setObjectName(_fromUtf8("y_coordsComboBox"))
        self.horizontalLayout_2.addWidget(self.y_coordsComboBox)
        self.x_coordsComboBox = QtGui.QComboBox(self.groupBox)
        self.x_coordsComboBox.setObjectName(_fromUtf8("x_coordsComboBox"))
        self.horizontalLayout_2.addWidget(self.x_coordsComboBox)
        self.PlayerSelectionBox = QtGui.QGroupBox(self.groupBox)
        self.PlayerSelectionBox.setObjectName(_fromUtf8("PlayerSelectionBox"))
        self.RadioButtonLayout = QtGui.QVBoxLayout(self.PlayerSelectionBox)
        self.RadioButtonLayout.setMargin(11)
        self.RadioButtonLayout.setSpacing(6)
        self.RadioButtonLayout.setObjectName(_fromUtf8("RadioButtonLayout"))
        self.radioButton_2 = QtGui.QRadioButton(self.PlayerSelectionBox)
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.RadioButtonLayout.addWidget(self.radioButton_2)
        self.radioButton = QtGui.QRadioButton(self.PlayerSelectionBox)
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.RadioButtonLayout.addWidget(self.radioButton)
        self.horizontalLayout_2.addWidget(self.PlayerSelectionBox)
        self.startGameButton = QtGui.QPushButton(self.groupBox)
        self.startGameButton.setObjectName(_fromUtf8("startGameButton"))
        self.horizontalLayout_2.addWidget(self.startGameButton)
        self.verticalLayout.addWidget(self.groupBox)
        MainWindow.setCentralWidget(self.centralWidget)
        self.connectionsStatus = QtGui.QStatusBar(MainWindow)
        self.connectionsStatus.setObjectName(_fromUtf8("connectionsStatus"))
        MainWindow.setStatusBar(self.connectionsStatus)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.rabbitMQhost.setTitle(_translate("MainWindow", "rabbitMQ host", None))
        self.hostLineEdit.setText(_translate("MainWindow", "localhost", None))
        self.brokerConnectButton.setText(_translate("MainWindow", "connect to host", None))
        self.serverGroupBox.setTitle(_translate("MainWindow", "servers", None))
        self.serverConnectButton.setText(_translate("MainWindow", "Connect to game server", None))
        self.gamesGroupBox.setTitle(_translate("MainWindow", "games", None))
        self.joinGameButton.setText(_translate("MainWindow", "Join Game", None))
        self.createGameButton.setText(_translate("MainWindow", "Create Game", None))
        self.groupBox.setTitle(_translate("MainWindow", "Game Controls", None))
        self.attackButton.setText(_translate("MainWindow", "Attack!", None))
        self.PlayerSelectionBox.setTitle(_translate("MainWindow", "Select player to attack", None))
        self.radioButton_2.setText(_translate("MainWindow", "RadioButton", None))
        self.radioButton.setText(_translate("MainWindow", "RadioButton", None))
        self.startGameButton.setText(_translate("MainWindow", "Start Game", None))

