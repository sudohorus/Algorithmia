from PyQt6.QtGui import QPalette
from ..utils.config import Config

class ThemeManager:
    """ gerenciador de temas """
    def __init__(self):
        self.current_theme = "light"

    def apply_theme(self, theme_name, window):
        """ aplica o tema em toda a interface """
        if theme_name == self.current_theme:
            return

        self.current_theme = theme_name
        theme = Config.get_light_theme() if theme_name == "light" else Config.get_dark_theme()

        # aplica as cores do tema no editor
        window.text_editor.set_theme_colors(
            bg_color=theme['line_number_bg'],
            text_color=theme['line_number_text'],
            current_color=theme['current_line_highlight'],
            current_number_color=theme['line_number_current']
        )
        
        # atualiza cores do editor
        editor_palette = window.text_editor.palette()
        editor_palette.setColor(QPalette.ColorRole.Base, theme['editor_bg'])
        editor_palette.setColor(QPalette.ColorRole.Text, theme['editor_text'])
        editor_palette.setColor(QPalette.ColorRole.Highlight, theme['selection_bg'])
        editor_palette.setColor(QPalette.ColorRole.HighlightedText, theme['selection_text'])
        window.text_editor.setPalette(editor_palette)

        # atualiza cores da janela principal
        window_palette = window.palette()
        window_palette.setColor(QPalette.ColorRole.Window, theme['window_bg'])
        window_palette.setColor(QPalette.ColorRole.WindowText, theme['menu_text'])
        window_palette.setColor(QPalette.ColorRole.ButtonText, theme['menu_text'])
        window_palette.setColor(QPalette.ColorRole.Button, theme['menu_bg'])
        window.setPalette(window_palette)

        # atualiza cores do menu
        menu_palette = window.menuBar().palette()
        menu_palette.setColor(QPalette.ColorRole.Window, theme['menu_bg'])
        menu_palette.setColor(QPalette.ColorRole.WindowText, theme['menu_text'])
        menu_palette.setColor(QPalette.ColorRole.ButtonText, theme['menu_text'])
        menu_palette.setColor(QPalette.ColorRole.Button, theme['menu_bg'])
        window.menuBar().setPalette(menu_palette)

        # atualiza cores da barra de status
        status_palette = window.status_bar.palette()
        status_palette.setColor(QPalette.ColorRole.Window, theme['status_bar_bg'])
        status_palette.setColor(QPalette.ColorRole.WindowText, theme['status_bar_text'])
        window.status_bar.setPalette(status_palette)
        
        # atualiza cores dos labels na barra de status
        for widget in [window.line_col_label, window.char_count_label, window.encoding_label]:
            widget_palette = widget.palette()
            widget_palette.setColor(QPalette.ColorRole.WindowText, theme['status_bar_text'])
            widget.setPalette(widget_palette)

        # atualiza o diálogo de busca e substituição se estiver aberto
        if window.find_replace_dialog:
            window.find_replace_dialog.apply_theme(theme_name)

        # força atualização da interface
        window.update() 