"""
Screen untuk menampilkan detail rumus fisika
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.metrics import dp, sp

from app_ui import Colors, Fonts, Spacing
from components.buttons import PrimaryButton, OutlineButton, IconButton
from components.cards import Card, InfoCard

class DetailScreen(Screen):
    """Screen untuk menampilkan detail lengkap rumus"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'detail'
        
        # Layout utama
        self.main_layout = BoxLayout(
            orientation='vertical',
            padding=[0, 0, 0, 0]
        )
        
        # Header
        self.header = self.create_header()
        self.main_layout.add_widget(self.header)
        
        # Konten (akan diisi dinamis)
        self.content_scroll = ScrollView(
            do_scroll_x=False,
            bar_width=dp(4)
        )
        
        self.content_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=[Spacing.MD, Spacing.MD, Spacing.MD, Spacing.XL],
            spacing=Spacing.MD
        )
        self.content_container.bind(minimum_height=self.content_container.setter('height'))
        
        self.content_scroll.add_widget(self.content_container)
        self.main_layout.add_widget(self.content_scroll)
        
        self.add_widget(self.main_layout)
        
        # State untuk data rumus
        self.current_formula = None
    
    def create_header(self):
        """Membuat header dengan tombol kembali"""
        header_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=[Spacing.MD, Spacing.MD, Spacing.MD, Spacing.SM],
            spacing=Spacing.SM
        )
        
        # Top bar
        top_bar = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            spacing=Spacing.SM
        )
        
        # Tombol kembali
        self.back_btn = Button(
            text='←',
            font_size=Fonts.H3,
            size_hint_x=None,
            width=dp(50),
            background_color=(0, 0, 0, 0),
            background_normal='',
            color=Colors.DARK
        )
        self.back_btn.bind(on_press=self.go_back)
        
        # Judul (akan diupdate)
        self.title_label = Label(
            text='Formula Detail',
            font_size=Fonts.H2,
            bold=True,
            color=Colors.DARK,
            size_hint_x=1
        )
        
        # Tombol aksi (favorit)
        self.fav_btn = Button(
            text='☆',
            font_size=Fonts.H4,
            size_hint_x=None,
            width=dp(50),
            background_color=(0, 0, 0, 0),
            background_normal='',
            color=Colors.DARK
        )
        self.fav_btn.bind(on_press=self.toggle_favorite)
        
        top_bar.add_widget(self.back_btn)
        top_bar.add_widget(self.title_label)
        top_bar.add_widget(self.fav_btn)
        
        # Subtitle (kategori)
        self.subtitle_label = Label(
            text='',
            font_size=Fonts.BODY_SMALL,
            color=Colors.GRAY_DARK,
            size_hint_y=None,
            height=dp(20)
        )
        
        header_layout.add_widget(top_bar)
        header_layout.add_widget(self.subtitle_label)
        
        return header_layout
    
    def display_formula(self, formula_key):
        """Menampilkan detail rumus berdasarkan kunci"""
        # Hapus konten sebelumnya
        self.content_container.clear_widgets()
        
        # Dapatkan data rumus
        app = self.manager.app
        formula_data = app.formula_data.get(formula_key, {})
        self.current_formula = formula_data
        
        # Update header
        self.title_label.text = formula_data.get('title', 'Formula Detail')
        self.subtitle_label.text = formula_data.get('category', '')
        
        # Animasi fade in
        self.content_container.opacity = 0
        
        # 1. Kartu rumus utama
        formula_card = self.create_formula_card(formula_data)
        self.content_container.add_widget(formula_card)
        
        # 2. Kartu deskripsi
        desc_card = self.create_description_card(formula_data)
        self.content_container.add_widget(desc_card)
        
        # 3. Kartu variabel
        variables_card = self.create_variables_card(formula_data)
        self.content_container.add_widget(variables_card)
        
        # 4. Kartu contoh
        example_card = self.create_example_card(formula_data)
        self.content_container.add_widget(example_card)
        
        # 5. Kartu info tambahan
        info_card = self.create_info_card(formula_data)
        self.content_container.add_widget(info_card)
        
        # 6. Tombol aksi
        action_buttons = self.create_action_buttons(formula_key)
        self.content_container.add_widget(action_buttons)
        
        # Animasi fade in
        anim = Animation(opacity=1, duration=0.5)
        anim.start(self.content_container)
        
        # Scroll ke atas
        Clock.schedule_once(lambda dt: self.content_scroll.scroll_y(1), 0.1)
    
    def create_formula_card(self, formula_data):
        """Membuat kartu untuk menampilkan rumus utama"""
        card = Card(
            padding=Spacing.LG,
            spacing=Spacing.MD,
            size_hint_y=None,
            height=dp(150)
        )
        
        # Ikon rumus
        icon_label = Label(
            text=formula_data.get('icon', '⚛️'),
            font_size=dp(40),
            size_hint_y=None,
            height=dp(60)
        )
        
        # Rumus dalam ukuran besar
        formula_label = Label(
            text=formula_data.get('formula', ''),
            font_size=Fonts.H1,
            bold=True,
            color=Colors.PRIMARY,
            size_hint_y=None,
            height=dp(60)
        )
        
        # Deskripsi singkat
        display_formula = Label(
            text=formula_data.get('formula_display', ''),
            font_size=Fonts.BODY,
            color=Colors.GRAY_DARK,
            size_hint_y=None,
            height=dp(30)
        )
        
        card.add_widget(icon_label)
        card.add_widget(formula_label)
        card.add_widget(display_formula)
        
        return card
    
    def create_description_card(self, formula_data):
        """Membuat kartu deskripsi rumus"""
        card = Card(
            padding=Spacing.MD,
            spacing=Spacing.SM,
            size_hint_y=None
        )
        
        # Header dengan judul
        header = BoxLayout(
            size_hint_y=None,
            height=dp(30),
            spacing=Spacing.SM
        )
        
        # Icon kecil
        icon = Label(
            text='📖',
            font_size=Fonts.H5,
            size_hint_x=None,
            width=dp(30)
        )
        
        title = Label(
            text='Description',
            font_size=Fonts.H5,
            bold=True,
            color=Colors.DARK,
            size_hint_x=1
        )
        
        header.add_widget(icon)
        header.add_widget(title)
        
        # Deskripsi
        description = Label(
            text=formula_data.get('description', ''),
            font_size=Fonts.BODY,
            color=Colors.GRAY_DARK,
            halign='left',
            valign='top',
            size_hint_y=None
        )
        
        # Hitung tinggi berdasarkan teks
        text = formula_data.get('description', '')
        lines = text.count('\n') + 1
        description.height = max(dp(80), lines * dp(24))
        description.bind(size=description.setter('text_size'))
        
        card.add_widget(header)
        card.add_widget(description)
        
        return card
    
    def create_variables_card(self, formula_data):
        """Membuat kartu variabel dan satuan"""
        variables = formula_data.get('variables', [])
        
        card = Card(
            padding=Spacing.MD,
            spacing=Spacing.SM,
            size_hint_y=None,
            height=dp(80 + len(variables) * dp(50))
        )
        
        # Header
        header = BoxLayout(
            size_hint_y=None,
            height=dp(30),
            spacing=Spacing.SM
        )
        
        icon = Label(
            text='📐',
            font_size=Fonts.H5,
            size_hint_x=None,
            width=dp(30)
        )
        
        title = Label(
            text='Variables and Units',
            font_size=Fonts.H5,
            bold=True,
            color=Colors.DARK,
            size_hint_x=1
        )
        
        header.add_widget(icon)
        header.add_widget(title)
        card.add_widget(header)
        
        # Tabel variabel
        for var in variables:
            var_row = self.create_variable_row(var)
            card.add_widget(var_row)
        
        return card
    
    def create_variable_row(self, variable):
        """Membuat baris untuk setiap variabel"""
        row = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            spacing=Spacing.SM,
            padding=[dp(10), 0, dp(10), 0]
        )
        
        # Symbol dengan background
        symbol_container = BoxLayout(
            size_hint_x=None,
            width=dp(50),
            padding=[dp(5), dp(5)]
        )
        
        with symbol_container.canvas.before:
            Color(*Colors.PRIMARY_LIGHT)
            RoundedRectangle(
                pos=symbol_container.pos,
                size=symbol_container.size,
                radius=[Spacing.RADIUS_SM]
            )
        
        symbol = Label(
            text=variable.get('symbol', ''),
            font_size=Fonts.H4,
            bold=True,
            color=Colors.WHITE
        )
        symbol_container.add_widget(symbol)
        
        # Nama variabel
        name = Label(
            text=variable.get('name', ''),
            font_size=Fonts.BODY,
            color=Colors.DARK,
            halign='left',
            size_hint_x=0.5
        )
        name.bind(size=name.setter('text_size'))
        
        # Satuan
        unit = Label(
            text=variable.get('unit', ''),
            font_size=Fonts.BODY_SMALL,
            color=Colors.GRAY_DARK,
            halign='right',
            size_hint_x=0.4
        )
        unit.bind(size=unit.setter('text_size'))
        
        row.add_widget(symbol_container)
        row.add_widget(name)
        row.add_widget(unit)
        
        return row
    
    def create_example_card(self, formula_data):
        """Membuat kartu contoh soal"""
        card = Card(
            padding=Spacing.MD,
            spacing=Spacing.SM,
            size_hint_y=None
        )
        
        # Header
        header = BoxLayout(
            size_hint_y=None,
            height=dp(30),
            spacing=Spacing.SM
        )
        
        icon = Label(
            text='💡',
            font_size=Fonts.H5,
            size_hint_x=None,
            width=dp(30)
        )
        
        title = Label(
            text='Example',
            font_size=Fonts.H5,
            bold=True,
            color=Colors.DARK,
            size_hint_x=1
        )
        
        header.add_widget(icon)
        header.add_widget(title)
        
        # Contoh
        example = Label(
            text=formula_data.get('example', ''),
            font_size=Fonts.BODY,
            color=Colors.DARK,
            halign='left',
            valign='top',
            size_hint_y=None
        )
        
        # Hitung tinggi berdasarkan teks
        text = formula_data.get('example', '')
        lines = text.count('\n') + 1
        example.height = max(dp(100), lines * dp(24))
        example.bind(size=example.setter('text_size'))
        
        card.add_widget(header)
        card.add_widget(example)
        
        return card
    
    def create_info_card(self, formula_data):
        """Membuat kartu informasi tambahan"""
        card = Card(
            padding=Spacing.MD,
            spacing=Spacing.MD,
            size_hint_y=None,
            height=dp(100)
        )
        
        # Grid untuk info
        grid = BoxLayout(
            orientation='horizontal',
            spacing=Spacing.MD
        )
        
        # Kesulitan
        diff_card = self.create_info_item(
            '⚡',
            'Difficulty',
            formula_data.get('difficulty', 'N/A')
        )
        
        # Kategori
        cat_card = self.create_info_item(
            '📁',
            'Category',
            formula_data.get('category', 'N/A')
        )
        
        grid.add_widget(diff_card)
        grid.add_widget(cat_card)
        
        card.add_widget(grid)
        return card
    
    def create_info_item(self, icon, title, value):
        """Membuat item informasi"""
        container = BoxLayout(
            orientation='vertical',
            spacing=Spacing.XS,
            size_hint_x=0.5
        )
        
        # Icon
        icon_label = Label(
            text=icon,
            font_size=Fonts.H4,
            size_hint_y=None,
            height=dp(30)
        )
        
        # Title
        title_label = Label(
            text=title,
            font_size=Fonts.CAPTION,
            color=Colors.GRAY,
            size_hint_y=None,
            height=dp(20)
        )
        
        # Value
        value_label = Label(
            text=value,
            font_size=Fonts.BODY_SMALL,
            bold=True,
            color=Colors.DARK,
            size_hint_y=None,
            height=dp(25)
        )
        
        container.add_widget(icon_label)
        container.add_widget(title_label)
        container.add_widget(value_label)
        
        return container
    
    def create_action_buttons(self, formula_key):
        """Membuat tombol aksi"""
        container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            spacing=Spacing.MD
        )
        
        # Tombol kalkulator
        calc_btn = OutlineButton(
            text='🧮 Calculate',
            size_hint_x=0.5,
            on_press=lambda x: self.open_calculator(formula_key)
        )
        
        # Tombol bagikan (placeholder)
        share_btn = OutlineButton(
            text='📤 Share',
            size_hint_x=0.5,
            on_press=self.share_formula
        )
        
        container.add_widget(calc_btn)
        container.add_widget(share_btn)
        
        return container
    
    def open_calculator(self, formula_key):
        """Buka kalkulator untuk rumus ini"""
        # Untuk sekarang, navigasi ke calculator screen
        self.manager.current = 'calculator'
    
    def share_formula(self, instance):
        """Bagikan rumus (placeholder)"""
        print("Share formula:", self.current_formula.get('title', ''))
    
    def toggle_favorite(self, instance):
        """Toggle status favorit"""
        if instance.text == '☆':
            instance.text = '★'
            instance.color = Colors.WARNING
            print("Added to favorites")
        else:
            instance.text = '☆'
            instance.color = Colors.DARK
            print("Removed from favorites")
    
    def go_back(self, instance):
        """Kembali ke screen sebelumnya"""
        self.manager.current = 'formulas'