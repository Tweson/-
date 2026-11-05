STYLE_MAIN_WINDOW = "background-color: #F8FAFC; font-family: Arial, sans-serif; font-weight: bold;"
STYLE_SIDEBAR = "background-color: #FFFFFF; border-right: 1px solid #E2E8F0;"
STYLE_LOGO = """
    font-size: 26px; 
    font-weight: 900; 
    color: #2563EB; 
    border: none; 
    padding-left: 5px;
"""
STYLE_BTN_MENU = """
    QPushButton { 
        text-align: left; padding: 12px 15px; font-size: 14px; 
        border: 1px solid #D1D5DB; border-radius: 10px; 
        color: #64748B; background-color: #FFFFFF; font-weight: bold;
    }
    QPushButton:hover { 
        background-color: #F1F5F9; border: 1px solid #94A3B8; color: #0F172A; 
    }
"""
STYLE_BTN_MENU_ACTIVE = """
    QPushButton { 
        text-align: left; padding: 12px 15px; font-size: 14px; 
        border: 1px solid #2563EB; border-radius: 10px; 
        color: #FFFFFF; background-color: #2563EB; font-weight: bold;
    }
"""
STYLE_BTN_RESTORE = """
    QPushButton { 
        text-align: left; padding: 12px 15px; font-size: 14px; 
        border: 1px solid #EF4444; border-radius: 10px; 
        color: #EF4444; background-color: #FEF2F2; font-weight: bold;
    }
    QPushButton:hover { background-color: #FEE2E2; }
"""
STYLE_AVATAR = """
    background-color: #E2E8F0; border-radius: 20px; 
    color: #64748B; font-size: 16px; font-weight: bold;
    border: 1px solid #CBD5E1;
"""
STYLE_TITLE = "font-size: 32px; font-weight: 900; color: #0F172A; border: none;"
STYLE_CARD = "background: white; border-radius: 12px; border: 1px solid #E2E8F0;"
STYLE_CARD_TITLE = "<b style='color:#0F172A; font-size:16px; border:none;'>"
STYLE_LABEL_SMALL = "color: #64748B; font-size: 12px; font-weight: bold; border: none;"
STYLE_INPUT = "padding: 10px; border: 1px solid #D1D5DB; border-radius: 8px; background: white; color: #0F172A; font-size: 14px; font-weight: bold;"
STYLE_COMBO = """
    QComboBox {
        padding: 10px 15px; border: 1px solid #D1D5DB; border-radius: 8px;
        background: white; color: #0F172A; font-size: 14px; font-weight: bold;
    }
    QComboBox:hover { border: 1px solid #2563EB; }
    QComboBox::drop-down { 
        subcontrol-origin: padding; subcontrol-position: top right; 
        width: 40px; border-left-width: 0px; 
    }
    QComboBox::down-arrow {
        image: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNiIgaGVpZ2h0PSIxNiIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiM2NDc0OEMiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj48cG9seWxpbmUgcG9pbnRzPSI2IDkgMTIgMTUgMTggOSI+PC9wb2x5bGluZT48L3N2Zz4=);
        width: 16px; height: 16px; margin-right: 10px;
    }
    QComboBox QAbstractItemView {
        background-color: white; border: 1px solid #E2E8F0; border-radius: 8px;
        selection-background-color: #F1F5F9; selection-color: #2563EB; 
        color: #0F172A; outline: none; padding: 5px;
    }
"""
STYLE_PRICE_CARD = "background: #2563EB; border-radius: 12px; border: none;"
STYLE_PRICE_TITLE = "color:#DBEAFE; font-size:14px; border:none; font-weight: bold;"
STYLE_PRICE_VALUE = "color: white; font-size: 38px; font-weight: 900; border: none;"
STYLE_BTN_GREEN = "background: #10B981; color: white; padding: 15px; border-radius: 8px; font-weight: bold; font-size: 15px; border: none;"
STYLE_BTN_BLUE = "background: #2563EB; color: white; padding: 15px; border-radius: 8px; font-weight: bold; font-size: 15px; border: none;"
STYLE_TABLE = """
    QTableWidget { 
        background: white; border: 1px solid #E2E8F0; border-radius: 12px; 
        color: #0F172A; outline: none; font-weight: bold; 
    }
    QTableWidget::item { border-bottom: 1px solid #F1F5F9; padding: 10px; }
    QHeaderView::section { 
        background: #F8FAFC; padding: 12px; border: none; 
        border-bottom: 1px solid #E2E8F0; font-weight: 900; 
        color: #64748B; font-size: 12px; 
    }
"""
STYLE_FILTER_BTN = "background: white; color: #64748B; border: 1px solid #D1D5DB; padding: 8px 15px; border-radius: 8px; font-weight: bold;"
STYLE_FILTER_BTN_ACTIVE = "background: #EFF6FF; color: #2563EB; border: 1px solid #2563EB; padding: 8px 15px; border-radius: 8px; font-weight: bold;"
STYLE_BTN_GEAR = """
    QPushButton {
        background: transparent; border: none; font-size: 20px; color: #64748B;
    }
    QPushButton:hover { color: #0F172A; }
"""