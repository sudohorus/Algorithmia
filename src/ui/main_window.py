from PyQt6.QtWidgets import (
    QMainWindow, QTextEdit, QVBoxLayout,
    QWidget, QMenuBar, QStatusBar, QToolBar
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QAction, QIcon

class MainWindow(QMainWindow):
    """ janela principal do editor """
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_editor()
        self.create_menu_bar()
        self.create_status_bar()

    def init_ui(self):
        """ inicializa a interface da janela """
        self.setWindowTitle("Algorithmia - No title")
        self.setGeometry(100, 100, 1000, 700)
        self.setMinimumSize(QSize(800, 600))

        # widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # layout principal
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

    def setup_editor(self):
        """ configura o campo de texto """
        self.text_editor = QTextEdit()

        # configuracao da fonte
        font = QFont("Consolas", 11)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.text_editor.setFont(font)

        self.text_editor.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.text_editor.setAcceptRichText(False)

        self.centralWidget().layout().addWidget(self.text_editor)

    def create_menu_bar(self):
        """ cria a barra de menu básica """
        menubar = self.menuBar()

        # menu arquivo
        file_menu = menubar.addMenu("&File")

        new_action = QAction("&New", self)
        new_action.setShortcut("Ctrl+N")
        file_menu.addAction(new_action)

        open_action = QAction("&Open", self)
        open_action.setShortcut("Ctrl+O")
        file_menu.addAction(open_action)
        
        save_action = QAction("&Save", self)
        save_action.setShortcut("Ctrl+S")
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()

        exit_action = QAction("&Exit", self)
        exit_action.setShortcut("Alt+F4")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # menu editor
        edit_menu = menubar.addMenu("&Edit")
        
        undo_action = QAction("&Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("&Redo", self)
        redo_action.setShortcut("Ctrl+Y")
        edit_menu.addAction(redo_action)
    
    def create_status_bar(self):
        """ cria a barra de status """
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.status_bar.showMessage("Ready", 2000)


