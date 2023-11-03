from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from graphics_socket import QDMGraphicsSocket
from graphics_edge import QDMGraphicsEdge

MODE_NOOP = 1
MODE_EDGE_DRAG = 2
EDGE_DRAG_START_THRESHOLD = 10
DEBUG = True


class QDMGraphicsView(QGraphicsView):
    def __init__(self, grScene, parent=None):
        super().__init__(parent)

        self.grScene = grScene
        self.initUI()
        self.setScene(self.grScene)

        self.mode = MODE_NOOP

        self.zoomInFactor = 1.25
        self.zoomClamp = True
        self.zoom = 10
        self.zoomStep = 1
        self.zoomRange = [0, 10]

    def initUI(self):
        self.setRenderHints(QPainter.RenderHint.Antialiasing |
                            QPainter.RenderHint.TextAntialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        self.setViewportUpdateMode(
            QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setTransformationAnchor(
            QGraphicsView.ViewportAnchor.AnchorUnderMouse)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.MouseButton.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.MouseButton.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.MouseButton.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.MouseButton.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)

    def middleMouseButtonPress(self, event):
        releaseEvent = QMouseEvent(QEvent.Type.MouseButtonRelease, QPointF(event.pos()),
                                   Qt.MouseButton.LeftButton, Qt.MouseButton.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), QPointF(event.pos()),
                                Qt.MouseButton.LeftButton, event.buttons() | Qt.MouseButton.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)

    def middleMouseButtonRelease(self, event):
        fakeEvent = QMouseEvent(event.type(), QPointF(event.pos()),
                                Qt.MouseButton.LeftButton, event.buttons() & ~Qt.MouseButton.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)

    def leftMouseButtonPress(self, event):
        # get item which we clicked on
        item = self.getItemAtClick(event)

        # we store the position of last LMB click
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())

        # logic
        if type(item) is QDMGraphicsSocket:
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart(item)
                return

        if self.mode == MODE_EDGE_DRAG:
            res = self.edgeDragEnd(item)
            if res:
                return

        super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event):
        # get item which we release mouse button on
        item = self.getItemAtClick(event)

        # logic
        if self.mode == MODE_EDGE_DRAG:
            if self.distanceBetweenClickAndReleaseIsOff(event):
                res = self.edgeDragEnd(item)
                if res:
                    return

        super().mouseReleaseEvent(event)

    def rightMouseButtonPress(self, event):
        super().mousePressEvent(event)
        item = self.getItemAtClick(event)

        if DEBUG:
            if isinstance(item, QDMGraphicsEdge):
                print('RMB DEBUG:', item.edge, ' connecting sockets:',
                      item.edge.start_socket, '<-->', item.edge.end_socket)
            if type(item) is QDMGraphicsSocket:
                print('RMB DEBUG:', item.socket, 'has edge:', item.socket.edge)

            if item is None:
                print('SCENE:')
                print('  Nodes:')
                for node in self.grScene.scene.nodes:
                    print('    ', node)
                print('  Edges:')
                for edge in self.grScene.scene.edges:
                    print('    ', edge)

    def rightMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)

    def getItemAtClick(self, event):
        """ return the object on which we've clicked/release mouse button """
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    def edgeDragStart(self, item):
        if DEBUG:
            print('View::edgeDragStart ~ Start dragging edge')
        if DEBUG:
            print('View::edgeDragStart ~   assign Start Socket')

    def edgeDragEnd(self, item):
        """ return True if skip the rest of the code """
        self.mode = MODE_NOOP
        if DEBUG:
            print('View::edgeDragEnd ~ End dragging edge')

        if type(item) is QDMGraphicsSocket:
            if DEBUG:
                print('View::edgeDragEnd ~   assign End Socket')
            return True

        return False

    def distanceBetweenClickAndReleaseIsOff(self, event):
        """ measures if we are too far from the last LMB click scene position """
        new_lmb_release_scene_pos = self.mapToScene(event.pos())
        dist_scene = new_lmb_release_scene_pos - self.last_lmb_click_scene_pos
        edge_drag_threshold_sq = EDGE_DRAG_START_THRESHOLD*EDGE_DRAG_START_THRESHOLD
        return (dist_scene.x()*dist_scene.x() + dist_scene.y()*dist_scene.y()) > edge_drag_threshold_sq

    def wheelEvent(self, event: QWheelEvent):
        # calc zoom factor
        zoomOutFactor = 1 / self.zoomInFactor

        # calculate zoom
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep

        clamped = False
        if self.zoom < self.zoomRange[0]:
            self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]:
            self.zoom, clamped = self.zoomRange[1], True

        # set scene scale
        if not clamped or self.zoomClamp is False:
            self.scale(zoomFactor, zoomFactor)
