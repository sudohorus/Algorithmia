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
    AUTO_COMPLETE_PAIRS = True
    
    # janela
    DEFAULT_WIDTH = 1000
    DEFAULT_HEIGHT = 700
    MIN_WIDTH = 800
    MIN_HEIGHT = 600

    # cores - tema claro
    LIGHT_THEME = {
        'line_number_bg': QColor(245, 245, 245),
        'line_number_text': QColor(100, 100, 100),
        'line_number_current': QColor(50, 50, 50),
        'current_line_highlight': QColor(255, 255, 224, 80),
        'editor_bg': QColor(255, 255, 255),
        'editor_text': QColor(0, 0, 0),
        'window_bg': QColor(240, 240, 240),
        'menu_bg': QColor(240, 240, 240),
        'menu_text': QColor(0, 0, 0),
        'status_bar_bg': QColor(240, 240, 240),
        'status_bar_text': QColor(0, 0, 0),
        'selection_bg': QColor(51, 153, 255),
        'selection_text': QColor(255, 255, 255)
    }

    # cores - tema escuro
    DARK_THEME = {
        'line_number_bg': QColor(40, 40, 40),
        'line_number_text': QColor(120, 120, 120),
        'line_number_current': QColor(200, 200, 200),
        'current_line_highlight': QColor(60, 60, 60),
        'editor_bg': QColor(30, 30, 30),
        'editor_text': QColor(220, 220, 220),
        'window_bg': QColor(45, 45, 45),
        'menu_bg': QColor(45, 45, 45),
        'menu_text': QColor(220, 220, 220),
        'status_bar_bg': QColor(35, 35, 35),
        'status_bar_text': QColor(200, 200, 200),
        'selection_bg': QColor(70, 130, 180),
        'selection_text': QColor(255, 255, 255)
    }

    @classmethod
    def get_light_theme(cls):
        return cls.LIGHT_THEME
    
    @classmethod
    def get_dark_theme(cls):
        return cls.DARK_THEME