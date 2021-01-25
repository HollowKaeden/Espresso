import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
import sqlite3


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.setWindowTitle('Эспрессо')
        self.con = sqlite3.connect('coffee.db')
        self.cur = self.con.cursor()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ['ID', 'Название сорта', 'Степень обжарки', 'Молотый/в зёрнах',
             'Описание вкуса', 'Цена', 'Объём упаковки'])
        coffee = self.cur.execute("""SELECT * FROM coffee""")
        for i, row in enumerate(coffee):
            self.table.setRowCount(self.table.rowCount() + 1)
            for j, elem in enumerate(row):
                if j == 3:
                    if elem == 1:
                        self.table.setItem(i, j, QTableWidgetItem('Молотый'))
                    else:
                        self.table.setItem(i, j, QTableWidgetItem('В зёрнах'))
                else:
                    self.table.setItem(i, j, QTableWidgetItem(str(elem)))

    def addEdit_db(self, parameters):
        if parameters[0] in self.cur.execute("""SELECT ID from coffee""").fetchall():
            self.cur.execute("""UPDATE coffee SET roast_power=?, ground/in_grains=?, taste=?, price=?, volume=? 
WHERE ID=?""", *(parameters[1:] + parameters[0]))
        else:
            self.cur.execute("""INSERT INTO coffee(name_of_sort, roast_power, ground/in_grains, taste, price, volume)
VALUES(?, ?, ?, ?, ?, ?)""", *parameters)
        self.con.commit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())