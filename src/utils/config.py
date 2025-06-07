from PyQt6.QtGui import QColor
class Config:
    """ configurações globais do editor """
    
    # aparência
    DEFAULT_FONT_FAMILY = "Consolas"
    DEFAULT_FONT_SIZE = 11
    
    # editor
    DEFAULT_TAB_SIZE = 4
    SHOW_LINE_NUMBERS = True
    WORD_WRAP = False
    HIGHLIGHT_CURRENT_LINE = True
    CURSOR_WIDTH = 2
    
    # janela
    DEFAULT_WIDTH = 1000
    DEFAULT_HEIGHT = 700
    MIN_WIDTH = 800
    MIN_HEIGHT = 600

    # cores - linhas
    LINE_NUMBER_BG_COLOR = QColor(245, 245, 245)
    LINE_NUMBER_TEXT_COLOR = QColor(100, 100, 100)
    LINE_NUMBER_CURRENT_COLOR = QColor(50, 50, 50)

    # cores - editor
    CURRENT_LINE_HIGHLIGHT_COLOR = QColor(255, 255, 224, 80)
    EDITOR_BG_COLOR = QColor(255, 255, 255)
    EDITOR_TEXT_COLOR = QColor(0, 0, 0)

    # tema escuro
    DARK_THEME = {
        'line_number_bg': QColor(40, 40, 40),
        'line_number_text': QColor(120, 120, 120),
        'line_number_current': QColor(200, 200, 200),
        'current_line_highlight': QColor(60, 60, 60, 100),
        'editor_bg': QColor(30, 30, 30),
        'editor_text': QColor(220, 220, 220)
    }

    @classmethod
    def get_light_theme(cls):
        return {
            'line_number_bg': cls.LINE_NUMBER_BG_COLOR,
            'line_number_text': cls.LINE_NUMBER_TEXT_COLOR,
            'line_number_current': cls.LINE_NUMBER_CURRENT_COLOR,
            'current_line_highlight': cls.CURRENT_LINE_HIGHLIGHT_COLOR,
            'editor_bg': cls.EDITOR_BG_COLOR,
            'editor_text': cls.EDITOR_TEXT_COLOR
        }
    
    @classmethod
    def get_dark_theme(cls):
        return cls.DARK_THEME