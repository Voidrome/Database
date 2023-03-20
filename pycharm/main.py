import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem
from form_stuff import Ui_Form

Stuff_Posts = ['менеджер', 'бухгалтер', 'экономист', 'логист']


class MyWidget(QWidget, Ui_Form):
    def __init__(self):
        super(MyWidget, self).__init__()
        self.setupUi(self)
        self.cbpost.addItems(Stuff_Posts)
        self.pnopen.clicked.connect(self.open)
        self.pbin.clicked.connect(self.insert)

    def open(self):
        try:
            self.conn = sqlite3.connect("/home/user/Desktop/kys/Urackboiev/stuff.db")
            cur = self.conn.cursor()
            data = cur.execute('select * from stuff')
            col_name = [i[0] for i in data.description] # берем название наших столбцов, description - содержит описание полей нашей таблицы
            data_rows = data.fetchall() #остальные строки
        except Exception as e:
            print("Ошибки с подключением к БД")
            return e
        self.twStuffs.setColumnCount(len(col_name))
        self.twStuffs.setHorizontalHeaderLabels(col_name)
        self.twStuffs.setRowCount(0)
        for i, row in enumerate(data_rows): #заполнение
            self.twStuffs.setRowCount(self.twStuffs.rowCount() + 1) #увеличили количество строк на 1
            for j, elen in enumerate(row):
                self.twStuffs.setItem(i,j,QTableWidgetItem(str(elen)))
        self.twStuffs.resizeColumnsToContents()

    def update(self, query="select * from stuff"):
        try:
            cur= self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as e:
            print = (f"Проблемы с подключением к бд {e}")
            return e
        self.twStuffs.setRowCount(0)
        for i, row in enumerate(data):
            self.twStuffs.setRowCount(self.twStuffs.rowCount() + 1)
            for j, elen in enumerate(row):
                self.twStuffs.setItem(i,j,QTableWidgetItem(str(elen)))
        self.twStuffs.resizeColumnsToContents()


    def insert(self):
        row = [self.linefio.text(), 'муж' if self.rbwoman.isChecked() else 'жен', self.speg.text(),
               self.lephone.text(), self.leEmail.text(), self.cbpost.itemText(self.cbpost.currentIndex()),
               self.spexp.text()]
        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into stuff(fio, pol, phone, email, posishion, exp, age)
            values ('{row[0]}', '{row[1]}', {row[2]}, '{row[3]}', '{row[4]}', '{row[5]}', {row[6]})""")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
