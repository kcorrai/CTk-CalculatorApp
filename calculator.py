import darkdetect
import customtkinter as ctk
from settings import *
from buttons import Button, ImageButton
from PIL import Image
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

class Calculator(ctk.CTk):
    def __init__(self, is_dark):
        super().__init__(fg_color=(WHITE, BLACK))
        ctk.set_appearance_mode(f"dark" if is_dark else "light")
        self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}')
        self.resizable(False, False)
        self.title('')
        self.title_bar_color(is_dark)

        #grid layout
        self.rowconfigure(list(range(MAIN_ROWS)), weight=1, uniform='a')
        self.columnconfigure(list(range(MAIN_COLUMNS)), weight=1, uniform='a')
        
        #data
        self.result_string = ctk.StringVar(value='0')
        self.formula_string = ctk.StringVar(value='0')
        
        #widgets
        self.create_widgets()
        
        #run
        self.mainloop()
        
    def create_widgets(self):
        #fonts
        main_font = ctk.CTkFont(family=FONT, size=NORMAL_FONT_SIZE)
        result_font = ctk.CTkFont(family=FONT, size=OUTPUT_FONT_SIZE)
        
        OutputLabel(self, 0, 'SE', main_font, self.formula_string)
        OutputLabel(self, 1, 'E', result_font, self.result_string)
        
        Button(self, text=OPERATORS['clear']['text'], func=self.clear, col=OPERATORS['clear']['col'], row=OPERATORS['clear']['row'], font=main_font)
        Button(self, text=OPERATORS['percent']['text'], func=self.percent, col=OPERATORS['percent']['col'], row=OPERATORS['percent']['row'], font=main_font)
        #invert button
        invert_image = ctk.CTkImage(light_image=Image.open(OPERATORS['invert']['image_path']['light']), dark_image=Image.open(OPERATORS['invert']['image_path']['dark']))
        ImageButton(self, text=OPERATORS['invert']['text'], func=self.invert, col=OPERATORS['invert']['col'], row=OPERATORS['invert']['row'], font=main_font, image=invert_image)
            
    def title_bar_color(self, is_dark):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = TITLE_BAR_HEX_COLORS['dark'] if is_dark else TITLE_BAR_HEX_COLORS['light']
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass

    def clear(self):
        print('clear')
        
    def percent(self):
        print('percent')
    
    def invert(self):
        print('invert')
            
class OutputLabel(ctk.CTkLabel):
    def __init__(self, parent, row, anchor, font, string_var):
        super().__init__(parent, font=font, textvariable=string_var)
        self.grid(column=0, columnspan=4, row=row, sticky=anchor)
                    
if __name__ == '__main__':
    Calculator(darkdetect.isDark())