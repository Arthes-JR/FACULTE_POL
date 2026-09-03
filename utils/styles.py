"""
Styles et thèmes pour l'application
Système de Gestion de Faculté - UNIKIN
"""

# Palettes de couleurs UNIKIN
COLORS = {
    'primary': '#1a237e',
    'primary_dark': '#0d1a5e',
    'primary_light': '#3949ab',
    'primary_extra_light': '#e8eaf6',
    'secondary': '#ffd54f',
    'secondary_dark': '#f9a825',
    'accent': '#4CAF50',
    'warning': '#FF9800',
    'danger': '#d32f2f',
    'success': '#4CAF50',
    'info': '#2196F3',
    'background': '#f0f2f5',
    'white': '#ffffff',
    'text_primary': '#1a237e',
    'text_secondary': '#666666',
    'text_light': '#999999',
    'border': '#e0e0e0'
}

# Polices de caractères
FONTS = {
    'title': ("Segoe UI", 32, "bold"),
    'subtitle': ("Segoe UI", 18, "bold"),
    'heading': ("Segoe UI", 22, "bold"),
    'body': ("Segoe UI", 11),
    'body_bold': ("Segoe UI", 11, "bold"),
    'small': ("Segoe UI", 9),
    'small_bold': ("Segoe UI", 9, "bold"),
    'button': ("Segoe UI", 12, "bold"),
}

# Styles de boutons
BUTTON_STYLES = {
    'primary': {
        'bg': COLORS['primary'],
        'fg': COLORS['white'],
        'activebackground': COLORS['primary_dark'],
        'activeforeground': COLORS['white'],
        'font': FONTS['button'],
        'relief': 'flat',
        'cursor': 'hand2'
    },
    'secondary': {
        'bg': COLORS['secondary'],
        'fg': COLORS['primary'],
        'activebackground': COLORS['secondary_dark'],
        'activeforeground': COLORS['primary'],
        'font': FONTS['button'],
        'relief': 'flat',
        'cursor': 'hand2'
    },
    'danger': {
        'bg': COLORS['danger'],
        'fg': COLORS['white'],
        'activebackground': '#b71c1c',
        'activeforeground': COLORS['white'],
        'font': FONTS['button'],
        'relief': 'flat',
        'cursor': 'hand2'
    },
    'success': {
        'bg': COLORS['success'],
        'fg': COLORS['white'],
        'activebackground': '#388E3C',
        'activeforeground': COLORS['white'],
        'font': FONTS['button'],
        'relief': 'flat',
        'cursor': 'hand2'
    }
}

# Styles d'entrée
ENTRY_STYLES = {
    'default': {
        'font': FONTS['body'],
        'bg': '#f5f7fa',
        'relief': 'flat',
        'bd': 2,
        'highlightthickness': 1,
        'highlightcolor': COLORS['primary'],
        'highlightbackground': COLORS['border']
    }
}

# Styles de labels
LABEL_STYLES = {
    'title': {
        'font': FONTS['title'],
        'fg': COLORS['primary'],
        'bg': COLORS['white']
    },
    'subtitle': {
        'font': FONTS['subtitle'],
        'fg': COLORS['text_secondary'],
        'bg': COLORS['white']
    },
    'body': {
        'font': FONTS['body'],
        'fg': COLORS['text_secondary'],
        'bg': COLORS['white']
    },
    'body_bold': {
        'font': FONTS['body_bold'],
        'fg': COLORS['text_primary'],
        'bg': COLORS['white']
    }
}