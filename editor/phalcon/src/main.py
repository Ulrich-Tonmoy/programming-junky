import typing
from PyQt6.QtWidgets import *
from PyQt6 import QtGui, uic
from PyQt6.QtGui import *


class Editor(QMainWindow):
    def __init__(self):
        super(Editor, self).__init__()
        uic.loadUi("./src/editor.ui", self)
        self.show()

        self.setWindowTitle("Phalcon")
        self.setWindowIcon(QIcon("./src/phalcon.png"))

        self.font_size_change_action()
        self.actionOpen.triggered.connect(self.open_file)
        self.actionSave.triggered.connect(self.save_file)
        self.actionClose.triggered.connect(exit)

    def font_size_change_action(self):
        self.action10.triggered.connect(lambda: self.change_size(10))
        self.action12.triggered.connect(lambda: self.change_size(12))
        self.action14.triggered.connect(lambda: self.change_size(14))
        self.action16.triggered.connect(lambda: self.change_size(16))
        self.action18.triggered.connect(lambda: self.change_size(18))
        self.action24.triggered.connect(lambda: self.change_size(24))
        self.action28.triggered.connect(lambda: self.change_size(28))
        self.action32.triggered.connect(lambda: self.change_size(32))

    def change_size(self, size):
        self.plainTextEdit.setFont(QFont("Arial", size))

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open file", "", "Text Files (*.txt);;Python (*.py)")

        if filename != "":
            with open(filename, "r")as f:
                self.plainTextEdit.setPlainText(f.read())

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save file", "", "Text Files (*.txt);;All Files (*)")

        if filename != "":
            with open(filename, "w")as f:
                f.write(self.plainTextEdit.toPlainText())

    def closeEvent(self, event: QCloseEvent | None) -> None:
        dialog = QMessageBox()
        dialog.setText(
            "Do you want to save your data before exiting the application?")
        dialog.addButton(QPushButton("Yes"), QMessageBox.ButtonRole.YesRole)
        dialog.addButton(QPushButton("No"), QMessageBox.ButtonRole.NoRole)
        dialog.addButton(QPushButton("Cancel"),
                         QMessageBox.ButtonRole.RejectRole)
        dialog.setWindowIcon(QIcon("./src/phalcon.png"))
        dialog.setWindowTitle("Exit")
        dialog.setIcon(QMessageBox.Icon.Question)

        answer = dialog.exec()

        if answer == 0:
            self.save_file()
            event.accept()
        elif answer == 2:
            event.ignore()


def main():
    app = QApplication([])
    window = Editor()
    app.exec()


if __name__ == "__main__":
    main()
