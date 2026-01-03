"""
Database rumus fisika SMP dengan kategori dan detail lengkap
"""

physics_formulas = {
    'linear_motion': {
        'title': 'Linear Motion',
        'formula': 'v = s / t',
        'formula_display': 'Velocity = Displacement ÷ Time',
        'description': 'Velocity is defined as the rate of change of displacement with respect to time. It measures how fast an object moves in a specific direction.',
        'variables': [
            {'symbol': 'v', 'name': 'Velocity', 'unit': 'm/s (meter per second)'},
            {'symbol': 's', 'name': 'Displacement', 'unit': 'm (meter)'},
            {'symbol': 't', 'name': 'Time', 'unit': 's (second)'}
        ],
        'example': 'A car travels 100 meters in 5 seconds. What is its velocity?\n\nSolution:\nv = s / t\nv = 100 m / 5 s\nv = 20 m/s',
        'category': 'Kinematics',
        'icon': '🚗',
        'difficulty': 'Easy'
    },
    
    'force': {
        'title': 'Force',
        'formula': 'F = m × a',
        'formula_display': 'Force = Mass × Acceleration',
        'description': "Newton's Second Law of Motion states that the force acting on an object is equal to the mass of that object multiplied by its acceleration.",
        'variables': [
            {'symbol': 'F', 'name': 'Force', 'unit': 'N (Newton)'},
            {'symbol': 'm', 'name': 'Mass', 'unit': 'kg (kilogram)'},
            {'symbol': 'a', 'name': 'Acceleration', 'unit': 'm/s² (meter per second squared)'}
        ],
        'example': 'A 5 kg object accelerates at 3 m/s². Calculate the force.\n\nSolution:\nF = m × a\nF = 5 kg × 3 m/s²\nF = 15 N',
        'category': 'Dynamics',
        'icon': '⚡',
        'difficulty': 'Medium'
    },
    
    'pressure': {
        'title': 'Pressure',
        'formula': 'P = F / A',
        'formula_display': 'Pressure = Force ÷ Area',
        'description': 'Pressure is defined as force per unit area. It measures how concentrated a force is over a surface area.',
        'variables': [
            {'symbol': 'P', 'name': 'Pressure', 'unit': 'Pa (Pascal)'},
            {'symbol': 'F', 'name': 'Force', 'unit': 'N (Newton)'},
            {'symbol': 'A', 'name': 'Area', 'unit': 'm² (square meter)'}
        ],
        'example': 'A force of 500 N is applied over an area of 2 m². Find the pressure.\n\nSolution:\nP = F / A\nP = 500 N / 2 m²\nP = 250 Pa',
        'category': 'Fluid Mechanics',
        'icon': '💧',
        'difficulty': 'Easy'
    },
    
    'work': {
        'title': 'Work',
        'formula': 'W = F × s × cosθ',
        'formula_display': 'Work = Force × Displacement × cos(θ)',
        'description': 'Work is done when a force causes an object to move. It is the product of force and displacement in the direction of the force.',
        'variables': [
            {'symbol': 'W', 'name': 'Work', 'unit': 'J (Joule)'},
            {'symbol': 'F', 'name': 'Force', 'unit': 'N (Newton)'},
            {'symbol': 's', 'name': 'Displacement', 'unit': 'm (meter)'},
            {'symbol': 'θ', 'name': 'Angle', 'unit': 'degree'}
        ],
        'example': 'A person pushes a box with 20 N force for 5 meters in the same direction. Calculate work done.\n\nSolution:\nW = F × s × cos(0°)\nW = 20 N × 5 m × 1\nW = 100 J',
        'category': 'Energy',
        'icon': '💪',
        'difficulty': 'Medium'
    },
    
    'kinetic_energy': {
        'title': 'Kinetic Energy',
        'formula': 'Ek = ½ × m × v²',
        'formula_display': 'Kinetic Energy = ½ × Mass × Velocity²',
        'description': 'Kinetic energy is the energy possessed by an object due to its motion. It depends on both mass and velocity.',
        'variables': [
            {'symbol': 'Ek', 'name': 'Kinetic Energy', 'unit': 'J (Joule)'},
            {'symbol': 'm', 'name': 'Mass', 'unit': 'kg (kilogram)'},
            {'symbol': 'v', 'name': 'Velocity', 'unit': 'm/s (meter per second)'}
        ],
        'example': 'A 2 kg ball moves at 4 m/s. Calculate its kinetic energy.\n\nSolution:\nEk = ½ × m × v²\nEk = ½ × 2 kg × (4 m/s)²\nEk = ½ × 2 × 16\nEk = 16 J',
        'category': 'Energy',
        'icon': '⚡',
        'difficulty': 'Medium'
    },
    
    'potential_energy': {
        'title': 'Potential Energy',
        'formula': 'Ep = m × g × h',
        'formula_display': 'Potential Energy = Mass × Gravity × Height',
        'description': 'Potential energy is the energy stored in an object due to its position in a gravitational field. It depends on height and mass.',
        'variables': [
            {'symbol': 'Ep', 'name': 'Potential Energy', 'unit': 'J (Joule)'},
            {'symbol': 'm', 'name': 'Mass', 'unit': 'kg (kilogram)'},
            {'symbol': 'g', 'name': 'Gravity', 'unit': '9.8 m/s²'},
            {'symbol': 'h', 'name': 'Height', 'unit': 'm (meter)'}
        ],
        'example': 'A 3 kg book is placed on a shelf 2 meters high. Find its potential energy.\n\nSolution:\nEp = m × g × h\nEp = 3 kg × 9.8 m/s² × 2 m\nEp = 58.8 J',
        'category': 'Energy',
        'icon': '📚',
        'difficulty': 'Easy'
    },
    
    'power': {
        'title': 'Power',
        'formula': 'P = W / t',
        'formula_display': 'Power = Work ÷ Time',
        'description': 'Power is the rate at which work is done or energy is transferred. It measures how quickly work is completed.',
        'variables': [
            {'symbol': 'P', 'name': 'Power', 'unit': 'W (Watt)'},
            {'symbol': 'W', 'name': 'Work', 'unit': 'J (Joule)'},
            {'symbol': 't', 'name': 'Time', 'unit': 's (second)'}
        ],
        'example': 'A machine does 200 J of work in 4 seconds. Calculate its power.\n\nSolution:\nP = W / t\nP = 200 J / 4 s\nP = 50 W',
        'category': 'Energy',
        'icon': '⚡',
        'difficulty': 'Easy'
    },
    
    'density': {
        'title': 'Density',
        'formula': 'ρ = m / V',
        'formula_display': 'Density = Mass ÷ Volume',
        'description': 'Density is a measure of mass per unit volume. It indicates how much matter is packed into a given space.',
        'variables': [
            {'symbol': 'ρ', 'name': 'Density', 'unit': 'kg/m³'},
            {'symbol': 'm', 'name': 'Mass', 'unit': 'kg (kilogram)'},
            {'symbol': 'V', 'name': 'Volume', 'unit': 'm³ (cubic meter)'}
        ],
        'example': 'A metal block has mass 10 kg and volume 0.002 m³. Find its density.\n\nSolution:\nρ = m / V\nρ = 10 kg / 0.002 m³\nρ = 5000 kg/m³',
        'category': 'Properties of Matter',
        'icon': '⚖️',
        'difficulty': 'Easy'
    }
}

# Kategori untuk pengelompokan
formula_categories = {
    'Kinematics': ['linear_motion'],
    'Dynamics': ['force'],
    'Energy': ['work', 'kinetic_energy', 'potential_energy', 'power'],
    'Fluid Mechanics': ['pressure'],
    'Properties of Matter': ['density']
}

# Daftar semua rumus untuk easy access
all_formulas = list(physics_formulas.keys())