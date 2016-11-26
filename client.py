from PyQt4 import QtGui, QtCore
from gui import gui
import sys


class GuiApp(QtGui.QMainWindow, gui.Ui_MainWindow):
	def __init__(self, parent=None):
		super(GuiApp, self).__init__(parent)
		self.setupUi(self)
		self.widget = DragWidget(self)
		self.horizontalLayout.addWidget(self.widget)
		self.widget_2 = DragWidget(self)
		self.horizontalLayout.addWidget(self.widget_2)


class DragWidget(QtGui.QFrame):
	def __init__(self, parent=None):
		super(DragWidget, self).__init__(parent)
		self.setMinimumSize(200, 200)
		self.setFrameStyle(QtGui.QFrame.Sunken | QtGui.QFrame.StyledPanel)
		self.setAcceptDrops(True)

		boatIcon = QtGui.QLabel(self)
		boatIcon.setPixmap(QtGui.QPixmap("img/battleship.png"))
		boatIcon.move(10, 10)
		boatIcon.show()
		boatIcon.setAttribute(QtCore.Qt.WA_DeleteOnClose)

	def dragEnterEvent(self, event):
		if event.mimeData().hasFormat("application/x-dnditemdata"):
			if event.source() == self:
				event.setDropAction(QtCore.Qt.MoveAction)
				event.accept()
			else:
				event.acceptProposedAction()
		else:
			event.ignore()

	def dragMoveEvent(self, event):
		if event.mimeData().hasFormat("application/x-dnditemdata"):
			if event.source() == self:
				event.setDropAction(QtCore.Qt.CopyAction)
				event.accept()
			else:
				event.acceptProposedAction()
		else:
			event.ignore()

	def dropEvent(self, event):
		if event.mimeData().hasFormat("application/x-dnditemdata"):
			itemData = event.mimeData().data("application/x-dnditemdata")
			dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.ReadOnly)

			pixmap = QtGui.QPixmap()
			offset = QtCore.QPoint()
			dataStream >> pixmap >> offset

			newIcon = QtGui.QLabel(self)
			newIcon.setPixmap(pixmap)
			newIcon.move(event.pos() - offset)
			newIcon.show()
			newIcon.setAttribute(QtCore.Qt.WA_DeleteOnClose)

			if event.source() == self:
				event.setDropAction(QtCore.Qt.MoveAction)
				event.accept()
			else:
				event.acceptProposedAction()
		else:
			event.ignore()

	def mousePressEvent(self, event):
		child = self.childAt(event.pos())
		if not child:
			return

		pixmap = child.pixmap()

		itemData = QtCore.QByteArray()
		dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.WriteOnly)

		dataStream << pixmap << (event.pos() - child.pos())

		mimeData = QtCore.QMimeData()
		mimeData.setData("application/x-dnditemdata", itemData)

		drag = QtGui.QDrag(self)
		drag.setMimeData(mimeData)
		drag.setPixmap(pixmap)
		drag.setHotSpot(event.pos() - child.pos())


		result = drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction)
		print result, QtCore.Qt.MoveAction
		if result == QtCore.Qt.MoveAction:
			child.close()
		else:
			child.setPixmap(pixmap)
			child.show()



def main():
	app = QtGui.QApplication(sys.argv)
	form = GuiApp()
	form.show()
	sys.exit(app.exec_())


main()
