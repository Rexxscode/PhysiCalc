"""
Screen untuk kalkulator fisika
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.metrics import dp, sp
from kivy.app import App

from app_ui import Colors, Fonts, Spacing
from components.buttons import PrimaryButton, OutlineButton
from components.cards import Card, InfoCard
from utils import (
    calculate_velocity, calculate_force, calculate_pressure,
    calculate_work, calculate_kinetic_energy, calculate_potential_energy,
    calculate_density, calculate_power, format_result
)

class CalculatorScreen(Screen):
    """Screen untuk kalkulator rumus fisika"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'calculator'
        
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
        
        # State
        self.current_formula = 'velocity'
        self.input_values = {}
        self.result = None
        
        # Animasi saat screen muncul
        Clock.schedule_once(self.animate_entrance, 0.1)
    
    def create_header(self):
        """Membuat header dengan pemilih rumus"""
        header_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(180),
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
        back_btn = Button(
            text='←',
            font_size=Fonts.H3,
            size_hint_x=None,
            width=dp(50),
            background_color=(0, 0, 0, 0),
            background_normal='',
            color=Colors.DARK
        )
        back_btn.bind(on_press=self.go_back)
        
        # Judul
        title_label = Label(
            text='Physics Calculator',
            font_size=Fonts.H2,
            bold=True,
            color=Colors.DARK,
            size_hint_x=1
        )
        
        # Tombol reset
        reset_btn = Button(
            text='↻',
            font_size=Fonts.H4,
            size_hint_x=None,
            width=dp(50),
            background_color=(0, 0, 0, 0),
            background_normal='',
            color=Colors.DARK
        )
        reset_btn.bind(on_press=self.reset_calculator)
        
        top_bar.add_widget(back_btn)
        top_bar.add_widget(title_label)
        top_bar.add_widget(reset_btn)
        
        # Pemilih rumus
        formula_picker = self.create_formula_picker()
        
        # Kartu rumus aktif
        self.active_formula_card = self.create_active_formula_card()
        
        header_layout.add_widget(top_bar)
        header_layout.add_widget(formula_picker)
        header_layout.add_widget(self.active_formula_card)
        
        return header_layout
    
    def create_formula_picker(self):
        """Membuat pemilih rumus"""
        picker_layout = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            spacing=Spacing.SM
        )
        
        # Label
        label = Label(
            text='Formula:',
            font_size=Fonts.BODY,
            bold=True,
            color=Colors.DARK,
            size_hint_x=None,
            width=dp(80)
        )
        
        # Dropdown container
        dropdown_container = BoxLayout(
            size_hint_x=1,
            spacing=Spacing.XS
        )
        
        # Tombol dropdown
        self.formula_btn = Button(
            text='Velocity (v = s/t)',
            font_size=Fonts.BODY,
            background_color=Colors.WHITE,
            color=Colors.DARK,
            background_normal=''
        )
        
        # Background untuk tombol dropdown
        with self.formula_btn.canvas.before:
            Color(*Colors.GRAY_LIGHT)
            self.formula_btn.rect = RoundedRectangle(
                pos=self.formula_btn.pos,
                size=self.formula_btn.size,
                radius=[Spacing.RADIUS_MD]
            )
        
        # Border untuk tombol dropdown
        with self.formula_btn.canvas:
            Color(*Colors.GRAY)
            self.formula_btn._border_line = Line(
                rounded_rectangle=(self.formula_btn.x, self.formula_btn.y,
                                  self.formula_btn.width, self.formula_btn.height,
                                  Spacing.RADIUS_MD),
                width=1
            )
        
        self.formula_btn.bind(
            pos=self.update_formula_btn_bg,
            size=self.update_formula_btn_bg,
            on_press=self.show_formula_dropdown
        )
        
        dropdown_container.add_widget(self.formula_btn)
        picker_layout.add_widget(label)
        picker_layout.add_widget(dropdown_container)
        
        return picker_layout
    
    def create_active_formula_card(self):
        """Membuat kartu untuk rumus yang aktif"""
        card = Card(
            padding=Spacing.MD,
            spacing=Spacing.XS,
            size_hint_y=None,
            height=dp(80)
        )
        
        # Rumus besar
        self.formula_display = Label(
            text='v = s / t',
            font_size=Fonts.H3,
            bold=True,
            color=Colors.PRIMARY,
            size_hint_y=None,
            height=dp(40)
        )
        
        # Deskripsi
        self.formula_desc = Label(
            text='Velocity = Displacement ÷ Time',
            font_size=Fonts.BODY_SMALL,
            color=Colors.GRAY_DARK,
            size_hint_y=None,
            height=dp(20)
        )
        
        card.add_widget(self.formula_display)
        card.add_widget(self.formula_desc)
        
        return card
    
    def create_content(self):
        """Membuat konten kalkulator"""
        scroll = ScrollView(
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
        
        # Input fields (akan diupdate berdasarkan rumus)
        self.input_section = self.create_input_section()
        self.content_container.add_widget(self.input_section)
        
        # Tombol hitung
        self.calculate_section = self.create_calculate_section()
        self.content_container.add_widget(self.calculate_section)
        
        # Hasil
        self.result_section = self.create_result_section()
        self.content_container.add_widget(self.result_section)
        
        # Info
        info_section = self.create_info_section()
        self.content_container.add_widget(info_section)
        
        scroll.add_widget(self.content_container)
        return scroll
    
    def create_input_section(self):
        """Membuat section input fields"""
        section = Card(
            padding=Spacing.MD,
            spacing=Spacing.MD,
            size_hint_y=None,
            height=dp(200)
        )
        
        # Title
        title = Label(
            text='Input Values',
            font_size=Fonts.H5,
            bold=True,
            color=Colors.DARK,
            size_hint_y=None,
            height=dp(30)
        )
        
        # Input fields container
        self.input_container = GridLayout(
            cols=2,
            spacing=Spacing.MD,
            size_hint_y=None,
            height=dp(140)
        )
        
        # Input fields untuk velocity (default)
        self.create_velocity_inputs()
        
        section.add_widget(title)
        section.add_widget(self.input_container)
        
        return section
    
    def create_calculate_section(self):
        """Membuat section tombol hitung"""
        section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(100),
            spacing=Spacing.MD
        )
        
        # Tombol hitung
        self.calculate_btn = PrimaryButton(
            text='Calculate',
            size_hint_y=None,
            height=dp(50),
            on_press=self.calculate
        )
        
        # Tombol clear
        clear_btn = OutlineButton(
            text='Clear Inputs',
            size_hint_y=None,
            height=dp(40),
            on_press=self.clear_inputs
        )
        
        section.add_widget(self.calculate_btn)
        section.add_widget(clear_btn)
        
        return section
    
    def create_result_section(self):
        """Membuat section hasil"""
        section = Card(
            padding=Spacing.LG,
            spacing=Spacing.SM,
            size_hint_y=None,
            height=dp(150)
        )
        
        # Title
        title = Label(
            text='Result',
            font_size=Fonts.H5,
            bold=True,
            color=Colors.DARK,
            size_hint_y=None,
            height=dp(30)
        )
        
        # Result display
        self.result_label = Label(
            text='--',
            font_size=Fonts.H1,
            bold=True,
            color=Colors.PRIMARY,
            size_hint_y=None,
            height=dp(60)
        )
        
        # Unit
        self.unit_label = Label(
            text='',
            font_size=Fonts.BODY,
            color=Colors.GRAY_DARK,
            size_hint_y=None,
            height=dp(30)
        )
        
        section.add_widget(title)
        section.add_widget(self.result_label)
        section.add_widget(self.unit_label)
        
        return section
    
    def create_info_section(self):
        """Membuat section informasi"""
        section = InfoCard(
            title='How to Use',
            content='1. Select a formula from the dropdown\n2. Enter values in the input fields\n3. Click Calculate to get the result',
            icon='💡'
        )
        
        return section
    
    def create_velocity_inputs(self):
        """Membuat input fields untuk rumus kecepatan"""
        self.input_container.clear_widgets()
        
        # Displacement
        displacement_label = Label(
            text='Displacement (s):',
            font_size=Fonts.BODY,
            color=Colors.DARK,
            halign='right',
            size_hint_x=0.6
        )
        displacement_label.bind(size=displacement_label.setter('text_size'))
        
        self.displacement_input = self.create_number_input('0', 'm')
        
        # Time
        time_label = Label(
            text='Time (t):',
            font_size=Fonts.BODY,
            color=Colors.DARK,
            halign='right',
            size_hint_x=0.6
        )
        time_label.bind(size=time_label.setter('text_size'))
        
        self.time_input = self.create_number_input('0', 's')
        
        self.input_container.add_widget(displacement_label)
        self.input_container.add_widget(self.displacement_input)
        self.input_container.add_widget(time_label)
        self.input_container.add_widget(self.time_input)
    
    def create_force_inputs(self):
        """Membuat input fields untuk rumus gaya"""
        self.input_container.clear_widgets()
        
        # Mass
        mass_label = Label(
            text='Mass (m):',
            font_size=Fonts.BODY,
            color=Colors.DARK,
            halign='right',
            size_hint_x=0.6
        )
        mass_label.bind(size=mass_label.setter('text_size'))
        
        self.mass_input = self.create_number_input('0', 'kg')
        
        # Acceleration
        accel_label = Label(
            text='Acceleration (a):',
            font_size=Fonts.BODY,
            color=Colors.DARK,
            halign='right',
            size_hint_x=0.6
        )
        accel_label.bind(size=accel_label.setter('text_size'))
        
        self.accel_input = self.create_number_input('0', 'm/s²')
        
        self.input_container.add_widget(mass_label)
        self.input_container.add_widget(self.mass_input)
        self.input_container.add_widget(accel_label)
        self.input_container.add_widget(self.accel_input)
    
    def create_pressure_inputs(self):
        """Membuat input fields untuk rumus tekanan"""
        self.input_container.clear_widgets()
        
        # Force
        force_label = Label(
            text='Force (F):',
            font_size=Fonts.BODY,
            color=Colors.DARK,
            halign='right',
            size_hint_x=0.6
        )
        force_label.bind(size=force_label.setter('text_size'))
        
        self.force_input = self.create_number_input('0', 'N')
        
        # Area
        area_label = Label(
            text='Area (A):',
            font_size=Fonts.BODY,
            color=Colors.DARK,
            halign='right',
            size_hint_x=0.6
        )
        area_label.bind(size=area_label.setter('text_size'))
        
        self.area_input = self.create_number_input('0', 'm²')
        
        self.input_container.add_widget(force_label)
        self.input_container.add_widget(self.force_input)
        self.input_container.add_widget(area_label)
        self.input_container.add_widget(self.area_input)
    
    def create_work_inputs(self):
        """Membuat input fields untuk rumus kerja"""
        self.input_container.clear_widgets()
        
        # Force
        force_label = Label(
            text='Force (F):',
            font_size=Fonts.BODY,
            color=Colors.DARK,
            halign='right',
            size_hint_x=0.6
        )
        force_label.bind(size=force_label.setter('text_size'))
        
        self.force_input = self.create_number_input('0', 'N')
        
        # Displacement
        displacement_label = Label(
            text='Displacement (s):',
            font_size=Fonts.BODY,
            color=Colors.DARK,
            halign='right',
            size_hint_x=0.6
        )
        displacement_label.bind(size=displacement_label.setter('text_size'))
        
        self.displacement_input = self.create_number_input('0', 'm')
        
        self.input_container.add_widget(force_label)
        self.input_container.add_widget(self.force_input)
        self.input_container.add_widget(displacement_label)
        self.input_container.add_widget(self.displacement_input)
    
    def create_kinetic_energy_inputs(self):
        """Membuat input fields untuk rumus energi kinetik"""
        self.input_container.clear_widgets()
        
        # Mass
        mass_label = Label(
            text='Mass (m):',
            font_size=Fonts.BODY,
            color=Colors.DARK,
            halign='right',
            size_hint_x=0.6
        )
        mass_label.bind(size=mass_label.setter('text_size'))
        
        self.mass_input = self.create_number_input('0', 'kg')
        
        # Velocity
        velocity_label = Label(
            text='Velocity (v):',
            font_size=Fonts.BODY,
            color=Colors.DARK,
            halign='right',
            size_hint_x=0.6
        )
        velocity_label.bind(size=velocity_label.setter('text_size'))
        
        self.velocity_input = self.create_number_input('0', 'm/s')
        
        self.input_container.add_widget(mass_label)
        self.input_container.add_widget(self.mass_input)
        self.input_container.add_widget(velocity_label)
        self.input_container.add_widget(self.velocity_input)
    
    def create_potential_energy_inputs(self):
        """Membuat input fields untuk rumus energi potensial"""
        self.input_container.clear_widgets()
        
        # Mass
        mass_label = Label(
            text='Mass (m):',
            font_size=Fonts.BODY,
            color=Colors.DARK,
            halign='right',
            size_hint_x=0.6
        )
        mass_label.bind(size=mass_label.setter('text_size'))
        
        self.mass_input = self.create_number_input('0', 'kg')
        
        # Height
        height_label = Label(
            text='Height (h):',
            font_size=Fonts.BODY,
            color=Colors.DARK,
            halign='right',
            size_hint_x=0.6
        )
        height_label.bind(size=height_label.setter('text_size'))
        
        self.height_input = self.create_number_input('0', 'm')
        
        # Gravity (konstan, 9.8 m/s²)
        gravity_label = Label(
            text='Gravity (g):',
            font_size=Fonts.BODY,
            color=Colors.DARK,
            halign='right',
            size_hint_x=0.6
        )
        gravity_label.bind(size=gravity_label.setter('text_size'))
        
        self.gravity_input = self.create_number_input('9.8', 'm/s²')
        
        self.input_container.add_widget(mass_label)
        self.input_container.add_widget(self.mass_input)
        self.input_container.add_widget(height_label)
        self.input_container.add_widget(self.height_input)
        self.input_container.add_widget(gravity_label)
        self.input_container.add_widget(self.gravity_input)
    
    def create_density_inputs(self):
        """Membuat input fields untuk rumus massa jenis"""
        self.input_container.clear_widgets()
        
        # Mass
        mass_label = Label(
            text='Mass (m):',
            font_size=Fonts.BODY,
            color=Colors.DARK,
            halign='right',
            size_hint_x=0.6
        )
        mass_label.bind(size=mass_label.setter('text_size'))
        
        self.mass_input = self.create_number_input('0', 'kg')
        
        # Volume
        volume_label = Label(
            text='Volume (V):',
            font_size=Fonts.BODY,
            color=Colors.DARK,
            halign='right',
            size_hint_x=0.6
        )
        volume_label.bind(size=volume_label.setter('text_size'))
        
        self.volume_input = self.create_number_input('0', 'm³')
        
        self.input_container.add_widget(mass_label)
        self.input_container.add_widget(self.mass_input)
        self.input_container.add_widget(volume_label)
        self.input_container.add_widget(self.volume_input)
    
    def create_power_inputs(self):
        """Membuat input fields untuk rumus daya"""
        self.input_container.clear_widgets()
        
        # Work
        work_label = Label(
            text='Work (W):',
            font_size=Fonts.BODY,
            color=Colors.DARK,
            halign='right',
            size_hint_x=0.6
        )
        work_label.bind(size=work_label.setter('text_size'))
        
        self.work_input = self.create_number_input('0', 'J')
        
        # Time
        time_label = Label(
            text='Time (t):',
            font_size=Fonts.BODY,
            color=Colors.DARK,
            halign='right',
            size_hint_x=0.6
        )
        time_label.bind(size=time_label.setter('text_size'))
        
        self.time_input = self.create_number_input('0', 's')
        
        self.input_container.add_widget(work_label)
        self.input_container.add_widget(self.work_input)
        self.input_container.add_widget(time_label)
        self.input_container.add_widget(self.time_input)
    
    def create_number_input(self, text, unit):
        """Membuat input field untuk angka"""
        container = BoxLayout(
            orientation='horizontal',
            size_hint_x=0.4,
            spacing=dp(5)
        )
        
        input_field = TextInput(
            text=text,
            font_size=Fonts.BODY,
            multiline=False,
            input_filter='float',
            halign='right',
            size_hint_x=0.7,
            background_normal='',
            background_color=(0, 0, 0, 0)
        )
        
        # Background
        with input_field.canvas.before:
            Color(*Colors.WHITE)
            input_field.rect = RoundedRectangle(
                pos=input_field.pos,
                size=input_field.size,
                radius=[Spacing.RADIUS_SM]
            )
        
        # Border di canvas yang sama
        with input_field.canvas.before:
            Color(*Colors.GRAY_LIGHT)
            input_field._border_line = Line(
                rounded_rectangle=(input_field.x, input_field.y,
                                  input_field.width, input_field.height,
                                  Spacing.RADIUS_SM),
                width=1
            )
        
        input_field.bind(pos=self.update_input_bg, size=self.update_input_bg)
        
        unit_label = Label(
            text=unit,
            font_size=Fonts.BODY_SMALL,
            color=Colors.GRAY_DARK,
            size_hint_x=0.3
        )
        
        container.add_widget(input_field)
        container.add_widget(unit_label)
        
        return container
    
    def show_formula_dropdown(self, instance):
        """Menampilkan dropdown pemilih rumus"""
        dropdown = DropDown()
        
        formulas = [
            ('Velocity (v = s/t)', 'velocity'),
            ('Force (F = m×a)', 'force'),
            ('Pressure (P = F/A)', 'pressure'),
            ('Work (W = F×s)', 'work'),
            ('Kinetic Energy (Ek = ½mv²)', 'kinetic_energy'),
            ('Potential Energy (Ep = mgh)', 'potential_energy'),
            ('Density (ρ = m/V)', 'density'),
            ('Power (P = W/t)', 'power')
        ]
        
        for text, key in formulas:
            btn = Button(
                text=text,
                size_hint_y=None,
                height=dp(44),
                background_color=Colors.WHITE,
                color=Colors.DARK
            )
            
            btn.bind(
                on_release=lambda btn=btn, k=key: self.select_formula(btn.text, k, dropdown)
            )
            
            dropdown.add_widget(btn)
        
        dropdown.open(instance)
    
    def select_formula(self, text, key, dropdown):
        """Memilih rumus dari dropdown"""
        self.formula_btn.text = text
        self.current_formula = key
        dropdown.dismiss()
        
        # Update tampilan berdasarkan rumus
        self.update_formula_display()
        self.update_input_fields()
        self.clear_result()
    
    def update_formula_display(self):
        """Update tampilan rumus berdasarkan pilihan"""
        formulas = {
            'velocity': ('v = s / t', 'Velocity = Displacement ÷ Time'),
            'force': ('F = m × a', 'Force = Mass × Acceleration'),
            'pressure': ('P = F / A', 'Pressure = Force ÷ Area'),
            'work': ('W = F × s', 'Work = Force × Displacement'),
            'kinetic_energy': ('Ek = ½ × m × v²', 'Kinetic Energy = ½ × Mass × Velocity²'),
            'potential_energy': ('Ep = m × g × h', 'Potential Energy = Mass × Gravity × Height'),
            'density': ('ρ = m / V', 'Density = Mass ÷ Volume'),
            'power': ('P = W / t', 'Power = Work ÷ Time')
        }
        
        formula, desc = formulas.get(self.current_formula, ('', ''))
        self.formula_display.text = formula
        self.formula_desc.text = desc
    
    def update_input_fields(self):
        """Update input fields berdasarkan rumus"""
        if self.current_formula == 'velocity':
            self.create_velocity_inputs()
            self.input_section.height = dp(200)
        elif self.current_formula == 'force':
            self.create_force_inputs()
            self.input_section.height = dp(200)
        elif self.current_formula == 'pressure':
            self.create_pressure_inputs()
            self.input_section.height = dp(200)
        elif self.current_formula == 'work':
            self.create_work_inputs()
            self.input_section.height = dp(200)
        elif self.current_formula == 'kinetic_energy':
            self.create_kinetic_energy_inputs()
            self.input_section.height = dp(200)
        elif self.current_formula == 'potential_energy':
            self.create_potential_energy_inputs()
            self.input_section.height = dp(250)  # Lebih tinggi karena 3 input
        elif self.current_formula == 'density':
            self.create_density_inputs()
            self.input_section.height = dp(200)
        elif self.current_formula == 'power':
            self.create_power_inputs()
            self.input_section.height = dp(200)
    
    def calculate(self, instance):
        """Melakukan perhitungan berdasarkan rumus"""
        try:
            if self.current_formula == 'velocity':
                # Dapatkan nilai dari input fields
                s_text = self.displacement_input.children[0].text
                t_text = self.time_input.children[0].text
                
                # Validasi input
                if not s_text or not t_text:
                    self.show_error("Please enter both values")
                    return
                
                s = float(s_text)
                t = float(t_text)
                
                if t == 0:
                    self.show_error("Time cannot be zero")
                    return
                
                result, _ = calculate_velocity(s, t)
                self.show_result(result, 'm/s')
                
            elif self.current_formula == 'force':
                # Dapatkan nilai dari input fields
                m_text = self.mass_input.children[0].text
                a_text = self.accel_input.children[0].text
                
                if not m_text or not a_text:
                    self.show_error("Please enter both values")
                    return
                
                m = float(m_text)
                a = float(a_text)
                
                result, _ = calculate_force(m, a)
                self.show_result(result, 'N')
            
            elif self.current_formula == 'pressure':
                f_text = self.force_input.children[0].text
                a_text = self.area_input.children[0].text
                
                if not f_text or not a_text:
                    self.show_error("Please enter both values")
                    return
                
                f = float(f_text)
                a = float(a_text)
                
                if a == 0:
                    self.show_error("Area cannot be zero")
                    return
                
                result, _ = calculate_pressure(f, a)
                self.show_result(result, 'Pa')
            
            elif self.current_formula == 'work':
                f_text = self.force_input.children[0].text
                s_text = self.displacement_input.children[0].text
                
                if not f_text or not s_text:
                    self.show_error("Please enter both values")
                    return
                
                f = float(f_text)
                s = float(s_text)
                
                result, _ = calculate_work(f, s)
                self.show_result(result, 'J')
            
            elif self.current_formula == 'kinetic_energy':
                m_text = self.mass_input.children[0].text
                v_text = self.velocity_input.children[0].text
                
                if not m_text or not v_text:
                    self.show_error("Please enter both values")
                    return
                
                m = float(m_text)
                v = float(v_text)
                
                result, _ = calculate_kinetic_energy(m, v)
                self.show_result(result, 'J')
            
            elif self.current_formula == 'potential_energy':
                m_text = self.mass_input.children[0].text
                h_text = self.height_input.children[0].text
                g_text = self.gravity_input.children[0].text
                
                if not m_text or not h_text or not g_text:
                    self.show_error("Please enter all values")
                    return
                
                m = float(m_text)
                h = float(h_text)
                g = float(g_text)
                
                result, _ = calculate_potential_energy(m, g, h)
                self.show_result(result, 'J')
            
            elif self.current_formula == 'density':
                m_text = self.mass_input.children[0].text
                v_text = self.volume_input.children[0].text
                
                if not m_text or not v_text:
                    self.show_error("Please enter both values")
                    return
                
                m = float(m_text)
                v = float(v_text)
                
                if v == 0:
                    self.show_error("Volume cannot be zero")
                    return
                
                result, _ = calculate_density(m, v)
                self.show_result(result, 'kg/m³')
            
            elif self.current_formula == 'power':
                w_text = self.work_input.children[0].text
                t_text = self.time_input.children[0].text
                
                if not w_text or not t_text:
                    self.show_error("Please enter both values")
                    return
                
                w = float(w_text)
                t = float(t_text)
                
                if t == 0:
                    self.show_error("Time cannot be zero")
                    return
                
                result, _ = calculate_power(w, t)
                self.show_result(result, 'W')
            
        except ValueError:
            self.show_error("Please enter valid numbers")
        except Exception as e:
            self.show_error(f"Calculation error: {str(e)}")
    
    def show_result(self, value, unit):
        """Menampilkan hasil perhitungan"""
        if value is None:
            self.show_error("Calculation error")
            return
        
        formatted = format_result(value, unit, 2)
        # Pisahkan angka dan unit
        parts = formatted.split()
        if len(parts) >= 2:
            self.result_label.text = parts[0]
            self.unit_label.text = ' '.join(parts[1:])
        else:
            self.result_label.text = formatted
            self.unit_label.text = unit
        
        # Animasi
        self.result_label.color = Colors.SUCCESS
        anim = Animation(color=Colors.PRIMARY, duration=1.5)
        anim.start(self.result_label)
    
    def show_error(self, message):
        """Menampilkan error"""
        self.result_label.text = 'Error'
        self.unit_label.text = message
        self.result_label.color = Colors.DANGER
        
        # Animasi
        anim = Animation(opacity=0.5, duration=0.1) + Animation(opacity=1, duration=0.1)
        anim.repeat = True
        anim.start(self.result_label)
        Clock.schedule_once(lambda dt: anim.stop(self.result_label), 0.5)
    
    def clear_result(self):
        """Membersihkan hasil"""
        self.result_label.text = '--'
        self.unit_label.text = ''
        self.result_label.color = Colors.PRIMARY
    
    def clear_inputs(self, instance):
        """Membersihkan semua input"""
        # Clear berdasarkan rumus yang aktif
        if self.current_formula == 'velocity':
            if hasattr(self, 'displacement_input'):
                self.displacement_input.children[0].text = '0'
            if hasattr(self, 'time_input'):
                self.time_input.children[0].text = '0'
        elif self.current_formula == 'force':
            if hasattr(self, 'mass_input'):
                self.mass_input.children[0].text = '0'
            if hasattr(self, 'accel_input'):
                self.accel_input.children[0].text = '0'
        elif self.current_formula == 'pressure':
            if hasattr(self, 'force_input'):
                self.force_input.children[0].text = '0'
            if hasattr(self, 'area_input'):
                self.area_input.children[0].text = '0'
        elif self.current_formula == 'work':
            if hasattr(self, 'force_input'):
                self.force_input.children[0].text = '0'
            if hasattr(self, 'displacement_input'):
                self.displacement_input.children[0].text = '0'
        elif self.current_formula == 'kinetic_energy':
            if hasattr(self, 'mass_input'):
                self.mass_input.children[0].text = '0'
            if hasattr(self, 'velocity_input'):
                self.velocity_input.children[0].text = '0'
        elif self.current_formula == 'potential_energy':
            if hasattr(self, 'mass_input'):
                self.mass_input.children[0].text = '0'
            if hasattr(self, 'height_input'):
                self.height_input.children[0].text = '0'
            if hasattr(self, 'gravity_input'):
                self.gravity_input.children[0].text = '9.8'
        elif self.current_formula == 'density':
            if hasattr(self, 'mass_input'):
                self.mass_input.children[0].text = '0'
            if hasattr(self, 'volume_input'):
                self.volume_input.children[0].text = '0'
        elif self.current_formula == 'power':
            if hasattr(self, 'work_input'):
                self.work_input.children[0].text = '0'
            if hasattr(self, 'time_input'):
                self.time_input.children[0].text = '0'
        
        self.clear_result()
    
    def reset_calculator(self, instance):
        """Reset kalkulator ke default"""
        self.current_formula = 'velocity'
        self.formula_btn.text = 'Velocity (v = s/t)'
        self.update_formula_display()
        self.update_input_fields()
        self.clear_inputs(instance)
    
    def go_back(self, instance):
        """Kembali ke home screen"""
        self.manager.current = 'home'
    
    def animate_entrance(self, *args):
    # Semua anak dibuat transparan dulu
     for child in self.content_container.children:
        child.opacity = 0

    # Animasi fade-in bertahap
     for i, child in enumerate(reversed(self.content_container.children)):
        anim = Animation(opacity=1, duration=0.3)

        Clock.schedule_once(
            lambda dt, a=anim, c=child: a.start(c),
            i * 0.08   # jeda antar widget
        )

    # Update background functions
    def update_formula_btn_bg(self, instance, value):
        """Update background formula button"""
        if hasattr(instance, 'rect'):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size
        if hasattr(instance, '_border_line'):
            instance._border_line.rounded_rectangle = (instance.x, instance.y,
                                                instance.width, instance.height,
                                                Spacing.RADIUS_MD)
    
    def update_input_bg(self, instance, value):
        """Update background input field"""
        if hasattr(instance, 'rect'):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size
        if hasattr(instance, '_border_line'):
            instance._border_line.rounded_rectangle = (instance.x, instance.y,
                                                instance.width, instance.height,
                                                Spacing.RADIUS_SM)