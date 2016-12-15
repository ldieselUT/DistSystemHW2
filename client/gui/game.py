# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'game.ui'
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

class Ui_Game(object):
    def setupUi(self, Game):
        Game.setObjectName(_fromUtf8("Game"))
        Game.resize(775, 602)
        self.centralWidget = QtGui.QWidget(Game)
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
        self.horizontalLayout_2.addWidget(self.PlayerSelectionBox)
        self.startGameButton = QtGui.QPushButton(self.groupBox)
        self.startGameButton.setObjectName(_fromUtf8("startGameButton"))
        self.horizontalLayout_2.addWidget(self.startGameButton)
        self.leaveGameButton = QtGui.QPushButton(self.groupBox)
        self.leaveGameButton.setObjectName(_fromUtf8("leaveGameButton"))
        self.horizontalLayout_2.addWidget(self.leaveGameButton)
        self.verticalLayout.addWidget(self.groupBox)
        Game.setCentralWidget(self.centralWidget)
        self.connectionsStatus = QtGui.QStatusBar(Game)
        self.connectionsStatus.setObjectName(_fromUtf8("connectionsStatus"))
        Game.setStatusBar(self.connectionsStatus)

        self.retranslateUi(Game)
        QtCore.QMetaObject.connectSlotsByName(Game)

    def retranslateUi(self, Game):
        Game.setWindowTitle(_translate("Game", "MainWindow", None))
        self.groupBox.setTitle(_translate("Game", "Game Controls", None))
        self.attackButton.setText(_translate("Game", "Attack!", None))
        self.PlayerSelectionBox.setTitle(_translate("Game", "Select player to attack", None))
        self.startGameButton.setText(_translate("Game", "Start Game", None))
        self.leaveGameButton.setText(_translate("Game", "Leave Game", None))

