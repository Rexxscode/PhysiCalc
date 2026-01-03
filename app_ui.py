"""
Konfigurasi UI dan styling untuk aplikasi
Menentukan warna, font, dan style yang konsisten
"""

from kivy.utils import get_color_from_hex
from kivy.metrics import dp, sp

# ===== Warna Tema =====
class Colors:
    """Class untuk warna tema aplikasi"""
    # Primary Colors
    PRIMARY = get_color_from_hex('#4361ee')
    PRIMARY_LIGHT = get_color_from_hex('#4895ef')
    PRIMARY_DARK = get_color_from_hex('#3a0ca3')
    
    # Secondary Colors
    SECONDARY = get_color_from_hex('#7209b7')
    SECONDARY_LIGHT = get_color_from_hex('#b5179e')
    
    # Accent Colors
    ACCENT = get_color_from_hex('#f72585')
    SUCCESS = get_color_from_hex('#4cc9f0')
    WARNING = get_color_from_hex('#f8961e')
    DANGER = get_color_from_hex('#f94144')
    
    # Neutral Colors
    WHITE = get_color_from_hex('#ffffff')
    LIGHT = get_color_from_hex('#f8f9fa')
    GRAY_LIGHT = get_color_from_hex('#e9ecef')
    GRAY = get_color_from_hex('#adb5bd')
    GRAY_DARK = get_color_from_hex('#495057')
    DARK = get_color_from_hex('#212529')
    BLACK = get_color_from_hex('#000000')
    
    # Background Colors
    BG_LIGHT = get_color_from_hex('#f8f9fa')
    BG_DARK = get_color_from_hex('#343a40')
    
    # Card Colors
    CARD_LIGHT = WHITE
    CARD_DARK = get_color_from_hex('#2d3748')

# ===== Font Configuration =====
class Fonts:
    """Class untuk konfigurasi font"""
    # Ukuran font (dalam sp)
    H1 = sp(32)
    H2 = sp(24)
    H3 = sp(20)
    H4 = sp(18)
    H5 = sp(16)
    BODY_LARGE = sp(18)
    BODY = sp(16)
    BODY_SMALL = sp(14)
    CAPTION = sp(12)
    
    # Weight
    LIGHT = 'light'
    REGULAR = 'regular'
    MEDIUM = 'medium'
    BOLD = 'bold'
    
    # Family (default Kivy font)
    FAMILY = 'Roboto'

# ===== Spacing =====
class Spacing:
    """Class untuk spacing yang konsisten"""
    XS = dp(4)
    SM = dp(8)
    MD = dp(16)
    LG = dp(24)
    XL = dp(32)
    XXL = dp(48)
    
    # Padding
    SCREEN_PADDING = dp(16)
    CARD_PADDING = dp(16)
    BUTTON_PADDING = (dp(24), dp(12))
    
    # Border Radius
    RADIUS_SM = dp(4)
    RADIUS_MD = dp(8)
    RADIUS_LG = dp(12)
    RADIUS_XL = dp(16)
    RADIUS_ROUND = dp(50)

# ===== Shadows =====
class Shadows:
    """Efek shadow untuk elemen UI"""
    @staticmethod
    def get_shadow(elevation=1):
        """Mengembalikan shadow effect berdasarkan elevation"""
        shadows = {
            1: {
                'offset': (0, dp(1)),
                'blur': dp(3),
                'color': (0, 0, 0, 0.12)
            },
            2: {
                'offset': (0, dp(2)),
                'blur': dp(4),
                'color': (0, 0, 0, 0.14)
            },
            3: {
                'offset': (0, dp(3)),
                'blur': dp(6),
                'color': (0, 0, 0, 0.16)
            },
            4: {
                'offset': (0, dp(4)),
                'blur': dp(8),
                'color': (0, 0, 0, 0.18)
            },
            5: {
                'offset': (0, dp(5)),
                'blur': dp(10),
                'color': (0, 0, 0, 0.20)
            }
        }
        return shadows.get(elevation, shadows[1])

# ===== Styles untuk Widget =====
class Styles:
    """Kumpulan style untuk widget umum"""
    
    @staticmethod
    def get_button_style(variant='primary', size='medium'):
        """Mengembalikan style untuk button berdasarkan variant dan size"""
        styles = {
            'primary': {
                'bg_color': Colors.PRIMARY,
                'text_color': Colors.WHITE,
                'border_color': Colors.PRIMARY,
            },
            'secondary': {
                'bg_color': Colors.SECONDARY,
                'text_color': Colors.WHITE,
                'border_color': Colors.SECONDARY,
            },
            'outline': {
                'bg_color': Colors.WHITE,
                'text_color': Colors.PRIMARY,
                'border_color': Colors.PRIMARY,
            },
            'text': {
                'bg_color': (0, 0, 0, 0),
                'text_color': Colors.PRIMARY,
                'border_color': (0, 0, 0, 0),
            }
        }
        
        sizes = {
            'small': {
                'height': dp(36),
                'font_size': Fonts.BODY_SMALL,
                'padding': (dp(16), dp(8)),
            },
            'medium': {
                'height': dp(44),
                'font_size': Fonts.BODY,
                'padding': (dp(24), dp(12)),
            },
            'large': {
                'height': dp(52),
                'font_size': Fonts.BODY_LARGE,
                'padding': (dp(32), dp(16)),
            }
        }
        
        style = styles.get(variant, styles['primary'])
        size_style = sizes.get(size, sizes['medium'])
        
        return {**style, **size_style}
    
    @staticmethod
    def get_card_style(elevation=1):
        """Mengembalikan style untuk card"""
        return {
            'bg_color': Colors.WHITE,
            'radius': Spacing.RADIUS_LG,
            'padding': Spacing.CARD_PADDING,
            'shadow': Shadows.get_shadow(elevation)
        }
    
    @staticmethod
    def get_input_style():
        """Mengembalikan style untuk input field"""
        return {
            'bg_color': Colors.WHITE,
            'border_color': Colors.GRAY_LIGHT,
            'border_width': dp(1),
            'radius': Spacing.RADIUS_MD,
            'padding': (dp(12), dp(12)),
            'font_size': Fonts.BODY,
            'color': Colors.DARK,
        }

# Export semua class
__all__ = ['Colors', 'Fonts', 'Spacing', 'Shadows', 'Styles']