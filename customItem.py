from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5.QtCore import QRectF, Qt, QPointF, QPropertyAnimation, QParallelAnimationGroup, QAbstractAnimation
from controlPoint import ControlPoint
from icon import Icon

class ItemText(QtWidgets.QGraphicsObject):
    

    def __init__(self, text= "New Iteme", rect = QRectF(0, 0, 100, 100), fillColor = "", borderColor = "", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setAcceptHoverEvents(True)

        self.rect = rect
        self.controls = []

        self.itemFocused = False
        self.itemHovered = False
        self.parentDisplayed = False
        self.colorUpdated = False

        self.fillColor = fillColor
        self.borderColor = borderColor
        self.opacity_effect = QGraphicsOpacityEffect()

        self.pen = QtGui.QPen(QtGui.QColor(self.borderColor), 1)
        self.brush = QtGui.QBrush(QtGui.QColor(self.fillColor))
        self.controlBrush = QtGui.QBrush(QtGui.QColor(214, 13, 36))

        self.textItem = ItemLabel("Item Text", parent=self)

        self.text=text
        self.setText(text)

    def boundingRect(self):
        adjust = self.pen.width() / 2
        return self.rect.adjusted(-adjust, -adjust, adjust, adjust)
    
    def paint(self, painter, option, widget=None):
        painter.save()
        if self.itemFocused :
            painter.setPen(QtGui.QPen(QtGui.QColor( 20, 20, 200, 150), 1))
        else: 
            painter.setPen(self.pen)

        painter.setBrush(self.brush)
        # if self.itemHovered:
        #     

        #     clr = QtGui.QColor(self.fillColor)
        #     clr.setAlpha(200)
        #     painter.setBrush(QtGui.QBrush(clr))
        # else:
        #     

        # if self.colorUpdated:


        painter.drawRoundedRect(self.rect, 10, 10)
        painter.restore()

    def hoverEnterEvent (self, event):
        self.itemHovered = True
        self.opacity_effect.setOpacity(0.1)
        self.setGraphicsEffect(self.opacity_effect)
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(Qt.PointingHandCursor))
        super().hoverEnterEvent(event)

    def hoverLeaveEvent (self, event):
        self.itemHovered = False
        self.opacity_effect.setOpacity(1)
        self.setGraphicsEffect(self.opacity_effect)
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(Qt.ArrowCursor))
        super().hoverLeaveEvent(event)

    def updateColors(self, fill, border, text):
        self.fillColor = fill
        self.borderColor = border
        self.pen = QtGui.QPen(QtGui.QColor(border), 1)
        self.brush = QtGui.QBrush(QtGui.QColor(fill))
        # self.controlBrush = QtGui.QBrush(QtGui.QColor(214, 13, 36))

    def setText(self, text):
        #textItem = ItemLabel(text, parent=self)

        self.textItem.setHtml(f'<center>{text}</center>')
        self.textItem.setTextWidth(self.boundingRect().width())
        rect2 = self.textItem.boundingRect()
        
        rect2.moveCenter(self.boundingRect().center())
        self.textItem.setPos(rect2.topLeft())


