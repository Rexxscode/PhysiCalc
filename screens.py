"""
File berisi semua screen/layar aplikasi
Menggunakan Kivy untuk UI
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.stacklayout import StackLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.clock import Clock

# Impor data rumus
from rumus_data import physics_formulas, formula_categories


class CustomButton(Button):
    """Tombol kustom dengan styling yang lebih baik"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)  # Transparan
        self.background_normal = ''
        self.font_size = sp(16)
        self.bold = True
        self.color = get_color_from_hex('#ffffff')
        
        # Atur padding dan ukuran
        self.padding = (dp(20), dp(15))
        self.size_hint_y = None
        self.height = dp(60)


class FormulaCard(BoxLayout):
    """Card untuk menampilkan setiap rumus dalam daftar"""
    
    formula_key = StringProperty()
    
    def __init__(self, formula_key, **kwargs):
        super().__init__(**kwargs)
        self.formula_key = formula_key
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(100)
        self.padding = dp(15)
        self.spacing = dp(5)
        
        # Ambil data rumus
        formula_data = physics_formulas.get(formula_key, {})
        
        # Tambahkan judul
        title_label = Label(
            text=formula_data.get('title', ''),
            font_size=sp(18),
            bold=True,
            color=get_color_from_hex('#2c3e50'),
            size_hint_y=None,
            height=dp(30)
        )
        
        # Tambahkan rumus
        formula_label = Label(
            text=formula_data.get('formula', ''),
            font_size=sp(22),
            bold=True,
            color=get_color_from_hex('#3498db'),
            size_hint_y=None,
            height=dp(40)
        )
        
        # Tambahkan kategori
        category_label = Label(
            text=f"Category: {formula_data.get('category', '')}",
            font_size=sp(14),
            color=get_color_from_hex('#7f8c8d'),
            size_hint_y=None,
            height=dp(20)
        )
        
        self.add_widget(title_label)
        self.add_widget(formula_label)
        self.add_widget(category_label)
        
        # Tambahkan background rounded rectangle
        with self.canvas.before:
            Color(rgba=get_color_from_hex('#ffffff'))
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
        
        # Binding untuk update posisi dan ukuran
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, *args):
        """Update posisi dan ukuran rounded rectangle"""
        self.rect.pos = self.pos
        self.rect.size = self.size


