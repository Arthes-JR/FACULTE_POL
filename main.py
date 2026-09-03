#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
import sys

from database.db_manager import DatabaseManager
from views.login_view import LoginView
from views.main_view import MainView

def init_database():
    db = DatabaseManager()
    
    # Créer la base si elle n'existe pas
    if not db.create_database():
        return False
    
    # Se connecter
    if not db.connect():
        return False
    
    # Créer les tables
    if not db.create_tables():
        return False
    
    # Insérer les données
    db.seed_data()
    
    return True

def main():
    try:
        # Initialiser la base
        if not init_database():
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Erreur", 
                "Impossible de se connecter à PostgreSQL.\n"
                "Vérifiez que le serveur est en cours d'exécution.")
            root.destroy()
            sys.exit(1)
        
        # Lancer l'application
        root = tk.Tk()
        
        def on_login_success(user, role):
            root.destroy()
            MainView(user, role)
        
        LoginView(root, on_login_success)
        root.mainloop()
        
    except Exception as e:
        print(f"Erreur: {e}")
        messagebox.showerror("Erreur", str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()