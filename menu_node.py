from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QRectF, Qt
from controlPoint import ControlPoint
        
class MenuNode(QtWidgets.QGraphicsObject):
    pen = QtGui.QPen(QtGui.QColor(0, 0, 0), 2)
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
    controlBrush = QtGui.QBrush(QtGui.QColor(214, 13, 36))
    rect = QRectF(0, 0, 300, 200)

    def __init__(self, rect = QRectF(-5, -5, 210, 110), moveable=False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.rect = rect
        self.controls = []

        if moveable:
            self.setFlags(self.ItemIsMovable)

    def boundingRect(self):
        adjust = self.pen.width() / 2
        return self.rect.adjusted(-adjust, -adjust, adjust, adjust)

    def paint(self, painter, option, widget=None):
        painter.save()
        painter.setPen(self.pen)
        #painter.setBrush(self.brush)
        painter.drawRoundedRect(self.rect, 10, 10)
        painter.restore()