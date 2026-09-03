import tkinter as tk
from tkinter import ttk, messagebox

class MainView:
    def __init__(self, user, role):
        self.user = user
        self.role = role
        self.root = tk.Tk()
        self.root.title(f"UNIKIN - {role}")
        self.root.geometry("900x600")
        
        self.setup_ui()
        self.root.mainloop()
    
    def setup_ui(self):
        # Menu
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Déconnexion", command=self.logout)
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.root.quit)
        
        # Barre d'outils
        toolbar = tk.Frame(self.root, bg="#1a237e", height=50)
        toolbar.pack(fill="x")
        
        user_info = tk.Label(toolbar, text=f"👤 {self.user.get_identite()} | {self.role}", 
                            bg="#1a237e", fg="white", font=("Arial", 11))
        user_info.pack(side="left", padx=20)
        
        # Contenu principal
        main_frame = tk.Frame(self.root, bg="#f5f5f5")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Bienvenue
        welcome = tk.Label(main_frame, text=f"Bienvenue, {self.user.get_identite()} !", 
                          font=("Arial", 18, "bold"), bg="#f5f5f5", fg="#1a237e")
        welcome.pack(anchor="w", pady=10)
        
        # Rôle
        role_label = tk.Label(main_frame, text=f"Rôle: {self.role}", 
                             font=("Arial", 12), bg="#f5f5f5", fg="#666")
        role_label.pack(anchor="w")
        
        # Séparateur
        ttk.Separator(main_frame, orient="horizontal").pack(fill="x", pady=15)
        
        # Actions
        actions_frame = tk.LabelFrame(main_frame, text="⚡ Actions", font=("Arial", 12, "bold"), 
                                     bg="#f5f5f5", padx=15, pady=15)
        actions_frame.pack(fill="x", pady=10)
        
        # Boutons d'actions selon le rôle
        btn_frame = tk.Frame(actions_frame, bg="#f5f5f5")
        btn_frame.pack()
        
        if self.role == "Doyen":
            tk.Button(btn_frame, text="📊 Statistiques", command=self.show_stats,
                     bg="#e3f2fd", padx=20, pady=10).pack(side="left", padx=10)
            tk.Button(btn_frame, text="👨‍🎓 Étudiants", command=self.show_etudiants,
                     bg="#e3f2fd", padx=20, pady=10).pack(side="left", padx=10)
    
    def logout(self):
        if messagebox.askyesno("Déconnexion", "Voulez-vous quitter ?"):
            self.root.destroy()
            root = tk.Tk()
            from views.login_view import LoginView
            LoginView(root, lambda u, r: MainView(u, r))
            root.mainloop()
    
    def show_stats(self):
        if hasattr(self.user, 'consulter_statistiques'):
            stats = self.user.consulter_statistiques()
            messagebox.showinfo("Statistiques", 
                f"📊 Statistiques\n\n"
                f"Étudiants: {stats.get('nb_etudiants', 0)}\n"
                f"Enseignants: {stats.get('nb_enseignants', 0)}\n"
                f"Cours: {stats.get('nb_cours', 0)}"
            )
    
    def show_etudiants(self):
        messagebox.showinfo("Étudiants", "Module en développement")