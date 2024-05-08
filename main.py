import sys
from PyQt5.QtWidgets import QMainWindow, QAction, QGraphicsView, QWidget, QHBoxLayout, QMenuBar, QMenu, QApplication, QFileDialog
from PyQt5 import QtCore
from PyQt5.QtGui import QBrush, QColor, QPainter
from PyQt5.QtCore import QRectF

from groupItem import GroupItem
from scene import Scene
from node import Node

import json
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setWindowTitle("OptiMap")
        self.fileName = ""

        self._createActions()
        self._createMenuBar()

        self.mainScene = Scene()
        self.mainScene.setBackgroundBrush(QBrush(QColor(248, 250, 252)))

        # grp = GroupItem(0, 0,self.mainScene)
        # self.mainScene.addItem(grp)
        

        self.mainGraphicsView = QGraphicsView(self.mainScene)
        self.mainGraphicsView.setGeometry(QtCore.QRect(0, 21, 1000, 1000))
        self.mainGraphicsView.setRenderHints(QPainter.Antialiasing)

        central_widget = QWidget()
        layout = QHBoxLayout(central_widget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.mainGraphicsView)

        self.setCentralWidget(central_widget)

    def _createActions(self):

        # Creating action using the first constructor
        self.newAction = QAction("&New", self)
        self.newAction.triggered.connect(self.newDiagram)
        self.openAction = QAction("&Open", self)
        self.openAction.triggered.connect(self.openDiagram)
        self.saveAction = QAction("&Save", self)
        self.saveAction.triggered.connect(self.saveDiagram)
        self.saveAsAction = QAction("&Save As...", self)
        self.saveAsAction.triggered.connect(self.saveDiagramAs)
        self.exitAction = QAction("&Exit", self)

        self.copyAction = QAction("&Copy", self)
        self.pasteAction = QAction("&Paste", self)
        self.cutAction = QAction("C&ut", self)

        self.helpContentAction = QAction("&Help Content", self)
        self.aboutAction = QAction("&About", self)

    def _createMenuBar(self):
        menuBar = QMenuBar(self)
        self.setMenuBar(menuBar)

        # Creating menus using a QMenu object
        fileMenu = QMenu("&File", self)
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.saveAsAction)
        fileMenu.addAction(self.exitAction)

        menuBar.addMenu(fileMenu)
        # Creating menus using a title
        editMenu = menuBar.addMenu("&Edit")
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addAction(self.cutAction)

        helpMenu = menuBar.addMenu("&Help")
        helpMenu.addAction(self.helpContentAction)
        helpMenu.addAction(self.aboutAction)

        menuBar.addMenu(editMenu)
        menuBar.addMenu(helpMenu)

    def newDiagram(self):

        data = [{
            "items" : [
                {"text": "Database"},
                {"text": "Business Rules"},
                {"text": "MVC"},
                {"text": "Classes"}
            ]
        }]
        rect = QRectF(0, 0, 240, 160)
        self.mainNode = Node(data[0]["items"], [], self.mainScene, 0, 0, rect)

    def saveDiagram(self):
        mainNode : Node = list(filter( lambda ele : isinstance( ele, Node ) and ele.type == "primary" , self.mainScene.items(QtCore.Qt.AscendingOrder) ))

        with open(self.fileName, "w") as outfile:
            json.dump(self.getData(mainNode[0]), outfile)

        print("Saving diagram ...")

    def saveDiagramAs(self):
        mainNode : Node = list(filter( lambda ele : isinstance( ele, Node ) and ele.type == "primary" , self.mainScene.items(QtCore.Qt.AscendingOrder) ))

        print(self.getData(mainNode[0]))
        fileName = self.saveFileDialog()
        if fileName:
            with open(fileName, "w") as outfile:
                json.dump(self.getData(mainNode[0]), outfile)

            self.fileName = fileName
            self.setWindowTitle(str(os.path.basename(fileName)) + " - OptiMap")
        print("Saving diagram ...")

    def openDiagram(self):
        # Opening JSON file
        fileName = self.openFileNameDialog()
        if fileName:
            self.fileName = fileName
            f = open(fileName)
 
            # returns JSON object as 
            # a dictionary
            data = json.load(f)
 
            # Closing file
            f.close()

            self.fileName = fileName
            self.setWindowTitle(str(os.path.basename(fileName)) + " - OptiMap")
            self.loadDataNode(data)

    def getData(self, node):

        if len(node.childrenNodes) > 0:

            children = []
            for nod in node.childrenNodes:
                children.append(self.getData(nod))

            return {
                "node": {
                        "itemSelected" : node.text,
                        "x" : node.x(),
                        "y" : node.y(),
                        "type" : node.type,
                        "items": [
                            {
                                "text" : _.text,
                                "parentText" : _.parentItemText,
                                "fillColor" : _.fillColor,
                                "borderColor" : _.borderColor
                            } for _ in node.buildedItems
                        ]

                    },
                "children": children
            }

        
        else :
            return {
                "node": {
                        "itemSelected" : node.text,
                        "x" : node.x(),
                        "y" : node.y(),
                        "type" : node.type,
                        "items": [
                            {
                                "text" : _.text,
                                "parentText" : _.parentItemText,
                                "fillColor" : _.fillColor,
                                "borderColor" : _.borderColor
                            } for _ in node.buildedItems
                        ]

                    },
                "children": []
                }
                
    def loadDataNode(self, data):
        
        rect = QRectF(0, 0, 240, 160)
        self.mainNode = Node(data["node"]["items"], data["children"], self.mainScene, data["node"]["x"], data["node"]["y"], rect)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileName(self,"Select OptiMap File", "","All Files ();;Python Files (.py)", options=options)
        return files

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files ();;Text Files (.txt)", options=options)
        return fileName

if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWindow = MainWindow()

    mainWindow.show()
    sys.exit(app.exec_())