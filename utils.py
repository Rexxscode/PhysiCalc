"""
Fungsi utilitas untuk aplikasi fisika SMP
"""

from kivy.utils import get_color_from_hex
from kivy.metrics import dp
import math

def validate_number_input(text, allow_negative=False, allow_zero=True, allow_empty=False):
    """Validasi input angka dengan berbagai kondisi"""
    if not text:
        if allow_empty:
            return True, ""
        return False, "Please enter a value"
    
    # Cek jika teks adalah angka valid
    try:
        # Coba parsing sebagai float
        value = float(text)
        
        # Cek infinity
        if math.isinf(value):
            return False, "Value is too large"
        
        # Cek NaN
        if math.isnan(value):
            return False, "Invalid number"
        
        # Validasi berdasarkan kondisi
        if not allow_negative and value < 0:
            return False, "Value cannot be negative"
        
        if not allow_zero and value == 0:
            return False, "Value cannot be zero"
        
        return True, ""
    
    except ValueError:
        # Coba parsing sebagai eksponen
        if 'e' in text.lower():
            try:
                value = float(text)
                return True, ""
            except:
                pass
        
        return False, "Invalid number format"

def format_result(value, unit, precision=2, scientific_threshold=1e-4):
    """
    Format hasil perhitungan dengan unit yang sesuai
    
    Args:
        value: Nilai yang akan diformat
        unit: Unit pengukuran
        precision: Jumlah digit desimal
        scientific_threshold: Threshold untuk notasi ilmiah
    """
    if value is None:
        return f"-- {unit}"
    
    try:
        value = float(value)
        
        # Handle nilai khusus
        if math.isnan(value):
            return f"NaN {unit}"
        
        if math.isinf(value):
            return f"∞ {unit}" if value > 0 else f"-∞ {unit}"
        
        # Format berdasarkan besaran nilai
        if value == 0:
            return f"0 {unit}"
        
        abs_value = abs(value)
        
        # Gunakan notasi ilmiah untuk nilai sangat kecil atau besar
        if abs_value < scientific_threshold or abs_value >= 1/scientific_threshold:
            formatted = f"{value:.{precision}e}"
        else:
            # Format biasa dengan separator ribuan jika perlu
            if abs_value >= 10000:
                formatted = f"{value:,.{precision}f}"
            else:
                formatted = f"{value:.{precision}f}"
            
            # Hapus trailing zeros
            if '.' in formatted:
                formatted = formatted.rstrip('0').rstrip('.')
        
        return f"{formatted} {unit}"
    
    except (ValueError, TypeError):
        return f"{value} {unit}"

def get_category_color(category):
    """Mengembalikan warna berdasarkan kategori rumus"""
    from app_ui import Colors
    
    color_map = {
        'Kinematics': Colors.PRIMARY,
        'Dynamics': Colors.SECONDARY,
        'Energy': get_color_from_hex('#2ecc71'),
        'Fluid Mechanics': get_color_from_hex('#3498db'),
        'Properties of Matter': get_color_from_hex('#9b59b6'),
        'Mechanics': get_color_from_hex('#e74c3c'),
        'Thermodynamics': get_color_from_hex('#f39c12')
    }
    
    return color_map.get(category, Colors.GRAY)

# Fungsi perhitungan fisika
def calculate_velocity(displacement, time):
    """Menghitung kecepatan v = s / t"""
    if time == 0:
        return None, "Time cannot be zero"
    return displacement / time, "Velocity calculated successfully"

def calculate_force(mass, acceleration):
    """Menghitung gaya F = m × a"""
    return mass * acceleration, "Force calculated successfully"

def calculate_pressure(force, area):
    """Menghitung tekanan P = F / A"""
    if area == 0:
        return None, "Area cannot be zero"
    return force / area, "Pressure calculated successfully"

def calculate_work(force, displacement, angle=0):
    """Menghitung usaha W = F × s × cosθ"""
    try:
        radians = math.radians(angle)
        result = force * displacement * math.cos(radians)
        return result, "Work calculated successfully"
    except:
        return None, "Calculation error"

