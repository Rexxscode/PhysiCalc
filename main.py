"""
Aplikasi Mobile Pendidikan Fisika SMP
Dibuat dengan Python Kivy
Kompatibel untuk Android menggunakan Buildozer
"""

import kivy
from kivy.app import App

from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.graphics import Color, Rectangle, RoundedRectangle

from kivy.properties import (
    StringProperty,
    NumericProperty,
    ListProperty,
    ObjectProperty,
    BooleanProperty
)

from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.spinner import Spinner
from kivy.uix.slider import Slider
from kivy.uix.switch import Switch
from kivy.uix.progressbar import ProgressBar
from kivy.uix.carousel import Carousel
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.dropdown import DropDown
from kivy.uix.modalview import ModalView

# RecycleView imports (BENAR)
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import RecycleLayoutManagerBehavior

import math
import json
import os
import sys
import random
from datetime import datetime

# Konfigurasi ukuran window untuk pengembangan
Window.size = (280, 640)
Window.clearcolor = (0.95, 0.96, 0.98, 1)  # Warna latar belakang aplikasi

# ============================================================================
# KELAS UTAMA APLIKASI
# ============================================================================

class PhysicsApp(App):
    """Kelas utama aplikasi Fisika SMP"""
    
    def build(self):
        """Membangun antarmuka aplikasi"""
        self.title = "Physicalc"
        self.icon = "assets/icon.png" if os.path.exists("assets/icon.png") else ""
        
        # Inisialisasi ScreenManager
        self.sm = ScreenManager(transition=SlideTransition())
        
        # Tambahkan screen
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(FormulaListScreen(name='formula_list'))
        self.sm.add_widget(CalculatorScreen(name='calculator'))
        self.sm.add_widget(FormulaDetailScreen(name='formula_detail'))
        self.sm.add_widget(AboutScreen(name='about'))
        self.sm.add_widget(QuizScreen(name='quiz'))
        self.sm.add_widget(SettingsScreen(name='settings'))
        
        return self.sm
    
    def on_start(self):
        """Dipanggil saat aplikasi dimulai"""
        # Inisialisasi data jika diperlukan
        pass
    
    def on_pause(self):
        """Dipanggil saat aplikasi di-pause (untuk mobile)"""
        return True
    
    def on_resume(self):
        """Dipanggil saat aplikasi di-resume (untuk mobile)"""
        pass

# ============================================================================
# DATA RUMUS FISIKA SMP
# ============================================================================

