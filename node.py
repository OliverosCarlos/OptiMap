from PyQt5.QtWidgets import  QGraphicsItem, QGraphicsObject
from PyQt5.QtCore import QRectF, Qt, QPropertyAnimation, QPoint, QPointF, QLineF, QParallelAnimationGroup, QAbstractAnimation, pyqtSignal, pyqtProperty
from customItem import CustomItem
from menu_node import MenuNode
from icon import Icon
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5 import QtGui, QtWidgets

from connection import Connection

from utils import Utils

class Node(QGraphicsItem):
    pen = QPen(QColor( 255, 20, 255, 0), 2)
    brush = QBrush(QColor(255, 255, 255))
    # controlBrush = QtGui.QBrush(QtGui.QColor(214, 13, 36))

    def __init__(self, items, children, scene, x=0, y=0, rect = None, left_connection = None, parentNode=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
        if parentNode:
            self._id = parentNode._id + 1
            self.parentNode = parentNode
            self.type = "secondary"

        else:
            self._id = 0
            self.parentNode = self
            self.type = "primary"

        self.scene = scene
        self.rect = rect
        
        self.setFlag(self.ItemIsMovable)
        self.setFlag(self.ItemIsFocusable)

        self.opacityManager = OpacityManager(self.opacity())
        self.opacityManager.opacityChanged.connect(self.setOpacity)
        self.posManager = PosManager(self.pos())
        self.posManager.posChanged.connect(self.setPos)

        self.buildedItems = []

        self.currentItem = None
        self.childrenNodes = []
        self.right_connections = []
        self.left_connection = left_connection
        self.connections : Connection = []
        self.util = Utils()
        
        #control variables
        self.items_displayed = False
        self.menu_node = None
        self.nodeFocused = False

        #to delete

        self.x_ = x
        self.y_ = y
        #BUILD CHILDREN
        
        self.text = "NODE"
        
        #BUILD ITEMS
        self.buildItems(items)

        #BUILD CHILDREN
        if len(children) > 0:
            self.buildChildren(children)
            

        self.setPos(x,y)
         
        self.add_node = Icon(QtGui.QPixmap("add_node.png"), -10, -10, "node", parent = self)
        self.add_node.hide()
        self.add_item = Icon(QtGui.QPixmap("add_item.png"), 30, -10, "item", parent = self)
        self.add_item.hide()

    def boundingRect(self):
        return self.rect
        

    
    def mousePressEvent(self, event):
        if not self.items_displayed :
            if event.button() == 2:
                self.add_node.show()
                self.add_item.show()
                self.iconAnimation()
        else:
            event.ignore()
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        if not self.items_displayed:
            self.anim_group = QParallelAnimationGroup()
            for n,item in enumerate(list(filter(lambda item: isinstance(item, CustomItem),self.buildedItems))):
                
                item.changeEventAvailability(True)

                self.anim = QPropertyAnimation(item, b"pos")
                if n == 0:
                    self.anim.setEndValue(QPoint(0, -10))
                else:
                    self.anim.setEndValue(QPoint(0, (100*(n))+(n)*25))

                self.anim.setDuration(200)

                self.anim_2 = QPropertyAnimation(item, b"opacity")
                self.anim_2.setStartValue(0)
                self.anim_2.setEndValue(1)
                self.anim_2.setDuration(200)


                self.anim_group.addAnimation(self.anim)
                self.anim_group.addAnimation(self.anim_2)
            self.anim_group.start(QAbstractAnimation.DeleteWhenStopped)
        else :
            self.anim_group = QParallelAnimationGroup()
            for n,item in enumerate(list(filter(lambda item: isinstance(item, CustomItem),self.buildedItems))):
                
                item.changeEventAvailability(False)
                item.hideOptions()

                yOffset = 0
                xOffset = 0


                if n <= 2:
                    yOffset = 40+n*10
                    xOffset = n*2
                else:
                    yOffset = 60
                    xOffset = 4

                self.anim = QPropertyAnimation(item, b"pos")
                self.anim.setEndValue(QPoint(xOffset, yOffset))
                self.anim.setDuration(200)
                                 
                self.anim_2 = QPropertyAnimation(item, b"opacity")
                self.anim_2.setStartValue(0)
                self.anim_2.setEndValue(1)
                self.anim_2.setDuration(200)
                                   
                
                self.anim_group.addAnimation(self.anim)
                self.anim_group.addAnimation(self.anim_2)
            self.anim_group.start(QAbstractAnimation.DeleteWhenStopped)
        self.items_displayed = not self.items_displayed

    def mouseMoveEvent(self, event):

        if len(self.right_connections) > 0:
            for connection in self.right_connections:
                connection.setP1(QPointF(self.pos().x()+203,self.pos().y()+90))
            
        if self.left_connection:
            self.left_connection.setP2(QPointF(self.pos().x(),self.pos().y()+90))
                
        super().mouseMoveEvent(event)

    def focusOutEvent(self,  event):
        self.add_node.hide()
        self.add_item.hide()
        super().focusOutEvent(event)

    def focusInEvent(self,  event):
        self.nodeFocused = True
        super().focusOutEvent(event)
        
    def paint(self, painter, option, widget=None):
        pass
        # painter.save()
        # painter.setPen(self.pen)
        # painter.setBrush(self.brush)
        # painter.drawRoundedRect(self.rect, 4, 4)
        # painter.restore()


    def buildItems(self, items):
        for n, itm in enumerate(items):
            yOffset = 0
            xOffset = 0
            
            if n <= 2:
                yOffset = 40+n*10
                xOffset = n*2
            else:
                yOffset = 60
                xOffset = 4


            rect = QRectF(0, 0, 240, 100)
            item = CustomItem(xOffset, yOffset, rect=rect, text=itm["text"], parent = self, parentNode=self.parentNode, parentItemText=itm["parentText"], data=itm)
            item.setZValue(n*-1)
            item.changeEventAvailability(False)
            if n == 0:
                item.changeItemTop(True)
                self.currentItem = item
            self.buildedItems.append(item)
        self.scene.addItem(self)
        
    def buildChildren(self, children):
        
        for n, node in enumerate(children):
            
            #CONNECTION POINT
            p1 = QPointF( self.x_+203, self.y_+90)
            p2 = QPointF( node["node"]["x"], node["node"]["y"]+90 )
            connection = Connection(p1, p2)
            self.right_connections.append(connection)
            self.scene.addItem(connection)
            
            
            ch = node["children"] if len(node["children"]) > 0 else []
            newNode = Node(node["node"]["items"], ch, self.scene, node["node"]["x"], node["node"]["y"], QRectF(0,0, 260, 160), connection,  parentNode=self)                 
            self.childrenNodes.append(newNode)
        
    def newNode(self):

        #CONNECTION POINT
        p1 = QPointF(self.pos().x()+203,self.pos().y()+90)
        p2 = QPointF(self.pos().x()+500,self.pos().y()+90)
        connection = Connection(p1, p2)
        self.right_connections.append(connection)
        self.scene.addItem(connection)

        items = {
                    "items" : [
                        {"text": "New Node", "parentText" : ""},
                    ]
                }
        
        newNode = Node(items["items"], [], self.scene, self.pos().x()+300, self.pos().y(), QRectF(0,0, 260, 160), connection, parentNode=self)
        self.childrenNodes.append(newNode)
        self.newNodeAnimation(newNode, connection)

    def newItem(self):
        newItem = CustomItem(0, 0, rect=QRectF(0, 0, 240, 100), text="new item", createdManually=True, parent = self, parentNode=self.parentNode)
        newItem.setZValue(len(self.buildedItems)*-1)
        self.buildedItems.append(newItem)
        self.newItemAnimation(newItem)

    def iconAnimation(self):
        self.anim_group = QParallelAnimationGroup()

        #NODE ANIMATION
        self.addNodeAnimation = QPropertyAnimation(self.add_node.posManager, b"pos")
        self.addNodeAnimation.setStartValue(QPointF(0, 40))
        self.addNodeAnimation.setEndValue(QPointF(0, 0))
        self.addNodeAnimation.setDuration(200)
        
        self.addNodeAnimation_2 = QPropertyAnimation(self.add_node.opacityManager, b"opacity")
        self.addNodeAnimation_2.setStartValue(0)
        self.addNodeAnimation_2.setEndValue(1)
        self.addNodeAnimation_2.setDuration(200)

        #ITEM ANIMATION
        self.addItemAnimation = QPropertyAnimation(self.add_item.posManager, b"pos")
        self.addItemAnimation.setStartValue(QPointF(40, 40))
        self.addItemAnimation.setEndValue(QPointF(40, 0))
        self.addItemAnimation.setDuration(200)

        self.addItemAnimation_2 = QPropertyAnimation(self.add_item.opacityManager, b"opacity")
        self.addItemAnimation_2.setStartValue(0)
        self.addItemAnimation_2.setEndValue(1)
        self.addItemAnimation_2.setDuration(200)

        #ADD ANIMATION TO GROUP
        self.anim_group.addAnimation(self.addNodeAnimation)
        self.anim_group.addAnimation(self.addNodeAnimation_2)
        self.anim_group.addAnimation(self.addItemAnimation)
        self.anim_group.addAnimation(self.addItemAnimation_2)
        #START ANIMATION GROUP
        self.anim_group.start(QAbstractAnimation.DeleteWhenStopped)

    def newNodeAnimation(self, node, connection):
        self.anim_group = QParallelAnimationGroup()

        self.anim = QPropertyAnimation(node.posManager, b"pos")
        self.anim.setStartValue(QPointF(self.pos().x(), self.pos().y()))
        self.anim.setEndValue(QPointF(self.pos().x()+300, self.pos().y()))
        self.anim.setDuration(200)

        self.anim_2 = QPropertyAnimation(node.opacityManager, b"opacity")
        self.anim_2.setStartValue(0)
        self.anim_2.setEndValue(1)
        self.anim_2.setDuration(200)

        #LINE ANIMATION
        self.connectionAnimation = QPropertyAnimation(connection.posP2Manager, b"pos")
        self.connectionAnimation.setStartValue(
            QLineF(
                QPointF(self.pos().x()+200, self.pos().y()+90),
                QPointF(self.pos().x()+200, self.pos().y()+90)
                )
            )
        self.connectionAnimation.setEndValue(
            QLineF(
                QPointF(self.pos().x()+200, self.pos().y()+90),
                QPointF(self.pos().x()+300,self.pos().y()+90)
                )
            )
        self.connectionAnimation.setDuration(200)

        #ADD GROUP ANIMATIONS
        self.anim_group.addAnimation(self.anim)
        self.anim_group.addAnimation(self.anim_2)
        self.anim_group.addAnimation(self.connectionAnimation)


        self.anim_group.start(QAbstractAnimation.DeleteWhenStopped)

    def newItemAnimation(self, item):
        self.itemAnimationGroup = QParallelAnimationGroup()

        self.itemAnimation = QPropertyAnimation(item, b"pos")
        self.itemAnimation.setEndValue(QPointF(300, 40))
        self.itemAnimation.setDuration(200)

        self.itemAnimation_2 = QPropertyAnimation(item, b"opacity")
        self.itemAnimation_2.setStartValue(0)
        self.itemAnimation_2.setEndValue(1)
        self.itemAnimation_2.setDuration(200)

        self.itemAnimationGroup.addAnimation(self.itemAnimation)
        self.itemAnimationGroup.addAnimation(self.itemAnimation_2)

        self.itemAnimationGroup.start(QAbstractAnimation.DeleteWhenStopped)

    def changeItemOrder(self, itemId):
        
        buildedItemsAux = []
        zAux = self.currentItem.zValue()
        posAux = self.currentItem.pos()

        itemSelected = list( filter( lambda item : id(item)==itemId, self.buildedItems) )[0]

        self.currentItem.setZValue(itemSelected.zValue())
        self.currentItem.setPos(itemSelected.pos())
        self.currentItem.changeItemTop(False)

        itemSelected.setZValue(zAux)
        self.moveItem2TopAnimation(itemSelected,posAux)
        itemSelected.setPos(posAux)
        itemSelected.changeItemTop(True)

        buildedItemsAux.append(itemSelected)

        for item in self.buildedItems[1:]:
            if id(item) == itemId:
                buildedItemsAux.append(self.currentItem)
            else:
                buildedItemsAux.append(item)

        self.buildedItems = buildedItemsAux
        self.currentItem = itemSelected
        self.updateChildren()
        
    def updateChildren(self):
        if len(self.childrenNodes) > 0:
            for nod in self.childrenNodes:
                for item in nod.buildedItems:
                    if id(self.currentItem) == item.parentItemId:
                        nod.changeItemOrder(id(item))

    def moveItem2TopAnimation(self, item, newPos):
        self.itemAnimationGroup = QParallelAnimationGroup()

        self.itemAnimation = QPropertyAnimation(item, b"pos")
        self.itemAnimation.setEndValue(newPos)
        self.itemAnimation.setDuration(200)

        self.itemAnimation_2 = QPropertyAnimation(item, b"opacity")
        self.itemAnimation_2.setStartValue(0)
        self.itemAnimation_2.setEndValue(1)
        self.itemAnimation_2.setDuration(200)

        self.itemAnimationGroup.addAnimation(self.itemAnimation)
        self.itemAnimationGroup.addAnimation(self.itemAnimation_2)

        self.itemAnimationGroup.start(QAbstractAnimation.DeleteWhenStopped)

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