class HomeScreen(Screen):
    """Screen utama/beranda aplikasi"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Layout utama
        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        # Header dengan judul
        header_layout = BoxLayout(orientation='vertical', size_hint_y=0.3)
        
        # Logo/title image placeholder
        title_image = Label(
            text='🧬',
            font_size=sp(80),
            size_hint_y=0.7
        )
        
        app_title = Label(
            text='Physics Formulas SMP',
            font_size=sp(32),
            bold=True,
            color=get_color_from_hex('#2c3e50')
        )
        
        app_subtitle = Label(
            text='Complete Junior High School Physics Formulas',
            font_size=sp(16),
            color=get_color_from_hex('#7f8c8d')
        )
        
        header_layout.add_widget(title_image)
        header_layout.add_widget(app_title)
        header_layout.add_widget(app_subtitle)
        
        # Menu pilihan
        menu_layout = BoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=0.6)
        
        # Tombol daftar rumus
        btn_formulas = CustomButton(text='📚 Formula List')
        btn_formulas.background_color = get_color_from_hex('#3498db')
        btn_formulas.bind(on_press=self.go_to_formulas)
        
        # Tombol kalkulator
        btn_calculator = CustomButton(text='🧮 Formula Calculator')
        btn_calculator.background_color = get_color_from_hex('#2ecc71')
        btn_calculator.bind(on_press=self.go_to_calculator)
        
        # Footer
        footer_label = Label(
            text='v1.0 • Made with Kivy',
            font_size=sp(14),
            color=get_color_from_hex('#95a5a6'),
            size_hint_y=0.1
        )
        
        # Tambahkan semua widget ke layout
        menu_layout.add_widget(btn_formulas)
        menu_layout.add_widget(btn_calculator)
        
        main_layout.add_widget(header_layout)
        main_layout.add_widget(menu_layout)
        main_layout.add_widget(footer_label)
        
        self.add_widget(main_layout)
    
    def go_to_formulas(self, instance):
        """Navigasi ke layar daftar rumus"""
        self.manager.current = 'formula_list'
    
    def go_to_calculator(self, instance):
        """Navigasi ke layar kalkulator"""
        self.manager.current = 'calculator'


class FormulaListScreen(Screen):
    """Screen untuk menampilkan daftar rumus"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Layout utama
        main_layout = BoxLayout(orientation='vertical')
        
        # Header dengan tombol kembali
        header = BoxLayout(size_hint_y=0.12, padding=[dp(10), dp(5), dp(10), dp(5)])
        
        back_btn = Button(
            text='← Back',
            size_hint_x=0.3,
            background_color=get_color_from_hex('#34495e'),
            color=get_color_from_hex('#ffffff'),
            bold=True
        )
        back_btn.bind(on_press=self.go_back)
        
        title_label = Label(
            text='Formula List',
            font_size=sp(24),
            bold=True,
            color=get_color_from_hex('#2c3e50')
        )
        
        header.add_widget(back_btn)
        header.add_widget(title_label)
        
        # ScrollView untuk daftar rumus
        scroll = ScrollView()
        
        # Container untuk daftar rumus
        formulas_container = GridLayout(
            cols=1,
            spacing=dp(15),
            size_hint_y=None,
            padding=dp(20)
        )
        formulas_container.bind(minimum_height=formulas_container.setter('height'))
        
        # Tambahkan rumus berdasarkan kategori
        for category, formula_keys in formula_categories.items():
            # Label kategori
            category_label = Label(
                text=category,
                font_size=sp(20),
                bold=True,
                color=get_color_from_hex('#2c3e50'),
                size_hint_y=None,
                height=dp(40)
            )
            formulas_container.add_widget(category_label)
            
            # Tambahkan rumus dalam kategori ini
            for formula_key in formula_keys:
                # Buat card untuk setiap rumus
                card = FormulaCard(formula_key=formula_key)
                
                # Tambahkan tombol transparan di atas card untuk interaksi
                card_button = Button(
                    size_hint_y=None,
                    height=dp(100),
                    background_color=(0, 0, 0, 0),
                    background_normal=''
                )
                card_button.formula_key = formula_key
                card_button.bind(on_press=self.show_formula_detail)
                
                # Stack card dan button
                card_stack = StackLayout()
                card_stack.add_widget(card)
                card_stack.add_widget(card_button)
                
                formulas_container.add_widget(card_stack)
        
        scroll.add_widget(formulas_container)
        
        # Tambahkan semua ke layout utama
        main_layout.add_widget(header)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def go_back(self, instance):
        """Kembali ke home screen"""
        self.manager.current = 'home'
    
    def show_formula_detail(self, instance):
        """Menampilkan detail rumus"""
        app = App.get_running_app()
        app.show_formula_detail(instance.formula_key)