class FormulaData:
    """Kelas untuk menyimpan dan mengelola data rumus fisika"""
    
    @staticmethod
    def get_all_formulas():
        """Mengembalikan semua rumus fisika SMP"""
        formulas = {
            'gerak_lurus': {
                'id': 'gerak_lurus',
                'title': 'Gerak Lurus',
                'category': 'Kinematika',
                'icon': 'run',
                'color': [0.2, 0.6, 0.9, 1],  # Biru
                'formulas': [
                    {
                        'name': 'Kecepatan',
                        'formula': 'v = s / t',
                        'latex': 'v = \\frac{s}{t}',
                        'description': 'Kecepatan adalah jarak yang ditempuh per satuan waktu.',
                        'variables': [
                            {'symbol': 'v', 'name': 'Kecepatan', 'unit': 'm/s'},
                            {'symbol': 's', 'name': 'Jarak', 'unit': 'm'},
                            {'symbol': 't', 'name': 'Waktu', 'unit': 's'}
                        ],
                        'example': 'Jika sebuah mobil menempuh jarak 100 meter dalam waktu 20 detik, maka kecepatannya adalah 5 m/s.',
                        'notes': 'Kecepatan adalah besaran vektor yang memiliki nilai dan arah.'
                    },
                    {
                        'name': 'Percepatan',
                        'formula': 'a = Δv / Δt',
                        'latex': 'a = \\frac{\\Delta v}{\\Delta t}',
                        'description': 'Percepatan adalah perubahan kecepatan per satuan waktu.',
                        'variables': [
                            {'symbol': 'a', 'name': 'Percepatan', 'unit': 'm/s²'},
                            {'symbol': 'Δv', 'name': 'Perubahan Kecepatan', 'unit': 'm/s'},
                            {'symbol': 'Δt', 'name': 'Perubahan Waktu', 'unit': 's'}
                        ],
                        'example': 'Jika kecepatan meningkat dari 10 m/s menjadi 30 m/s dalam 5 detik, percepatannya adalah 4 m/s².',
                        'notes': 'Percepatan bisa positif (percepatan) atau negatif (perlambatan).'
                    },
                    {
                        'name': 'Gerak Lurus Beraturan (GLB)',
                        'formula': 's = v × t',
                        'latex': 's = v \\times t',
                        'description': 'Jarak yang ditempuh dalam gerak lurus beraturan.',
                        'variables': [
                            {'symbol': 's', 'name': 'Jarak', 'unit': 'm'},
                            {'symbol': 'v', 'name': 'Kecepatan', 'unit': 'm/s'},
                            {'symbol': 't', 'name': 'Waktu', 'unit': 's'}
                        ],
                        'example': 'Jika bergerak dengan kecepatan 5 m/s selama 10 detik, jarak yang ditempuh adalah 50 meter.',
                        'notes': 'Kecepatan konstan pada GLB.'
                    }
                ]
            },
            'gaya': {
                'id': 'gaya',
                'title': 'Gaya',
                'category': 'Dinamika',
                'icon': 'weight',
                'color': [0.9, 0.5, 0.2, 1],  # Oranye
                'formulas': [
                    {
                        'name': 'Hukum Newton II',
                        'formula': 'F = m × a',
                        'latex': 'F = m \\times a',
                        'description': 'Gaya yang bekerja pada suatu benda sebanding dengan massa benda dan percepatannya.',
                        'variables': [
                            {'symbol': 'F', 'name': 'Gaya', 'unit': 'N (Newton)'},
                            {'symbol': 'm', 'name': 'Massa', 'unit': 'kg'},
                            {'symbol': 'a', 'name': 'Percepatan', 'unit': 'm/s²'}
                        ],
                        'example': 'Sebuah benda bermassa 2 kg mengalami percepatan 3 m/s², maka gaya yang bekerja adalah 6 Newton.',
                        'notes': '1 Newton = 1 kg·m/s²'
                    },
                    {
                        'name': 'Gaya Berat',
                        'formula': 'w = m × g',
                        'latex': 'w = m \\times g',
                        'description': 'Gaya berat adalah gaya gravitasi yang bekerja pada suatu benda.',
                        'variables': [
                            {'symbol': 'w', 'name': 'Gaya Berat', 'unit': 'N'},
                            {'symbol': 'm', 'name': 'Massa', 'unit': 'kg'},
                            {'symbol': 'g', 'name': 'Percepatan Gravitasi', 'unit': 'm/s²'}
                        ],
                        'example': 'Benda bermassa 10 kg memiliki berat sekitar 98 N (dengan g = 9.8 m/s²).',
                        'notes': 'Nilai g di permukaan bumi sekitar 9.8 m/s².'
                    },
                    {
                        'name': 'Gaya Gesek',
                        'formula': 'f = μ × N',
                        'latex': 'f = \\mu \\times N',
                        'description': 'Gaya gesek sebanding dengan gaya normal dan koefisien gesekan.',
                        'variables': [
                            {'symbol': 'f', 'name': 'Gaya Gesek', 'unit': 'N'},
                            {'symbol': 'μ', 'name': 'Koefisien Gesek', 'unit': '-'},
                            {'symbol': 'N', 'name': 'Gaya Normal', 'unit': 'N'}
                        ],
                        'example': 'Jika koefisien gesek 0.3 dan gaya normal 50 N, maka gaya gesek adalah 15 N.',
                        'notes': 'Koefisien gesek bergantung pada permukaan yang bersentuhan.'
                    }
                ]
            },
            'tekanan': {
                'id': 'tekanan',
                'title': 'Tekanan',
                'category': 'Fluida',
                'icon': 'water',
                'color': [0.3, 0.7, 0.5, 1],  # Hijau
                'formulas': [
                    {
                        'name': 'Tekanan',
                        'formula': 'P = F / A',
                        'latex': 'P = \\frac{F}{A}',
                        'description': 'Tekanan adalah gaya yang bekerja tegak lurus pada suatu permukaan per satuan luas.',
                        'variables': [
                            {'symbol': 'P', 'name': 'Tekanan', 'unit': 'Pa (Pascal)'},
                            {'symbol': 'F', 'name': 'Gaya', 'unit': 'N'},
                            {'symbol': 'A', 'name': 'Luas Permukaan', 'unit': 'm²'}
                        ],
                        'example': 'Jika gaya 100 N bekerja pada luas 2 m², maka tekanannya adalah 50 Pa.',
                        'notes': '1 Pa = 1 N/m²'
                    },
                    {
                        'name': 'Tekanan Hidrostatis',
                        'formula': 'P = ρ × g × h',
                        'latex': 'P = \\rho \\times g \\times h',
                        'description': 'Tekanan pada zat cair akibat berat zat cair itu sendiri.',
                        'variables': [
                            {'symbol': 'P', 'name': 'Tekanan Hidrostatis', 'unit': 'Pa'},
                            {'symbol': 'ρ', 'name': 'Massa Jenis', 'unit': 'kg/m³'},
                            {'symbol': 'g', 'name': 'Percepatan Gravitasi', 'unit': 'm/s²'},
                            {'symbol': 'h', 'name': 'Kedalaman', 'unit': 'm'}
                        ],
                        'example': 'Pada kedalaman 10 m dalam air (ρ=1000 kg/m³), tekanan hidrostatisnya sekitar 98.000 Pa.',
                        'notes': 'Tekanan meningkat dengan bertambahnya kedalaman.'
                    },
                    {
                        'name': 'Hukum Pascal',
                        'formula': 'F₁/A₁ = F₂/A₂',
                        'latex': '\\frac{F_1}{A_1} = \\frac{F_2}{A_2}',
                        'description': 'Tekanan yang diberikan pada zat cair dalam ruang tertutup diteruskan sama besar ke segala arah.',
                        'variables': [
                            {'symbol': 'F₁, F₂', 'name': 'Gaya pada Piston', 'unit': 'N'},
                            {'symbol': 'A₁, A₂', 'name': 'Luas Penampang Piston', 'unit': 'm²'}
                        ],
                        'example': 'Pada dongkrak hidrolik, gaya kecil pada piston kecil dapat menghasilkan gaya besar pada piston besar.',
                        'notes': 'Prinsip ini digunakan dalam rem hidrolik dan dongkrak.'
                    }
                ]
            },
            'usaha': {
                'id': 'usaha',
                'title': 'Usaha',
                'category': 'Energi',
                'icon': 'cog',
                'color': [0.8, 0.4, 0.7, 1],  # Ungu
                'formulas': [
                    {
                        'name': 'Usaha',
                        'formula': 'W = F × s × cos θ',
                        'latex': 'W = F \\times s \\times \\cos\\theta',
                        'description': 'Usaha adalah hasil kali gaya dengan perpindahan benda dan cosinus sudut antara keduanya.',
                        'variables': [
                            {'symbol': 'W', 'name': 'Usaha', 'unit': 'J (Joule)'},
                            {'symbol': 'F', 'name': 'Gaya', 'unit': 'N'},
                            {'symbol': 's', 'name': 'Perpindahan', 'unit': 'm'},
                            {'symbol': 'θ', 'name': 'Sudut antara Gaya dan Perpindahan', 'unit': '°'}
                        ],
                        'example': 'Gaya 10 N menggerakkan benda sejauh 5 m searah gaya, maka usaha = 50 Joule.',
                        'notes': 'Jika gaya tegak lurus perpindahan, usaha = 0.'
                    },
                    {
                        'name': 'Usaha oleh Gaya Konstan',
                        'formula': 'W = F × s',
                        'latex': 'W = F \\times s',
                        'description': 'Usaha ketika gaya searah dengan perpindahan.',
                        'variables': [
                            {'symbol': 'W', 'name': 'Usaha', 'unit': 'J'},
                            {'symbol': 'F', 'name': 'Gaya', 'unit': 'N'},
                            {'symbol': 's', 'name': 'Perpindahan', 'unit': 'm'}
                        ],
                        'example': 'Mendorong meja dengan gaya 20 N sejauh 3 m menghasilkan usaha 60 J.',
                        'notes': 'Ini adalah kasus khusus ketika cos θ = 1.'
                    }
                ]
            },
            'energi_kinetik': {
                'id': 'energi_kinetik',
                'title': 'Energi Kinetik',
                'category': 'Energi',
                'icon': 'rocket',
                'color': [0.9, 0.8, 0.2, 1],  # Kuning
                'formulas': [
                    {
                        'name': 'Energi Kinetik',
                        'formula': 'EK = ½ × m × v²',
                        'latex': 'EK = \\frac{1}{2} \\times m \\times v^2',
                        'description': 'Energi yang dimiliki benda karena geraknya.',
                        'variables': [
                            {'symbol': 'EK', 'name': 'Energi Kinetik', 'unit': 'J'},
                            {'symbol': 'm', 'name': 'Massa', 'unit': 'kg'},
                            {'symbol': 'v', 'name': 'Kecepatan', 'unit': 'm/s'}
                        ],
                        'example': 'Bola bermassa 0.5 kg bergerak dengan kecepatan 4 m/s memiliki energi kinetik 4 Joule.',
                        'notes': 'Energi kinetik sebanding dengan kuadrat kecepatan.'
                    },
                    {
                        'name': 'Teorema Usaha-Energi',
                        'formula': 'W = ΔEK',
                        'latex': 'W = \\Delta EK',
                        'description': 'Usaha total yang dilakukan pada benda sama dengan perubahan energi kinetiknya.',
                        'variables': [
                            {'symbol': 'W', 'name': 'Usaha Total', 'unit': 'J'},
                            {'symbol': 'ΔEK', 'name': 'Perubahan Energi Kinetik', 'unit': 'J'}
                        ],
                        'example': 'Jika energi kinetik bertambah 30 J, maka usaha total yang dilakukan adalah 30 J.',
                        'notes': 'Teorema ini menghubungkan konsep usaha dan energi kinetik.'
                    }
                ]
            },
            'energi_potensial': {
                'id': 'energi_potensial',
                'title': 'Energi Potensial',
                'category': 'Energi',
                'icon': 'arrow-up-bold',
                'color': [0.4, 0.8, 0.6, 1],  # Hijau muda
                'formulas': [
                    {
                        'name': 'Energi Potensial Gravitasi',
                        'formula': 'EP = m × g × h',
                        'latex': 'EP = m \\times g \\times h',
                        'description': 'Energi yang dimiliki benda karena kedudukannya terhadap bumi.',
                        'variables': [
                            {'symbol': 'EP', 'name': 'Energi Potensial', 'unit': 'J'},
                            {'symbol': 'm', 'name': 'Massa', 'unit': 'kg'},
                            {'symbol': 'g', 'name': 'Percepatan Gravitasi', 'unit': 'm/s²'},
                            {'symbol': 'h', 'name': 'Ketinggian', 'unit': 'm'}
                        ],
                        'example': 'Buku bermassa 1 kg pada ketinggian 2 m memiliki energi potensial sekitar 19.6 J.',
                        'notes': 'Energi potensial nol pada ketinggian nol (acuan).'
                    },
                    {
                        'name': 'Energi Potensial Pegas',
                        'formula': 'EP = ½ × k × x²',
                        'latex': 'EP = \\frac{1}{2} \\times k \\times x^2',
                        'description': 'Energi yang tersimpan pada pegas yang diregangkan atau ditekan.',
                        'variables': [
                            {'symbol': 'EP', 'name': 'Energi Potensial Pegas', 'unit': 'J'},
                            {'symbol': 'k', 'name': 'Konstanta Pegas', 'unit': 'N/m'},
                            {'symbol': 'x', 'name': 'Simpangan', 'unit': 'm'}
                        ],
                        'example': 'Pegas dengan k = 100 N/m diregangkan 0.1 m menyimpan energi 0.5 J.',
                        'notes': 'Energi potensial pegas selalu positif.'
                    }
                ]
            },
            'daya': {
                'id': 'daya',
                'title': 'Daya',
                'category': 'Energi',
                'icon': 'flash',
                'color': [1, 0.6, 0.2, 1],  # Jingga
                'formulas': [
                    {
                        'name': 'Daya',
                        'formula': 'P = W / t',
                        'latex': 'P = \\frac{W}{t}',
                        'description': 'Daya adalah laju usaha dilakukan atau energi ditransfer per satuan waktu.',
                        'variables': [
                            {'symbol': 'P', 'name': 'Daya', 'unit': 'W (Watt)'},
                            {'symbol': 'W', 'name': 'Usaha', 'unit': 'J'},
                            {'symbol': 't', 'name': 'Waktu', 'unit': 's'}
                        ],
                        'example': 'Jika usaha 600 J dilakukan dalam 2 detik, dayanya adalah 300 Watt.',
                        'notes': '1 Watt = 1 Joule/detik'
                    },
                    {
                        'name': 'Daya dalam Gerak',
                        'formula': 'P = F × v',
                        'latex': 'P = F \\times v',
                        'description': 'Daya juga dapat dihitung sebagai hasil kali gaya dan kecepatan.',
                        'variables': [
                            {'symbol': 'P', 'name': 'Daya', 'unit': 'W'},
                            {'symbol': 'F', 'name': 'Gaya', 'unit': 'N'},
                            {'symbol': 'v', 'name': 'Kecepatan', 'unit': 'm/s'}
                        ],
                        'example': 'Gaya 50 N menggerakkan benda dengan kecepatan 3 m/s menghasilkan daya 150 W.',
                        'notes': 'Rumus ini berguna ketika gaya konstan searah kecepatan.'
                    }
                ]
            },
            'massa_jenis': {
                'id': 'massa_jenis',
                'title': 'Massa Jenis',
                'category': 'Materi',
                'icon': 'cube',
                'color': [0.6, 0.4, 0.8, 1],  # Ungu tua
                'formulas': [
                    {
                        'name': 'Massa Jenis',
                        'formula': 'ρ = m / V',
                        'latex': '\\rho = \\frac{m}{V}',
                        'description': 'Massa jenis adalah massa per satuan volume suatu zat.',
                        'variables': [
                            {'symbol': 'ρ', 'name': 'Massa Jenis', 'unit': 'kg/m³'},
                            {'symbol': 'm', 'name': 'Massa', 'unit': 'kg'},
                            {'symbol': 'V', 'name': 'Volume', 'unit': 'm³'}
                        ],
                        'example': 'Benda bermassa 500 kg dengan volume 0.2 m³ memiliki massa jenis 2500 kg/m³.',
                        'notes': 'Massa jenis air sekitar 1000 kg/m³.'
                    },
                    {
                        'name': 'Massa Jenis Relatif',
                        'formula': 'ρ_relatif = ρ_benda / ρ_air',
                        'latex': '\\rho_{relatif} = \\frac{\\rho_{benda}}{\\rho_{air}}',
                        'description': 'Perbandingan massa jenis benda terhadap massa jenis air.',
                        'variables': [
                            {'symbol': 'ρ_relatif', 'name': 'Massa Jenis Relatif', 'unit': '-'},
                            {'symbol': 'ρ_benda', 'name': 'Massa Jenis Benda', 'unit': 'kg/m³'},
                            {'symbol': 'ρ_air', 'name': 'Massa Jenis Air', 'unit': 'kg/m³'}
                        ],
                        'example': 'Jika massa jenis benda 800 kg/m³, massa jenis relatifnya adalah 0.8.',
                        'notes': 'Benda dengan ρ < 1 akan mengapung di air.'
                    }
                ]
            }
        }
        
        # Tambahkan materi tambahan untuk mencapai 8 materi
        # (sudah ada 8 materi di atas)
        
        return formulas
    
    @staticmethod
    def get_formula_by_id(formula_id):
        """Mengembalikan rumus berdasarkan ID"""
        formulas = FormulaData.get_all_formulas()
        return formulas.get(formula_id, None)
    
    @staticmethod
    def get_all_categories():
        """Mengembalikan semua kategori rumus"""
        formulas = FormulaData.get_all_formulas()
        categories = set()
        for formula in formulas.values():
            categories.add(formula['category'])
        return list(categories)

