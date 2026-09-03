import tkinter as tk
from tkinter import ttk, messagebox
from controllers.auth_controller import AuthController

class LoginView:
    def __init__(self, root, on_login_success):
        self.root = root
        self.root.title("UNIKIN - Gestion de Faculté")
        self.root.geometry("450x400")
        self.root.resizable(False, False)
        self.on_login_success = on_login_success
        self.auth_controller = AuthController()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Titre
        title = tk.Label(self.root, text="🏛️ UNIKIN", font=("Arial", 20, "bold"), fg="#1a237e")
        title.pack(pady=20)
        
        subtitle = tk.Label(self.root, text="Système de Gestion de Faculté", font=("Arial", 12))
        subtitle.pack()
        
        # Séparateur
        ttk.Separator(self.root, orient="horizontal").pack(fill="x", padx=30, pady=15)
        
        # Formulaire
        frame = tk.Frame(self.root)
        frame.pack(pady=20)
        
        # Email
        tk.Label(frame, text="Email:", font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=5)
        self.email_entry = tk.Entry(frame, width=30, font=("Arial", 11))
        self.email_entry.grid(row=0, column=1, pady=5, padx=10)
        self.email_entry.insert(0, "doyen@unikin.com")
        
        # Mot de passe
        tk.Label(frame, text="Mot de passe:", font=("Arial", 11)).grid(row=1, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(frame, width=30, font=("Arial", 11), show="*")
        self.password_entry.grid(row=1, column=1, pady=5, padx=10)
        self.password_entry.insert(0, "password")
        
        # Rôle
        tk.Label(frame, text="Rôle:", font=("Arial", 11)).grid(row=2, column=0, sticky="w", pady=5)
        self.role_var = tk.StringVar(value="Doyen")
        roles = ["Doyen", "Professeur", "Etudiant"]
        role_menu = ttk.Combobox(frame, textvariable=self.role_var, values=roles, width=27, state="readonly")
        role_menu.grid(row=2, column=1, pady=5, padx=10)
        
        # Boutons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)
        
        login_btn = tk.Button(btn_frame, text="Se connecter", command=self.login, 
                             bg="#1a237e", fg="white", padx=30, pady=8, font=("Arial", 11))
        login_btn.pack(side="left", padx=5)
        
        quit_btn = tk.Button(btn_frame, text="Quitter", command=self.root.quit,
                            bg="#e0e0e0", padx=30, pady=8, font=("Arial", 11))
        quit_btn.pack(side="left", padx=5)
        
        # Status
        self.status_label = tk.Label(self.root, text="", fg="red")
        self.status_label.pack(pady=5)
        
        # Enter key
        self.root.bind("<Return>", lambda e: self.login())
    
    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get()
        
        if not email or not password:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return
        
        user = self.auth_controller.authenticate(email, password, role)
        if user:
            self.root.destroy()
            self.on_login_success(user, role)
        else:
            messagebox.showerror("Erreur", "Identifiants incorrects")