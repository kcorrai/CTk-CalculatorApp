from customtkinter import CTkButton
from settings import *

class Button(CTkButton):
    def __init__(self, parent, text, func, col, row, font, span, color='dark-gray'):
        super().__init__(
            master=parent,
            command=func,
            text=text,
            corner_radius=STYLING['corner-radius'],
            font=font,
            fg_color=COLORS[color]['fg'],
            hover_color=COLORS[color]['hover'],
            text_color=COLORS[color]['text'])
        self.grid(column=col, row=row, sticky='news', columnspan=span, padx=STYLING['gap'], pady=STYLING['gap'])
        
class NumButton(Button):
    def __init__(self, parent, text, func, col, row, font, span, color='light-gray'):
        super().__init__(
            parent=parent,
            text=text,
            func=lambda: func(text),
            col=col,
            row=row,
            font=font,
            color=color,
            span=span,
        )
        
class MathButton(Button):
    def __init__(self, parent, text, operator, func, col, row, font, span,color='orange'):
        super().__init__(
            parent=parent,
            text=text,
            func=lambda: func(operator),
            col=col,
            row=row,
            font=font,
            color=color,
            span=span
        )

class ImageButton(CTkButton):
    def __init__(self, parent, text, func, col, row, font, image,color='dark-gray'):
        super().__init__(
            master=parent,
            command=func,
            text=text,
            corner_radius=STYLING['corner-radius'],
            font=font,
            image=image,
            fg_color=COLORS[color]['fg'],
            hover_color=COLORS[color]['hover'],
            text_color=COLORS[color]['text'],
            )
        self.grid(column=col, row=row, sticky='news', padx=STYLING['gap'], pady=STYLING['gap'])
        
class MathImageButton(CTkButton):
    def __init__(self, parent, func, operator, col, row, text, font, image, color='orange'):
        super().__init__(
            master=parent,
            text=text,
            command=lambda: func(operator),
            corner_radius=STYLING['corner-radius'],
            font=font,
            image=image,
            fg_color=COLORS[color]['fg'],
            hover_color=COLORS[color]['hover']
            )
        self.grid(column=col, row=row, sticky='news', padx=STYLING['gap'], pady=STYLING['gap'])