# ============================================================================
# KOMPONEN UI KUSTOM
# ============================================================================

class RoundedButton(ButtonBehavior, BoxLayout):
    """Tombol dengan sudut membulat"""
    text = StringProperty('')
    background_color = ListProperty([0.2, 0.6, 0.9, 1])
    text_color = ListProperty([1, 1, 1, 1])
    radius = ListProperty([10])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.height = dp(50)
        self.width = dp(200)
        self.padding = dp(10)
        
        with self.canvas.before:
            Color(*self.background_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)
        
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        label = Label(
            text=self.text,
            color=self.text_color,
            font_size=sp(16),
            bold=True
        )
        self.add_widget(label)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class PhysicsCard(ButtonBehavior, BoxLayout):
    """Kartu untuk menampilkan materi fisika"""
    title = StringProperty('')
    subtitle = StringProperty('')
    icon = StringProperty('')
    color = ListProperty([0.2, 0.6, 0.9, 1])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (1, None)
        self.height = dp(120)
        self.padding = dp(15)
        self.spacing = dp(10)
        
        with self.canvas.before:
            Color(*self.color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
        
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        # Header dengan ikon dan judul
        header = BoxLayout(size_hint=(1, None), height=dp(40))
        
        # Ikon (simulasi dengan label)
        icon_label = Label(
            text='[•]' if not self.icon else f'[{self.icon}]',
            font_size=sp(24),
            markup=True,
            size_hint=(None, 1),
            width=dp(40)
        )
        header.add_widget(icon_label)
        
        # Judul dan subjudul
        title_layout = BoxLayout(orientation='vertical')
        title_label = Label(
            text=self.title,
            font_size=sp(18),
            bold=True,
            color=[0, 0, 0, 1],
            halign='left'
        )
        title_label.bind(size=title_label.setter('text_size'))
        
        subtitle_label = Label(
            text=self.subtitle,
            font_size=sp(12),
            color=[0.3, 0.3, 0.3, 1],
            halign='left'
        )
        subtitle_label.bind(size=subtitle_label.setter('text_size'))
        
        title_layout.add_widget(title_label)
        title_layout.add_widget(subtitle_label)
        header.add_widget(title_layout)
        
        # Panah indikator
        arrow_label = Label(
            text='→',
            font_size=sp(24),
            color=[0, 0, 0, 0.5],
            size_hint=(None, 1),
            width=dp(30)
        )
        header.add_widget(arrow_label)
        
        self.add_widget(header)
        
        # Garis pemisah
        separator = Widget(size_hint=(1, None), height=dp(1))
        with separator.canvas:
            Color(0, 0, 0, 0.1)
            Rectangle(pos=separator.pos, size=separator.size)
        self.add_widget(separator)
        
        # Jumlah rumus
        formula_count = Label(
            text='3 rumus tersedia',
            font_size=sp(12),
            color=[0.5, 0.5, 0.5, 1],
            halign='left'
        )
        formula_count.bind(size=formula_count.setter('text_size'))
        self.add_widget(formula_count)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class FormulaCard(BoxLayout):
    """Kartu untuk menampilkan detail rumus"""
    formula_name = StringProperty('')
    formula = StringProperty('')
    description = StringProperty('')
    variables = ListProperty([])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (1, None)
        self.padding = dp(15)
        self.spacing = dp(10)
        
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[10])
            Color(0.9, 0.95, 1, 1)
            self.border = RoundedRectangle(pos=self.pos, size=self.size, radius=[10], width=dp(2))
        
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        # Nama rumus
        name_label = Label(
            text=self.formula_name,
            font_size=sp(18),
            bold=True,
            color=[0.1, 0.1, 0.1, 1],
            halign='left',
            size_hint=(1, None),
            height=dp(30)
        )
        name_label.bind(size=name_label.setter('text_size'))
        self.add_widget(name_label)
        
        # Rumus
        formula_label = Label(
            text=self.formula,
            font_size=sp(24),
            bold=True,
            color=[0.2, 0.6, 0.9, 1],
            halign='left',
            size_hint=(1, None),
            height=dp(40)
        )
        formula_label.bind(size=formula_label.setter('text_size'))
        self.add_widget(formula_label)
        
        # Deskripsi
        desc_label = Label(
            text=self.description,
            font_size=sp(14),
            color=[0.3, 0.3, 0.3, 1],
            halign='left',
            size_hint=(1, None),
            height=dp(60)
        )
        desc_label.bind(size=desc_label.setter('text_size'))
        self.add_widget(desc_label)
        
        # Variabel
        if self.variables:
            vars_label = Label(
                text='Variabel:',
                font_size=sp(14),
                bold=True,
                color=[0.2, 0.2, 0.2, 1],
                halign='left',
                size_hint=(1, None),
                height=dp(20)
            )
            vars_label.bind(size=vars_label.setter('text_size'))
            self.add_widget(vars_label)
            
            for var in self.variables:
                var_text = f"  {var['symbol']}: {var['name']} ({var['unit']})"
                var_label = Label(
                    text=var_text,
                    font_size=sp(13),
                    color=[0.4, 0.4, 0.4, 1],
                    halign='left',
                    size_hint=(1, None),
                    height=dp(20)
                )
                var_label.bind(size=var_label.setter('text_size'))
                self.add_widget(var_label)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.border.pos = [self.pos[0]-dp(1), self.pos[1]-dp(1)]
        self.border.size = [self.size[0]+dp(2), self.size[1]+dp(2)]

