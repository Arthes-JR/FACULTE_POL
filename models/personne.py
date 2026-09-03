"""
Modèles Personne
"""

from database.db_manager import DatabaseManager

class Personne:
    def __init__(self, id=None, nom=None, prenom=None, email=None, telephone=None):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.telephone = telephone
        self.db = DatabaseManager()
    
    def get_identite(self):
        return f"{self.prenom} {self.nom}"

class Etudiant(Personne):
    def __init__(self, id=None, nom=None, prenom=None, email=None, telephone=None,
                 matricule=None, filiere=None, annee_etude=None):
        super().__init__(id, nom, prenom, email, telephone)
        self.matricule = matricule
        self.filiere = filiere
        self.annee_etude = annee_etude

class Enseignant(Personne):
    pass

class Professeur(Personne):
    def __init__(self, id=None, nom=None, prenom=None, email=None, telephone=None, grade=None):
        super().__init__(id, nom, prenom, email, telephone)
        self.grade = grade

class Doyen(Personne):
    def __init__(self, id=None, nom=None, prenom=None, email=None, telephone=None, faculte_id=None):
        super().__init__(id, nom, prenom, email, telephone)
        self.faculte_id = faculte_id
    
    def consulter_statistiques(self):
        return {
            'nb_etudiants': 125,
            'nb_enseignants': 45,
            'nb_cours': 78,
            'nb_departements': 5
        }