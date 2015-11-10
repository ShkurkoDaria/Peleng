__author__ = 'shkurko'
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSignal

class CompassWidget(QtWidgets.QWidget):
    angleChanged = pyqtSignal(float)
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent)

        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QRect(0,0, 283, 82))

        self._angle = 0.0
        self._margins = 10
        self._pointText = {0: "С", 45: "СВ", 90: "В", 135: "ЮВ",
                           180: "Ю", 225: "ЮЗ", 270: "З", 315: "СЗ"}

        #self.setMaximumSize(250, 250)

#Рисование окружности и стрелки компаса
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.fillRect(event.rect(), self.palette().brush(QPalette.Window))
        self.drawMarkings(painter)
        self.drawNeedle(painter)

        painter.end()

#Рисование шкалы компаса
    def drawMarkings(self, painter):
        painter.save()
        painter.translate(self.width()/2, self.height()/2)
        scale = min((self.width() - self._margins)/120.0,
                        (self.height() - self._margins)/120.0)
        painter.scale(scale, scale)

        font = QFont(self.font())
        font.setPixelSize(10)
        metrics = QFontMetricsF(font)

        painter.setFont(font)
        #painter.setPen(self.palette().color(QPalette.Shadow))

        i = 0
        while i < 360:
            if i % 45 == 0:
                painter.drawLine(0, -40, 0, -50) #Прорисовка шкал 0, 90, 180, 270, 360
                painter.drawText(-metrics.width(self._pointText[i])/2.0, -52,
                                 self._pointText[i])
            else:
                painter.drawLine(0, -45, 0, -50) #Прорисовка промежуточных шкал

            painter.rotate(15)
            i += 15

        painter.restore()

    def drawNeedle(self, painter):
        painter.save()
        painter.translate(self.width()/2, self.height()/2)
        painter.rotate(self._angle)
        scale = min((self.width() - self._margins)/120.0,
                    (self.height() - self._margins)/120.0)
        painter.scale(scale, scale)

        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(self.palette().brush(QPalette.Shadow))

        painter.drawPolygon(QPolygon([QPoint(-5, 22.5), QPoint(0, -45), QPoint(5, 22.5),#Прорисовка стрелки без наконечника
                                QPoint(0, 0), QPoint(-5, 22.5)]))

        painter.setBrush(self.palette().brush(QPalette.Highlight))#Цвет наконечника стрелки

        painter.drawPolygon(QPolygon([QPoint(-5, -25), QPoint(0, -45), QPoint(5, -25),#Прорисовка наконечника стрелки
                        QPoint(0, -30), QPoint(-5, -25)]))
        painter.restore()

    def sizeHint(self):
        return QSize(150, 150)

    def angle(self):
        return self._angle

    #@pyqtSlot(float)
    #def setAngle(self, angle):
        #if angle != self._angle:
             #self._angle = angle
             #self.angleChanged.emit(angle)
             #self.update()

    #angle = pyqtProperty(float, angle, setAngle)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = QtWidgets.QWidget()
    compass = CompassWidget()
   #spinBox = QtWidgets.QSpinBox()
    #spinBox.setRange(0, 359)
   # spinBox.valueChanged.connect(compass.setAngle)

    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(compass)
    #layout.addWidget(spinBox)
    window.setLayout(layout)

    window.show()
    sys.exit(app.exec_())



