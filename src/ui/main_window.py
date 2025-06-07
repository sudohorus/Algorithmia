from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QMenuBar, 
    QStatusBar, QFileDialog, QMessageBox, QLabel,
    QCheckBox, QHBoxLayout
)
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QFont, QAction, QIcon
from ..core.editor import EditorCore
from ..utils.config import Config
from .code_editor import CodeEditor
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
        
        # Timer para atualizar status
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status_info)
        self.status_timer.start(100)

    def init_ui(self):
        """ inicializa a interface da janela """
        self.setWindowTitle("Algorithmia - No title")
        self.setGeometry(100, 100, Config.DEFAULT_WIDTH, Config.DEFAULT_HEIGHT)
        self.setMinimumSize(QSize(Config.MIN_WIDTH, Config.MIN_HEIGHT))

        # widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # layout principal
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

    def setup_editor(self):
        """ configura o editor de código com numeração """
        self.text_editor = CodeEditor()
        
        font = QFont(Config.DEFAULT_FONT_FAMILY, Config.DEFAULT_FONT_SIZE)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.text_editor.setFont(font)
        
        self.text_editor.show_line_numbers = Config.SHOW_LINE_NUMBERS
        self.text_editor.highlight_current_line = Config.HIGHLIGHT_CURRENT_LINE
        self.text_editor.setCursorWidth(Config.CURSOR_WIDTH)
        
        theme = Config.get_light_theme()
        self.text_editor.set_theme_colors(
            bg_color=theme['line_number_bg'],
            text_color=theme['line_number_text'],
            current_color=theme['current_line_highlight'],
            current_number_color=theme['line_number_current']
        )
        
        if Config.WORD_WRAP:
            self.text_editor.setLineWrapMode(self.text_editor.LineWrapMode.WidgetWidth)
        else:
            self.text_editor.setLineWrapMode(self.text_editor.LineWrapMode.NoWrap)

        self.centralWidget().layout().addWidget(self.text_editor)

    def create_menu_bar(self):
        """ cria a barra de menu """
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
        
        edit_menu.addSeparator()
        
        self.goto_line_action = QAction("&Go to Line...", self)
        self.goto_line_action.setShortcut("Ctrl+G")
        edit_menu.addAction(self.goto_line_action)
        
        # menu view
        view_menu = menubar.addMenu("&View")
        
        self.toggle_line_numbers_action = QAction("Show &Line Numbers", self)
        self.toggle_line_numbers_action.setCheckable(True)
        self.toggle_line_numbers_action.setChecked(Config.SHOW_LINE_NUMBERS)
        view_menu.addAction(self.toggle_line_numbers_action)
        
        self.toggle_current_line_action = QAction("&Highlight Current Line", self)
        self.toggle_current_line_action.setCheckable(True)
        self.toggle_current_line_action.setChecked(Config.HIGHLIGHT_CURRENT_LINE)
        view_menu.addAction(self.toggle_current_line_action)
        
        view_menu.addSeparator()
        
        self.toggle_word_wrap_action = QAction("&Word Wrap", self)
        self.toggle_word_wrap_action.setCheckable(True)
        self.toggle_word_wrap_action.setChecked(Config.WORD_WRAP)
        view_menu.addAction(self.toggle_word_wrap_action)
    
    def create_status_bar(self):
        """ cria a barra de status com informações detalhadas """
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.line_col_label = QLabel("Line 1, Col 1")
        self.line_col_label.setMinimumWidth(100)
        self.status_bar.addPermanentWidget(self.line_col_label)
        
        self.char_count_label = QLabel("0 chars")
        self.char_count_label.setMinimumWidth(80)
        self.status_bar.addPermanentWidget(self.char_count_label)
        
        self.encoding_label = QLabel("UTF-8")
        self.encoding_label.setMinimumWidth(60)
        self.status_bar.addPermanentWidget(self.encoding_label)

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
        self.goto_line_action.triggered.connect(self.go_to_line_dialog)

        # ações de visualização
        self.toggle_line_numbers_action.triggered.connect(self.toggle_line_numbers)
        self.toggle_current_line_action.triggered.connect(self.toggle_current_line_highlight)
        self.toggle_word_wrap_action.triggered.connect(self.toggle_word_wrap)

        # detecta mudanças no texto
        self.text_editor.textChanged.connect(self.on_text_changed)

    def update_status_info(self):
        """ atualiza informações na barra de status """
        line = self.text_editor.get_current_line_number()
        col = self.text_editor.get_current_column_number()
        self.line_col_label.setText(f"Line {line}, Col {col}")
        
        # contagem de caracteres
        char_count = len(self.text_editor.toPlainText())
        self.char_count_label.setText(f"{char_count} chars")

    def new_file(self):
        """ cria um novo arquivo """
        if self.check_unsaved_changes():
            self.text_editor.clear()
            self.editor_core.new_file()
            self.update_window_title()
            self.status_bar.showMessage("New file created", 2000)

    def open_file(self):
        """ abrir arquivo existente """
        if not self.check_unsaved_changes():
            return
            
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "All Files (*.*);;Python Files (*.py);;Text Files (*.txt)"
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
                self.status_bar.showMessage(f"File saved: {os.path.basename(self.editor_core.current_file)}", 2000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error saving file:\n{str(e)}")

    def save_as_file(self):
        """ salvar arquivo como """
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save As",
            "",
            "All Files (*.*);;Python Files (*.py);;Text Files (*.txt)"
        )

        if file_path:
            try:
                content = self.text_editor.toPlainText()
                self.editor_core.save_file(content, file_path)
                self.update_window_title()
                self.status_bar.showMessage(f"File saved: {os.path.basename(file_path)}", 2000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error saving file:\n{str(e)}")

    def go_to_line_dialog(self):
        """ dialog para ir para linha específica """
        from PyQt6.QtWidgets import QInputDialog
        
        current_line = self.text_editor.get_current_line_number()
        total_lines = self.text_editor.blockCount()
        
        line_number, ok = QInputDialog.getInt(
            self, "Go to Line", 
            f"Line number (1-{total_lines}):", 
            current_line, 1, total_lines
        )
        
        if ok:
            if self.text_editor.go_to_line(line_number):
                self.status_bar.showMessage(f"Moved to line {line_number}", 2000)

    def toggle_line_numbers(self):
        """ alterna numeração de linhas """
        self.text_editor.toggle_line_numbers()
        self.status_bar.showMessage("Line numbers toggled", 1000)

    def toggle_current_line_highlight(self):
        """ alterna destaque da linha atual """
        self.text_editor.toggle_current_line_highlight()
        self.status_bar.showMessage("Current line highlight toggled", 1000)

    def toggle_word_wrap(self):
        """ alterna quebra de linha """
        if self.toggle_word_wrap_action.isChecked():
            self.text_editor.setLineWrapMode(self.text_editor.LineWrapMode.WidgetWidth)
        else:
            self.text_editor.setLineWrapMode(self.text_editor.LineWrapMode.NoWrap)
        self.status_bar.showMessage("Word wrap toggled", 1000)
                
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