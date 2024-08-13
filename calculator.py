import darkdetect
import customtkinter as ctk
from settings import *
from buttons import Button, ImageButton, NumButton, MathButton, MathImageButton
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
        self.display_nums = []
        self.full_operation = []
        
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
        
        Button(self, text=OPERATORS['clear']['text'], func=self.clear, col=OPERATORS['clear']['col'], row=OPERATORS['clear']['row'], font=main_font, span=1)
        Button(self, text=OPERATORS['percent']['text'], func=self.percent, col=OPERATORS['percent']['col'], row=OPERATORS['percent']['row'], font=main_font, span=1)
        #invert button
        self.new_size = (1024,1024)
        invert_image = ctk.CTkImage(light_image=Image.open(OPERATORS['invert']['image_path']['light']).resize(self.new_size), dark_image=Image.open(OPERATORS['invert']['image_path']['dark']).resize(self.new_size))
        ImageButton(self, text=OPERATORS['invert']['text'], func=self.invert, col=OPERATORS['invert']['col'], row=OPERATORS['invert']['row'], font=main_font, image=invert_image)
            
        for num, data in NUM_POSITIONS.items():
            NumButton(self, text=num, func=self.num_press, col=data['col'], row=data['row'], font=main_font, span=data['span'])    

        for operator, data in MATH_POSITIONS.items():
            if data['image_path']:
                divide_image = ctk.CTkImage(light_image=Image.open(data['image_path']['dark']), dark_image=Image.open(data['image_path']['light']).resize((512,512)))
                MathImageButton(self, text='', func=self.math_press, operator=operator, col=data['col'], row=data['row'], font=main_font, image=divide_image)
            else:
                MathButton(self, text=data['character'], operator=operator, func=self.math_press, col=data['col'], row=data['row'], font=main_font, span=1)
        
    def num_press(self, value):
        self.display_nums.append(str(value))
        full_number = ''.join(self.display_nums)
        self.result_string.set(full_number)
    
    def math_press(self, value):
        current_number = ''.join(self.display_nums)
        if current_number:
            self.full_operation.append(current_number)
            if value != '=':
                # update data
                self.full_operation.append(value)
                self.display_nums.clear()
                
                # update output
                self.result_string.set('')
                self.formula_string.set(' '.join(self.full_operation))
            else:
                formula = ' '.join(self.full_operation)
                result = eval(formula)
                
                if isinstance(result, float):
                    if result.is_integer():
                        result = int(result)
                    else:
                        result = round(result, 3)
                
                # update data
                self.full_operation.clear()
                self.display_nums = [str(result)]
                
                # update output
                self.result_string.set(result)
                self.formula_string.set(formula)
    
    def clear(self):
        # clear output
        self.result_string.set(0)
        self.formula_string.set('')
        # clear data
        self.display_nums.clear()
        self.full_operation.clear()
        
    def percent(self):
        if self.display_nums:
            current_number = float(''.join(self.display_nums))
            percent_number = current_number / 100
            
            self.display_nums = list(str(percent_number))
            self.result_string.set(''.join(self.display_nums))
    
    def invert(self):
        current_number = ''.join(self.display_nums)
        if current_number:
        # pozitif/negatif
            if float(current_number) > 0:
                self.display_nums.insert(0, '-')
            else:
                del self.display_nums[0]
            
        self.result_string.set(''.join(self.display_nums))
        
    def title_bar_color(self, is_dark):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = TITLE_BAR_HEX_COLORS['dark'] if is_dark else TITLE_BAR_HEX_COLORS['light']
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass
            
class OutputLabel(ctk.CTkLabel):
    def __init__(self, parent, row, anchor, font, string_var):
        super().__init__(parent, font=font, textvariable=string_var)
        self.grid(column=0, columnspan=4, row=row, sticky=anchor)
                    
if __name__ == '__main__':
    Calculator(darkdetect.isLight())