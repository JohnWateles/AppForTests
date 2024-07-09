import dearpygui.dearpygui as dpg


with dpg.font_registry():
    default_font = dpg.add_font(file="fonts/ProggyClean.ttf", size=13)
    big_default_font = dpg.add_font(file="fonts/ProggyClean.ttf", size=26)
    with dpg.font("fonts/Arial.ttf", 20, default_font=True) as arial:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
    # arial = dpg.add_font(file="fonts/Arial.ttf", size=15, default_font=True)
    # new_font = dpg.add_font(file="fonts/britannic-bold.ttf", size=30)
