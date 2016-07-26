import sys
from PySide.QtGui import QApplication, QMainWindow, QTableView, QAbstractItemView
from PySide.QtSql import QSqlDatabase, QSqlTableModel


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        database = QSqlDatabase.addDatabase('QSQLITE')
        database.setDatabaseName('astatsscraper.db') # Better lookup logic needed
        if not database.open():
            print('Error opening database!')
        model = QSqlTableModel(db=database)
        model.setTable('steam_apps')
        table = QTableView()
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setModel(model)
        self.setCentralWidget(table)
        table.show()

app = QApplication(sys.argv)
app.setApplicationName("AStatsScraperGui")
main_window = MainWindow()
main_window.show()
app.exec_()
