import sys
from PyQt6.QtWidgets import *

from editor_wnd import NodeEditorWnd

if __name__ == "__main__":
    app = QApplication(sys.argv)

    wnd = NodeEditorWnd()

    sys.exit(app.exec())
