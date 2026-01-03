"""
Komponen input custom untuk aplikasi
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.metrics import dp, sp

from app_ui import Colors, Fonts, Spacing

class NumberInput(BoxLayout):
    """Input field untuk angka dengan validasi"""
    
    value = StringProperty('0')
    unit = StringProperty('')
    hint_text = StringProperty('Enter number')
    error = StringProperty('')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.orientation = 'vertical'
        self.spacing = Spacing.XS
        self.size_hint_y = None
        self.height = dp(70)
        
        # Input field dengan unit
        input_container = BoxLayout(
            orientation='horizontal',
            spacing=Spacing.SM,
            size_hint_y=None,
            height=dp(44)
        )
        
        # Text input
        self.text_input = TextInput(
            text=self.value,
            hint_text=self.hint_text,
            font_size=Fonts.BODY,
            multiline=False,
            input_filter='float',
            halign='right',
            size_hint_x=0.7,
            background_normal='',
            background_color=(0, 0, 0, 0),
            foreground_color=Colors.DARK,
            padding=[dp(10), dp(10)]
        )
        
        # Unit label
        self.unit_label = Label(
            text=self.unit,
            font_size=Fonts.BODY_SMALL,
            color=Colors.GRAY_DARK,
            size_hint_x=0.3
        )
        
        # Background untuk input
        with self.text_input.canvas.before:
            Color(*Colors.WHITE)
            self.input_rect = RoundedRectangle(
                pos=self.text_input.pos,
                size=self.text_input.size,
                radius=[Spacing.RADIUS_SM]
            )
            
            # Border di canvas yang sama
            Color(*Colors.GRAY_LIGHT)
            self.input_border = Line(
                rounded_rectangle=(self.text_input.x, self.text_input.y,
                                  self.text_input.width, self.text_input.height,
                                  Spacing.RADIUS_SM),
                width=1
            )
        
        self.text_input.bind(
            pos=self.update_input_bg,
            size=self.update_input_bg,
            text=self.on_text_change
        )
        
        input_container.add_widget(self.text_input)
        input_container.add_widget(self.unit_label)
        
        # Error label
        self.error_label = Label(
            text='',
            font_size=Fonts.CAPTION,
            color=Colors.DANGER,
            size_hint_y=None,
            height=dp(20)
        )
        
        self.add_widget(input_container)
        self.add_widget(self.error_label)
    
    def update_input_bg(self, instance, value):
        """Update background input"""
        self.input_rect.pos = instance.pos
        self.input_rect.size = instance.size
        self.input_border.rounded_rectangle = (instance.x, instance.y,
                                              instance.width, instance.height,
                                              Spacing.RADIUS_SM)
    
    def on_text_change(self, instance, value):
        """Handle text change dengan validasi"""
        self.value = value
        self.error = ''
        self.error_label.text = ''
        
        # Validasi
        if value:
            try:
                float(value)
                # Jika valid, ubah border menjadi hijau
                self.input_border.rgba = Colors.SUCCESS
            except ValueError:
                self.error = 'Invalid number'
                self.error_label.text = self.error
                self.input_border.rgba = Colors.DANGER
        else:
            self.input_border.rgba = Colors.GRAY_LIGHT
    
    def get_value(self):
        """Mendapatkan nilai sebagai float"""
        try:
            return float(self.value)
        except ValueError:
            return 0.0
    
    def set_error(self, message):
        """Set error message"""
        self.error = message
        self.error_label.text = message
        self.input_border.rgba = Colors.DANGER

class UnitInput(NumberInput):
    """Input dengan unit yang bisa dipilih"""
    
    def __init__(self, units=None, **kwargs):
        super().__init__(**kwargs)
        
        # Hapus unit label yang lama
        self.remove_widget(self.children[0])  # Error label
        input_container = self.children[0]
        input_container.remove_widget(self.unit_label)
        
        # Dropdown untuk unit
        self.unit_dropdown = Button(
            text=self.unit,
            font_size=Fonts.BODY_SMALL,
            size_hint_x=0.3,
            background_color=Colors.GRAY_LIGHT,
            color=Colors.DARK,
            background_normal=''
        )
        
        with self.unit_dropdown.canvas.before:
            Color(*Colors.GRAY_LIGHT)
            self.unit_rect = RoundedRectangle(
                pos=self.unit_dropdown.pos,
                size=self.unit_dropdown.size,
                radius=[Spacing.RADIUS_SM]
            )
        
        self.unit_dropdown.bind(
            pos=self.update_unit_bg,
            size=self.update_unit_bg,
            on_press=self.show_unit_dropdown
        )
        
        input_container.add_widget(self.unit_dropdown)
        self.add_widget(self.error_label)
        
        # Daftar unit
        self.units = units or [self.unit]
    
    def update_unit_bg(self, instance, value):
        """Update background unit button"""
        self.unit_rect.pos = instance.pos
        self.unit_rect.size = instance.size
    
    def show_unit_dropdown(self, instance):
        """Menampilkan dropdown unit"""
        from kivy.uix.dropdown import DropDown
        
        dropdown = DropDown()
        
        for unit in self.units:
            btn = Button(
                text=unit,
                size_hint_y=None,
                height=dp(40),
                background_color=Colors.WHITE,
                color=Colors.DARK
            )
            
            btn.bind(on_release=lambda btn=btn: self.select_unit(btn.text, dropdown))
            dropdown.add_widget(btn)
        
        dropdown.open(instance)
    
    def select_unit(self, unit, dropdown):
        """Memilih unit"""
        self.unit = unit
        self.unit_dropdown.text = unit
        dropdown.dismiss()

class SearchInput(BoxLayout):
    """Input field untuk pencarian"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(44)
        self.spacing = dp(5)
        
        # Icon pencarian
        icon = Label(
            text='🔍',
            font_size=Fonts.BODY,
            size_hint_x=None,
            width=dp(30)
        )
        
        # Input field
        self.text_input = TextInput(
            hint_text='Search...',
            font_size=Fonts.BODY,
            multiline=False,
            size_hint_x=1,
            background_normal='',
            background_color=(0, 0, 0, 0),
            foreground_color=Colors.DARK,
            padding=[dp(10), dp(10)]
        )
        
        # Background
        with self.canvas.before:
            Color(*Colors.WHITE)
            self.bg_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[Spacing.RADIUS_MD]
            )
        
        # Border terpisah
        with self.canvas.after:
            Color(*Colors.GRAY_LIGHT)
            self._border_line = Line(
                rounded_rectangle=(self.x, self.y, self.width, self.height, Spacing.RADIUS_MD),
                width=1
            )
        
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        self.add_widget(icon)
        self.add_widget(self.text_input)
    
    def update_bg(self, *args):
        """Update background"""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border.rounded_rectangle = (self.x, self.y, self.width, self.height, Spacing.RADIUS_MD)
    
    def get_text(self):
        """Mendapatkan teks pencarian"""
        return self.text_input.text
    
    def clear(self):
        """Membersihkan input"""
        self.text_input.text = ''