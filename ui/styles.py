THEME_LIGHT = {
    "bg": "#F8FAFC", "sidebar": "#FFFFFF", "card": "#FFFFFF",
    "border": "#E2E8F0", "text_main": "#0F172A", "text_sub": "#64748B",
    "input_bg": "#FFFFFF", "input_border": "#D1D5DB", "table_header": "#F8FAFC",
    "stats_bg": "#FFFFFF", "btn_menu_text": "#64748B", "btn_menu_hover": "#F1F5F9"
}

THEME_DARK = {
    "bg": "#0F172A", "sidebar": "#1E293B", "card": "#1E293B",
    "border": "#334155", "text_main": "#F8FAFC", "text_sub": "#94A3B8",
    "input_bg": "#0F172A", "input_border": "#334155", "table_header": "#1E293B",
    "stats_bg": "#1E293B", "btn_menu_text": "#94A3B8", "btn_menu_hover": "#334155"
}

CURRENT_THEME = THEME_LIGHT

def set_theme(theme_name):
    global CURRENT_THEME
    if theme_name == "dark":
        CURRENT_THEME = THEME_DARK
    else:
        CURRENT_THEME = THEME_LIGHT

def get_main_style():
    return f"background-color: {CURRENT_THEME['bg']}; font-family: Arial, sans-serif; font-weight: bold;"

def get_sidebar_style():
    return f"background-color: {CURRENT_THEME['sidebar']}; border-right: 1px solid {CURRENT_THEME['border']};"

def get_card_style():
    return f"""
        background-color: {CURRENT_THEME['card']}; 
        border-radius: 12px; 
        border: 1px solid {CURRENT_THEME['border']};
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
    """

def get_text_main():
    return f"color: {CURRENT_THEME['text_main']}; border: none;"

def get_text_sub():
    return f"color: {CURRENT_THEME['text_sub']}; border: none;"

def get_input_style():
    return f"padding: 10px; border: 1px solid {CURRENT_THEME['input_border']}; border-radius: 8px; background: {CURRENT_THEME['input_bg']}; color: {CURRENT_THEME['text_main']}; font-weight: bold;"

def get_table_style():
    return f"""
        QTableWidget {{ 
            background: {CURRENT_THEME['card']}; border: 1px solid {CURRENT_THEME['border']}; 
            border-radius: 12px; color: {CURRENT_THEME['text_main']}; outline: none; font-weight: bold; 
        }}
        QTableWidget::item {{ border-bottom: 1px solid {CURRENT_THEME['border']}; padding: 10px; background: {CURRENT_THEME['card']}; }}
        QTableWidget::item:selected {{ background: {CURRENT_THEME['btn_menu_hover']}; color: {CURRENT_THEME['text_main']}; }}
        QHeaderView::section {{ background: {CURRENT_THEME['table_header']}; padding: 12px; border: none; border-bottom: 1px solid {CURRENT_THEME['border']}; font-weight: 900; color: {CURRENT_THEME['text_sub']}; font-size: 12px; }}
    """

def get_stats_card_style():
    return f"""
        background-color: {CURRENT_THEME['stats_bg']}; 
        border-radius: 12px; 
        border: 1px solid {CURRENT_THEME['border']};
    """

def get_btn_menu_style():
    return f"""
        QPushButton {{ 
            text-align: left; padding: 12px 15px; font-size: 14px; 
            border: 1px solid transparent; border-radius: 10px; 
            color: {CURRENT_THEME['btn_menu_text']}; background-color: transparent; font-weight: bold;
            outline: none;
        }}
        QPushButton:hover {{ background-color: {CURRENT_THEME['btn_menu_hover']}; color: {CURRENT_THEME['text_main']}; }}
    """

def get_btn_menu_active_style():
    return """
        QPushButton { 
            text-align: left; padding: 12px 15px; font-size: 14px; 
            border: 1px solid #2563EB; border-radius: 10px; 
            color: #FFFFFF; background-color: #2563EB; font-weight: bold;
            outline: none;
        }
    """

def get_auth_style():
    return f"background-color: {CURRENT_THEME['bg']}; font-family: Arial;"

STYLE_BTN_GREEN = "background: #10B981; color: white; padding: 15px; border-radius: 8px; font-weight: bold; font-size: 15px; border: none;"
STYLE_BTN_BLUE = "background: #2563EB; color: white; padding: 15px; border-radius: 8px; font-weight: bold; font-size: 15px; border: none;"
STYLE_FILTER_BTN = "background: transparent; color: #64748B; border: 1px solid #D1D5DB; padding: 8px 15px; border-radius: 8px; font-weight: bold;"
STYLE_FILTER_BTN_ACTIVE = "background: #EFF6FF; color: #2563EB; border: 1px solid #2563EB; padding: 8px 15px; border-radius: 8px; font-weight: bold;"
STYLE_AVATAR = "background-color: #E2E8F0; border-radius: 20px; color: #64748B; font-size: 16px; font-weight: bold; border: 1px solid #CBD5E1;"