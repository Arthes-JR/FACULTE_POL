#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Système de Gestion de Faculté - UNIKIN
Point d'entrée de l'application
"""

import tkinter as tk
from tkinter import messagebox
import sys
from dotenv import load_dotenv

load_dotenv()

from database.db_manager import DatabaseManager
from views.login_view_enhanced import LoginViewEnhanced
from views.main_view import MainView

def init_database():
    """Initialiser la base de données"""
    try:
        db = DatabaseManager()
        if not db.create_database():
            return False
        if not db.connect():
            return False
        print("✅ Base de données prête")
        return True
    except Exception as e:
        print(f"❌ Erreur d'initialisation: {e}")
        return False

def main():
    """Fonction principale"""
    try:
        if not init_database():
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Erreur de Base de Données",
                "Impossible de se connecter à PostgreSQL.\n"
                "Vérifiez que le serveur est en cours d'exécution."
            )
            root.destroy()
            sys.exit(1)
        
        root = tk.Tk()
        
        def on_login_success(user, role):
            # La fenêtre de connexion est détruite dans LoginViewEnhanced
            # On crée directement la fenêtre principale
            MainView(user, role)
        
        LoginViewEnhanced(root, on_login_success)
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()