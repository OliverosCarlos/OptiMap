from PyQt5.QtGui import QPen, QColor, QBrush, QPixmap, QCursor
from PyQt5.QtWidgets import QApplication, QGraphicsPixmapItem, QGraphicsEllipseItem, QGraphicsObject
from PyQt5.QtCore import QRectF, Qt, QPointF, pyqtSignal, pyqtProperty
from controlPoint import ControlPoint

from connection import Connection

class Icon(QGraphicsPixmapItem):
    pen = QPen(QColor(0, 0, 0), 2)
    brush = QBrush(QColor(255, 255, 255))
    controlBrush = QBrush(QColor(214, 13, 36))
    rect = QRectF(0, 0, 200, 100)

    def __init__(self, pixmap, x, y, type, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.opacityManager = OpacityManager(self.opacity())
        self.opacityManager.opacityChanged.connect(self.setOpacity)
        self.posManager = PosManager(self.pos())
        self.posManager.posChanged.connect(self.setPos)

        self.parent = kwargs["parent"]
        self.setPixmap(pixmap)
        self.setAcceptHoverEvents(True)
        #self.setOffset(x,y)
        self.setPos(x,y)

        self.type = type
        
        self.hoverElipse = QGraphicsEllipseItem(-3,-3,30,30, parent=self)
        self.hoverElipse.setPen(QPen(QColor(200, 200, 200, 200)))
        self.hoverElipse.setBrush(QBrush(QColor(200, 200, 200, 200)))
        self.hoverElipse.hide()

    def mousePressEvent(self, event):
        if event.button() == 1:
            self.setOpacity(0.5)
            if self.type == "node":
                self.parent.newNode()
            elif self.type == "item":
                self.parent.newItem()
            elif self.type == "setItem":
                self.parent.setupItemAsCurrent()
            elif self.type == "openDialog":
                self.parent.openDialog()

    def mouseReleaseEvent(self, event):
        self.setOpacity(0.3)

    def hoverEnterEvent(self, event):
        #self.hoverElipse.show()
        self.setOpacity(0.3)
        #self.setPixmap(QPixmap("plus_2.png"))
        QApplication.setOverrideCursor(QCursor(Qt.PointingHandCursor))

    def hoverLeaveEvent(self, event):
        self.setOpacity(1)
        #self.hoverElipse.hide()
        #self.setPixmap(QPixmap("plus_1.png"))
        QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))

class OpacityManager(QGraphicsObject):
    opacityChanged = pyqtSignal(float)

    def __init__(self, initial_opacity, parent=None):
        super(OpacityManager, self).__init__(parent)
        self._opacity = initial_opacity

    @pyqtProperty(float, notify=opacityChanged)
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, v):
        if self._opacity != v:
            self._opacity = v
            self.opacityChanged.emit(self._opacity)

class PosManager(QGraphicsObject):
    posChanged = pyqtSignal(QPointF)

    def __init__(self, initial_pos, parent=None):
        super(PosManager, self).__init__(parent)
        self._pos = initial_pos

    @pyqtProperty(QPointF, notify=posChanged)
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, v):
        if self._pos != v:
            self._pos = v
            self.posChanged.emit(self._pos)