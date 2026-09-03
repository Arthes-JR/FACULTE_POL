"""
Interface principale - Version Premium
Système de Gestion de Faculté - UNIKIN
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class MainView:
    """Fenêtre principale avec design moderne"""

    def __init__(self, user, role):
        self.user = user
        self.role = role
        self.root = tk.Tk()
        self.root.title("UNIKIN - Système de Gestion de Faculté")
        self.root.geometry("1300x800")
        self.root.configure(bg='#f0f2f5')
        self.root.minsize(1100, 700)

        self.setup_ui()
        self.root.mainloop()

    def setup_ui(self):
        """Configurer l'interface"""
        self.create_menu()
        self.create_header()
        self.create_sidebar()
        self.create_main_area()
        self.create_statusbar()

    def create_menu(self):
        """Créer le menu principal"""
        menubar = tk.Menu(self.root, bg='white', fg='#333333')
        self.root.config(menu=menubar)

        # Fichier
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Déconnexion", command=self.logout, accelerator="Ctrl+Q")
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.root.quit, accelerator="Ctrl+X")

        # Gestion
        gestion_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Gestion", menu=gestion_menu)

        if self.role in ['Doyen', 'Secrétaire']:
            gestion_menu.add_command(label="Étudiants", command=self.open_etudiants)
            gestion_menu.add_command(label="Enseignants", command=self.open_enseignants)
            gestion_menu.add_command(label="Cours", command=self.open_cours)

        if self.role == 'Doyen':
            gestion_menu.add_separator()
            gestion_menu.add_command(label="Départements", command=self.open_departements)
            gestion_menu.add_command(label="Jurys", command=self.open_jury)

        if self.role == 'Professeur':
            gestion_menu.add_command(label="Mes Cours", command=self.open_mes_cours)
            gestion_menu.add_command(label="Saisie Notes", command=self.open_saisie_notes)

        if self.role == 'Étudiant':
            gestion_menu.add_command(label="Mes Notes", command=self.open_mes_notes)
            gestion_menu.add_command(label="Paiements", command=self.open_paiements)

        # Rapports
        rapports_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Rapports", menu=rapports_menu)
        rapports_menu.add_command(label="Liste des Étudiants", command=self.rapport_etudiants)
        rapports_menu.add_command(label="Relevé de Notes", command=self.rapport_notes)
        rapports_menu.add_command(label="Palmarès", command=self.rapport_palmares)

        # Aide
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Aide", menu=help_menu)
        help_menu.add_command(label="Documentation", command=self.show_doc)
        help_menu.add_command(label="À propos", command=self.show_about)

        # Raccourcis
        self.root.bind('<Control-q>', lambda e: self.logout())
        self.root.bind('<Control-x>', lambda e: self.root.quit())

    def create_header(self):
        """Créer l'en-tête"""
        header = tk.Frame(self.root, bg='#1a237e', height=65)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        # Logo
        logo_frame = tk.Frame(header, bg='#1a237e')
        logo_frame.pack(side=tk.LEFT, padx=20, pady=10)

        tk.Label(
            logo_frame,
            text="🏛️ UNIKIN",
            font=("Segoe UI", 16, "bold"),
            bg='#1a237e',
            fg='white'
        ).pack(side=tk.LEFT)

        tk.Label(
            logo_frame,
            text="| Gestion de Faculté",
            font=("Segoe UI", 13),
            bg='#1a237e',
            fg='#9fa8da'
        ).pack(side=tk.LEFT, padx=10)

        # Horloge
        self.time_label = tk.Label(
            header,
            font=("Segoe UI", 10),
            bg='#1a237e',
            fg='#9fa8da'
        )
        self.time_label.pack(side=tk.RIGHT, padx=20)
        self.update_time()

        # Informations utilisateur
        user_frame = tk.Frame(header, bg='#1a237e')
        user_frame.pack(side=tk.RIGHT, padx=20)

        user_name = self.user.get_identite() if hasattr(self.user, 'get_identite') else 'Utilisateur'

        tk.Label(
            user_frame,
            text=f"👤 {user_name}",
            font=("Segoe UI", 10, "bold"),
            bg='#1a237e',
            fg='#ffd54f'
        ).pack(side=tk.LEFT)

        tk.Label(
            user_frame,
            text=f"• {self.role}",
            font=("Segoe UI", 10),
            bg='#1a237e',
            fg='#9fa8da'
        ).pack(side=tk.LEFT, padx=5)

    def create_sidebar(self):
        """Créer la barre latérale"""
        sidebar = tk.Frame(self.root, bg='white', width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        # Menu latéral
        menu_items = [
            ("🏠 Accueil", self.show_accueil),
            ("📊 Dashboard", self.show_dashboard),
            ("👨‍🎓 Étudiants", self.open_etudiants),
            ("👨‍🏫 Enseignants", self.open_enseignants),
            ("📚 Cours", self.open_cours),
            ("⚖️ Jurys", self.open_jury),
            ("📈 Rapports", self.rapport_etudiants),
            ("⚙️ Paramètres", self.show_settings)
        ]

        for text, command in menu_items:
            btn = tk.Button(
                sidebar,
                text=text,
                command=command,
                font=("Segoe UI", 10),
                bg='white',
                fg='#333333',
                relief=tk.FLAT,
                anchor=tk.W,
                padx=20,
                pady=12,
                cursor='hand2',
                activebackground='#e8eaf6',
                activeforeground='#1a237e'
            )
            btn.pack(fill=tk.X)

            # Séparateur
            tk.Frame(sidebar, bg='#f0f2f5', height=1).pack(fill=tk.X)

    def create_main_area(self):
        """Créer la zone principale"""
        self.main_frame = tk.Frame(self.root, bg='#f0f2f5')
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Afficher l'accueil par défaut
        self.show_accueil()

    def clear_main_area(self):
        """Vider la zone principale"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_accueil(self):
        """Afficher la page d'accueil"""
        self.clear_main_area()

        main = tk.Frame(self.main_frame, bg='#f0f2f5')
        main.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # En-tête
        user_name = self.user.get_identite() if hasattr(self.user, 'get_identite') else ''

        tk.Label(
            main,
            text=f"Bonjour, {user_name} 👋",
            font=("Segoe UI", 26, "bold"),
            bg='#f0f2f5',
            fg='#1a237e'
        ).pack(anchor=tk.W)

        tk.Label(
            main,
            text=f"Rôle: {self.role} | Année académique 2025-2026",
            font=("Segoe UI", 13),
            bg='#f0f2f5',
            fg='#666666'
        ).pack(anchor=tk.W, pady=(0, 20))

        # Cartes statistiques
        self.create_stats_cards(main)

        # Actions rapides
        self.create_quick_actions(main)

    def create_stats_cards(self, parent):
        """Créer les cartes statistiques"""
        stats_frame = tk.Frame(parent, bg='#f0f2f5')
        stats_frame.pack(fill=tk.X, pady=10)

        stats = {}
        if hasattr(self.user, 'consulter_statistiques'):
            try:
                stats = self.user.consulter_statistiques()
            except:
                pass

        stats_data = [
            ("👨‍🎓 Étudiants", stats.get('nb_etudiants', 0), "#4CAF50"),
            ("👨‍🏫 Enseignants", stats.get('nb_enseignants', 0), "#2196F3"),
            ("📚 Cours", stats.get('nb_cours', 0), "#FF9800"),
            ("🏛️ Départements", stats.get('nb_departements', 0), "#9C27B0"),
        ]

        for i, (label, value, color) in enumerate(stats_data):
            card = tk.Frame(
                stats_frame,
                bg='white',
                relief=tk.RAISED,
                bd=1,
                padx=20,
                pady=15
            )
            card.grid(row=0, column=i, padx=10, pady=5, sticky='nsew')
            stats_frame.grid_columnconfigure(i, weight=1)

            tk.Label(
                card,
                text=str(value),
                font=("Segoe UI", 28, "bold"),
                bg='white',
                fg=color
            ).pack(anchor=tk.W)

            tk.Label(
                card,
                text=label,
                font=("Segoe UI", 11),
                bg='white',
                fg='#333333'
            ).pack(anchor=tk.W)

    def create_quick_actions(self, parent):
        """Créer les actions rapides"""
        actions_frame = tk.LabelFrame(
            parent,
            text="⚡ Actions Rapides",
            font=("Segoe UI", 13, "bold"),
            bg='#f0f2f5',
            fg='#1a237e',
            padx=15,
            pady=15
        )
        actions_frame.pack(fill=tk.X, pady=10)

        btn_frame = tk.Frame(actions_frame, bg='#f0f2f5')
        btn_frame.pack()

        actions = []
        if self.role in ['Doyen', 'Secrétaire']:
            actions.append(("👨‍🎓 Gestion Étudiants", self.open_etudiants))
            actions.append(("📚 Gestion Cours", self.open_cours))

        if self.role == 'Doyen':
            actions.append(("⚖️ Organiser Jury", self.open_jury))
            actions.append(("📊 Statistiques", self.open_statistiques))

        if self.role == 'Professeur':
            actions.append(("✏️ Saisie Notes", self.open_saisie_notes))
            actions.append(("📖 Mes Cours", self.open_mes_cours))

        if self.role == 'Étudiant':
            actions.append(("📄 Mes Notes", self.open_mes_notes))
            actions.append(("💰 Paiements", self.open_paiements))

        for i, (text, command) in enumerate(actions):
            btn = tk.Button(
                btn_frame,
                text=text,
                command=command,
                font=("Segoe UI", 11),
                bg='white',
                fg='#1a237e',
                padx=25,
                pady=12,
                relief=tk.RAISED,
                bd=1,
                cursor='hand2',
                activebackground='#e8eaf6',
                activeforeground='#1a237e'
            )
            btn.grid(row=0, column=i, padx=10, pady=5)
            btn_frame.grid_columnconfigure(i, weight=1)

    def show_dashboard(self):
        """Afficher le tableau de bord"""
        self.clear_main_area()

        main = tk.Frame(self.main_frame, bg='#f0f2f5')
        main.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        tk.Label(
            main,
            text="📊 Tableau de bord",
            font=("Segoe UI", 24, "bold"),
            bg='#f0f2f5',
            fg='#1a237e'
        ).pack(anchor=tk.W, pady=(0, 20))

        # Indicateurs de performance
        if self.role == 'Doyen' and hasattr(self.user, 'consulter_statistiques'):
            try:
                stats = self.user.consulter_statistiques()

                # Barres de progression
                items = [
                    ("Taux de réussite", 78, "#4CAF50"),
                    ("Taux de présence", 85, "#2196F3"),
                    ("Satisfaction", 72, "#FF9800"),
                    ("Diplômés", 65, "#9C27B0")
                ]

                for label, value, color in items:
                    frame = tk.Frame(main, bg='white', relief=tk.RAISED, bd=1, padx=15, pady=10)
                    frame.pack(fill=tk.X, pady=5)

                    tk.Label(
                        frame,
                        text=label,
                        font=("Segoe UI", 11),
                        bg='white',
                        fg='#333333'
                    ).pack(anchor=tk.W)

                    # Barre de progression
                    progress_bg = tk.Frame(frame, bg='#e0e0e0', height=8)
                    progress_bg.pack(fill=tk.X, pady=5)

                    progress_fg = tk.Frame(progress_bg, bg=color, height=8, width=f"{value}%")
                    progress_fg.pack(side=tk.LEFT)

                    tk.Label(
                        frame,
                        text=f"{value}%",
                        font=("Segoe UI", 10, "bold"),
                        bg='white',
                        fg=color
                    ).pack(anchor=tk.E)
            except:
                pass

    def create_statusbar(self):
        """Créer la barre de statut"""
        statusbar = tk.Frame(self.root, bg='#e0e0e0', height=30)
        statusbar.pack(fill=tk.X, side=tk.BOTTOM)

        tk.Label(
            statusbar,
            text="✅ Prêt",
            font=("Segoe UI", 9),
            bg='#e0e0e0',
            fg='#333333'
        ).pack(side=tk.LEFT, padx=15)

        tk.Label(
            statusbar,
            text="UNIKIN - Système de Gestion de Faculté v2.0",
            font=("Segoe UI", 9),
            bg='#e0e0e0',
            fg='#666666'
        ).pack(side=tk.RIGHT, padx=15)

    def update_time(self):
        """Mettre à jour l'horloge"""
        now = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        self.time_label.config(text=f"🕐 {now}")
        self.root.after(1000, self.update_time)

    # ==================== ACTIONS ====================

    def logout(self):
        """Déconnexion - CORRIGÉ"""
        if messagebox.askyesno("Déconnexion", "Voulez-vous vous déconnecter ?"):
            self.root.destroy()
            root = tk.Tk()
            from views.login_view_enhanced import LoginViewEnhanced
            LoginViewEnhanced(root, lambda u, r: MainView(u, r))
            root.mainloop()

    def show_about(self):
        """Afficher À propos"""
        messagebox.showinfo(
            "À propos",
            "🏛️ Système de Gestion de Faculté\n\n"
            "Université de Kinshasa (UNIKIN)\n"
            "Faculté de Génie Informatique\n\n"
            "Version : 2.0\n"
            "Technologies : Python, Tkinter, PostgreSQL\n\n"
            "© 2026 - Tous droits réservés"
        )

    def show_doc(self):
        """Afficher la documentation"""
        messagebox.showinfo(
            "Documentation",
            "📚 Documentation du Système\n\n"
            "1. 🔐 Connexion\n"
            "   - Sélectionnez votre rôle\n"
            "   - Utilisez vos identifiants\n\n"
            "2. 📊 Gestion\n"
            "   - Étudiants, Enseignants, Cours\n"
            "   - Jurys, Délibérations\n\n"
            "3. 📈 Rapports\n"
            "   - Listes, Relevés, Palmarès\n"
            "4. 📊 Dashboard\n"
            "   - Statistiques en temps réel"
        )

    def show_settings(self):
        """Afficher les paramètres"""
        messagebox.showinfo("Paramètres", "⚙️ Module de paramètres en développement")

    # ==================== MODULES ====================

    def open_etudiants(self):
        messagebox.showinfo("Gestion", "👨‍🎓 Module de gestion des Étudiants")

    def open_enseignants(self):
        messagebox.showinfo("Gestion", "👨‍🏫 Module de gestion des Enseignants")

    def open_cours(self):
        messagebox.showinfo("Gestion", "📚 Module de gestion des Cours")

    def open_departements(self):
        messagebox.showinfo("Gestion", "🏛️ Module de gestion des Départements")

    def open_jury(self):
        messagebox.showinfo("Gestion", "⚖️ Module de gestion des Jurys")

    def open_deliberations(self):
        messagebox.showinfo("Gestion", "📊 Module de gestion des Délibérations")

    def open_statistiques(self):
        """Afficher les statistiques"""
        stats = {}
        if hasattr(self.user, 'consulter_statistiques'):
            try:
                stats = self.user.consulter_statistiques()
            except:
                pass

        messagebox.showinfo(
            "📊 Statistiques",
            f"👨‍🎓 Étudiants : {stats.get('nb_etudiants', 0)}\n"
            f"👨‍🏫 Enseignants : {stats.get('nb_enseignants', 0)}\n"
            f"📚 Cours : {stats.get('nb_cours', 0)}\n"
            f"🏛️ Départements : {stats.get('nb_departements', 0)}\n\n"
            "Année académique : 2025-2026"
        )

    def open_mes_cours(self):
        messagebox.showinfo("Professeur", "📖 Mes Cours")

    def open_saisie_notes(self):
        messagebox.showinfo("Professeur", "✏️ Saisie des Notes")

    def open_mes_notes(self):
        messagebox.showinfo("Étudiant", "📄 Mes Notes")

    def open_paiements(self):
        messagebox.showinfo("Étudiant", "💰 Mes Paiements")

    def rapport_etudiants(self):
        messagebox.showinfo("Rapport", "📋 Liste des Étudiants")

    def rapport_notes(self):
        messagebox.showinfo("Rapport", "📊 Relevé de Notes")

    def rapport_palmares(self):
        messagebox.showinfo("Rapport", "🏆 Palmarès")