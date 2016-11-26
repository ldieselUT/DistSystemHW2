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
				event.setDropAction(QtCore.QtMoveAction)
				event.accept()
			else:
				event.acceptProposedAction()
		else:
			event.ignore()

	def dropEvent(self, event):
		pass

	def mousePressEvent(self, event):
		child = QtGui.QLabel.childAt(event.pos())
		if not child:
			return

		pixmap = child.pixmap()

		itemData = QtGui.QByteArray()
		dataStream = QtGui.QDataStream(itemData, QtCore.QIODevice.WriteOnly)

		dataStream << pixmap << QPoint(event->pos() - child->pos());

		QMimeData * mimeData = new
		QMimeData;
		mimeData->setData("application/x-dnditemdata", itemData);

		QDrag * drag = new
		QDrag(this);
		drag->setMimeData(mimeData);
		drag->setPixmap(pixmap);
		drag->setHotSpot(event->pos() - child->pos());

		QPixmap
		tempPixmap = pixmap;
		QPainter
		painter;
		painter.begin( & tempPixmap);
		painter.fillRect(pixmap.rect(), QColor(127, 127, 127, 127));
		painter.end();

		child->setPixmap(tempPixmap);

		if (drag-> exec (Qt::
			CopyAction | Qt::MoveAction, Qt::CopyAction) == Qt::MoveAction) {
			child->close();
		} else {
			child->show();
		child->setPixmap(pixmap);
		}


def main():
	app = QtGui.QApplication(sys.argv)
	form = GuiApp()
	form.show()
	sys.exit(app.exec_())


main()
