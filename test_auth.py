#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test simple d'authentification
"""

from dotenv import load_dotenv
load_dotenv()

from database.db_manager import DatabaseManager
from controllers.auth_controller import AuthController

def test_auth():
    print("=" * 60)
    print("🧪 TEST D'AUTHENTIFICATION")
    print("=" * 60)
    
    # Tester les emails
    tests = [
        ("doyen.fd@unikin.com", "Doyen"),
        ("professeur@unikin.com", "Professeur"),
        ("etudiant@unikin.com", "Étudiant")
    ]
    
    for email, role in tests:
        print(f"\n📝 Test avec: {email} / Rôle: {role}")
        print("-" * 40)
        
        auth = AuthController()
        user = auth.authenticate(email, "password", role)
        
        if user:
            print(f"✅ AUTHENTIFICATION RÉUSSIE!")
            print(f"   Utilisateur: {user.get_identite()}")
            print(f"   Email: {user.email}")
        else:
            print(f"❌ Échec d'authentification")
    
    print("\n" + "=" * 60)
    print("🔚 FIN DU TEST")
    print("=" * 60)

if __name__ == "__main__":
    test_auth()