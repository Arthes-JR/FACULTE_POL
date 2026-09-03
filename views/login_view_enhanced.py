"""
Interface de connexion - Version Améliorée
Système de Gestion de Faculté - UNIKIN
"""

import tkinter as tk
from tkinter import ttk, messagebox
from controllers.auth_controller import AuthController

class LoginViewEnhanced:
    """Fenêtre de connexion avec animations et design amélioré"""

    def __init__(self, root, on_login_success):
        self.root = root
        self.root.title("UNIKIN - Système de Gestion de Faculté")
        self.root.geometry("950x580")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f2f5')
        self.on_login_success = on_login_success
        self.auth_controller = AuthController()
        
        # Variables pour les animations
        self.is_loading = False
        self.animation_after_id = None
        self.show_pass = False
        
        self.setup_ui()

    def setup_ui(self):
        """Configurer l'interface utilisateur améliorée"""
        
        # Fenêtre principale avec ombre portée
        main_container = tk.Frame(self.root, bg='white', relief=tk.RAISED, bd=2)
        main_container.place(relx=0.5, rely=0.5, anchor='center', width=900, height=540)

        # ========== PARTIE GAUCHE - BANNIÈRE ==========
        left_panel = tk.Frame(main_container, bg='#1a237e', width=350, height=540)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH)
        left_panel.pack_propagate(False)

        # Logo
        logo_frame = tk.Frame(left_panel, bg='#1a237e')
        logo_frame.pack(pady=(50, 5))

        icon_bg = tk.Canvas(logo_frame, width=80, height=80, bg='#1a237e', highlightthickness=0)
        icon_bg.pack()
        icon_bg.create_oval(10, 10, 70, 70, fill='#3949ab', outline='')
        icon_bg.create_text(40, 40, text='🏛️', font=("Segoe UI", 32))

        tk.Label(
            left_panel,
            text="UNIKIN",
            font=("Segoe UI", 32, "bold"),
            bg='#1a237e',
            fg='white'
        ).pack()

        tk.Label(
            left_panel,
            text="Université de Kinshasa",
            font=("Segoe UI", 13),
            bg='#1a237e',
            fg='#9fa8da'
        ).pack()

        # Séparateur
        sep_frame = tk.Frame(left_panel, bg='#1a237e')
        sep_frame.pack(pady=15)
        tk.Frame(sep_frame, bg='#3949ab', width=60, height=2).pack(side=tk.LEFT)
        tk.Frame(sep_frame, bg='#ffd54f', width=30, height=2).pack(side=tk.LEFT, padx=5)
        tk.Frame(sep_frame, bg='#3949ab', width=60, height=2).pack(side=tk.LEFT)

        tk.Label(
            left_panel,
            text="Système de Gestion\nIntégré des Facultés",
            font=("Segoe UI", 18, "bold"),
            bg='#1a237e',
            fg='white',
            justify=tk.CENTER
        ).pack(pady=10)

        tk.Label(
            left_panel,
            text="Version 3.0 - Premium",
            font=("Segoe UI", 10),
            bg='#1a237e',
            fg='#7986cb'
        ).pack()

        version_badge = tk.Label(
            left_panel,
            text="LMD",
            font=("Segoe UI", 9, "bold"),
            bg='#ffd54f',
            fg='#1a237e',
            padx=15,
            pady=3
        )
        version_badge.pack(pady=(30, 0))

        # ========== PARTIE DROITE - FORMULAIRE ==========
        right_panel = tk.Frame(main_container, bg='white', width=550, height=540)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        right_panel.pack_propagate(False)

        # En-tête
        header_frame = tk.Frame(right_panel, bg='white')
        header_frame.pack(fill=tk.X, padx=45, pady=(35, 5))

        tk.Label(
            header_frame,
            text="👋",
            font=("Segoe UI", 28),
            bg='white'
        ).pack(anchor='w')

        tk.Label(
            header_frame,
            text="Bienvenue",
            font=("Segoe UI", 24, "bold"),
            bg='white',
            fg='#1a237e'
        ).pack(anchor='w')

        tk.Label(
            header_frame,
            text="Connectez-vous à votre espace de travail",
            font=("Segoe UI", 11),
            bg='white',
            fg='#666666'
        ).pack(anchor='w', pady=(2, 10))

        # Formulaire
        form_frame = tk.Frame(right_panel, bg='white')
        form_frame.pack(fill=tk.X, padx=45, pady=5)

        # Email
        email_container = tk.Frame(form_frame, bg='white')
        email_container.pack(fill=tk.X, pady=(0, 12))

        tk.Label(
            email_container,
            text="Adresse email",
            font=("Segoe UI", 10, "bold"),
            fg='#333333',
            bg='white'
        ).pack(anchor='w')

        self.email_entry = tk.Entry(
            email_container,
            font=("Segoe UI", 11),
            bg='#f5f7fa',
            relief=tk.FLAT,
            bd=2,
            highlightthickness=1,
            highlightcolor='#1a237e',
            highlightbackground='#d0d0d0'
        )
        self.email_entry.pack(fill=tk.X, pady=(4, 0), ipady=10)
        self.email_entry.insert(0, "doyen.fd@unikin.com")

        # Mot de passe
        password_container = tk.Frame(form_frame, bg='white')
        password_container.pack(fill=tk.X, pady=(0, 12))

        tk.Label(
            password_container,
            text="Mot de passe",
            font=("Segoe UI", 10, "bold"),
            fg='#333333',
            bg='white'
        ).pack(anchor='w')

        pass_frame = tk.Frame(password_container, bg='#f5f7fa', bd=2, relief=tk.FLAT)
        pass_frame.pack(fill=tk.X, pady=(4, 0))

        self.password_entry = tk.Entry(
            pass_frame,
            font=("Segoe UI", 11),
            bg='#f5f7fa',
            relief=tk.FLAT,
            bd=0,
            show='●'
        )
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=10, padx=10)
        self.password_entry.insert(0, "password")

        self.toggle_btn = tk.Label(
            pass_frame,
            text="👁️",
            font=("Segoe UI", 12),
            bg='#f5f7fa',
            cursor='hand2'
        )
        self.toggle_btn.pack(side=tk.RIGHT, padx=10)
        self.toggle_btn.bind('<Button-1>', self.toggle_password)

        # Rôle
        role_container = tk.Frame(form_frame, bg='white')
        role_container.pack(fill=tk.X, pady=(0, 15))

        tk.Label(
            role_container,
            text="Sélectionnez votre rôle",
            font=("Segoe UI", 10, "bold"),
            fg='#333333',
            bg='white'
        ).pack(anchor='w')

        self.role_var = tk.StringVar(value="Doyen")
        role_frame = tk.Frame(role_container, bg='white')
        role_frame.pack(fill=tk.X, pady=(6, 0))

        # CORRECTION : Suppression de selectfrom=0
        roles = [
            ("👑 Doyen", "Doyen"),
            ("🎓 Professeur", "Professeur"),
            ("📚 Étudiant", "Étudiant"),
            ("📋 Secrétaire", "Secrétaire")
        ]

        for display, value in roles:
            rb = tk.Radiobutton(
                role_frame,
                text=display,
                variable=self.role_var,
                value=value,
                font=("Segoe UI", 10),
                bg='white',
                fg='#333333',
                selectcolor='#e8eaf6',
                activebackground='white',
                cursor='hand2'
            )
            rb.pack(side=tk.LEFT, padx=(0, 12), ipadx=8, ipady=4)

        # Message d'erreur
        self.error_label = tk.Label(
            form_frame,
            text="",
            font=("Segoe UI", 10),
            fg='#d32f2f',
            bg='white'
        )
        self.error_label.pack(pady=5)

        # Bouton de connexion
        btn_container = tk.Frame(form_frame, bg='white')
        btn_container.pack(fill=tk.X, pady=(5, 0))

        self.login_btn = tk.Button(
            btn_container,
            text="🔑 Se connecter",
            command=self.login,
            font=("Segoe UI", 12, "bold"),
            bg='#1a237e',
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            activebackground='#0d1a5e',
            activeforeground='white'
        )
        self.login_btn.pack(fill=tk.X, ipady=12)

        # Pied de page
        footer = tk.Frame(right_panel, bg='white')
        footer.pack(side=tk.BOTTOM, fill=tk.X, pady=(0, 20))

        tk.Frame(footer, bg='#e0e0e0', height=1).pack(fill=tk.X, padx=45)

        tk.Label(
            footer,
            text="© 2026 UNIKIN - Faculté de Génie Informatique | Tous droits réservés",
            font=("Segoe UI", 8),
            fg='#999999',
            bg='white'
        ).pack(pady=(10, 0))

        # Raccourci Enter
        self.root.bind('<Return>', lambda e: self.login())

    def toggle_password(self, event):
        """Afficher/masquer le mot de passe"""
        self.show_pass = not self.show_pass
        if self.show_pass:
            self.password_entry.config(show='')
            self.toggle_btn.config(text='👁️‍🗨️')
        else:
            self.password_entry.config(show='●')
            self.toggle_btn.config(text='👁️')

    def login(self):
        """Gérer la connexion - CORRIGÉ"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get()

        print(f"\n🔍 Tentative de connexion avec: {email}, rôle: {role}")

        if not email:
            self.error_label.config(text="⚠️ Veuillez saisir votre adresse email")
            return

        if not password:
            self.error_label.config(text="⚠️ Veuillez saisir votre mot de passe")
            return

        try:
            user = self.auth_controller.authenticate(email, password, role)
            if user:
                print(f"✅ Connexion réussie pour {email}")
                # Sauvegarder la référence avant de détruire
                on_success = self.on_login_success
                self.root.destroy()
                on_success(user, role)
            else:
                self.error_label.config(text="❌ Email, mot de passe ou rôle incorrect")
                print(f"❌ Échec de connexion pour {email}")
        except Exception as e:
            # Vérifier que la fenêtre existe avant de modifier l'erreur
            try:
                self.error_label.config(text=f"❌ Erreur: {str(e)}")
            except:
                pass
            print(f"❌ Erreur: {e}")