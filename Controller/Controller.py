from PyQt5.QtWidgets import *
from PyQt5.uic import *
from PyQt5 import QtSql
from PyQt5.QtCore import *

class MyApp(QMainWindow) :
    def __init__(self) :
        super().__init__()
        loadUi("Controller.ui", self)
        
        self.db = QtSql.QSqlDatabase.addDatabase("QMYSQL")
        self.db.setHostName("13.209.64.111")
        self.db.setDatabaseName("IoT_data")
        self.db.setUserName("ujin")
        self.db.setPassword("ujin")
        self.db.open()
        
        self.query = QtSql.QSqlQuery()
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.pollingQuery)
        self.timer.start()
        self.time = QDateTime().currentDateTime()
        
    def pollingQuery(self):
        self.query = QtSql.QSqlQuery("SELECT * FROM command ORDER BY time DESC LIMIT 15")
        str = ""
        
        while (self.query.next()):
            self.record = self.query.record()
            str += "%s | %10s | %10s | %4d\n" % (self.record.value(0).toString(), self.record.value(1), self.record.value(2), self.record.value(3))
        
        self.text.setPlainText(str)
        
        self.query = QtSql.QSqlQuery("SELECT * FROM sensing ORDER BY time DESC LIMIT 15")
        str = ""
        while (self.query.next()):
            self.record = self.query.record()
            str += "%s | %10s | %10s | %10s\n" % (self.record.value(0).toString(), self.record.value(1), self.record.value(2), self.record.value(3))
        self.text_2.setPlainText(str)
        
    def commandQuery(self, cmd, arg):
        self.time = QDateTime().currentDateTime()
        self.query.prepare("insert into command (time, cmd_string, arg_string, is_finish) values (:time, :cmd, :arg, :finish)");
        self.query.bindValue(":time", self.time)
        self.query.bindValue(":cmd", cmd)
        self.query.bindValue(":arg", arg)
        self.query.bindValue(":finish", 0)
        self.query.exec()
        
    def clickedSetSpeed(self):
        #print(self.text_speed.toPlainText())
        self.commandQuery("speed", self.spin_speed.value())
        
    def clickedStop(self):
        self.commandQuery("stop", "")
        
    def clickedRight(self):
        self.commandQuery("right", "1 sec")
        
    def clickedLeft(self):
        self.commandQuery("left", "1 sec")
        
    def clickedGo(self):
        self.commandQuery("go", "1 sec")
        
    def clickedBack(self):
        self.commandQuery("back", "1 sec")
        
    def clickedMid(self):
        self.commandQuery("mid", "1 sec")
        
        
app = QApplication([])
win = MyApp()
win.show()
app.exec()