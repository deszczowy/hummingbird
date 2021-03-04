from hb_enums import (EditorTheme)
from style import (dark, light)

class Stylist():

    def get_style_sheet(self, theme):
        if theme == EditorTheme.Dark:
            return dark.stylesheet_dark
        else:
            return light.stylesheet_light