class CalculatorInput(BoxLayout):
    """Input field untuk kalkulator dengan label"""
    label = StringProperty('')
    unit = StringProperty('')
    value = StringProperty('')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint = (1, None)
        self.height = dp(60)
        self.spacing = dp(10)
        
        # Label
        label_widget = Label(
            text=self.label,
            font_size=sp(16),
            size_hint=(0.4, 1),
            halign='left'
        )
        label_widget.bind(size=label_widget.setter('text_size'))
        self.add_widget(label_widget)
        
        # Input field
        self.input_field = TextInput(
            text=self.value,
            multiline=False,
            font_size=sp(16),
            size_hint=(0.4, 1),
            background_color=[1, 1, 1, 1],
            foreground_color=[0, 0, 0, 1],
            padding=[dp(10), dp(10)],
            write_tab=False,
            input_filter='float'
        )
        self.add_widget(self.input_field)
        
        # Unit
        unit_widget = Label(
            text=self.unit,
            font_size=sp(16),
            size_hint=(0.2, 1),
            halign='left'
        )
        self.add_widget(unit_widget)

# ============================================================================
# SCREEN APLIKASI
# ============================================================================

class HomeScreen(Screen):
    """Halaman utama aplikasi"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'home'
        
        # Layout utama
        main_layout = BoxLayout(orientation='vertical')
        
        # Header
        header = BoxLayout(size_hint=(1, 0.15))
        with header.canvas.before:
            Color(0.2, 0.6, 0.9, 1)
            Rectangle(pos=header.pos, size=header.size)
        
        title_label = Label(
            text='JHS Physics Formulas',
            font_size=sp(28),
            bold=True,
            color=[0, 0, 0, 1]
        )
        header.add_widget(title_label)
        
        # Konten utama
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        # Gambar/ilustrasi (simulasi)
        illustration = BoxLayout(
            size_hint=(1, 0.3),
            orientation='vertical',
            padding=dp(10)
        )
        
        with illustration.canvas.before:
            Color(0.9, 0.95, 1, 1)
            RoundedRectangle(pos=illustration.pos, size=illustration.size, radius=[20])
        
        illustration_label = Label(
            text='[📚]',
            font_size=sp(40),
            markup=True
        )
        illustration.add_widget(illustration_label)
        
        illustration_text = Label(
            text='Pelajari rumus fisika SMP dengan mudah',
            font_size=sp(14),
            color=[0.4, 0.4, 0.4, 1]
        )
        illustration.add_widget(illustration_text)
        
        content.add_widget(illustration)
        
        # Menu utama
        menu_layout = GridLayout(cols=2, spacing=dp(15), size_hint=(1, 0.5))
        
        # Tombol Daftar Rumus
        btn_formulas = Button(
            text='[📋] Daftar\nRumus',
            font_size=sp(18),
            bold=True,
            background_color=[0.3, 0.7, 0.5, 1],
            color=[1, 1, 1, 1],
            size_hint=(1, 1),
            on_press=self.go_to_formulas
        )
        btn_formulas.bind(size=self.update_button_font)
        
        # Tombol Kalkulator
        btn_calculator = Button(
            text='[🧮] Kalkulator\nFisika',
            font_size=sp(18),
            bold=True,
            background_color=[0.9, 0.5, 0.2, 1],
            color=[1, 1, 1, 1],
            size_hint=(1, 1),
            on_press=self.go_to_calculator
        )
        btn_calculator.bind(size=self.update_button_font)
        
        # Tombol Kuis
        btn_quiz = Button(
            text='[📝] Kuis\nFisika',
            font_size=sp(18),
            bold=True,
            background_color=[0.8, 0.4, 0.7, 1],
            color=[1, 1, 1, 1],
            size_hint=(1, 1),
            on_press=self.go_to_quiz
        )
        btn_quiz.bind(size=self.update_button_font)
        
        # Tombol Tentang
        btn_about = Button(
            text='[ℹ️] Tentang\nAplikasi',
            font_size=sp(18),
            bold=True,
            background_color=[0.6, 0.4, 0.8, 1],
            color=[1, 1, 1, 1],
            size_hint=(1, 1),
            on_press=self.go_to_about
        )
        btn_about.bind(size=self.update_button_font)
        
        menu_layout.add_widget(btn_formulas)
        menu_layout.add_widget(btn_calculator)
        menu_layout.add_widget(btn_quiz)
        menu_layout.add_widget(btn_about)
        
        content.add_widget(menu_layout)
        
        # Footer
        footer = BoxLayout(size_hint=(1, 0.1))
        footer_label = Label(
            text='© 2026 Fisika SMP App v1.0',
            font_size=sp(12),
            color=[0.5, 0.5, 0.5, 1]
        )
        footer.add_widget(footer_label)
        
        # Gabungkan semua komponen
        main_layout.add_widget(header)
        main_layout.add_widget(content)
        main_layout.add_widget(footer)
        
        self.add_widget(main_layout)
    
    def update_button_font(self, instance, value):
        """Menyesuaikan ukuran font tombol"""
        instance.font_size = sp(min(18, instance.height * 0.15))
    
    def go_to_formulas(self, instance):
        """Navigasi ke halaman daftar rumus"""
        self.manager.current = 'formula_list'
    
    def go_to_calculator(self, instance):
        """Navigasi ke halaman kalkulator"""
        self.manager.current = 'calculator'
    
    def go_to_quiz(self, instance):
        """Navigasi ke halaman kuis"""
        self.manager.current = 'quiz'
    
    def go_to_about(self, instance):
        """Navigasi ke halaman tentang"""
        self.manager.current = 'about'

class FormulaListScreen(Screen):
    """Halaman daftar rumus fisika"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'formula_list'
        
        # Layout utama
        main_layout = BoxLayout(orientation='vertical')
        
        # Header dengan tombol kembali
        header = BoxLayout(size_hint=(1, 0.12), padding=[dp(10), 0, dp(10), 0])
        with header.canvas.before:
            Color(0.2, 0.6, 0.9, 1)
            Rectangle(pos=header.pos, size=header.size)
        
        # Tombol kembali
        back_btn = Button(
            text='←',
            font_size=sp(28),
            size_hint=(None, 1),
            width=dp(50),
            background_color=[0.2, 0.6, 0.9, 1],
            color=[1, 1, 1, 1],
            on_press=self.go_back
        )
        
        # Judul
        title_label = Label(
            text='Daftar Rumus Fisika',
            font_size=sp(22),
            bold=True,
            color=[0, 0, 0, 1]
        )
        
        # Spacer
        spacer = Widget(size_hint=(None, 1), width=dp(50))
        
        header.add_widget(back_btn)
        header.add_widget(title_label)
        header.add_widget(spacer)
        
        # Konten dengan ScrollView
        scroll = ScrollView(size_hint=(1, 1))
        
        # Grid layout untuk kartu-kartu rumus
        self.content_layout = GridLayout(
            cols=1,
            spacing=dp(15),
            size_hint_y=None,
            padding=[dp(15), dp(15), dp(15), dp(15)]
        )
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))
        
        # Ambil data rumus
        formulas = FormulaData.get_all_formulas()
        
        # Tambahkan kartu untuk setiap materi
        for formula_id, formula_data in formulas.items():
            card = PhysicsCard(
                title=formula_data['title'],
                subtitle=formula_data['category'],
                color=formula_data['color']
            )
            card.bind(on_press=lambda instance, fid=formula_id: self.show_formula_detail(fid))
            self.content_layout.add_widget(card)
        
        scroll.add_widget(self.content_layout)
        
        # Gabungkan semua komponen
        main_layout.add_widget(header)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def go_back(self, instance):
        """Kembali ke halaman sebelumnya"""
        self.manager.current = 'home'
    
    def show_formula_detail(self, formula_id):
        """Menampilkan detail rumus"""
        self.manager.get_screen('formula_detail').load_formula(formula_id)
        self.manager.current = 'formula_detail'

