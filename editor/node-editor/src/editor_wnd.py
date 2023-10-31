from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import *

from graphics_view import QDMGraphicsView
from node import Node

from scene import Scene


class NodeEditorWnd(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 800, 600)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # graphic scene
        self.scene = Scene()
        node = Node(self.scene, "Node")

        # graphic view
        self.view = QDMGraphicsView(self.scene.grScene, self)
        self.layout.addWidget(self.view)

        self.setWindowTitle("Node Editor")
        self.setWindowIcon(QIcon("./src/icon.png"))
        self.show()

        # self.addDebugContent()

    def addDebugContent(self):
        greenBrush = QBrush(Qt.GlobalColor.green)
        outlinePen = QPen(Qt.GlobalColor.black)
        outlinePen.setWidth(2)

        rect = self.grScene.addRect(-100, -100, 80,
                                    100, outlinePen, greenBrush)
        rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

        text = self.grScene.addText(
            "This is a sample node editor", QFont("Ubuntu"))
        text.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        text.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        text.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 1.0))

        widget1 = QPushButton("Click")
        proxy1 = self.grScene.addWidget(widget1)
        proxy1.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        proxy1.setPos(0, 30)

        widget2 = QTextEdit()
        proxy2 = self.grScene.addWidget(widget2)
        proxy2.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        proxy2.setPos(0, 60)

        line = self.grScene.addLine(-200, -200, 400, -100, outlinePen)
        line.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
