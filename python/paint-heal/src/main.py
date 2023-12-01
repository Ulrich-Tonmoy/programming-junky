import sys
import cv2
import copy

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QWidget, QFileDialog, QSlider, QGraphicsView, QGraphicsScene,
    QGraphicsPixmapItem, QScrollArea, QLabel, QStyle
)
from PyQt6.QtGui import QPixmap, QImage, QPainter, QKeySequence, QCursor, QKeyEvent, QIcon, QAction, QShortcut
from PyQt6.QtCore import Qt

from worker import Worker


class State:
    "Simple class to store state of our app"

    def __init__(self, app: "Paint") -> None:
        self.image = copy.deepcopy(app.image)
        self.radius = app.radius
        self.sample_radius = app.sample_radius
        self.opacity = app.opacity
        self.healing_brush_active = app.healing_brush_active


class Paint(QMainWindow):
    def __init__(self):
        super().__init__()

        self.worker = Worker()
        self.worker.done.connect(self.process_done)

        self.WIDTH = 1280
        self.HEIGHT = 720

        self.image = None
        self.healing_brush_active = False
        self.radius = 15
        self.sample_radius = 5
        self.zoom_level = 0
        self.opacity = 0.2

        self.history = []

        self.space_pressed = False
        self.last_cursor_pos = None
        self.dragging = False

        self.round_cursor = self.create_round_cursor(self.radius)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Paint Heal")
        self.setWindowIcon(QIcon("src/Xcode.png"))
        self.setFixedSize(self.WIDTH, self.HEIGHT)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)

        self.image_view = QGraphicsView(self)
        self.image_view.setFixedSize(self.WIDTH, self.HEIGHT)
        self.image_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.image_view.mousePressEvent = self.mousePressEventIMG
        self.image_view.mouseMoveEvent = self.mouseMoveEventIMG
        self.image_view.mouseReleaseEvent = self.mouseReleaseEventIMG
        self.image_view.wheelEvent = self.wheelEventIMG

        self.image_view.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.image_view.setTransformationAnchor(
            QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.image_view.setResizeAnchor(
            QGraphicsView.ViewportAnchor.AnchorUnderMouse)

        self.image_view.setStyleSheet("border: none;")
        self.image_view.setViewportUpdateMode(
            QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.image_view.setCursor(self.round_cursor)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidget(self.image_view)

        self.main_layout.addWidget(self.scroll_area)

        self.scene = QGraphicsScene()
        self.image_view.setScene(self.scene)

        self.image_item = QGraphicsPixmapItem()
        self.scene.addItem(self.image_item)

        self.radius_slider_layout = QHBoxLayout()
        self.radius_slider = QSlider(Qt.Orientation.Horizontal)
        self.radius_slider.setRange(1, 100)
        self.radius_slider.setValue(self.radius)
        self.radius_slider.valueChanged.connect(self.radius_changed)

        self.radius_label = QLabel(f"Radius ({self.radius})")

        self.radius_slider_layout.addWidget(self.radius_label)
        self.radius_slider_layout.addWidget(self.radius_slider)

        self.sample_slider_layout = QHBoxLayout()
        self.sample_slider = QSlider(Qt.Orientation.Horizontal)
        self.sample_slider.setRange(1, 50)
        self.sample_slider.setValue(self.sample_radius)
        self.sample_slider.valueChanged.connect(self.sample_changed)

        self.sample_label = QLabel(
            f"Sample Radius (Higher is slower) ({self.sample_radius})")

        self.sample_slider_layout.addWidget(self.sample_label)
        self.sample_slider_layout.addWidget(self.sample_slider)

        self.opacity_slider_layout = QHBoxLayout()
        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setRange(1, 5)
        self.opacity_slider.setSingleStep(1)
        self.opacity_slider.setTickPosition(
            QSlider.TickPosition.TicksBothSides)
        self.opacity_slider.setTickInterval(1)
        self.opacity_slider.setValue(int(self.opacity * 10))
        self.opacity_slider.valueChanged.connect(self.opacity_changed)

        self.opacity_label = QLabel(f"Opacity: {self.opacity}")
        self.opacity_slider_layout.addWidget(self.opacity_label)
        self.opacity_slider_layout.addWidget(self.opacity_slider)

        self.main_layout.addLayout(self.radius_slider_layout)
        self.main_layout.addLayout(self.sample_slider_layout)
        self.main_layout.addLayout(self.opacity_slider_layout)

        # shortcuts
        self.shortcut_undo = QShortcut(
            QKeySequence(Qt.Modifier.CTRL and Qt.Key.Key_Z), self)
        self.shortcut_undo.activated.connect(self.load_last_state)

        self.shortcut_redo = QShortcut(
            QKeySequence(Qt.Modifier.CTRL and Qt.Key.Key_Y), self)
        self.shortcut_redo.activated.connect(self.revert_last_state)

        self.shortcut_save = QShortcut(
            QKeySequence(Qt.Modifier.CTRL and Qt.Key.Key_S), self)
        self.shortcut_save.activated.connect(self.saveImage)

        # menu bar
        menuBar = self.menuBar()
        menuBar.setStyleSheet("font-size: 15px")

        fileMenu = menuBar.addMenu("&File")
        editMenu = menuBar.addMenu("&Edit")

        load_act = QAction("Load Image", self)
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DirHomeIcon)
        load_act.setIcon(icon)
        load_act.setStatusTip("Load an Image")
        load_act.triggered.connect(self.load_image)
        fileMenu.addAction(load_act)

        undo_act = QAction("Undo", self)
        undo_act.setStatusTip("Undo")
        undo_act.triggered.connect(self.load_last_state)
        editMenu.addAction(undo_act)

        redo_act = QAction("Redo", self)
        redo_act.setStatusTip("Redo")
        redo_act.triggered.connect(self.revert_last_state)
        editMenu.addAction(redo_act)

        save_act = QAction("Save", self)
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton)
        save_act.setIcon(icon)
        save_act.triggered.connect(self.saveImage)
        fileMenu.addAction(save_act)

    def create_round_cursor(self, radius):
        cursor_size = radius * 2 + 1
        pixmap = QPixmap(cursor_size, cursor_size)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setOpacity(0.5)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(Qt.GlobalColor.black)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, cursor_size, cursor_size)
        painter.end()

        return QCursor(pixmap, radius, radius)

    def process_done(self, img):
        self.image = img
        self.updateImageLabel()

    def updateImageLabel(self):
        if self.image is not None:
            colored_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            qt_img = QImage(
                colored_img.data, colored_img.shape[1], colored_img.shape[0],
                colored_img.shape[1] * 3, QImage.Format.Format_RGB888
            )
            pixmap = QPixmap.fromImage(qt_img)
            self.image_item.setPixmap(pixmap)

    def load_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)"
        )
        if file_path:
            self.image = cv2.imread(file_path)
            self.updateImageLabel()
            self.image_view.fitInView(
                self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio
            )
            self.save_state()

    def saveImage(self):
        file, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file:
            cv2.imwrite(file, self.image)

    def radius_changed(self):
        self.radius = self.radius_slider.value()
        self.radius_label.setText(f"Radius ({self.radius})")
        self.round_cursor = self.create_round_cursor(self.radius)
        self.image_view.setCursor(self.round_cursor)
        self.save_state()

    def sample_changed(self):
        self.sample_radius = self.sample_slider.value()
        self.sample_label.setText(
            f"Sample Radius (Higher is slower) ({self.sample_radius})")
        self.save_state()

    def opacity_changed(self):
        self.opacity = self.opacity_slider.value() / 10.0
        self.opacity_label.setText(f"Opacity: {self.opacity: .2f}")
        self.save_state()

    def isInsideImage(self, x, y):
        return 0 <= x < self.image.shape[1] and 0 <= y < self.image.shape[0]

    def healImage(self, x, y):
        self.worker.set_and_run(
            self.image, x, y, self.radius, self.sample_radius, self.opacity)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Space:
            self.space_pressed = True
            if self.image_view.dragMode() == QGraphicsView.DragMode.RubberBandDrag:
                self.image_view.setDragMode(
                    QGraphicsView.DragMode.ScrollHandDrag)

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Space and self.space_pressed:
            self.space_pressed = False
            if self.image_view.dragMode() == QGraphicsView.DragMode.ScrollHandDrag:
                self.image_view.setDragMode(
                    QGraphicsView.DragMode.RubberBandDrag)

    def mousePressEventIMG(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.space_pressed:
            self.last_cursor_pos = event.pos()
            self.dragging = True
            return

        if self.image is not None and event.button() == Qt.MouseButton.LeftButton:
            pos = self.image_view.mapToScene(event.pos())
            x, y = int(pos.x()), int(pos.y())
            if self.isInsideImage(x, y):
                self.healing_brush_active = True
                self.healImage(x, y)
                self.update()

    def mouseMoveEventIMG(self, event):
        if self.dragging:
            delta = self.image_view.mapToScene(
                event.pos()) - self.image_view.mapToScene(self.last_cursor_pos)
            self.last_cursor_pos = event.pos()
            self.image_view.setSceneRect(
                self.image_view.sceneRect().translated(-delta))
            return

        if self.image is not None and self.healing_brush_active:
            pos = self.image_view.mapToScene(event.pos())
            x, y = int(pos.x()), int(pos.y())
            if self.isInsideImage(x, y):
                self.healImage(x, y)
                self.update()

    def mouseReleaseEventIMG(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.space_pressed:
            self.dragging = False
            return

        if self.healing_brush_active:
            self.healing_brush_active = False
            self.save_state()

    def get_zoom_level(self):
        matrix = self.image_view.transform()
        horizontal_scale = matrix.m11()
        vertical_scale = matrix.m22()
        zoom_level = (horizontal_scale * vertical_scale) * 100
        return zoom_level

    def wheelEventIMG(self, event):
        delta = event.angleDelta().y()
        if delta > 0:
            if self.zoom_level > 300000:
                return
            self.image_view.scale(1.2, 1.2)
            self.zoom_level = self.get_zoom_level()
        else:
            if self.zoom_level < 0.09:
                return

            self.image_view.scale(1 / 1.2, 1 / 1.2)
            self.zoom_level = self.get_zoom_level()

    def save_state(self):
        state = State(self)
        self.history.append(state)

    def load_last_state(self):
        if len(self.history) == 0:
            return

        state: State = self.history.pop()
        self.image = state.image
        self.radius = state.radius
        self.opacity = state.opacity
        self.sample_radius = state.sample_radius
        self.healing_brush_active = state.healing_brush_active
        self.radius_slider.setValue(self.radius)
        self.sample_slider.setValue(self.sample_radius)
        self.opacity_slider.setValue(int(self.opacity * 10))
        self.updateImageLabel()
        self.update()

    def revert_last_state():
        # take another variable and do the opposite of load_last_state
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Paint()
    window.show()
    sys.exit(app.exec())