class FormulaDetailScreen(Screen):
    """Halaman detail rumus"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'formula_detail'
        self.current_formula_id = None
        
        # Layout utama
        main_layout = BoxLayout(orientation='vertical')
        
        # Header dengan tombol kembali
        self.header = BoxLayout(size_hint=(1, 0.12), padding=[dp(10), 0, dp(10), 0])
        with self.header.canvas.before:
            Color(0.2, 0.6, 0.9, 1)
            self.header_rect = Rectangle(pos=self.header.pos, size=self.header.size)
        
        self.header.bind(pos=self.update_header_rect, size=self.update_header_rect)
        
        # Tombol kembali
        back_btn = Button(
            text='←',
            font_size=sp(28),
            size_hint=(None, 1),
            width=dp(50),
            background_color=[0.2, 0.6, 0.9, 1],
            color=[1, 1, 1, 1],
            on_press=self.go_back
        )
        
        # Judul (akan diupdate)
        self.title_label = Label(
            text='Detail Rumus',
            font_size=sp(22),
            bold=True,
            color=[1, 1, 1, 1]
        )
        
        # Spacer
        spacer = Widget(size_hint=(None, 1), width=dp(50))
        
        self.header.add_widget(back_btn)
        self.header.add_widget(self.title_label)
        self.header.add_widget(spacer)
        
        # Konten dengan ScrollView
        self.scroll = ScrollView(size_hint=(1, 1))
        
        # Layout konten
        self.content_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=[dp(20), dp(20), dp(20), dp(20)],
            spacing=dp(20)
        )
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))
        
        self.scroll.add_widget(self.content_layout)
        
        # Gabungkan semua komponen
        main_layout.add_widget(self.header)
        main_layout.add_widget(self.scroll)
        
        self.add_widget(main_layout)
    
    def update_header_rect(self, *args):
        self.header_rect.pos = self.header.pos
        self.header_rect.size = self.header.size
    
    def load_formula(self, formula_id):
        """Memuat data rumus berdasarkan ID"""
        self.current_formula_id = formula_id
        formula_data = FormulaData.get_formula_by_id(formula_id)
        
        if not formula_data:
            return
        
        # Update header
        self.title_label.text = formula_data['title']
        with self.header.canvas.before:
            Color(*formula_data['color'])
            self.header_rect = Rectangle(pos=self.header.pos, size=self.header.size)
        
        # Clear konten sebelumnya
        self.content_layout.clear_widgets()
        
        # Tambahkan judul dan kategori
        title_container = BoxLayout(orientation='vertical', size_hint=(1, None), height=dp(80))
        
        main_title = Label(
            text=formula_data['title'],
            font_size=sp(28),
            bold=True,
            color=[0.1, 0.1, 0.1, 1],
            halign='center',
            size_hint=(1, 0.6)
        )
        main_title.bind(size=main_title.setter('text_size'))
        
        category = Label(
            text=formula_data['category'],
            font_size=sp(16),
            color=[0.5, 0.5, 0.5, 1],
            halign='center',
            size_hint=(1, 0.4)
        )
        category.bind(size=category.setter('text_size'))
        
        title_container.add_widget(main_title)
        title_container.add_widget(category)
        self.content_layout.add_widget(title_container)
        
        # Tambahkan kartu untuk setiap rumus
        for formula in formula_data['formulas']:
            card = FormulaCard(
                formula_name=formula['name'],
                formula=formula['formula'],
                description=formula['description'],
                variables=formula['variables']
            )
            self.content_layout.add_widget(card)
            
            # Tambahkan contoh jika ada
            if 'example' in formula:
                example_box = BoxLayout(
                    orientation='vertical',
                    size_hint=(1, None),
                    padding=[dp(10), dp(10)],
                    spacing=dp(5)
                )
                
                with example_box.canvas.before:
                    Color(0.95, 0.98, 0.95, 1)
                    RoundedRectangle(pos=example_box.pos, size=example_box.size, radius=[10])
                
                example_title = Label(
                    text='Contoh:',
                    font_size=sp(14),
                    bold=True,
                    color=[0.2, 0.5, 0.2, 1],
                    halign='left',
                    size_hint=(1, None),
                    height=dp(20)
                )
                example_title.bind(size=example_title.setter('text_size'))
                
                example_text = Label(
                    text=formula['example'],
                    font_size=sp(13),
                    color=[0.3, 0.3, 0.3, 1],
                    halign='left',
                    size_hint=(1, None),
                    height=dp(40)
                )
                example_text.bind(size=example_text.setter('text_size'))
                
                example_box.add_widget(example_title)
                example_box.add_widget(example_text)
                self.content_layout.add_widget(example_box)
            
            # Tambahkan catatan jika ada
            if 'notes' in formula:
                notes_box = BoxLayout(
                    orientation='vertical',
                    size_hint=(1, None),
                    padding=[dp(10), dp(10)],
                    spacing=dp(5)
                )
                
                with notes_box.canvas.before:
                    Color(0.98, 0.98, 0.9, 1)
                    RoundedRectangle(pos=notes_box.pos, size=notes_box.size, radius=[10])
                
                notes_title = Label(
                    text='Catatan:',
                    font_size=sp(14),
                    bold=True,
                    color=[0.6, 0.5, 0.1, 1],
                    halign='left',
                    size_hint=(1, None),
                    height=dp(20)
                )
                notes_title.bind(size=notes_title.setter('text_size'))
                
                notes_text = Label(
                    text=formula['notes'],
                    font_size=sp(13),
                    color=[0.4, 0.4, 0.2, 1],
                    halign='left',
                    size_hint=(1, None),
                    height=dp(40)
                )
                notes_text.bind(size=notes_text.setter('text_size'))
                
                notes_box.add_widget(notes_title)
                notes_box.add_widget(notes_text)
                self.content_layout.add_widget(notes_box)
        
        # Update tinggi konten layout
        self.content_layout.height = sum(child.height for child in self.content_layout.children) + dp(40)
    
    def go_back(self, instance):
        """Kembali ke halaman daftar rumus"""
        self.manager.current = 'formula_list'

class CalculatorScreen(Screen):
    """Halaman kalkulator fisika"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'calculator'
        self.current_calculator = 'kecepatan'  # Default
        
        # Layout utama
        main_layout = BoxLayout(orientation='vertical')
        
        # Header dengan tombol kembali
        header = BoxLayout(size_hint=(1, 0.12), padding=[dp(10), 0, dp(10), 0])
        with header.canvas.before:
            Color(0.2, 0.6, 0.9, 1)
            Rectangle(pos=header.pos, size=header.size)
        
        # Tombol kembali
        back_btn = Button(
            text='←',
            font_size=sp(28),
            size_hint=(None, 1),
            width=dp(50),
            background_color=[0.2, 0.6, 0.9, 1],
            color=[1, 1, 1, 1],
            on_press=self.go_back
        )
        
        # Judul
        title_label = Label(
            text='Kalkulator Fisika',
            font_size=sp(22),
            bold=True,
            color=[1, 1, 1, 1]
        )
        
        # Spacer
        spacer = Widget(size_hint=(None, 1), width=dp(50))
        
        header.add_widget(back_btn)
        header.add_widget(title_label)
        header.add_widget(spacer)
        
        # Konten
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        # Pilihan kalkulator
        calc_selector = GridLayout(cols=3, spacing=dp(10), size_hint=(1, None), height=dp(50))
        
        kecepatan_btn = ToggleButton(
            text='Kecepatan',
            group='calculator',
            state='down' if self.current_calculator == 'kecepatan' else 'normal',
            on_press=lambda x: self.switch_calculator('kecepatan')
        )
        
        gaya_btn = ToggleButton(
            text='Gaya',
            group='calculator',
            state='down' if self.current_calculator == 'gaya' else 'normal',
            on_press=lambda x: self.switch_calculator('gaya')
        )
        
        tekanan_btn = ToggleButton(
            text='Tekanan',
            group='calculator',
            state='down' if self.current_calculator == 'tekanan' else 'normal',
            on_press=lambda x: self.switch_calculator('tekanan')
        )
        
        calc_selector.add_widget(kecepatan_btn)
        calc_selector.add_widget(gaya_btn)
        calc_selector.add_widget(tekanan_btn)
        
        content.add_widget(calc_selector)
        
        # Area kalkulator
        self.calculator_area = BoxLayout(orientation='vertical', spacing=dp(15))
        self.setup_kecepatan_calculator()
        
        content.add_widget(self.calculator_area)
        
        # Gabungkan semua komponen
        main_layout.add_widget(header)
        main_layout.add_widget(content)
        
        self.add_widget(main_layout)
    
    def go_back(self, instance):
        """Kembali ke halaman utama"""
        self.manager.current = 'home'
    
    def switch_calculator(self, calculator_type):
        """Mengganti jenis kalkulator"""
        self.current_calculator = calculator_type
        self.calculator_area.clear_widgets()
        
        if calculator_type == 'kecepatan':
            self.setup_kecepatan_calculator()
        elif calculator_type == 'gaya':
            self.setup_gaya_calculator()
        elif calculator_type == 'tekanan':
            self.setup_tekanan_calculator()
    
    def setup_kecepatan_calculator(self):
        """Setup kalkulator kecepatan"""
        # Judul
        title = Label(
            text='Hitung Kecepatan (v = s/t)',
            font_size=sp(20),
            bold=True,
            color=[0.1, 0.1, 0.1, 1],
            size_hint=(1, None),
            height=dp(40)
        )
        self.calculator_area.add_widget(title)
        
        # Input jarak
        self.jarak_input = CalculatorInput(label='Jarak (s):', unit='m')
        self.calculator_area.add_widget(self.jarak_input)
        
        # Input waktu
        self.waktu_input = CalculatorInput(label='Waktu (t):', unit='s')
        self.calculator_area.add_widget(self.waktu_input)
        
        # Tombol hitung
        calculate_btn = Button(
            text='HITUNG KECEPATAN',
            font_size=sp(18),
            bold=True,
            background_color=[0.2, 0.6, 0.9, 1],
            color=[1, 1, 1, 1],
            size_hint=(1, None),
            height=dp(50),
            on_press=self.calculate_kecepatan
        )
        self.calculator_area.add_widget(calculate_btn)
        
        # Hasil
        self.result_label = Label(
            text='Hasil akan muncul di sini',
            font_size=sp(16),
            color=[0.3, 0.3, 0.3, 1],
            size_hint=(1, None),
            height=dp(80)
        )
        self.calculator_area.add_widget(self.result_label)
    
    def setup_gaya_calculator(self):
        """Setup kalkulator gaya"""
        # Judul
        title = Label(
            text='Hitung Gaya (F = m × a)',
            font_size=sp(20),
            bold=True,
            color=[0.1, 0.1, 0.1, 1],
            size_hint=(1, None),
            height=dp(40)
        )
        self.calculator_area.add_widget(title)
        
        # Input massa
        self.massa_input = CalculatorInput(label='Massa (m):', unit='kg')
        self.calculator_area.add_widget(self.massa_input)
        
        # Input percepatan
        self.percepatan_input = CalculatorInput(label='Percepatan (a):', unit='m/s²')
        self.calculator_area.add_widget(self.percepatan_input)
        
        # Tombol hitung
        calculate_btn = Button(
            text='HITUNG GAYA',
            font_size=sp(18),
            bold=True,
            background_color=[0.9, 0.5, 0.2, 1],
            color=[1, 1, 1, 1],
            size_hint=(1, None),
            height=dp(50),
            on_press=self.calculate_gaya
        )
        self.calculator_area.add_widget(calculate_btn)
        
        # Hasil
        self.result_label = Label(
            text='Hasil akan muncul di sini',
            font_size=sp(16),
            color=[0.3, 0.3, 0.3, 1],
            size_hint=(1, None),
            height=dp(80)
        )
        self.calculator_area.add_widget(self.result_label)
    
    def setup_tekanan_calculator(self):
        """Setup kalkulator tekanan"""
        # Judul
        title = Label(
            text='Hitung Tekanan (P = F/A)',
            font_size=sp(20),
            bold=True,
            color=[0.1, 0.1, 0.1, 1],
            size_hint=(1, None),
            height=dp(40)
        )
        self.calculator_area.add_widget(title)
        
        # Input gaya
        self.gaya_input = CalculatorInput(label='Gaya (F):', unit='N')
        self.calculator_area.add_widget(self.gaya_input)
        
        # Input luas
        self.luas_input = CalculatorInput(label='Luas (A):', unit='m²')
        self.calculator_area.add_widget(self.luas_input)
        
        # Tombol hitung
        calculate_btn = Button(
            text='HITUNG TEKANAN',
            font_size=sp(18),
            bold=True,
            background_color=[0.3, 0.7, 0.5, 1],
            color=[1, 1, 1, 1],
            size_hint=(1, None),
            height=dp(50),
            on_press=self.calculate_tekanan
        )
        self.calculator_area.add_widget(calculate_btn)
        
        # Hasil
        self.result_label = Label(
            text='Hasil akan muncul di sini',
            font_size=sp(16),
            color=[0.3, 0.3, 0.3, 1],
            size_hint=(1, None),
            height=dp(80)
        )
        self.calculator_area.add_widget(self.result_label)
    
    def calculate_kecepatan(self, instance):
        """Menghitung kecepatan"""
        try:
            # Ambil nilai dari input
            jarak = float(self.jarak_input.input_field.text)
            waktu = float(self.waktu_input.input_field.text)
            
            # Validasi input
            if waktu == 0:
                self.result_label.text = 'Error: Waktu tidak boleh nol!'
                self.result_label.color = [1, 0, 0, 1]
                return
            
            # Hitung kecepatan
            kecepatan = jarak / waktu
            
            # Tampilkan hasil
            self.result_label.text = f'Hasil:\nKecepatan = {kecepatan:.2f} m/s\n\nv = s / t\nv = {jarak} / {waktu}\nv = {kecepatan:.2f} m/s'
            self.result_label.color = [0, 0.5, 0, 1]
            
        except ValueError:
            self.result_label.text = 'Error: Masukkan angka yang valid!'
            self.result_label.color = [1, 0, 0, 1]
        except Exception as e:
            self.result_label.text = f'Error: {str(e)}'
            self.result_label.color = [1, 0, 0, 1]
    
    def calculate_gaya(self, instance):
        """Menghitung gaya"""
        try:
            # Ambil nilai dari input
            massa = float(self.massa_input.input_field.text)
            percepatan = float(self.percepatan_input.input_field.text)
            
            # Hitung gaya
            gaya = massa * percepatan
            
            # Tampilkan hasil
            self.result_label.text = f'Hasil:\nGaya = {gaya:.2f} N\n\nF = m × a\nF = {massa} × {percepatan}\nF = {gaya:.2f} N'
            self.result_label.color = [0, 0.5, 0, 1]
            
        except ValueError:
            self.result_label.text = 'Error: Masukkan angka yang valid!'
            self.result_label.color = [1, 0, 0, 1]
        except Exception as e:
            self.result_label.text = f'Error: {str(e)}'
            self.result_label.color = [1, 0, 0, 1]
    
    def calculate_tekanan(self, instance):
        """Menghitung tekanan"""
        try:
            # Ambil nilai dari input
            gaya = float(self.gaya_input.input_field.text)
            luas = float(self.luas_input.input_field.text)
            
            # Validasi input
            if luas == 0:
                self.result_label.text = 'Error: Luas tidak boleh nol!'
                self.result_label.color = [1, 0, 0, 1]
                return
            
            # Hitung tekanan
            tekanan = gaya / luas
            
            # Tampilkan hasil
            self.result_label.text = f'Hasil:\nTekanan = {tekanan:.2f} Pa\n\nP = F / A\nP = {gaya} / {luas}\nP = {tekanan:.2f} Pa'
            self.result_label.color = [0, 0.5, 0, 1]
            
        except ValueError:
            self.result_label.text = 'Error: Masukkan angka yang valid!'
            self.result_label.color = [1, 0, 0, 1]
        except Exception as e:
            self.result_label.text = f'Error: {str(e)}'
            self.result_label.color = [1, 0, 0, 1]

