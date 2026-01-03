"""
Komponen card custom untuk menampilkan konten
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.metrics import dp, sp  # TAMBAHKAN INI

from app_ui import Colors, Fonts, Spacing

class Card(BoxLayout):
    """Card dasar dengan rounded corners dan shadow"""
    
    bg_color = ListProperty(Colors.WHITE)
    radius = NumericProperty(Spacing.RADIUS_LG)
    elevation = NumericProperty(1)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.orientation = 'vertical'
        self.padding = Spacing.MD
        self.spacing = Spacing.SM
        
        # Background dengan rounded corners
        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[self.radius]
            )
            
            # Shadow effect (simplified)
            if self.elevation > 0:
                Color(0, 0, 0, 0.1)
                self.shadow = RoundedRectangle(
                    pos=(self.x, self.y - dp(2)),
                    size=self.size,
                    radius=[self.radius]
                )
        
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, *args):
        """Update rectangle position and size"""
        self.rect.pos = self.pos
        self.rect.size = self.size
        if hasattr(self, 'shadow'):
            self.shadow.pos = (self.x, self.y - dp(2))
            self.shadow.size = self.size

class FormulaCard(Card):
    """Card khusus untuk menampilkan rumus"""
    
    def __init__(self, title='', formula='', category='', on_press=None, **kwargs):
        super().__init__(**kwargs)
        
        self.size_hint_y = None
        self.height = dp(120)
        self.padding = Spacing.MD
        self.spacing = Spacing.SM
        
        # Title
        title_label = Label(
            text=title,
            font_size=Fonts.H4,
            bold=True,
            color=Colors.DARK,
            size_hint_y=None,
            height=dp(30),
            halign='left'
        )
        title_label.bind(size=title_label.setter('text_size'))
        
        # Formula (lebih besar dan menonjol)
        formula_label = Label(
            text=formula,
            font_size=Fonts.H3,
            bold=True,
            color=Colors.PRIMARY,
            size_hint_y=None,
            height=dp(40)
        )
        
        # Category badge
        category_layout = BoxLayout(
            size_hint_y=None,
            height=dp(24),
            spacing=Spacing.XS
        )
        
        # Badge kecil untuk kategori
        with category_layout.canvas.before:
            Color(*Colors.PRIMARY_LIGHT)
            RoundedRectangle(
                pos=category_layout.pos,
                size=category_layout.size,
                radius=[dp(12)]
            )
        
        category_label = Label(
            text=category,
            font_size=Fonts.CAPTION,
            color=Colors.WHITE,
            bold=True,
            size_hint_x=1
        )
        category_layout.add_widget(category_label)
        
        self.add_widget(title_label)
        self.add_widget(formula_label)
        self.add_widget(category_layout)
        
        # Jika ada callback, buat button transparan di atas card
        if on_press:
            overlay = Button(
                size_hint=(1, 1),
                background_color=(0, 0, 0, 0),
                background_normal=''
            )
            overlay.bind(on_press=on_press)
            self.add_widget(overlay)

class FeatureCard(Card):
    """Card untuk menampilkan fitur aplikasi"""
    
    def __init__(self, icon='', title='', description='', color=Colors.PRIMARY, on_press=None, **kwargs):
        super().__init__(**kwargs)
        
        self.size_hint_y = None
        self.height = dp(140)
        self.padding = Spacing.LG
        
        # Icon dengan background circle
        icon_layout = BoxLayout(
            size_hint_y=None,
            height=dp(60)
        )
        
        with icon_layout.canvas.before:
            Color(*color)
            RoundedRectangle(
                pos=(icon_layout.center_x - dp(25), icon_layout.center_y - dp(25)),
                size=(dp(50), dp(50)),
                radius=[dp(25)]
            )
        
        icon_label = Label(
            text=icon,
            font_size=dp(32),
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        icon_layout.add_widget(icon_label)
        
        # Title
        title_label = Label(
            text=title,
            font_size=Fonts.H5,
            bold=True,
            color=Colors.DARK,
            size_hint_y=None,
            height=dp(25),
            halign='center'
        )
        title_label.bind(size=title_label.setter('text_size'))
        
        # Description
        desc_label = Label(
            text=description,
            font_size=Fonts.BODY_SMALL,
            color=Colors.GRAY_DARK,
            size_hint_y=None,
            height=dp(40),
            halign='center'
        )
        desc_label.bind(size=desc_label.setter('text_size'))
        
        self.add_widget(icon_layout)
        self.add_widget(title_label)
        self.add_widget(desc_label)
        
        # Overlay button jika ada callback
        if on_press:
            overlay = Button(
                size_hint=(1, 1),
                background_color=(0, 0, 0, 0),
                background_normal=''
            )
            overlay.bind(on_press=on_press)
            self.add_widget(overlay)
        
        # Animasi hover
        self.bind(on_enter=self.animate_hover)
        self.bind(on_leave=self.animate_leave)
    
    def animate_hover(self, instance):
        """Animasi saat hover"""
        from kivy.animation import Animation
        anim = Animation(scale=1.02, duration=0.2)
        anim.start(self)
    
    def animate_leave(self, instance):
        """Animasi saat leave"""
        from kivy.animation import Animation
        anim = Animation(scale=1, duration=0.2)
        anim.start(self)

class InfoCard(Card):
    """Card untuk menampilkan informasi"""
    
    def __init__(self, title='', content='', icon='', **kwargs):
        super().__init__(**kwargs)
        
        self.orientation = 'horizontal'
        self.spacing = Spacing.MD
        
        # Icon jika ada
        if icon:
            icon_label = Label(
                text=icon,
                font_size=Fonts.H3,
                size_hint_x=None,
                width=dp(40)
            )
            self.add_widget(icon_label)
        
        # Content
        content_layout = BoxLayout(orientation='vertical')
        
        title_label = Label(
            text=title,
            font_size=Fonts.H5,
            bold=True,
            color=Colors.DARK,
            size_hint_y=None,
            height=dp(25),
            halign='left'
        )
        title_label.bind(size=title_label.setter('text_size'))
        
        content_label = Label(
            text=content,
            font_size=Fonts.BODY_SMALL,
            color=Colors.GRAY_DARK,
            halign='left',
            valign='top'
        )
        content_label.bind(size=content_label.setter('text_size'))
        
        content_layout.add_widget(title_label)
        content_layout.add_widget(content_label)
        
        self.add_widget(content_layout)

# Export semua card class
__all__ = [
    'Card',
    'FormulaCard',
    'FeatureCard',
    'InfoCard'
]