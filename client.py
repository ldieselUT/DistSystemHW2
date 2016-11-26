from PyQt4 import QtGui
from gui import gui
import sys


class GuiApp(QtGui.QMainWindow, gui.Ui_MainWindow):
	def __init__(self, parent=None):
		super(GuiApp, self).__init__(parent)
		self.setupUi(self)


def main():
	app = QtGui.QApplication(sys.argv)
	form = GuiApp()
	form.show()
	sys.exit(app.exec_())


main()