class CustomItem(QtWidgets.QGraphicsObject):
    pen = QtGui.QPen(QtGui.QColor( 200, 0, 200, 150), 1)
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
    controlBrush = QtGui.QBrush(QtGui.QColor(214, 13, 36))

    def __init__(self, x=0, y=0, rect=None, text="", moveable=False, createdManually=False, parentNode=None, parentItemText="", data={}, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.rect = rect
        self.controls = []
        self.parent = kwargs["parent"]
        self.parentNode = parentNode
        self.parentItemId = None
        self.parentItemText = ""
        self.fillColor = "#ffffff"
        self.borderColor = "#000000"
        self.itemTop = False

        #Control variables
        self.createdManually = createdManually
        self.eventEnabled = False

        if moveable:
            self.setFlags(self.ItemIsMovable)
        self.text=text

        self.setup(data)

        self.itemText = ItemText(text=text, rect=QRectF(rect.x(), rect.y(), rect.width()-40, 100), fillColor = self.fillColor, borderColor = self.borderColor, parent=self )
        
        self.setPos(x,y)

        if self.createdManually:
            self.itemText.setFocus()
            self.openDialog()

        if self.parent.type == "secondary" and parentItemText != "":
            self.setParentItemByText(parentItemText)

        self.save = Icon(QtGui.QPixmap("setup.png"), -10, -10, "node", parent = self)
        self.save.hide()
        self.edit = Icon(QtGui.QPixmap("edit.png"), 25, -10, "openDialog", parent = self)
        self.edit.hide()
        self.setItem = Icon(QtGui.QPixmap("convert.png"), 60, -10, "setItem", parent = self)
        self.setItem.hide()

        

    def boundingRect(self):
        return self.rect

    def setup(self, data):

        if 'fillColor' in data:
            self.fillColor = data["fillColor"]
        if 'borderColor' in data:
            self.borderColor = data["borderColor"]

    def paint(self, painter, option, widget=None):
        pass
        # painter.save()
        # painter.setPen(self.pen)
        # painter.setBrush(self.brush)
        # painter.drawRoundedRect(self.rect, 4, 4)
        # painter.restore()

    def openDialog(self):
        data = {
            "text" : self.text,
            "parentItemText" : self.parentItemText,
            "parentItems" : self.getParentItems()
        }
        dialog = Dialog(data)
        dialog.setAttribute(Qt.WA_DeleteOnClose)
        if dialog.exec_():
            self.itemText.setText(dialog.res["text"])
            self.itemText.text = dialog.res["text"]
            self.text = dialog.res["text"]
            self.parentItemId, self.parentItemText = self.getItemByTitle(self.getParentItems(), dialog.res["parentItem"])

            self.fillColor = dialog.res["fillColor"]
            self.borderColor = dialog.res["borderColor"]
            self.itemText.updateColors(dialog.res["fillColor"], dialog.res["borderColor"], dialog.res["textColor"])

    def getParentItems(self):
        return list(map(lambda item: {"id": id(item), "text": item.text} , self.parentNode.buildedItems))

    def setParentItemByText(self, parentText):
        self.parentItemId, self.parentItemText = self.getItemByTitle(self.getParentItems(), parentText)

    def changeEventAvailability(self, state):
        self.eventEnabled = state
        if state:
            self.setFlag(self.ItemIsFocusable, True)
        else:
            self.setFlag(self.ItemIsFocusable, False)

    def mousePressEvent(self, event):
        if self.eventEnabled :
            if event.button() == 2:
                self.save.show()
                self.edit.show()
                self.setItem.show()
                self.iconAnimation()
        # else:
        #     print("Child unable to process events")
            
        super().mousePressEvent(event)
    
    def focusInEvent(self, event: QtGui.QFocusEvent | None) -> None:
        self.itemText.itemFocused = True
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.itemText.itemFocused = False
        self.hideOptions()
        super().focusOutEvent(event)
        
    def iconAnimation(self):
        self.anim_group = QParallelAnimationGroup()

        #NODE ANIMATION
        self.addNodeAnimation = QPropertyAnimation(self.save.posManager, b"pos")
        self.addNodeAnimation.setStartValue(QPointF(200, 0))
        self.addNodeAnimation.setEndValue(QPointF(210, 0))
        self.addNodeAnimation.setDuration(200)
        
        self.addNodeAnimation_2 = QPropertyAnimation(self.save.opacityManager, b"opacity")
        self.addNodeAnimation_2.setStartValue(0)
        self.addNodeAnimation_2.setEndValue(1)
        self.addNodeAnimation_2.setDuration(200)

        #ITEM ANIMATION
        self.addItemAnimation = QPropertyAnimation(self.edit.posManager, b"pos")
        self.addItemAnimation.setStartValue(QPointF(200, 35))
        self.addItemAnimation.setEndValue(QPointF(210, 35))
        self.addItemAnimation.setDuration(200)

        self.addItemAnimation_2 = QPropertyAnimation(self.edit.opacityManager, b"opacity")
        self.addItemAnimation_2.setStartValue(0)
        self.addItemAnimation_2.setEndValue(1)
        self.addItemAnimation_2.setDuration(200)

        #SETITEM ANIMATION
        self.setItemAnimation = QPropertyAnimation(self.setItem.posManager, b"pos")
        self.setItemAnimation.setStartValue(QPointF(200, 70))
        self.setItemAnimation.setEndValue(QPointF(210, 70))
        self.setItemAnimation.setDuration(200)

        self.setItemAnimation_2 = QPropertyAnimation(self.setItem.opacityManager, b"opacity")
        self.setItemAnimation_2.setStartValue(0)
        self.setItemAnimation_2.setEndValue(1)
        self.setItemAnimation_2.setDuration(200)

        #ADD ANIMATION TO GROUP
        self.anim_group.addAnimation(self.addNodeAnimation)
        self.anim_group.addAnimation(self.addNodeAnimation_2)
        self.anim_group.addAnimation(self.addItemAnimation)
        self.anim_group.addAnimation(self.addItemAnimation_2)
        self.anim_group.addAnimation(self.setItemAnimation)
        self.anim_group.addAnimation(self.setItemAnimation_2)
        #START ANIMATION GROUP
        self.anim_group.start(QAbstractAnimation.DeleteWhenStopped)

    def hideOptions(self):
        self.save.hide()
        self.edit.hide()
        self.setItem.hide()

    def getItemByTitle(self, parentItems, title):
        return [ (item["id"], item["text"]) for item in parentItems if item["text"] == title][0]
    
    def isItemTop(self):
        return self.itemTop
    
    def changeItemTop(self, status):
        self.itemTop = status

    def setupItemAsCurrent(self):
        self.parent.changeItemOrder(id(self))

class ItemLabel(QtWidgets.QGraphicsTextItem):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        # self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        # self.setTextInteractionFlags(Qt.TextEditable)

class Dialog(QtWidgets.QDialog):
    def __init__(self, data):
        super().__init__()
        self.fillColor = "#ffffff"
        self.borderColor = "#000000"
        self.textColor = "#000000"

        self.resize(240, 120)
        self.setWindowTitle("Editing item")

        self.exampleItem = QtWidgets.QLabel("New Item", self)
        self.exampleItem.setAlignment(Qt.AlignCenter)
        self.exampleItem.setStyleSheet("background-color: {}; border: 1px solid {}; border-radius: 5px; padding : 10 px; color: {};".format(self.fillColor, self.borderColor, self.textColor))

        self.titleInput = QtWidgets.QLineEdit(placeholderText="Insert")
        self.titleInput.setText(data["text"])
        self.parentItemsCMB = QtWidgets.QComboBox()
        self.parentItemsCMB.addItems( [ _["text"] for _ in data["parentItems"] ] )

        #Color buttons
        self.fillColorBTN = QtWidgets.QPushButton(text="", objectName='fill', parent=self)
        self.fillColorBTN.setStyleSheet("background-color: red;")
        self.fillColorBTN.setToolTip('Opens color dialog')
        self.fillColorBTN.clicked.connect(self.openColorDialog)
        
        self.borderColorBTN = QtWidgets.QPushButton(text="", objectName='border', parent=self)
        self.borderColorBTN.setStyleSheet("background-color: red;")
        self.borderColorBTN.setToolTip('Opens color dialog')
        self.borderColorBTN.clicked.connect(self.openColorDialog)

        self.textColorBTN = QtWidgets.QPushButton(text="", objectName='text', parent=self)
        self.textColorBTN.setStyleSheet("background-color: red;")
        self.textColorBTN.setToolTip('Opens color dialog')
        self.textColorBTN.clicked.connect(self.openColorDialog)

        self.saveBtn = QtWidgets.QPushButton("Save", self)
        self.saveBtn.setToolTip("Save configuration")

        self.createFormGroupBox()

        self.res = {}

        # creamos un layout y lo establecemos en el widget
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(self.exampleItem)
        self.setLayout(mainLayout)


        # podemos añadir una etiqueta

        # creamos unos botones predeterminados
        botones = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        # y los añadimos al layout
        mainLayout.addWidget(botones)
        mainLayout.addWidget(self.saveBtn)
        

        self.saveBtn.clicked.connect(self.submitclose)
        # botones.accepted.connect(self.submit())
        botones.rejected.connect(self.reject)

    def createFormGroupBox(self):
        self.formGroupBox = QtWidgets.QGroupBox("General")
        layout = QtWidgets.QFormLayout()
        layout.addRow(QtWidgets.QLabel("Title :"), self.titleInput)
        layout.addRow(QtWidgets.QLabel("Parent :"), self.parentItemsCMB)
        layout.addRow(QtWidgets.QLabel("Fill color :"), self.fillColorBTN)
        layout.addRow(QtWidgets.QLabel("Border color :"), self.borderColorBTN)
        layout.addRow(QtWidgets.QLabel("text color :"), self.textColorBTN)


        self.formGroupBox.setLayout(layout)

    def openColorDialog(self):
        color = QtWidgets.QColorDialog.getColor()

        if color.isValid():
            self.changeColor(self.sender(), color.name())

    def changeColor(self, element, color):
        element.setStyleSheet("background-color: {};".format(color))
        if element.objectName() == "fill":
            self.fillColor = color
        elif element.objectName() == "border":
            self.borderColor = color
        elif element.objectName() == "text":
            self.textColor = color

        self.updateExampleItemColor()

    def updateExampleItemColor(self):
        self.exampleItem.setStyleSheet("background-color: {}; border: 1px solid {}; border-radius: 5px; padding : 10 px; color: {};".format(self.fillColor, self.borderColor, self.textColor))


    def submitclose(self):
        self.res = {
            "text": self.titleInput.text(), 
            "parentItem": self.parentItemsCMB.currentText(),
            "fillColor" : self.fillColor,
            "borderColor" : self.borderColor,
            "textColor" : self.textColor
            }
        
        self.accept()