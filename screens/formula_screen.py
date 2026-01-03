"""
Screen untuk menampilkan daftar rumus fisika
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.metrics import dp
from kivy.app import App

from app_ui import Colors, Fonts, Spacing
from components.cards import FormulaCard, InfoCard
from data.formulas import physics_formulas, formula_categories


class FormulaScreen(Screen):
    """Screen untuk menampilkan daftar semua rumus"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'formulas'

        # Layout utama
        main_layout = BoxLayout(
            orientation='vertical',
            padding=[0, 0, 0, 0]
        )

        # Header
        header = self.create_header()
        main_layout.add_widget(header)

        # Konten
        content = self.create_content()
        main_layout.add_widget(content)

        self.add_widget(main_layout)

        # Animasi
        Clock.schedule_once(self.animate_entrance, 0.1)

    # ========================= HEADER ==============================

    def create_header(self):
        header_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(180),
            padding=[Spacing.MD, Spacing.MD, Spacing.MD, Spacing.SM],
            spacing=Spacing.SM
        )

        # ---------- Top Bar ----------
        top_bar = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            spacing=Spacing.SM
        )

        back_btn = Button(
            text='←',
            font_size=Fonts.H3,
            size_hint_x=None,
            width=dp(50),
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=Colors.DARK
        )
        back_btn.bind(on_press=self.go_back)

        title_label = Label(
            text='Physics Formulas',
            font_size=Fonts.H2,
            bold=True,
            color=Colors.DARK
        )

        search_btn = Button(
            text='🔍',
            font_size=Fonts.H4,
            size_hint_x=None,
            width=dp(50),
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=Colors.DARK
        )

        top_bar.add_widget(back_btn)
        top_bar.add_widget(title_label)
        top_bar.add_widget(search_btn)

        # ---------- Search Bar ----------
        search_layout = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            spacing=Spacing.SM
        )

        search_input = TextInput(
            hint_text='Search formulas...',
            font_size=Fonts.BODY,
            multiline=False,
            size_hint_x=1,
            padding=[dp(15), dp(15)],
            background_normal='',
            background_active='',
            background_color=(0, 0, 0, 0),
            foreground_color=Colors.DARK
        )

        # Background search box
        with search_input.canvas.before:
            Color(*Colors.WHITE)
            search_input.rect = RoundedRectangle(
                pos=search_input.pos,
                size=search_input.size,
                radius=[Spacing.RADIUS_MD]
            )

        # Border search box
        with search_input.canvas.after:
            Color(*Colors.GRAY_LIGHT)
            search_input._border_line = Line(
                rounded_rectangle=(
                    search_input.x,
                    search_input.y,
                    search_input.width,
                    search_input.height,
                    Spacing.RADIUS_MD
                ),
                width=1
            )

        search_input.bind(pos=self.update_search_bg, size=self.update_search_bg)

        # ---------- Filter Button ----------
        filter_btn = Button(
            text='☰',
            font_size=Fonts.H4,
            size_hint_x=None,
            width=dp(50),
            background_normal='',
            color=Colors.WHITE
        )

        with filter_btn.canvas.before:
            Color(*Colors.PRIMARY)
            filter_btn.rect = RoundedRectangle(
                pos=filter_btn.pos,
                size=filter_btn.size,
                radius=[Spacing.RADIUS_MD]
            )

        filter_btn.bind(pos=self.update_filter_bg, size=self.update_filter_bg)

        search_layout.add_widget(search_input)
        search_layout.add_widget(filter_btn)

        # ---------- Tabs ----------
        categories = self.create_category_tabs()

        header_layout.add_widget(top_bar)
        header_layout.add_widget(search_layout)
        header_layout.add_widget(categories)

        return header_layout

    # ========================= CATEGORY TABS ==============================

    def create_category_tabs(self):
        scroll = ScrollView(
            size_hint_y=None,
            height=dp(60),
            do_scroll_x=True,
            do_scroll_y=False
        )

        inner = BoxLayout(
            size_hint_x=None,
            spacing=Spacing.SM
        )

        # Hitung width total
        inner.width = dp(90 * (len(formula_categories.keys()) + 1))

        all_tab = self.create_tab_button("All", True)
        all_tab.bind(on_press=lambda x: self.filter_formulas("all"))
        inner.add_widget(all_tab)

        for cat in formula_categories.keys():
            tab = self.create_tab_button(cat, False)
            tab.bind(on_press=lambda x, c=cat: self.filter_formulas(c))
            inner.add_widget(tab)

        scroll.add_widget(inner)
        return scroll

    def create_tab_button(self, text, active=False):
        btn = Button(
            text=text,
            font_size=Fonts.BODY_SMALL,
            bold=True,
            size_hint_x=None,
            width=dp(80),
            background_normal='',
            background_color=(0, 0, 0, 0),
        )

        if active:
            bg = Colors.PRIMARY
            btn.color = Colors.WHITE
        else:
            bg = Colors.GRAY_LIGHT
            btn.color = Colors.GRAY_DARK

        with btn.canvas.before:
            Color(*bg)
            btn.rect = RoundedRectangle(
                pos=btn.pos,
                size=btn.size,
                radius=[Spacing.RADIUS_MD]
            )

        btn.bind(pos=self.update_tab_bg, size=self.update_tab_bg)
        return btn

    # ========================= CONTENT ==============================

    def create_content(self):
        scroll = ScrollView(do_scroll_x=False, bar_width=dp(4))

        self.formulas_container = GridLayout(
            cols=1,
            spacing=Spacing.MD,
            size_hint_y=None,
            padding=[Spacing.MD, Spacing.MD, Spacing.MD, Spacing.XL]
        )
        self.formulas_container.bind(
            minimum_height=self.formulas_container.setter("height")
        )

        info = InfoCard(
            title=f"Total {len(physics_formulas)} Formulas",
            content="Tap on any formula to see detailed explanation",
            icon="📚"
        )
        self.formulas_container.add_widget(info)

        self.display_all_formulas()

        scroll.add_widget(self.formulas_container)
        return scroll

    def display_all_formulas(self):
        # Hapus selain info card
        if len(self.formulas_container.children) > 1:
            for child in self.formulas_container.children[1:]:
                self.formulas_container.remove_widget(child)

        for category, formula_keys in formula_categories.items():
            header = BoxLayout(
                size_hint_y=None,
                height=dp(50),
                spacing=Spacing.SM
            )

            line = Widget(size_hint_x=None, width=dp(4))
            with line.canvas:
                Color(*Colors.PRIMARY)
                line.rect = RoundedRectangle(
                    pos=line.pos,
                    size=line.size,
                    radius=[dp(2)]
                )
            line.bind(pos=self.update_line_bg, size=self.update_line_bg)

            label = Label(
                text=category,
                font_size=Fonts.H4,
                bold=True,
                color=Colors.DARK,
                size_hint_x=1,
                halign='left'
            )
            label.bind(size=label.setter("text_size"))

            count = Label(
                text=f"{len(formula_keys)}",
                font_size=Fonts.BODY_SMALL,
                color=Colors.GRAY,
                size_hint_x=None,
                width=dp(40)
            )

            header.add_widget(line)
            header.add_widget(label)
            header.add_widget(count)

            self.formulas_container.add_widget(header)

            for key in formula_keys:
                data = physics_formulas.get(key, {})
                card = FormulaCard(
                    title=data.get("title", ""),
                    formula=data.get("formula", ""),
                    category=data.get("category", ""),
                    on_press=lambda x, k=key: self.show_formula_detail(k)
                )
                self.formulas_container.add_widget(card)

    # ========================= ACTIONS ==============================

    def filter_formulas(self, category):
        print("Filter:", category)
        self.display_all_formulas()

    def show_formula_detail(self, key):
        App.get_running_app().show_formula_detail(key)

    def go_back(self, instance):
        self.manager.current = 'home'

    def animate_entrance(self, dt):
    # Set semua widget jadi transparan dulu
     for child in self.formulas_container.children:
        if hasattr(child, "opacity"):
            child.opacity = 0

    # Lalu animasikan satu-satu dengan jeda
     for i, child in enumerate(reversed(self.formulas_container.children)):
        anim = Animation(opacity=1, duration=0.3)

        Clock.schedule_once(
            lambda t, a=anim, c=child: a.start(c),
            i * 0.05
        )


    # ========================= UPDATE BACKGROUND ==============================

    def update_search_bg(self, instance, value):
      instance.rect.pos = instance.pos
      instance.rect.size = instance.size
      instance._border_line.rounded_rectangle = (
          instance.x,
           instance.y,
         instance.width,
           instance.height,
          Spacing.RADIUS_MD
        )


    def update_filter_bg(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def update_tab_bg(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def update_line_bg(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size
