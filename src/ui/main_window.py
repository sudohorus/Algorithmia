from PyQt6.QtWidgets import (
    QMainWindow, QTextEdit, QVBoxLayout,
    QWidget, QMenuBar, QStatusBar, QToolBar,
    QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QAction, QIcon
from ..core.editor import EditorCore
import os

class MainWindow(QMainWindow):
    """ janela principal do editor """
    def __init__(self):
        super().__init__()
        self.editor_core = EditorCore()
        self.init_ui()
        self.setup_editor()
        self.create_menu_bar()
        self.create_status_bar()
        self.connect_signals()

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

        self.new_action = QAction("&New", self)
        self.new_action.setShortcut("Ctrl+N")
        file_menu.addAction(self.new_action)

        self.open_action = QAction("&Open", self)
        self.open_action.setShortcut("Ctrl+O")
        file_menu.addAction(self.open_action)
        
        self.save_action = QAction("&Save", self)
        self.save_action.setShortcut("Ctrl+S")
        file_menu.addAction(self.save_action)

        self.save_as_action = QAction("Save &As...", self)
        self.save_as_action.setShortcut("Ctrl+Shift+S")
        file_menu.addAction(self.save_as_action)
        
        file_menu.addSeparator()

        exit_action = QAction("&Exit", self)
        exit_action.setShortcut("Alt+F4")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # menu editor
        edit_menu = menubar.addMenu("&Edit")
        
        self.undo_action = QAction("&Undo", self)
        self.undo_action.setShortcut("Ctrl+Z")
        edit_menu.addAction(self.undo_action)
        
        self.redo_action = QAction("&Redo", self)
        self.redo_action.setShortcut("Ctrl+Y")
        edit_menu.addAction(self.redo_action)
    
    def create_status_bar(self):
        """ cria a barra de status """
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.status_bar.showMessage("Ready", 2000)

    def connect_signals(self):
        # ações de arquivos
        self.new_action.triggered.connect(self.new_file)
        self.open_action.triggered.connect(self.open_file)
        self.save_action.triggered.connect(self.save_file)
        self.save_as_action.triggered.connect(self.save_as_file)

        # ações de edição
        self.undo_action.triggered.connect(self.text_editor.undo)
        self.redo_action.triggered.connect(self.text_editor.redo)

        # detecta mudanças no texto
        self.text_editor.textChanged.connect(self.on_text_changed)

    def new_file(self):
        """ cria um novo arquivo """
        if self.check_unsaved_changes():
            self.text_editor.clear()
            self.editor_core.new_file()
            self.update_window_title()
            self.status_bar.showMessage("new file created", 2000)

    def open_file(self):
        """ abrir arquivo existente """
        if not self.check_unsaved_changes():
            return
            
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "All Files (*.*)"
        )

        if file_path:
            try:
                content = self.editor_core.open_file(file_path)
                self.text_editor.setPlainText(content)
                self.update_window_title()
                self.status_bar.showMessage(f"File opened: {os.path.basename(file_path)}", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error opening file:\n{str(e)}")

    def save_file(self):
        """ salvar arquivo """
        if self.editor_core.current_file is None:
            self.save_as_file()
        else:
            try:
                content = self.text_editor.toPlainText()
                self.editor_core.save_file(content)
                self.update_window_title()
                self.status_bar.showMessage(f"saved file: {os.path.basename(self.editor_core.current_file)}", 2000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error saving file:\n{str(e)}")

    def save_as_file(self):
        """ salvar arquivo como """
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save As",
            "",
            "All Files (*.*)"
        )

        if file_path:
            try:
                content = self.text_editor.toPlainText()
                self.editor_core.save_file(content, file_path)
                self.update_window_title()
                self.status_bar.showMessage(f"File saved: {os.path.basename(file_path)}", 2000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error saving file:\n{str(e)}")
                
    def on_text_changed(self):
        """ quando modificar texto """
        if not self.editor_core.is_modified:
            self.editor_core.is_modified = True
            self.update_window_title()

    def update_window_title(self):
        """ atualiza o título da janela """
        title = "Algorithmia - "

        if self.editor_core.current_file:
            title += os.path.basename(self.editor_core.current_file)
        else:
            title += "No title"
            
        if self.editor_core.is_modified:
            title += " *"
            
        self.setWindowTitle(title)

    def check_unsaved_changes(self):
        """ verifica se há mudanças não salvas """
        if not self.editor_core.is_modified:
            return True
            
        reply = QMessageBox.question(
            self,
            "Unsaved Changes",
            "There are unsaved changes. Do you want to save before continuing?",
            QMessageBox.StandardButton.Save | 
            QMessageBox.StandardButton.Discard | 
            QMessageBox.StandardButton.Cancel
        )
        
        if reply == QMessageBox.StandardButton.Save:
            self.save_file()
            return not self.editor_core.is_modified 
        elif reply == QMessageBox.StandardButton.Discard:
            return True
        else: 
            return False
    
    def closeEvent(self, event):
        """ chamado quando a janela está sendo fechada """
        if self.check_unsaved_changes():
            event.accept()
        else:
            event.ignore()

