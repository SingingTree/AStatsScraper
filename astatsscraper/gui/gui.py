import sys
from PySide.QtGui import QApplication, QMainWindow, QTableView


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        table = QTableView()
        self.setCentralWidget(table)

app = QApplication(sys.argv)
app.setApplicationName("AStatsScraperGui")
main_window = MainWindow()
main_window.show()
app.exec_()
