from PyQt6.QtWidgets import QWidget, QTextEdit
from PyQt6.QtCore import Qt, QRect, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QTextFormat, QFont, QPaintEvent, QResizeEvent

class LineNumberArea(QWidget):
    """ widget para exibir a numeração de linhas """
    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor
        
    def sizeHint(self):
        return self.code_editor.line_number_area_width()
    
    def paintEvent(self, event: QPaintEvent):
        self.code_editor.line_number_area_paint_event(event)

class CodeEditor(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.line_number_area = LineNumberArea(self)
        
        self.setup_appearance()
        self.setup_editor_behavior()
        self.connect_update_signals()
        
        self.line_number_bg_color = QColor(245, 245, 245)
        self.line_number_text_color = QColor(100, 100, 100)
        self.current_line_color = QColor(255, 255, 224, 80)
        self.current_line_number_color = QColor(50, 50, 50)
        
        self.show_line_numbers = True
        self.highlight_current_line = True
        
        self.update_line_number_area_width()
        self.highlight_current_line_func()
        
    def setup_appearance(self):
        """ configura a aparência do editor """
        font = QFont("Consolas", 11)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.setFont(font)
        
        self.setAcceptRichText(False)
        
        # configuração de tabs (4 espaços)
        tab_width = 4 * self.fontMetrics().horizontalAdvance(' ')
        self.setTabStopDistance(tab_width)
        
    def setup_editor_behavior(self):
        """ configura comportamentos do editor """
        self.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        
        self.setCursorWidth(2)
        
    def connect_update_signals(self):
        """ conecta sinais para atualização da interface """
        self.textChanged.connect(self.update_line_number_area_width)
        self.cursorPositionChanged.connect(self.highlight_current_line_func)
        self.cursorPositionChanged.connect(self.update_line_number_area_full)

        self.verticalScrollBar().valueChanged.connect(self.update_line_number_area_full)
        
    def line_number_area_width(self):
        """ calcula largura necessária para área de numeração """
        if not self.show_line_numbers:
            return 0
            
        digits = len(str(max(1, self.document().blockCount())))
        
        space = 10 + self.fontMetrics().horizontalAdvance('9') * (digits + 1)
        return space
    
    def update_line_number_area_width(self):
        """ atualiza a largura da área de numeração """
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)
    
    def update_line_number_area_full(self):
        """ atualiza toda a área de numeração """
        self.line_number_area.update()
        
    def resizeEvent(self, event: QResizeEvent):
        """ redimensiona área de numeração junto com editor """
        super().resizeEvent(event)
        
        cr = self.contentsRect()
        self.line_number_area.setGeometry(
            QRect(cr.left(), cr.top(), 
                  self.line_number_area_width(), cr.height())
        )
    
    def highlight_current_line_func(self):
        """ destaca linha atual """
        if not self.highlight_current_line:
            self.setExtraSelections([])
            return
            
        extra_selections = []
        
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(self.current_line_color)
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        
        self.setExtraSelections(extra_selections)
    
    def get_first_visible_block(self):
        """ encontra o primeiro bloco visível na área de visualização """
        cursor_at_top = self.cursorForPosition(self.viewport().rect().topLeft())
        block = cursor_at_top.block()
        return block
    
    def line_number_area_paint_event(self, event: QPaintEvent):
        """ desenha numeração de linhas """
        if not self.show_line_numbers:
            return
            
        painter = QPainter(self.line_number_area)
        
        painter.fillRect(event.rect(), self.line_number_bg_color)
        
        font_height = self.fontMetrics().height()
        
        viewport_rect = self.viewport().rect()
        
        first_visible_cursor = self.cursorForPosition(viewport_rect.topLeft())
        last_visible_cursor = self.cursorForPosition(viewport_rect.bottomRight())
        
        first_line = first_visible_cursor.blockNumber()
        last_line = last_visible_cursor.blockNumber()
        
        current_line = self.textCursor().blockNumber()
        
        for line_number in range(first_line, last_line + 1):
            block = self.document().findBlockByLineNumber(line_number)
            if not block.isValid():
                continue
                
            cursor = self.textCursor()
            cursor.setPosition(block.position())
            rect = self.cursorRect(cursor)
            y_pos = rect.top()
            
            if y_pos < event.rect().top() - font_height or y_pos > event.rect().bottom():
                continue
            
            display_number = str(line_number + 1)
            
            if line_number == current_line:
                painter.setPen(self.current_line_number_color)
                font = painter.font()
                font.setBold(True)
                painter.setFont(font)
            else:
                painter.setPen(self.line_number_text_color)
                font = painter.font()
                font.setBold(False)
                painter.setFont(font)
            
            painter.drawText(0, y_pos, 
                           self.line_number_area.width() - 5, 
                           font_height,
                           Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, 
                           display_number)
    
    def toggle_line_numbers(self):
        """ alterna exibição da numeração """
        self.show_line_numbers = not self.show_line_numbers
        self.update_line_number_area_width()
        self.line_number_area.setVisible(self.show_line_numbers)
        
    def toggle_current_line_highlight(self):
        """ alterna destaque da linha atual """
        self.highlight_current_line = not self.highlight_current_line
        self.highlight_current_line_func()
    
    def set_theme_colors(self, bg_color=None, text_color=None, 
                        current_color=None, current_number_color=None):
        """ define cores do tema """
        if bg_color:
            self.line_number_bg_color = bg_color
        if text_color:
            self.line_number_text_color = text_color
        if current_color:
            self.current_line_color = current_color
        if current_number_color:
            self.current_line_number_color = current_number_color
        
        self.line_number_area.update()
        self.highlight_current_line_func()
    
    def get_current_line_number(self):
        """ retorna número da linha atual (1-indexed) """
        return self.textCursor().blockNumber() + 1
    
    def get_current_column_number(self):
        """ retorna número da coluna atual (1-indexed) """
        return self.textCursor().columnNumber() + 1
    
    def go_to_line(self, line_number):
        """ move cursor para linha específica """
        if line_number < 1:
            line_number = 1
        
        block = self.document().findBlockByLineNumber(line_number - 1)
        if block.isValid():
            cursor = self.textCursor()
            cursor.setPosition(block.position())
            self.setTextCursor(cursor)
            self.ensureCursorVisible()
            return True
        return False