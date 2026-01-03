"""
Home Screen untuk aplikasi
Tampilan utama dengan menu navigasi
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle

from app_ui import Colors, Fonts, Spacing, Styles
from components.buttons import PrimaryButton, IconButton
from components.cards import FeatureCard

class HomeScreen(Screen):
    """Screen utama/beranda aplikasi"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'home'
        
        # Layout utama dengan background gradient
        main_layout = BoxLayout(
            orientation='vertical',
            padding=[Spacing.MD, Spacing.MD, Spacing.MD, Spacing.XL],
            spacing=Spacing.MD
        )
        
        # Header dengan logo dan judul
        header = self.create_header()
        main_layout.add_widget(header)
        
        # Konten utama
        content = self.create_content()
        main_layout.add_widget(content)
        
        # Footer
        footer = self.create_footer()
        main_layout.add_widget(footer)
        
        self.add_widget(main_layout)
        
        # Animasi saat screen muncul
        Clock.schedule_once(self.animate_entrance, 0.1)
    
    def create_header(self):
        """Membuat header dengan logo dan judul"""
        header_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(180),
            spacing=Spacing.SM
        )
        
        # Logo/ikon aplikasi
        logo_layout = BoxLayout(
            size_hint_y=None,
            height=dp(80),
            padding=[dp(20), 0]
        )
        
        # Ikon fisika dengan background bulat
        with logo_layout.canvas.before:
            Color(rgba=Colors.PRIMARY)
            self.logo_bg = RoundedRectangle(
                pos=[logo_layout.center_x - dp(40), logo_layout.center_y - dp(40)],
                size=[dp(80), dp(80)],
                radius=[dp(40)]
            )
        
        # Teks logo
        logo_text = Label(
            text='⚛️',
            font_size=dp(48),
            size_hint=(None, None),
            size=(dp(80), dp(80)),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        logo_layout.add_widget(logo_text)
        
        # Judul aplikasi
        title_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(80),
            spacing=Spacing.XS
        )
        
        app_title = Label(
            text='Physics Formulas',
            font_size=Fonts.H1,
            bold=True,
            color=Colors.DARK,
            size_hint_y=None,
            height=dp(40)
        )
        
        app_subtitle = Label(
            text='Complete Junior High School Physics Reference',
            font_size=Fonts.BODY_SMALL,
            color=Colors.GRAY_DARK,
            size_hint_y=None,
            height=dp(20)
        )
        
        title_layout.add_widget(app_title)
        title_layout.add_widget(app_subtitle)
        
        header_layout.add_widget(logo_layout)
        header_layout.add_widget(title_layout)
        
        return header_layout
    
    def create_content(self):
        """Membuat konten utama dengan menu"""
        content_layout = BoxLayout(
            orientation='vertical',
            spacing=Spacing.LG,
            padding=[0, Spacing.XL, 0, 0]
        )
        
        # Grid untuk fitur utama
        grid = GridLayout(
            cols=2,
            spacing=Spacing.MD,
            size_hint_y=None,
            height=dp(400)
        )
        
        # Kartu fitur 1: Daftar Rumus
        formula_card = FeatureCard(
            icon='📚',
            title='Formula List',
            description='Complete collection of physics formulas',
            color=Colors.PRIMARY,
            on_press=self.go_to_formulas
        )
        grid.add_widget(formula_card)
        
        # Kartu fitur 2: Kalkulator
        calculator_card = FeatureCard(
            icon='🧮',
            title='Calculator',
            description='Calculate physics formulas instantly',
            color=Colors.SECONDARY,
            on_press=self.go_to_calculator
        )
        grid.add_widget(calculator_card)
        
        # Kartu fitur 3: Contoh Soal (opsional)
        example_card = FeatureCard(
            icon='📝',
            title='Examples',
            description='Practical examples with solutions',
            color=Colors.SUCCESS,
            on_press=self.show_examples
        )
        grid.add_widget(example_card)
        
        # Kartu fitur 4: Quiz (opsional)
        quiz_card = FeatureCard(
            icon='🎯',
            title='Quick Quiz',
            description='Test your physics knowledge',
            color=Colors.WARNING,
            on_press=self.show_quiz
        )
        grid.add_widget(quiz_card)
        
        content_layout.add_widget(grid)
        
        # Quick actions
        quick_actions = self.create_quick_actions()
        content_layout.add_widget(quick_actions)
        
        return content_layout
    
    def create_quick_actions(self):
        """Membuat quick actions di bagian bawah"""
        actions_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            spacing=Spacing.MD
        )
        
        # Tombol favorit
        btn_fav = IconButton(
            icon='⭐',
            text='Favorites',
            size_hint_x=0.5,
            variant='outline',
            on_press=self.show_favorites
        )
        
        # Tombol riwayat
        btn_history = IconButton(
            icon='📖',
            text='History',
            size_hint_x=0.5,
            variant='outline',
            on_press=self.show_history
        )
        
        actions_layout.add_widget(btn_fav)
        actions_layout.add_widget(btn_history)
        
        return actions_layout
    
    def create_footer(self):
        """Membuat footer dengan info versi"""
        footer_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(60),
            spacing=Spacing.XS
        )
        
        version_label = Label(
            text='v1.0.0',
            font_size=Fonts.CAPTION,
            color=Colors.GRAY,
            size_hint_y=None,
            height=dp(20)
        )
        
        credit_label = Label(
            text='Made with ❤️ using Kivy',
            font_size=Fonts.CAPTION,
            color=Colors.GRAY,
            size_hint_y=None,
            height=dp(20)
        )
        
        footer_layout.add_widget(version_label)
        footer_layout.add_widget(credit_label)
        
        return footer_layout
    
    def animate_entrance(self, dt):
        """Animasi saat screen muncul"""
        # Animasi fade in untuk semua child
        for child in self.children[0].children:
            child.opacity = 0
            anim = Animation(opacity=1, duration=0.5)
            anim.start(child)
    
    def go_to_formulas(self, instance):
        """Navigasi ke screen daftar rumus"""
        self.manager.current = 'formulas'
    
    def go_to_calculator(self, instance):
        """Navigasi ke screen kalkulator"""
        self.manager.current = 'calculator'
    
    def show_examples(self, instance):
        """Menampilkan contoh soal (placeholder)"""
        from kivy.uix.modalview import ModalView
        from kivy.uix.label import Label
        
        modal = ModalView(size_hint=(0.8, 0.4))
        content = BoxLayout(orientation='vertical', padding=Spacing.MD)
        content.add_widget(Label(
            text='Examples feature coming soon!',
            font_size=Fonts.H4,
            color=Colors.DARK
        ))
        
        btn = PrimaryButton(text='OK', on_press=lambda x: modal.dismiss())
        content.add_widget(btn)
        
        modal.add_widget(content)
        modal.open()
    
    def show_quiz(self, instance):
        """Menampilkan quiz (placeholder)"""
        from kivy.uix.modalview import ModalView
        from kivy.uix.label import Label
        
        modal = ModalView(size_hint=(0.8, 0.4))
        content = BoxLayout(orientation='vertical', padding=Spacing.MD)
        content.add_widget(Label(
            text='Quiz feature coming soon!',
            font_size=Fonts.H4,
            color=Colors.DARK
        ))
        
        btn = PrimaryButton(text='OK', on_press=lambda x: modal.dismiss())
        content.add_widget(btn)
        
        modal.add_widget(content)
        modal.open()
    
    def show_favorites(self, instance):
        """Menampilkan favorit (placeholder)"""
        pass
    
    def show_history(self, instance):
        """Menampilkan riwayat (placeholder)"""
        pass

# Helper untuk dp
from kivy.metrics import dp