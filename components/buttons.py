"""
Komponen button custom dengan berbagai style
"""

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivy.animation import Animation
from kivy.metrics import dp, sp
from kivy.clock import Clock

from app_ui import Colors, Fonts, Spacing, Styles

class PrimaryButton(Button):
    """Button primary dengan style modern"""
    
    bg_color = ListProperty(Colors.PRIMARY)
    text_color = ListProperty(Colors.WHITE)
    radius = NumericProperty(Spacing.RADIUS_LG)
    elevation = NumericProperty(2)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Set default properties
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''
        self.background_down = ''
        self.color = self.text_color
        self.font_size = Fonts.BODY
        self.bold = True
        
        # Bind properties
        self.bind(
            pos=self.update_canvas,
            size=self.update_canvas,
            bg_color=self.update_canvas,
            radius=self.update_canvas
        )
        
        # Animation for press effect
        self.bind(on_press=self.animate_press)
        self.bind(on_release=self.animate_release)
        
        # Initial canvas update
        Clock.schedule_once(lambda dt: self.update_canvas(), 0.1)
    
    def update_canvas(self, *args):
        """Update canvas dengan rounded rectangle"""
        self.canvas.before.clear()
        
        with self.canvas.before:
            # Background
            Color(*self.bg_color)
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[self.radius]
            )
            
            # Border
            Color(*self.bg_color)
            Line(
                rounded_rectangle=(self.x, self.y, self.width, self.height, self.radius),
                width=1.5
            )
    
    def animate_press(self, instance):
        """Animasi saat button ditekan"""
        anim = Animation(
            opacity=0.8,
            scale=0.98,
            duration=0.1
        )
        anim.start(self)
    
    def animate_release(self, instance):
        """Animasi saat button dilepas"""
        anim = Animation(
            opacity=1,
            scale=1,
            duration=0.2
        )
        anim.start(self)

class SecondaryButton(PrimaryButton):
    """Button secondary dengan warna berbeda"""
    
    def __init__(self, **kwargs):
        kwargs.setdefault('bg_color', Colors.SECONDARY)
        super().__init__(**kwargs)

class OutlineButton(PrimaryButton):
    """Button dengan outline saja"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = Colors.WHITE
        self.text_color = Colors.PRIMARY
    
    def update_canvas(self, *args):
        """Override update_canvas untuk outline saja"""
        self.canvas.before.clear()
        
        with self.canvas.before:
            # Background transparan
            Color(1, 1, 1, 1)
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[self.radius]
            )
            
            # Border
            Color(*Colors.PRIMARY)
            Line(
                rounded_rectangle=(self.x, self.y, self.width, self.height, self.radius),
                width=1.5
            )

class IconButton(BoxLayout):
    """Button dengan ikon dan teks"""
    
    def __init__(self, icon='', text='', on_press=None, variant='primary', **kwargs):
        super().__init__(**kwargs)
        
        self.orientation = 'horizontal'
        self.spacing = Spacing.SM
        self.padding = Spacing.SM
        self.size_hint_y = None
        self.height = dp(44)
        
        # Style berdasarkan variant
        style = Styles.get_button_style(variant)
        
        # Ikon
        icon_label = Label(
            text=icon,
            font_size=Fonts.H4,
            size_hint_x=None,
            width=dp(24),
            color=style['text_color']
        )
        
        # Teks
        text_label = Label(
            text=text,
            font_size=style['font_size'],
            color=style['text_color'],
            bold=True
        )
        
        self.add_widget(icon_label)
        self.add_widget(text_label)
        
        # Background
        with self.canvas.before:
            Color(*style['bg_color'])
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[Spacing.RADIUS_MD]
            )
        
        # Binding untuk interaksi
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        # Touch event
        if on_press:
            self.bind(on_touch_down=self.on_touch)
            self.callback = on_press
    
    def update_rect(self, *args):
        """Update background rectangle"""
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def on_touch(self, instance, touch):
        """Handle touch event"""
        if self.collide_point(*touch.pos):
            if touch.is_double_tap:
                return False
            
            if touch.is_mouse_scrolling:
                return False
            
            if 'button' in touch.profile and touch.button in ('scrollup', 'scrolldown'):
                return False
            
            # Animasi press
            anim = Animation(opacity=0.7, duration=0.1) + Animation(opacity=1, duration=0.2)
            anim.start(self)
            
            # Jalankan callback
            if hasattr(self, 'callback'):
                self.callback(self)
            
            return True
        
        return False

class FloatingActionButton(Button):
    """Floating Action Button untuk aksi utama"""
    
    def __init__(self, icon='+', on_press=None, **kwargs):
        super().__init__(**kwargs)
        
        self.size_hint = (None, None)
        self.size = (dp(56), dp(56))
        self.text = icon
        self.font_size = Fonts.H2
        self.color = Colors.WHITE
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''
        
        # Position (bisa diatur dari parent)
        self.pos_hint = {'right': 0.9, 'y': 0.1}
        
        # Background circle
        with self.canvas.before:
            Color(*Colors.PRIMARY)
            self.circle = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(28)]
            )
        
        # Shadow effect (simulasi)
        with self.canvas.after:
            Color(0, 0, 0, 0.2)
            RoundedRectangle(
                pos=(self.x, self.y - dp(2)),
                size=self.size,
                radius=[dp(28)]
            )
        
        self.bind(pos=self.update_circle, size=self.update_circle)
        
        if on_press:
            self.bind(on_press=on_press)
    
    def update_circle(self, *args):
        """Update circle position"""
        self.circle.pos = self.pos

# Export semua button class
__all__ = [
    'PrimaryButton',
    'SecondaryButton',
    'OutlineButton',
    'IconButton',
    'FloatingActionButton'
]