def calculate_kinetic_energy(mass, velocity):
    """Menghitung energi kinetik Ek = ½ × m × v²"""
    try:
        result = 0.5 * mass * (velocity ** 2)
        return result, "Kinetic energy calculated successfully"
    except:
        return None, "Calculation error"

def calculate_potential_energy(mass, height, gravity=9.8):
    """Menghitung energi potensial Ep = m × g × h"""
    try:
        result = mass * gravity * height
        return result, "Potential energy calculated successfully"
    except:
        return None, "Calculation error"

def calculate_density(mass, volume):
    """Menghitung massa jenis ρ = m / V"""
    if volume == 0:
        return None, "Volume cannot be zero"
    return mass / volume, "Density calculated successfully"

def calculate_power(work, time):
    """Menghitung daya P = W / t"""
    if time == 0:
        return None, "Time cannot be zero"
    return work / time, "Power calculated successfully"

def calculate_acceleration(initial_velocity, final_velocity, time):
    """Menghitung percepatan a = (v₂ - v₁) / t"""
    if time == 0:
        return None, "Time cannot be zero"
    return (final_velocity - initial_velocity) / time, "Acceleration calculated successfully"

def calculate_momentum(mass, velocity):
    """Menghitung momentum p = m × v"""
    return mass * velocity, "Momentum calculated successfully"

# Cache untuk performa
_calculation_cache = {}

def cached_calculation(func, *args):
    """Melakukan perhitungan dengan caching untuk performa"""
    cache_key = (func.__name__, args)
    
    if cache_key in _calculation_cache:
        return _calculation_cache[cache_key]
    
    result = func(*args)
    _calculation_cache[cache_key] = result
    return result

def clear_calculation_cache():
    """Membersihkan cache perhitungan"""
    _calculation_cache.clear()

def round_to_significant(value, digits=3):
    """
    Membulatkan angka ke digit signifikan tertentu
    
    Args:
        value: Angka yang akan dibulatkan
        digits: Jumlah digit signifikan
    """
    if value == 0:
        return 0
    
    try:
        value = float(value)
        scale = 10 ** (digits - 1 - math.floor(math.log10(abs(value))))
        return round(value * scale) / scale
    except:
        return value

def convert_units(value, from_unit, to_unit):
    """
    Konversi satuan (placeholder untuk pengembangan)
    
    Args:
        value: Nilai dalam satuan asal
        from_unit: Satuan asal
        to_unit: Satuan tujuan
    """
    # Ini adalah placeholder - bisa dikembangkan lebih lanjut
    conversions = {
        ('m', 'cm'): 100,
        ('cm', 'm'): 0.01,
        ('kg', 'g'): 1000,
        ('g', 'kg'): 0.001,
        ('s', 'min'): 1/60,
        ('min', 's'): 60,
    }
    
    key = (from_unit, to_unit)
    if key in conversions:
        return value * conversions[key]
    
    # Jika tidak ada konversi, kembalikan nilai asli
    return value

def validate_physics_inputs(inputs_dict):
    """
    Validasi multiple inputs untuk perhitungan fisika
    
    Args:
        inputs_dict: Dictionary berisi nama input dan nilainya
    """
    errors = []
    validated = {}
    
    for name, value in inputs_dict.items():
        is_valid, error = validate_number_input(str(value), allow_negative=True)
        
        if not is_valid:
            errors.append(f"{name}: {error}")
        else:
            validated[name] = float(value)
    
    return validated, errors

def calculate_with_error_handling(func, *args):
    """
    Wrapper untuk fungsi perhitungan dengan error handling
    
    Args:
        func: Fungsi perhitungan
        *args: Argumen untuk fungsi
    """
    try:
        return func(*args)
    except ZeroDivisionError:
        return None, "Division by zero error"
    except ValueError as e:
        return None, f"Value error: {str(e)}"
    except Exception as e:
        return None, f"Calculation error: {str(e)}"