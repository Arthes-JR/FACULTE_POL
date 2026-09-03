from abc import ABC, abstractmethod
from database.db_manager import DatabaseManager

class Personne(ABC):
    def __init__(self, id=None, nom=None, prenom=None, email=None, telephone=None):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.telephone = telephone
        self.db = DatabaseManager()
    
    @abstractmethod
    def authentifier(self, password):
        pass
    
    def get_identite(self):
        return f"{self.prenom} {self.nom}"
    
    def save(self, type_personne):
        query = """
            INSERT INTO personne (nom, prenom, email, telephone, type_personne) 
            VALUES (%s, %s, %s, %s, %s) 
            ON CONFLICT (email) DO UPDATE SET 
                nom = EXCLUDED.nom,
                prenom = EXCLUDED.prenom,
                telephone = EXCLUDED.telephone
            RETURNING id
        """
        result = self.db.execute_query(query, (self.nom, self.prenom, self.email, self.telephone, type_personne))
        if result:
            self.id = result[0]['id']
        return self.id

class Etudiant(Personne):
    def __init__(self, id=None, nom=None, prenom=None, email=None, telephone=None,
                 matricule=None, filiere=None, annee_etude=None):
        super().__init__(id, nom, prenom, email, telephone)
        self.matricule = matricule
        self.filiere = filiere
        self.annee_etude = annee_etude
    
    def authentifier(self, password):
        return True
    
    def save(self):
        super().save('ETUDIANT')
        query = """
            INSERT INTO etudiant (id, matricule, filiere, annee_etude) 
            VALUES (%s, %s, %s, %s) 
            ON CONFLICT (id) DO UPDATE SET 
                matricule = EXCLUDED.matricule,
                filiere = EXCLUDED.filiere,
                annee_etude = EXCLUDED.annee_etude
        """
        self.db.execute_query(query, (self.id, self.matricule, self.filiere, self.annee_etude))
        return self.id

class Enseignant(Personne):
    def __init__(self, id=None, nom=None, prenom=None, email=None, telephone=None,
                 specialite=None, date_embauche=None, statut=None):
        super().__init__(id, nom, prenom, email, telephone)
        self.specialite = specialite
        self.date_embauche = date_embauche
        self.statut = statut
    
    def authentifier(self, password):
        return True
    
    def enseigner(self, cours_id):
        query = """
            SELECT * FROM charge_enseignement 
            WHERE enseignant_id = %s AND cours_id = %s AND statut = 'APPROUVE'
        """
        result = self.db.execute_query(query, (self.id, cours_id))
        return bool(result)
    
    def save(self):
        super().save('ENSEIGNANT')
        query = """
            INSERT INTO enseignant (id, specialite, date_embauche, statut) 
            VALUES (%s, %s, %s, %s) 
            ON CONFLICT (id) DO UPDATE SET 
                specialite = EXCLUDED.specialite,
                date_embauche = EXCLUDED.date_embauche,
                statut = EXCLUDED.statut
        """
        self.db.execute_query(query, (self.id, self.specialite, self.date_embauche, self.statut))
        return self.id

class Professeur(Enseignant):
    def __init__(self, id=None, nom=None, prenom=None, email=None, telephone=None,
                 specialite=None, date_embauche=None, statut=None, grade=None):
        super().__init__(id, nom, prenom, email, telephone, specialite, date_embauche, statut)
        self.grade = grade
    
    def save(self):
        super().save()
        query = """
            INSERT INTO professeur (id, grade) 
            VALUES (%s, %s) 
            ON CONFLICT (id) DO UPDATE SET grade = EXCLUDED.grade
        """
        self.db.execute_query(query, (self.id, self.grade))
        return self.id

class Doyen(Professeur):
    def __init__(self, id=None, nom=None, prenom=None, email=None, telephone=None,
                 specialite=None, date_embauche=None, statut=None, grade=None,
                 date_debut_mandat=None, faculte_id=None):
        super().__init__(id, nom, prenom, email, telephone, specialite, date_embauche, statut, grade)
        self.date_debut_mandat = date_debut_mandat
        self.faculte_id = faculte_id
    
    def valider_dossier(self, dossier_id):
        print(f"Dossier {dossier_id} validé par le Doyen")
        return True
    
    def consulter_statistiques(self):
        return {
            'nb_etudiants': 0,
            'nb_enseignants': 0,
            'nb_cours': 0
        }
    
    def save(self):
        super().save()
        query = """
            INSERT INTO doyen (id, date_debut_mandat, faculte_id) 
            VALUES (%s, %s, %s) 
            ON CONFLICT (id) DO UPDATE SET 
                date_debut_mandat = EXCLUDED.date_debut_mandat,
                faculte_id = EXCLUDED.faculte_id
        """
        self.db.execute_query(query, (self.id, self.date_debut_mandat, self.faculte_id))
        return self.id