class FormulaDetailScreen(Screen):
    """Screen untuk menampilkan detail rumus"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Layout utama
        self.main_layout = BoxLayout(orientation='vertical')
        
        # Header dengan tombol kembali
        header = BoxLayout(size_hint_y=0.12, padding=[dp(10), dp(5), dp(10), dp(5)])
        
        self.back_btn = Button(
            text='← Back',
            size_hint_x=0.3,
            background_color=get_color_from_hex('#34495e'),
            color=get_color_from_hex('#ffffff'),
            bold=True
        )
        self.back_btn.bind(on_press=self.go_back)
        
        self.title_label = Label(
            text='Formula Detail',
            font_size=sp(24),
            bold=True,
            color=get_color_from_hex('#2c3e50')
        )
        
        header.add_widget(self.back_btn)
        header.add_widget(self.title_label)
        
        # Container untuk konten
        self.content_scroll = ScrollView()
        self.content_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(20),
            spacing=dp(15)
        )
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))
        
        self.content_scroll.add_widget(self.content_layout)
        
        # Tambahkan semua ke layout utama
        self.main_layout.add_widget(header)
        self.main_layout.add_widget(self.content_scroll)
        
        self.add_widget(self.main_layout)
    
    def display_formula(self, formula_key):
        """Menampilkan detail rumus berdasarkan kunci"""
        # Hapus konten sebelumnya
        self.content_layout.clear_widgets()
        
        # Ambil data rumus
        formula_data = App.get_running_app().formula_data.get(formula_key, {})
        
        # Atur judul
        self.title_label.text = formula_data.get('title', 'Formula Detail')
        
        # Card untuk menampilkan rumus utama
        formula_card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=dp(20),
            spacing=dp(10)
        )
        
        # Tambahkan rumus
        formula_label = Label(
            text=formula_data.get('formula', ''),
            font_size=sp(32),
            bold=True,
            color=get_color_from_hex('#3498db')
        )
        
        # Tambahkan judul
        title_label = Label(
            text=formula_data.get('title', ''),
            font_size=sp(24),
            bold=True,
            color=get_color_from_hex('#2c3e50')
        )
        
        formula_card.add_widget(title_label)
        formula_card.add_widget(formula_label)
        
        # Tambahkan background ke card
        with formula_card.canvas.before:
            Color(rgba=get_color_from_hex('#ecf0f1'))
            self.formula_rect = RoundedRectangle(
                pos=formula_card.pos, 
                size=formula_card.size, 
                radius=[dp(15)]
            )
        
        formula_card.bind(pos=self.update_formula_rect, size=self.update_formula_rect)
        
        # Tambahkan card ke layout
        self.content_layout.add_widget(formula_card)
        
        # Deskripsi
        desc_card = self.create_card(
            title="Description",
            content=formula_data.get('description', ''),
            color=get_color_from_hex('#ffffff')
        )
        self.content_layout.add_widget(desc_card)
        
        # Variabel dan satuan
        variables_card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(50 + len(formula_data.get('variables', [])) * dp(40)),
            padding=dp(15),
            spacing=dp(10)
        )
        
        variables_title = Label(
            text="Variables and Units",
            font_size=sp(18),
            bold=True,
            color=get_color_from_hex('#2c3e50'),
            size_hint_y=None,
            height=dp(30)
        )
        variables_card.add_widget(variables_title)
        
        # Tambahkan setiap variabel
        for var in formula_data.get('variables', []):
            var_layout = BoxLayout(size_hint_y=None, height=dp(30))
            
            symbol_label = Label(
                text=f"{var.get('symbol', '')}:",
                font_size=sp(16),
                bold=True,
                color=get_color_from_hex('#e74c3c'),
                size_hint_x=0.2
            )
            
            name_label = Label(
                text=var.get('name', ''),
                font_size=sp(16),
                color=get_color_from_hex('#2c3e50'),
                size_hint_x=0.5
            )
            
            unit_label = Label(
                text=f"[{var.get('unit', '')}]",
                font_size=sp(14),
                color=get_color_from_hex('#7f8c8d'),
                size_hint_x=0.3
            )
            
            var_layout.add_widget(symbol_label)
            var_layout.add_widget(name_label)
            var_layout.add_widget(unit_label)
            variables_card.add_widget(var_layout)
        
        # Background untuk card variabel
        with variables_card.canvas.before:
            Color(rgba=get_color_from_hex('#ffffff'))
            self.var_rect = RoundedRectangle(
                pos=variables_card.pos, 
                size=variables_card.size, 
                radius=[dp(10)]
            )
        
        variables_card.bind(pos=self.update_var_rect, size=self.update_var_rect)
        self.content_layout.add_widget(variables_card)
        
        # Contoh
        example_card = self.create_card(
            title="Example",
            content=formula_data.get('example', ''),
            color=get_color_from_hex('#ffffff')
        )
        self.content_layout.add_widget(example_card)
        
        # Kategori
        category_card = self.create_card(
            title="Category",
            content=formula_data.get('category', ''),
            color=get_color_from_hex('#3498db'),
            text_color='#ffffff'
        )
        self.content_layout.add_widget(category_card)
    
    def create_card(self, title, content, color='#ffffff', text_color='#2c3e50'):
        """Membuat card dengan konten"""
        card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(15),
            spacing=dp(10)
        )
        
        # Hitung tinggi berdasarkan konten
        content_lines = content.count('\n') + 1
        card.height = dp(50 + content_lines * 20)
        
        # Judul card
        title_label = Label(
            text=title,
            font_size=sp(18),
            bold=True,
            color=get_color_from_hex(text_color),
            size_hint_y=None,
            height=dp(30)
        )
        
        # Konten card
        content_label = Label(
            text=content,
            font_size=sp(16),
            color=get_color_from_hex(text_color),
            halign='left',
            valign='top'
        )
        content_label.bind(size=content_label.setter('text_size'))
        
        card.add_widget(title_label)
        card.add_widget(content_label)
        
        # Background
        with card.canvas.before:
            Color(rgba=get_color_from_hex(color))
            rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(10)])
        
        # Binding untuk update background
        def update_card_rect(instance, value):
            rect.pos = instance.pos
            rect.size = instance.size
        
        card.bind(pos=update_card_rect, size=update_card_rect)
        
        return card
    
    def update_formula_rect(self, instance, value):
        """Update background untuk formula card"""
        self.formula_rect.pos = instance.pos
        self.formula_rect.size = instance.size
    
    def update_var_rect(self, instance, value):
        """Update background untuk variables card"""
        self.var_rect.pos = instance.pos
        self.var_rect.size = instance.size
    
    def go_back(self, instance):
        """Kembali ke daftar rumus"""
        self.manager.current = 'formula_list'


class CalculatorScreen(Screen):
    """Screen untuk kalkulator rumus"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Layout utama
        main_layout = BoxLayout(orientation='vertical')
        
        # Header dengan tombol kembali
        header = BoxLayout(size_hint_y=0.12, padding=[dp(10), dp(5), dp(10), dp(5)])
        
        back_btn = Button(
            text='← Back',
            size_hint_x=0.3,
            background_color=get_color_from_hex('#34495e'),
            color=get_color_from_hex('#ffffff'),
            bold=True
        )
        back_btn.bind(on_press=self.go_back)
        
        title_label = Label(
            text='Formula Calculator',
            font_size=sp(24),
            bold=True,
            color=get_color_from_hex('#2c3e50')
        )
        
        header.add_widget(back_btn)
        header.add_widget(title_label)
        
        # ScrollView untuk konten
        scroll = ScrollView()
        
        # Container untuk kalkulator
        calculator_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(20),
            spacing=dp(20)
        )
        calculator_container.bind(minimum_height=calculator_container.setter('height'))
        
        # Deskripsi kalkulator
        desc_label = Label(
            text='Calculate physics formulas instantly. Enter values and get results with units.',
            font_size=sp(16),
            color=get_color_from_hex('#7f8c8d'),
            halign='center',
            size_hint_y=None,
            height=dp(50)
        )
        desc_label.bind(size=desc_label.setter('text_size'))
        
        calculator_container.add_widget(desc_label)
        
        # Kalkulator Kecepatan
        velocity_calc = self.create_calculator(
            title='Velocity Calculator',
            formula='v = s / t',
            inputs=[
                {'label': 'Displacement (s)', 'unit': 'm', 'hint': 'Enter distance in meters'},
                {'label': 'Time (t)', 'unit': 's', 'hint': 'Enter time in seconds'}
            ],
            output={'label': 'Velocity (v)', 'unit': 'm/s'},
            calculation_func=self.calculate_velocity
        )
        calculator_container.add_widget(velocity_calc)
        
        # Kalkulator Gaya
        force_calc = self.create_calculator(
            title='Force Calculator',
            formula='F = m × a',
            inputs=[
                {'label': 'Mass (m)', 'unit': 'kg', 'hint': 'Enter mass in kilograms'},
                {'label': 'Acceleration (a)', 'unit': 'm/s²', 'hint': 'Enter acceleration in m/s²'}
            ],
            output={'label': 'Force (F)', 'unit': 'N'},
            calculation_func=self.calculate_force
        )
        calculator_container.add_widget(force_calc)
        
        # Kalkulator Tekanan
        pressure_calc = self.create_calculator(
            title='Pressure Calculator',
            formula='P = F / A',
            inputs=[
                {'label': 'Force (F)', 'unit': 'N', 'hint': 'Enter force in Newtons'},
                {'label': 'Area (A)', 'unit': 'm²', 'hint': 'Enter area in m²'}
            ],
            output={'label': 'Pressure (P)', 'unit': 'Pa'},
            calculation_func=self.calculate_pressure
        )
        calculator_container.add_widget(pressure_calc)
        
        # Informasi
        info_label = Label(
            text='Note: All calculations use standard SI units.\nEnter positive numbers only.',
            font_size=sp(14),
            color=get_color_from_hex('#95a5a6'),
            halign='center',
            size_hint_y=None,
            height=dp(60)
        )
        info_label.bind(size=info_label.setter('text_size'))
        
        calculator_container.add_widget(info_label)
        
        scroll.add_widget(calculator_container)
        
        # Tambahkan semua ke layout utama
        main_layout.add_widget(header)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def create_calculator(self, title, formula, inputs, output, calculation_func):
        """Membuat UI untuk kalkulator"""
        calculator = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(300),
            padding=dp(15),
            spacing=dp(10)
        )
        
        # Background untuk kalkulator
        with calculator.canvas.before:
            Color(rgba=get_color_from_hex('#ffffff'))
            self.calc_rect = RoundedRectangle(
                pos=calculator.pos, 
                size=calculator.size, 
                radius=[dp(15)]
            )
        
        calculator.bind(pos=self.update_calc_rect, size=self.update_calc_rect)
        
        # Judul kalkulator
        title_label = Label(
            text=title,
            font_size=sp(20),
            bold=True,
            color=get_color_from_hex('#2c3e50'),
            size_hint_y=None,
            height=dp(30)
        )
        
        # Rumus
        formula_label = Label(
            text=formula,
            font_size=sp(24),
            bold=True,
            color=get_color_from_hex('#3498db'),
            size_hint_y=None,
            height=dp(40)
        )
        
        calculator.add_widget(title_label)
        calculator.add_widget(formula_label)
        
        # Container untuk input
        input_container = GridLayout(
            cols=2,
            spacing=dp(10),
            size_hint_y=None,
            height=dp(100)
        )
        
        # Dictionary untuk menyimpan reference ke TextInput
        input_fields = {}
        
        # Tambahkan input fields
        for i, inp in enumerate(inputs):
            # Label
            input_label = Label(
                text=f"{inp['label']}:",
                font_size=sp(16),
                color=get_color_from_hex('#2c3e50'),
                halign='right',
                size_hint_x=0.6
            )
            input_label.bind(size=input_label.setter('text_size'))
            
            # TextInput
            text_input = TextInput(
                hint_text=inp['hint'],
                font_size=sp(16),
                multiline=False,
                input_filter='float',
                size_hint_x=0.4
            )
            
            # Simpan reference dengan kunci
            key = inp['label'].split(' ')[0].lower().strip('()')
            input_fields[key] = text_input
            
            input_container.add_widget(input_label)
            input_container.add_widget(text_input)
        
        calculator.input_fields = input_fields
        calculator.add_widget(input_container)
        
        # Tombol hitung
        calculate_btn = Button(
            text='Calculate',
            size_hint_y=None,
            height=dp(50),
            background_color=get_color_from_hex('#2ecc71'),
            color=get_color_from_hex('#ffffff'),
            bold=True
        )
        
        # Label hasil
        result_label = Label(
            text=f"{output['label']}: -- {output['unit']}",
            font_size=sp(18),
            bold=True,
            color=get_color_from_hex('#e74c3c'),
            size_hint_y=None,
            height=dp(40)
        )
        
        calculator.result_label = result_label
        calculator.add_widget(calculate_btn)
        calculator.add_widget(result_label)
        
        # Binding fungsi kalkulasi
        def on_calculate(instance):
            calculation_func(calculator)
        
        calculate_btn.bind(on_press=on_calculate)
        
        return calculator
    
    def update_calc_rect(self, instance, value):
        """Update background untuk calculator"""
        self.calc_rect.pos = instance.pos
        self.calc_rect.size = instance.size
    
    def calculate_velocity(self, calculator):
        """Menghitung kecepatan v = s / t"""
        try:
            # Ambil nilai dari input fields
            s_text = calculator.input_fields.get('displacement', TextInput()).text
            t_text = calculator.input_fields.get('time', TextInput()).text
            
            # Validasi input
            if not s_text or not t_text:
                calculator.result_label.text = "Velocity (v): Please enter both values"
                calculator.result_label.color = get_color_from_hex('#e74c3c')
                return
            
            s = float(s_text)
            t = float(t_text)
            
            if t == 0:
                calculator.result_label.text = "Velocity (v): Time cannot be zero"
                calculator.result_label.color = get_color_from_hex('#e74c3c')
                return
            
            # Hitung kecepatan
            v = s / t
            
            # Tampilkan hasil
            calculator.result_label.text = f"Velocity (v): {v:.2f} m/s"
            calculator.result_label.color = get_color_from_hex('#27ae60')
            
        except ValueError:
            calculator.result_label.text = "Velocity (v): Invalid input"
            calculator.result_label.color = get_color_from_hex('#e74c3c')
    
    def calculate_force(self, calculator):
        """Menghitung gaya F = m × a"""
        try:
            # Ambil nilai dari input fields
            m_text = calculator.input_fields.get('mass', TextInput()).text
            a_text = calculator.input_fields.get('acceleration', TextInput()).text
            
            # Validasi input
            if not m_text or not a_text:
                calculator.result_label.text = "Force (F): Please enter both values"
                calculator.result_label.color = get_color_from_hex('#e74c3c')
                return
            
            m = float(m_text)
            a = float(a_text)
            
            # Hitung gaya
            F = m * a
            
            # Tampilkan hasil
            calculator.result_label.text = f"Force (F): {F:.2f} N"
            calculator.result_label.color = get_color_from_hex('#27ae60')
            
        except ValueError:
            calculator.result_label.text = "Force (F): Invalid input"
            calculator.result_label.color = get_color_from_hex('#e74c3c')
    
    def calculate_pressure(self, calculator):
        """Menghitung tekanan P = F / A"""
        try:
            # Ambil nilai dari input fields
            f_text = calculator.input_fields.get('force', TextInput()).text
            a_text = calculator.input_fields.get('area', TextInput()).text
            
            # Validasi input
            if not f_text or not a_text:
                calculator.result_label.text = "Pressure (P): Please enter both values"
                calculator.result_label.color = get_color_from_hex('#e74c3c')
                return
            
            F = float(f_text)
            A = float(a_text)
            
            if A == 0:
                calculator.result_label.text = "Pressure (P): Area cannot be zero"
                calculator.result_label.color = get_color_from_hex('#e74c3c')
                return
            
            # Hitung tekanan
            P = F / A
            
            # Tampilkan hasil
            calculator.result_label.text = f"Pressure (P): {P:.2f} Pa"
            calculator.result_label.color = get_color_from_hex('#27ae60')
            
        except ValueError:
            calculator.result_label.text = "Pressure (P): Invalid input"
            calculator.result_label.color = get_color_from_hex('#e74c3c')
    
    def go_back(self, instance):
        """Kembali ke home screen"""
        self.manager.current = 'home'