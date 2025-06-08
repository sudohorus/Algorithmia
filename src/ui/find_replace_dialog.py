from PyQt6.QtWidgets import (
    QDialog, QGridLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox, QMessageBox
)
from PyQt6.QtGui import QTextDocument, QTextCursor, QPalette
from ..utils.config import Config

class FindReplaceDialog(QDialog):
    """ diálogo de busca e substituição """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.editor = parent.text_editor if parent else None
        self.parent_window = parent
        self.setup_ui()
        self.last_search = ""
        self.case_sensitive = False
        
        # aplica o tema inicial
        if parent and hasattr(parent, 'current_theme'):
            self.apply_theme(parent.current_theme)

    def setup_ui(self):
        self.setWindowTitle("Find and Replace")
        self.setModal(False)
        
        layout = QGridLayout()
        self.setLayout(layout)
        
        # campo de busca
        self.find_label = QLabel("Find:")
        self.find_edit = QLineEdit()
        layout.addWidget(self.find_label, 0, 0)
        layout.addWidget(self.find_edit, 0, 1, 1, 2)
        
        # campo de substituição
        self.replace_label = QLabel("Replace with:")
        self.replace_edit = QLineEdit()
        layout.addWidget(self.replace_label, 1, 0)
        layout.addWidget(self.replace_edit, 1, 1, 1, 2)
        
        # opções
        self.case_check = QCheckBox("Case sensitive")
        layout.addWidget(self.case_check, 2, 0, 1, 3)
        
        # botões
        self.find_button = QPushButton("Find Next")
        self.replace_button = QPushButton("Replace")
        self.replace_all_button = QPushButton("Replace All")
        
        layout.addWidget(self.find_button, 3, 0)
        layout.addWidget(self.replace_button, 3, 1)
        layout.addWidget(self.replace_all_button, 3, 2)
        
        # conecta sinais
        self.find_button.clicked.connect(self.find_next)
        self.replace_button.clicked.connect(self.replace)
        self.replace_all_button.clicked.connect(self.replace_all)
        self.case_check.stateChanged.connect(self.toggle_case_sensitive)
        
        self.find_edit.returnPressed.connect(self.find_next)
        
    def apply_theme(self, theme_name):
        """ aplica o tema ao diálogo """
        if not self.parent_window:
            return
            
        theme = (Config.get_light_theme() if theme_name == "light" 
                else Config.get_dark_theme())
        
        # aplica cores ao diálogo
        dialog_palette = self.palette()
        dialog_palette.setColor(QPalette.ColorRole.Window, theme['window_bg'])
        dialog_palette.setColor(QPalette.ColorRole.WindowText, theme['menu_text'])
        dialog_palette.setColor(QPalette.ColorRole.ButtonText, theme['menu_text'])
        dialog_palette.setColor(QPalette.ColorRole.Button, theme['menu_bg'])
        self.setPalette(dialog_palette)
        
        # aplica cores aos widgets
        for widget in [self.find_label, self.replace_label, self.case_check]:
            widget_palette = widget.palette()
            widget_palette.setColor(QPalette.ColorRole.WindowText, theme['menu_text'])
            widget.setPalette(widget_palette)
        
        # aplica cores aos campos de texto
        for widget in [self.find_edit, self.replace_edit]:
            widget_palette = widget.palette()
            widget_palette.setColor(QPalette.ColorRole.Base, theme['editor_bg'])
            widget_palette.setColor(QPalette.ColorRole.Text, theme['editor_text'])
            widget.setPalette(widget_palette)
        
        # aplica cores aos botões
        for widget in [self.find_button, self.replace_button, self.replace_all_button]:
            button_palette = widget.palette()
            button_palette.setColor(QPalette.ColorRole.Button, theme['menu_bg'])
            button_palette.setColor(QPalette.ColorRole.ButtonText, theme['menu_text'])
            button_palette.setColor(QPalette.ColorRole.Window, theme['menu_bg'])  # necessário para alguns estilos
            button_palette.setColor(QPalette.ColorRole.WindowText, theme['menu_text'])  # necessário para alguns estilos
            widget.setPalette(button_palette)
            widget.update()  # força atualização do botão

    def toggle_case_sensitive(self, state):
        self.case_sensitive = bool(state)
        
    def find_next(self):
        if not self.editor:
            return
            
        text = self.find_edit.text()
        if not text:
            return
            
        # inicia busca a partir da posição atual do cursor
        cursor = self.editor.textCursor()
        
        # se a busca mudou, começa do início
        if text != self.last_search:
            cursor.movePosition(QTextCursor.MoveOperation.Start)
            self.editor.setTextCursor(cursor)
            self.last_search = text
            
        # configura as opções de busca
        options = QTextDocument.FindFlag.FindCaseSensitively if self.case_sensitive else QTextDocument.FindFlag(0)
        
        # realiza a busca
        found = self.editor.find(text, options)
        
        if not found:
            # se não encontrou, tenta buscar do início
            cursor.movePosition(QTextCursor.MoveOperation.Start)
            self.editor.setTextCursor(cursor)
            found = self.editor.find(text, options)
            
    def replace(self):
        if not self.editor:
            return
            
        # substitui a seleção atual
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            cursor.insertText(self.replace_edit.text())
            
        # busca a próxima ocorrência
        self.find_next()
        
    def replace_all(self):
        if not self.editor:
            return
            
        text = self.find_edit.text()
        if not text:
            return
            
        replace_text = self.replace_edit.text()
        count = 0
        
        # volta para o início do documento
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Start)
        self.editor.setTextCursor(cursor)
        
        # configura as opções de busca
        options = QTextDocument.FindFlag.FindCaseSensitively if self.case_sensitive else QTextDocument.FindFlag(0)
        
        # substitui todas as ocorrências
        while self.editor.find(text, options):
            cursor = self.editor.textCursor()
            cursor.insertText(replace_text)
            count += 1
            
        QMessageBox.information(self, "Replace All", f"Replaced {count} occurrence(s)!") 