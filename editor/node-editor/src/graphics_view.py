from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from graphics_socket import QDMGraphicsSocket
from graphics_edge import QDMGraphicsEdge
from node_edge import Edge, EDGE_TYPE_BEZIER


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

        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)

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

        if DEBUG:
            print("LMB Click on", item, self.debug_modifiers(event))

        # logic
        if hasattr(item, "node") or isinstance(item, QDMGraphicsEdge) or item is None:
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(QEvent.Type.MouseButtonPress, QPointF(event.pos()),
                                        Qt.MouseButton.LeftButton, event.buttons() | Qt.MouseButton.LeftButton,
                                        event.modifiers() | Qt.KeyboardModifier.ControlModifier)
                super().mousePressEvent(fakeEvent)
                return

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
        if hasattr(item, "node") or isinstance(item, QDMGraphicsEdge) or item is None:
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(event.type(), QPointF(event.pos()),
                                        Qt.MouseButton.LeftButton, Qt.MouseButton.NoButton,
                                        event.modifiers() | Qt.KeyboardModifier.ControlModifier)
                super().mouseReleaseEvent(fakeEvent)
                return

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

    def mouseMoveEvent(self, event):
        if self.mode == MODE_EDGE_DRAG:
            pos = self.mapToScene(event.pos())
            self.dragEdge.grEdge.setDestination(pos.x(), pos.y())
            self.dragEdge.grEdge.update()

        super().mouseMoveEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.deleteSelected()
        else:
            super().keyPressEvent(event)

    def deleteSelected(self):
        for item in self.grScene.selectedItems():
            if isinstance(item, QDMGraphicsEdge):
                item.edge.remove()
            elif hasattr(item, 'node'):
                item.node.remove()

    def debug_modifiers(self, event):
        out = "MODS: "
        if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            out += "SHIFT "
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            out += "CTRL "
        if event.modifiers() & Qt.KeyboardModifier.AltModifier:
            out += "ALT "
        return out

    def getItemAtClick(self, event):
        """ return the object on which we've clicked/release mouse button """
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    def edgeDragStart(self, item):
        if DEBUG:
            print('View::edgeDragStart ~ Start dragging edge')
        if DEBUG:
            print('View::edgeDragStart ~   assign Start Socket to:', item.socket)
        self.previousEdge = item.socket.edge
        self.last_start_socket = item.socket
        self.dragEdge = Edge(self.grScene.scene,
                             item.socket, None, EDGE_TYPE_BEZIER)
        if DEBUG:
            print('View::edgeDragStart ~   dragEdge:', self.dragEdge)

    def edgeDragEnd(self, item):
        """ return True if skip the rest of the code """
        self.mode = MODE_NOOP

        if type(item) is QDMGraphicsSocket:
            if item.socket != self.last_start_socket:
                if DEBUG:
                    print('View::edgeDragEnd ~   previous edge:',
                          self.previousEdge)
                if item.socket.hasEdge():
                    item.socket.edge.remove()
                if DEBUG:
                    print('View::edgeDragEnd ~   assign End Socket', item.socket)
                if self.previousEdge is not None:
                    self.previousEdge.remove()
                if DEBUG:
                    print('View::edgeDragEnd ~  previous edge removed')
                self.dragEdge.start_socket = self.last_start_socket
                self.dragEdge.end_socket = item.socket
                self.dragEdge.start_socket.setConnectedEdge(self.dragEdge)
                self.dragEdge.end_socket.setConnectedEdge(self.dragEdge)
                if DEBUG:
                    print(
                        'View::edgeDragEnd ~  reassigned start & end sockets to drag edge')
                self.dragEdge.updatePositions()
                return True

        if DEBUG:
            print('View::edgeDragEnd ~ End dragging edge')
        self.dragEdge.remove()
        self.dragEdge = None
        if DEBUG:
            print(
                'View::edgeDragEnd ~ about to set socket to previous edge:', self.previousEdge)
        if self.previousEdge is not None:
            self.previousEdge.start_socket.edge = self.previousEdge
        if DEBUG:
            print('View::edgeDragEnd ~ everything done.')

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