class AboutScreen(Screen):
    """Halaman tentang aplikasi"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'about'
        
        # Layout utama
        main_layout = BoxLayout(orientation='vertical')
        
        # Header dengan tombol kembali
        header = BoxLayout(size_hint=(1, 0.12), padding=[dp(10), 0, dp(10), 0])
        with header.canvas.before:
            Color(0.2, 0.6, 0.9, 1)
            Rectangle(pos=header.pos, size=header.size)
        
        # Tombol kembali
        back_btn = Button(
            text='←',
            font_size=sp(28),
            size_hint=(None, 1),
            width=dp(50),
            background_color=[0.2, 0.6, 0.9, 1],
            color=[1, 1, 1, 1],
            on_press=self.go_back
        )
        
        # Judul
        title_label = Label(
            text='Tentang Aplikasi',
            font_size=sp(22),
            bold=True,
            color=[1, 1, 1, 1]
        )
        
        # Spacer
        spacer = Widget(size_hint=(None, 1), width=dp(50))
        
        header.add_widget(back_btn)
        header.add_widget(title_label)
        header.add_widget(spacer)
        
        # Konten dengan ScrollView
        scroll = ScrollView(size_hint=(1, 1))
        
        content = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=[dp(20), dp(20)],
            spacing=dp(20)
        )
        content.bind(minimum_height=content.setter('height'))
        
        # Logo/ikon aplikasi
        logo_container = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(150),
            spacing=dp(10)
        )
        
        logo_label = Label(
            text='[📚]',
            font_size=sp(60),
            markup=True
        )
        
        app_name_label = Label(
            text='Junior High School Physics Formulas',
            font_size=sp(28),
            bold=True,
            color=[0.1, 0.1, 0.1, 1]
        )
        
        version_label = Label(
            text='Versi 1.0',
            font_size=sp(16),
            color=[0.5, 0.5, 0.5, 1]
        )
        
        logo_container.add_widget(logo_label)
        logo_container.add_widget(app_name_label)
        logo_container.add_widget(version_label)
        
        content.add_widget(logo_container)
        
        # Deskripsi aplikasi
        desc_box = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            padding=[dp(15), dp(15)],
            spacing=dp(10)
        )
        
        with desc_box.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            RoundedRectangle(pos=desc_box.pos, size=desc_box.size, radius=[10])
        
        desc_title = Label(
            text='Deskripsi Aplikasi',
            font_size=sp(18),
            bold=True,
            color=[0.1, 0.1, 0.1, 1],
            size_hint=(1, None),
            height=dp(30)
        )
        desc_title.bind(size=desc_title.setter('text_size'))
        
        desc_text = Label(
            text='Aplikasi Rumus Fisika SMP adalah aplikasi mobile yang membantu siswa SMP mempelajari dan memahami rumus-rumus fisika dengan mudah. Aplikasi ini dilengkapi dengan:\n\n• Daftar rumus fisika SMP lengkap\n• Kalkulator fisika interaktif\n• Penjelasan detail setiap rumus\n• Contoh perhitungan\n• UI yang ramah pengguna',
            font_size=sp(14),
            color=[0.3, 0.3, 0.3, 1],
            size_hint=(1, None),
            height=dp(180)
        )
        desc_text.bind(size=desc_text.setter('text_size'))
        
        desc_box.add_widget(desc_title)
        desc_box.add_widget(desc_text)
        content.add_widget(desc_box)
        
        # Fitur aplikasi
        features_box = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            padding=[dp(15), dp(15)],
            spacing=dp(10)
        )
        
        with features_box.canvas.before:
            Color(0.9, 0.95, 1, 1)
            RoundedRectangle(pos=features_box.pos, size=features_box.size, radius=[10])
        
        features_title = Label(
            text='Fitur Utama',
            font_size=sp(18),
            bold=True,
            color=[0.1, 0.1, 0.1, 1],
            size_hint=(1, None),
            height=dp(30)
        )
        features_title.bind(size=features_title.setter('text_size'))
        
        features_text = Label(
            text='1. 📋 Daftar Rumus Lengkap\n   - 8 materi fisika SMP\n   - Detail setiap rumus\n   - Penjelasan dan contoh\n\n2. 🧮 Kalkulator Fisika\n   - Hitung kecepatan, gaya, tekanan\n   - Validasi input\n   - Tampilan langkah perhitungan\n\n3. 📝 Kuis Interaktif\n   - Latihan soal fisika\n   - Tingkat kesulitan berbeda\n   - Pembahasan jawaban\n\n4. 🎨 UI Responsif\n   - Desain modern dan rapi\n   - Navigasi mudah\n   - Kompatibel Android',
            font_size=sp(13),
            color=[0.3, 0.3, 0.3, 1],
            size_hint=(1, None),
            height=dp(280)
        )
        features_text.bind(size=features_text.setter('text_size'))
        
        features_box.add_widget(features_title)
        features_box.add_widget(features_text)
        content.add_widget(features_box)
        
        # Informasi pengembang
        dev_box = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            padding=[dp(15), dp(15)],
            spacing=dp(10)
        )
        
        with dev_box.canvas.before:
            Color(0.95, 0.98, 0.95, 1)
            RoundedRectangle(pos=dev_box.pos, size=dev_box.size, radius=[10])
        
        dev_title = Label(
            text='Pengembang',
            font_size=sp(18),
            bold=True,
            color=[0.1, 0.1, 0.1, 1],
            size_hint=(1, None),
            height=dp(30)
        )
        dev_title.bind(size=dev_title.setter('text_size'))
        
        dev_text = Label(
            text='Aplikasi ini dikembangkan untuk membantu pendidikan fisika di tingkat SMP.\n\nTeknologi:\n• Python 3.x\n• Kivy Framework\n• Buildozer (Android)\n\nKontak: fisika.smp@app.com\n\n© 2023 Rumus Fisika SMP',
            font_size=sp(13),
            color=[0.3, 0.3, 0.3, 1],
            size_hint=(1, None),
            height=dp(180)
        )
        dev_text.bind(size=dev_text.setter('text_size'))
        
        dev_box.add_widget(dev_title)
        dev_box.add_widget(dev_text)
        content.add_widget(dev_box)
        
        # Update tinggi konten
        content.height = sum(child.height for child in content.children) + dp(40)
        
        scroll.add_widget(content)
        
        # Gabungkan semua komponen
        main_layout.add_widget(header)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def go_back(self, instance):
        """Kembali ke halaman utama"""
        self.manager.current = 'home'

class QuizScreen(Screen):
    """Halaman kuis fisika"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'quiz'
        self.current_question = 0
        self.score = 0
        self.questions = self.load_questions()
        
        # Layout utama
        main_layout = BoxLayout(orientation='vertical')
        
        # Header dengan tombol kembali
        header = BoxLayout(size_hint=(1, 0.12), padding=[dp(10), 0, dp(10), 0])
        with header.canvas.before:
            Color(0.2, 0.6, 0.9, 1)
            Rectangle(pos=header.pos, size=header.size)
        
        # Tombol kembali
        back_btn = Button(
            text='←',
            font_size=sp(28),
            size_hint=(None, 1),
            width=dp(50),
            background_color=[0.2, 0.6, 0.9, 1],
            color=[1, 1, 1, 1],
            on_press=self.go_back
        )
        
        # Judul
        title_label = Label(
            text='Kuis Fisika',
            font_size=sp(22),
            bold=True,
            color=[1, 1, 1, 1]
        )
        
        # Spacer
        spacer = Widget(size_hint=(None, 1), width=dp(50))
        
        header.add_widget(back_btn)
        header.add_widget(title_label)
        header.add_widget(spacer)
        
        # Konten
        self.content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Inisialisasi kuis
        self.init_quiz()
        
        # Gabungkan semua komponen
        main_layout.add_widget(header)
        main_layout.add_widget(self.content)
        
        self.add_widget(main_layout)
    
    def load_questions(self):
        """Memuat soal-soal kuis"""
        questions = [
            {
                'question': 'Rumus untuk menghitung kecepatan adalah...',
                'options': ['v = s × t', 'v = s / t', 'v = t / s', 'v = m × a'],
                'correct': 1,
                'explanation': 'Kecepatan = Jarak / Waktu (v = s/t)'
            },
            {
                'question': 'Satuan dari gaya dalam SI adalah...',
                'options': ['Joule', 'Watt', 'Newton', 'Pascal'],
                'correct': 2,
                'explanation': 'Satuan gaya adalah Newton (N)'
            },
            {
                'question': 'Rumus hukum Newton II adalah...',
                'options': ['F = m / a', 'F = m × a', 'F = m + a', 'F = m - a'],
                'correct': 1,
                'explanation': 'Hukum Newton II: F = m × a'
            },
            {
                'question': 'Tekanan dihitung dengan rumus...',
                'options': ['P = F × A', 'P = F / A', 'P = A / F', 'P = F + A'],
                'correct': 1,
                'explanation': 'Tekanan = Gaya / Luas (P = F/A)'
            },
            {
                'question': 'Energi kinetik dihitung dengan...',
                'options': ['EK = m × v', 'EK = ½ × m × v²', 'EK = m × g × h', 'EK = F × s'],
                'correct': 1,
                'explanation': 'Energi kinetik = ½ × massa × kecepatan²'
            }
        ]
        return questions
    
    def init_quiz(self):
        """Inisialisasi tampilan kuis"""
        self.content.clear_widgets()
        
        # Judul kuis
        title = Label(
            text='Kuis Fisika SMP',
            font_size=sp(24),
            bold=True,
            color=[0.1, 0.1, 0.1, 1],
            size_hint=(1, None),
            height=dp(50)
        )
        self.content.add_widget(title)
        
        # Deskripsi
        desc = Label(
            text='Uji pemahamanmu tentang rumus fisika SMP!\nJawab 5 soal pilihan ganda.',
            font_size=sp(14),
            color=[0.4, 0.4, 0.4, 1],
            size_hint=(1, None),
            height=dp(60)
        )
        self.content.add_widget(desc)
        
        # Tombol mulai
        start_btn = Button(
            text='MULAI KUIS',
            font_size=sp(20),
            bold=True,
            background_color=[0.8, 0.4, 0.7, 1],
            color=[1, 1, 1, 1],
            size_hint=(1, None),
            height=dp(60),
            on_press=self.start_quiz
        )
        self.content.add_widget(start_btn)
    
    def start_quiz(self, instance):
        """Memulai kuis"""
        self.current_question = 0
        self.score = 0
        self.show_question()
    
    def show_question(self):
        """Menampilkan soal saat ini"""
        self.content.clear_widgets()
        
        # Progress bar
        progress_text = Label(
            text=f'Soal {self.current_question + 1} dari {len(self.questions)}',
            font_size=sp(16),
            color=[0.4, 0.4, 0.4, 1],
            size_hint=(1, None),
            height=dp(30)
        )
        self.content.add_widget(progress_text)
        
        # Progress bar visual
        progress_container = BoxLayout(size_hint=(1, None), height=dp(20))
        progress_bar = ProgressBar(
            max=len(self.questions),
            value=self.current_question + 1,
            size_hint=(1, 1)
        )
        progress_container.add_widget(progress_bar)
        self.content.add_widget(progress_container)
        
        # Skor
        score_label = Label(
            text=f'Skor: {self.score}',
            font_size=sp(16),
            bold=True,
            color=[0.2, 0.6, 0.2, 1],
            size_hint=(1, None),
            height=dp(30)
        )
        self.content.add_widget(score_label)
        
        # Soal
        question_data = self.questions[self.current_question]
        question_text = Label(
            text=question_data['question'],
            font_size=sp(18),
            bold=True,
            color=[0.1, 0.1, 0.1, 1],
            size_hint=(1, None),
            height=dp(100)
        )
        question_text.bind(size=question_text.setter('text_size'))
        self.content.add_widget(question_text)
        
        # Opsi jawaban
        options_container = BoxLayout(orientation='vertical', spacing=dp(10), size_hint=(1, 0.6))
        
        for i, option in enumerate(question_data['options']):
            option_btn = Button(
                text=option,
                font_size=sp(16),
                background_color=[0.9, 0.95, 1, 1],
                color=[0.1, 0.1, 0.1, 1],
                size_hint=(1, 1),
                on_press=lambda instance, idx=i: self.check_answer(idx)
            )
            options_container.add_widget(option_btn)
        
        self.content.add_widget(options_container)
    
    def check_answer(self, selected_option):
        """Memeriksa jawaban"""
        question_data = self.questions[self.current_question]
        correct = (selected_option == question_data['correct'])
        
        if correct:
            self.score += 1
        
        # Tampilkan hasil
        self.show_answer_result(correct, question_data)
    
    def show_answer_result(self, correct, question_data):
        """Menampilkan hasil jawaban"""
        self.content.clear_widgets()
        
        # Ikon hasil
        result_icon = Label(
            text='[✓]' if correct else '[✗]',
            font_size=sp(60),
            markup=True,
            color=[0, 0.6, 0, 1] if correct else [1, 0, 0, 1],
            size_hint=(1, None),
            height=dp(100)
        )
        self.content.add_widget(result_icon)
        
        # Pesan hasil
        result_text = Label(
            text='Benar!' if correct else 'Salah!',
            font_size=sp(24),
            bold=True,
            color=[0, 0.6, 0, 1] if correct else [1, 0, 0, 1],
            size_hint=(1, None),
            height=dp(50)
        )
        self.content.add_widget(result_text)
        
        # Penjelasan
        explanation = Label(
            text=question_data['explanation'],
            font_size=sp(16),
            color=[0.3, 0.3, 0.3, 1],
            size_hint=(1, None),
            height=dp(100)
        )
        explanation.bind(size=explanation.setter('text_size'))
        self.content.add_widget(explanation)
        
        # Skor saat ini
        score_label = Label(
            text=f'Skor: {self.score} / {len(self.questions)}',
            font_size=sp(18),
            bold=True,
            color=[0.2, 0.2, 0.8, 1],
            size_hint=(1, None),
            height=dp(50)
        )
        self.content.add_widget(score_label)
        
        # Tombol lanjut
        next_text = 'Lanjut' if self.current_question < len(self.questions) - 1 else 'Lihat Hasil'
        next_btn = Button(
            text=next_text,
            font_size=sp(18),
            bold=True,
            background_color=[0.2, 0.6, 0.9, 1],
            color=[1, 1, 1, 1],
            size_hint=(1, None),
            height=dp(50),
            on_press=self.next_question
        )
        self.content.add_widget(next_btn)
    
    def next_question(self, instance):
        """Lanjut ke soal berikutnya"""
        self.current_question += 1
        
        if self.current_question < len(self.questions):
            self.show_question()
        else:
            self.show_final_results()
    
    def show_final_results(self):
        """Menampilkan hasil akhir"""
        self.content.clear_widgets()
        
        # Judul hasil
        result_title = Label(
            text='Hasil Kuis',
            font_size=sp(28),
            bold=True,
            color=[0.1, 0.1, 0.1, 1],
            size_hint=(1, None),
            height=dp(60)
        )
        self.content.add_widget(result_title)
        
        # Skor akhir
        percentage = (self.score / len(self.questions)) * 100
        score_text = Label(
            text=f'{self.score} / {len(self.questions)}',
            font_size=sp(48),
            bold=True,
            color=[0.2, 0.6, 0.2, 1] if percentage >= 70 else [0.9, 0.5, 0.2, 1],
            size_hint=(1, None),
            height=dp(100)
        )
        self.content.add_widget(score_text)
        
        # Persentase
        percent_text = Label(
            text=f'{percentage:.1f}%',
            font_size=sp(24),
            color=[0.4, 0.4, 0.4, 1],
            size_hint=(1, None),
            height=dp(50)
        )
        self.content.add_widget(percent_text)
        
        # Pesan
        if percentage >= 80:
            message = 'Luar biasa! Kamu menguasai fisika dengan baik.'
            emoji = '[🎉]'
        elif percentage >= 60:
            message = 'Bagus! Pemahamanmu tentang fisika sudah baik.'
            emoji = '[👍]'
        else:
            message = 'Perlu belajar lagi. Gunakan aplikasi ini untuk latihan!'
            emoji = '[📚]'
        
        emoji_label = Label(
            text=emoji,
            font_size=sp(40),
            markup=True,
            size_hint=(1, None),
            height=dp(80)
        )
        self.content.add_widget(emoji_label)
        
        message_label = Label(
            text=message,
            font_size=sp(16),
            color=[0.3, 0.3, 0.3, 1],
            size_hint=(1, None),
            height=dp(80)
        )
        message_label.bind(size=message_label.setter('text_size'))
        self.content.add_widget(message_label)
        
        # Tombol
        btn_container = GridLayout(cols=2, spacing=dp(10), size_hint=(1, None), height=dp(60))
        
        restart_btn = Button(
            text='Ulangi Kuis',
            font_size=sp(16),
            background_color=[0.2, 0.6, 0.9, 1],
            color=[1, 1, 1, 1],
            on_press=self.start_quiz
        )
        
        home_btn = Button(
            text='Ke Beranda',
            font_size=sp(16),
            background_color=[0.8, 0.4, 0.7, 1],
            color=[1, 1, 1, 1],
            on_press=self.go_back
        )
        
        btn_container.add_widget(restart_btn)
        btn_container.add_widget(home_btn)
        self.content.add_widget(btn_container)
    
    def go_back(self, instance):
        """Kembali ke halaman utama"""
        self.manager.current = 'home'

