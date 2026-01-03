"""
Database rumus fisika SMP
Berisi semua rumus, penjelasan, dan satuan
"""

physics_formulas = {
    'linear_motion': {
        'title': 'Linear Motion',
        'formula': 'v = s / t',
        'formula_latex': 'v = \\frac{s}{t}',
        'description': 'Velocity is the rate of change of displacement with respect to time.',
        'variables': [
            {'symbol': 'v', 'name': 'Velocity', 'unit': 'm/s'},
            {'symbol': 's', 'name': 'Displacement', 'unit': 'm'},
            {'symbol': 't', 'name': 'Time', 'unit': 's'}
        ],
        'example': 'If a car travels 100 meters in 10 seconds, its velocity is 10 m/s.',
        'category': 'Mechanics'
    },
    
    'force': {
        'title': 'Force',
        'formula': 'F = m × a',
        'formula_latex': 'F = m \\times a',
        'description': "Force is the product of mass and acceleration (Newton's Second Law).",
        'variables': [
            {'symbol': 'F', 'name': 'Force', 'unit': 'N (Newton)'},
            {'symbol': 'm', 'name': 'Mass', 'unit': 'kg'},
            {'symbol': 'a', 'name': 'Acceleration', 'unit': 'm/s²'}
        ],
        'example': 'A 2 kg object accelerating at 3 m/s² experiences a force of 6 N.',
        'category': 'Mechanics'
    },
    
    'pressure': {
        'title': 'Pressure',
        'formula': 'P = F / A',
        'formula_latex': 'P = \\frac{F}{A}',
        'description': 'Pressure is the force applied perpendicular to a surface per unit area.',
        'variables': [
            {'symbol': 'P', 'name': 'Pressure', 'unit': 'Pa (Pascal)'},
            {'symbol': 'F', 'name': 'Force', 'unit': 'N'},
            {'symbol': 'A', 'name': 'Area', 'unit': 'm²'}
        ],
        'example': 'A force of 100 N on an area of 2 m² creates a pressure of 50 Pa.',
        'category': 'Mechanics'
    },
    
    'work': {
        'title': 'Work',
        'formula': 'W = F × s',
        'formula_latex': 'W = F \\times s',
        'description': 'Work is done when a force causes an object to move in the direction of the force.',
        'variables': [
            {'symbol': 'W', 'name': 'Work', 'unit': 'J (Joule)'},
            {'symbol': 'F', 'name': 'Force', 'unit': 'N'},
            {'symbol': 's', 'name': 'Displacement', 'unit': 'm'}
        ],
        'example': 'A force of 10 N moving an object 5 m does 50 J of work.',
        'category': 'Energy'
    },
    
    'kinetic_energy': {
        'title': 'Kinetic Energy',
        'formula': 'Ek = ½ × m × v²',
        'formula_latex': 'E_k = \\frac{1}{2} m v^2',
        'description': 'Kinetic energy is the energy possessed by an object due to its motion.',
        'variables': [
            {'symbol': 'Ek', 'name': 'Kinetic Energy', 'unit': 'J (Joule)'},
            {'symbol': 'm', 'name': 'Mass', 'unit': 'kg'},
            {'symbol': 'v', 'name': 'Velocity', 'unit': 'm/s'}
        ],
        'example': 'A 4 kg object moving at 3 m/s has kinetic energy of 18 J.',
        'category': 'Energy'
    },
    
    'potential_energy': {
        'title': 'Potential Energy',
        'formula': 'Ep = m × g × h',
        'formula_latex': 'E_p = m g h',
        'description': 'Potential energy is the energy stored in an object due to its position in a gravitational field.',
        'variables': [
            {'symbol': 'Ep', 'name': 'Potential Energy', 'unit': 'J (Joule)'},
            {'symbol': 'm', 'name': 'Mass', 'unit': 'kg'},
            {'symbol': 'g', 'name': 'Gravity', 'unit': 'm/s² (9.8)'},
            {'symbol': 'h', 'name': 'Height', 'unit': 'm'}
        ],
        'example': 'A 2 kg object at 5 m height has potential energy of 98 J (g=9.8).',
        'category': 'Energy'
    },
    
    'power': {
        'title': 'Power',
        'formula': 'P = W / t',
        'formula_latex': 'P = \\frac{W}{t}',
        'description': 'Power is the rate at which work is done or energy is transferred.',
        'variables': [
            {'symbol': 'P', 'name': 'Power', 'unit': 'W (Watt)'},
            {'symbol': 'W', 'name': 'Work', 'unit': 'J'},
            {'symbol': 't', 'name': 'Time', 'unit': 's'}
        ],
        'example': 'If 100 J of work is done in 5 seconds, the power is 20 W.',
        'category': 'Energy'
    },
    
    'density': {
        'title': 'Density',
        'formula': 'ρ = m / V',
        'formula_latex': '\\rho = \\frac{m}{V}',
        'description': 'Density is the mass per unit volume of a substance.',
        'variables': [
            {'symbol': 'ρ', 'name': 'Density', 'unit': 'kg/m³'},
            {'symbol': 'm', 'name': 'Mass', 'unit': 'kg'},
            {'symbol': 'V', 'name': 'Volume', 'unit': 'm³'}
        ],
        'example': 'A 10 kg object with volume 2 m³ has density of 5 kg/m³.',
        'category': 'Properties of Matter'
    }
}

# Daftar kategori untuk pengelompokan rumus
formula_categories = {
    'Mechanics': ['linear_motion', 'force', 'pressure'],
    'Energy': ['work', 'kinetic_energy', 'potential_energy', 'power'],
    'Properties of Matter': ['density']
}