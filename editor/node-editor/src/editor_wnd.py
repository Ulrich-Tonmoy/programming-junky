from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import *

from graphics_view import QDMGraphicsView
from node import Node
from node_edge import Edge, EDGE_TYPE_BEZIER
from scene import Scene


class NodeEditorWnd(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.stylesheet_filename = './src/qss/node_style.qss'
        self.loadStylesheet(self.stylesheet_filename)

        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 800, 600)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # graphic scene
        self.scene = Scene()

        self.addNodes()

        # graphic view
        self.view = QDMGraphicsView(self.scene.grScene, self)
        self.layout.addWidget(self.view)

        self.setWindowTitle("Node Editor")
        self.setWindowIcon(QIcon("./src/icon.png"))
        self.show()

        # self.addDebugContent()

    def addNodes(self):
        node1 = Node(self.scene, "Node 1", inputs=[1, 2, 3], outputs=[1])
        node2 = Node(self.scene, "Node 2", inputs=[1, 2, 3], outputs=[1])
        node3 = Node(self.scene, "Node 3", inputs=[1, 2, 3], outputs=[1])
        node1.setPos(-350, -250)
        node2.setPos(-75, 0)
        node3.setPos(200, -150)

        edge1 = Edge(
            self.scene, node1.outputs[0], node2.inputs[0], edge_type=EDGE_TYPE_BEZIER)
        edge2 = Edge(
            self.scene, node2.outputs[0], node3.inputs[0], edge_type=EDGE_TYPE_BEZIER)

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
        line.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

    def loadStylesheet(self, filename):
        print('STYLE loading:', filename)
        file = QFile(filename)
        file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))
