from PyQt5.QtWidgets import  QGraphicsItem, QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtCore import QRectF, Qt, QPropertyAnimation, QSequentialAnimationGroup, QPoint, QSize, QParallelAnimationGroup
from customItem import CustomItem
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5 import QtGui, QtWidgets

from node import Node

from utils import Utils

class GroupItem(QGraphicsItem):
    pen = QPen(QColor(255, 0, 0), 2)
    brush = QBrush(QColor(255, 255, 255))
    controlBrush = QtGui.QBrush(QtGui.QColor(214, 13, 36))
    rect = QRectF(0, 0, 300, 120)
    
    def __init__(self, x, y, scene):
        super().__init__()
        self.scene = scene
        self.util = Utils()

        data = [{
            "items" : [
                {
                    "text": "Database",
                    "children": []
                }, 
                {"text": "Business Rules"},
                {"text": "MVC"},
                {"text": "Classes"}
            ],
            
        }]
        
        # children = ["Carlos", "Moises", "Ruvalcaba", "Oliveros", "Roboe", "Roboe"]
        # items = ["Jessica", "Magali", "Madera"]
           
        # items_ws = Utils.getGroupCount(len(items),200)
                    
        self.scene.addItem(self)

        rect = QRectF(0, 0, 240, 160)
        
        self.mainNode = Node(data[0]["items"], data[0]["items"][0]["children"], self.scene, 0, 0, rect)
        
    
    def boundingRect(self):
        return self.rect

    def buildChildren(self, children):
        ver_coords, new_offset = self.util.getVerticalCoords(len(children), 100)
        for n, text in enumerate(children):
            rect = QRectF(300, ver_coords[n], 200, 100)
            CustomItem(left=True, rect=rect, text=text, parent = self)

    def paint(self, painter, option, widget=None):
        pass