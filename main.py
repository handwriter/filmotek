from PyQt5.QtWidgets import QWidget, QApplication, QInputDialog, QTableWidgetItem
import sys
import sqlite3
from design import Ui_Form as Design


class Widget(QWidget, Design):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("films.db")
        self.tableWidget.cellDoubleClicked.connect(self.changer)
        self.update_result()
        self.setUnvisibles()
        self.pushButton.clicked.connect(self.setVisibles)
        self.pushButton_2.clicked.connect(self.adds)
        cur = self.con.cursor()
        result = cur.execute("Select * from genres").fetchall()
        genres = [i[1] for i in result]
        for i in genres:
            self.comboBox.addItems(genres)

    def setUnvisibles(self):
        self.label.setVisible(False)
        self.label_2.setVisible(False)
        self.label_3.setVisible(False)
        self.label_4.setVisible(False)
        self.lineEdit.setVisible(False)
        self.spinBox.setVisible(False)
        self.comboBox.setVisible(False)
        self.spinBox_2.setVisible(False)
        self.tableWidget.setVisible(True)
        self.pushButton_2.setVisible(False)
        self.pushButton.setVisible(True)

    def setVisibles(self):
        self.label.setVisible(True)
        self.label_2.setVisible(True)
        self.label_3.setVisible(True)
        self.label_4.setVisible(True)
        self.lineEdit.setVisible(True)
        self.spinBox.setVisible(True)
        self.comboBox.setVisible(True)
        self.spinBox_2.setVisible(True)
        self.tableWidget.setVisible(False)
        self.pushButton_2.setVisible(True)
        self.pushButton.setVisible(False)

    def adds(self):
        if self.lineEdit.text() == '':
            pass
        else:
            try:
                cur2 = self.con.cursor()
                result2 = cur2.execute("""SELECT id FROM Films""").fetchall()
                print(self.comboBox.currentIndex())
                cur = self.con.cursor()
                result = cur.execute("""INSERT INTO Films(id,title,year,genre,duration) VALUES(?,?,?,?,?)""",
                                     (int(result2[-1][0] + 1), self.lineEdit.text(), int(self.spinBox.value()), int(self.comboBox.currentIndex() + 1), int(self.spinBox_2.value()))).fetchall()
                self.con.commit()
                self.setUnvisibles()
                self.con = sqlite3.connect("films.db")
                self.update_result()
            except:
                pass

    def update_result(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute("Select * from films").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        names = [i[0] for i in cur.description]
        for i in range(len(names)):
            self.tableWidget.setItem(0, i, QTableWidgetItem(str(names[i])))
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i + 1, j, QTableWidgetItem(str(val)))

    def changer(self):
        if self.tableWidget.currentRow() != 0:
            if self.tableWidget.currentColumn() == 0:
                pass
            elif self.tableWidget.currentColumn() == 1:
                m = QInputDialog.getText(self, 'Edit', 'Info:')[0]
                if m != '':
                    self.tableWidget.item(self.tableWidget.currentRow(), self.tableWidget.currentColumn()).setText(m)
                    cur = self.con.cursor()
                    result = cur.execute("""UPDATE films
                                            SET title = ?
                                            WHERE ROWID = ?""", (str(m), int(self.tableWidget.currentRow()))).fetchall()
                    self.con.commit()
            elif self.tableWidget.currentColumn() == 2:
                m = QInputDialog.getInt(self, 'Edit', 'Info:', 1, 1, 99999)[0]
                self.tableWidget.item(self.tableWidget.currentRow(), self.tableWidget.currentColumn()).setText(str(m))
                cur = self.con.cursor()
                result = cur.execute("""UPDATE films
                                        SET year = ?
                                        WHERE ROWID = ?""",
                                     (int(m), int(self.tableWidget.currentRow()))).fetchall()
                self.con.commit()
            elif self.tableWidget.currentColumn() == 3:
                cur = self.con.cursor()
                result = cur.execute("Select * from genres").fetchall()
                genres = [i[1] for i in result]
                m = QInputDialog.getItem(self, 'Edit', 'Info:', genres, int(self.tableWidget.item(self.tableWidget.currentRow(), self.tableWidget.currentColumn()).text()) - 1, False)
                self.tableWidget.item(self.tableWidget.currentRow(), self.tableWidget.currentColumn()).setText(str(genres.index(m[0]) + 1))
                cur = self.con.cursor()
                result = cur.execute("""UPDATE films
                                        SET genre = ?
                                        WHERE ROWID = ?""",
                                     (int(genres.index(m[0]) + 1), int(self.tableWidget.currentRow()))).fetchall()
                self.con.commit()
            elif self.tableWidget.currentColumn() == 4:
                m = QInputDialog.getInt(self, 'Edit', 'Info:', int(self.tableWidget.item(self.tableWidget.currentRow(), self.tableWidget.currentColumn()).text()), 1, 999)[0]
                self.tableWidget.item(self.tableWidget.currentRow(), self.tableWidget.currentColumn()).setText(str(m))
                cur = self.con.cursor()
                result = cur.execute("""UPDATE films
                                        SET duration = ?
                                        WHERE ROWID = ?""",
                                     (int(m), int(self.tableWidget.currentRow()))).fetchall()
                self.con.commit()


app = QApplication(sys.argv)
ex = Widget()
ex.show()
sys.exit(app.exec_())