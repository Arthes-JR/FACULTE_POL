"""
Contrôleur d'authentification - Version SIMPLIFIÉE
"""

from database.db_manager import DatabaseManager

class AuthController:
    def __init__(self):
        self.db = DatabaseManager()
        self.db.connect()

    def authenticate(self, email, password, role):
        print(f"🔍 Recherche de: {email}")
        
        # Chercher l'utilisateur
        query = "SELECT * FROM personnes WHERE email = %s"
        result = self.db.execute_query(query, (email,))
        
        if not result:
            print(f"❌ Email non trouvé: {email}")
            return None
        
        personne = result[0]
        print(f"✅ Utilisateur trouvé: {personne['nom']} {personne['prenom']}")
        
        # Créer un utilisateur simple sans vérification de rôle
        class User:
            def __init__(self, data):
                self.id = data['id']
                self.nom = data['nom']
                self.prenom = data['prenom']
                self.email = data['email']
                self.telephone = data['telephone']
            
            def get_identite(self):
                return f"{self.prenom} {self.nom}"
            
            def consulter_statistiques(self):
                return {'nb_etudiants': 0, 'nb_enseignants': 0, 'nb_cours': 0}
        
        print(f"✅ Authentification réussie!")
        return User(personne)