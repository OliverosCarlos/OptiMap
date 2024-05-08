from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtWidgets import QApplication, QGraphicsPixmapItem, QGraphicsEllipseItem, QGraphicsObject
from PyQt5.QtCore import QRectF, Qt, QPointF, pyqtSignal, pyqtProperty, QLineF

class Connection(QtWidgets.QGraphicsLineItem):
    def __init__(self, start, end, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start = start
        self.end = end
        self._line = QtCore.QLineF(start, end)
        self.setPen(QPen(QColor(200, 200, 200), 4))
        self.setLine(self._line)

        self.posP2Manager = PosP2Manager(self.line())

        self.posP2Manager.posChanged.connect(self.setLine)

    def setP1(self, p1):
        self._line.setP1(p1)
        self.setLine(self._line)
        
    def setP2(self, p2):
        self._line.setP2(p2)
        self.setLine(self._line)

class PosP2Manager(QGraphicsObject):
    posChanged = pyqtSignal(QLineF)

    def __init__(self, initial_pos, parent=None):
        super(PosP2Manager, self).__init__(parent)
        self._line = initial_pos

    @pyqtProperty(QLineF, notify=posChanged)
    def pos(self):
        return self._line

    @pos.setter
    def pos(self, v):
        if self._line != v:
            self._line = v
            self.posChanged.emit(self._line)