class SettingsScreen(Screen):
    """Halaman pengaturan (opsional)"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'settings'
        
        # Layout sederhana karena ini fitur opsional
        layout = BoxLayout(orientation='vertical')
        
        header = BoxLayout(size_hint=(1, 0.15))
        with header.canvas.before:
            Color(0.2, 0.6, 0.9, 1)
            Rectangle(pos=header.pos, size=header.size)
        
        title = Label(
            text='Pengaturan',
            font_size=sp(24),
            bold=True,
            color=[1, 1, 1, 1]
        )
        header.add_widget(title)
        
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        # Pesan
        message = Label(
            text='Fitur pengaturan akan dikembangkan lebih lanjut.\n\nAplikasi ini dalam versi 1.0 dengan fitur utama:\n• Daftar rumus lengkap\n• Kalkulator fisika\n• Kuis interaktif',
            font_size=sp(16),
            color=[0.3, 0.3, 0.3, 1],
            halign='center'
        )
        message.bind(size=message.setter('text_size'))
        
        content.add_widget(message)
        
        # Tombol kembali
        back_btn = Button(
            text='KEMBALI',
            font_size=sp(18),
            bold=True,
            background_color=[0.2, 0.6, 0.9, 1],
            color=[1, 1, 1, 1],
            size_hint=(1, None),
            height=dp(50),
            on_press=self.go_back
        )
        content.add_widget(back_btn)
        
        layout.add_widget(header)
        layout.add_widget(content)
        
        self.add_widget(layout)
    
    def go_back(self, instance):
        """Kembali ke halaman sebelumnya"""
        self.manager.current = 'home'

# ============================================================================
# FUNGSI UTAMA
# ============================================================================

if __name__ == '__main__':
    try:
        # Jalankan aplikasi
        PhysicsApp().run()
    except Exception as e:
        # Tangani error dan tampilkan pesan
        print(f"Error menjalankan aplikasi: {e}")
        import traceback
        traceback.print_exc()