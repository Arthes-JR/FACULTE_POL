from models.personne import Doyen, Etudiant, Professeur
from database.db_manager import DatabaseManager

class AuthController:
    def __init__(self):
        self.db = DatabaseManager()
        self.db.connect()
    
    def authenticate(self, email, password, role):
        query = "SELECT * FROM personne WHERE email = %s"
        result = self.db.execute_query(query, (email,))
        
        if not result:
            return None
        
        personne = result[0]
        
        if role == 'Doyen':
            query = "SELECT * FROM doyen WHERE id = %s"
            doyen_result = self.db.execute_query(query, (personne['id'],))
            if doyen_result:
                return Doyen(
                    id=personne['id'],
                    nom=personne['nom'],
                    prenom=personne['prenom'],
                    email=personne['email'],
                    telephone=personne['telephone'],
                    faculte_id=doyen_result[0].get('faculte_id')
                )
        
        elif role == 'Etudiant':
            query = "SELECT * FROM etudiant WHERE id = %s"
            etudiant_result = self.db.execute_query(query, (personne['id'],))
            if etudiant_result:
                return Etudiant(
                    id=personne['id'],
                    nom=personne['nom'],
                    prenom=personne['prenom'],
                    email=personne['email'],
                    telephone=personne['telephone'],
                    matricule=etudiant_result[0].get('matricule'),
                    filiere=etudiant_result[0].get('filiere'),
                    annee_etude=etudiant_result[0].get('annee_etude')
                )
        
        elif role == 'Professeur':
            query = "SELECT * FROM professeur WHERE id = %s"
            prof_result = self.db.execute_query(query, (personne['id'],))
            if prof_result:
                return Professeur(
                    id=personne['id'],
                    nom=personne['nom'],
                    prenom=personne['prenom'],
                    email=personne['email'],
                    telephone=personne['telephone'],
                    grade=prof_result[0].get('grade')
                )
        
        return None