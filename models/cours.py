"""
Modèles Cours et ChargeEnseignement
"""

from database.db_manager import DatabaseManager
from datetime import datetime

class Cours:
    """
    Cours dispensé dans un département
    """
    def __init__(self, id=None, code=None, intitule=None, credits=0, 
                 volume_horaire=0, heures_cours=0, heures_td=0, heures_tp=0,
                 semestre=None, type_cours=None, departement_id=None,
                 responsable_id=None, description=None):
        self.id = id
        self.code = code
        self.intitule = intitule
        self.credits = credits
        self.volume_horaire = volume_horaire
        self.heures_cours = heures_cours
        self.heures_td = heures_td
        self.heures_tp = heures_tp
        self.semestre = semestre
        self.type_cours = type_cours
        self.departement_id = departement_id
        self.responsable_id = responsable_id
        self.description = description
        self.db = DatabaseManager()
    
    def creer(self, data):
        """Créer un cours"""
        query = """
            INSERT INTO cours (
                code, intitule, description, credits, volume_horaire,
                heures_cours, heures_td, heures_tp, semestre, type_cours,
                departement_id, responsable_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        result = self.db.execute_query(query, (
            data['code'], data['intitule'], data.get('description'),
            data.get('credits', 0), data.get('volume_horaire', 0),
            data.get('heures_cours', 0), data.get('heures_td', 0),
            data.get('heures_tp', 0), data.get('semestre'),
            data.get('type_cours'), data['departement_id'],
            data.get('responsable_id')
        ))
        if result:
            self.id = result[0]['id']
            self.code = data['code']
            self.intitule = data['intitule']
        return self.id
    
    def modifier(self, data):
        """Modifier un cours"""
        query = """
            UPDATE cours SET
                intitule = %s,
                description = %s,
                credits = %s,
                volume_horaire = %s,
                heures_cours = %s,
                heures_td = %s,
                heures_tp = %s,
                semestre = %s,
                type_cours = %s,
                responsable_id = %s
            WHERE id = %s
        """
        return self.db.execute_query(query, (
            data.get('intitule', self.intitule),
            data.get('description'),
            data.get('credits', self.credits),
            data.get('volume_horaire', self.volume_horaire),
            data.get('heures_cours', self.heures_cours),
            data.get('heures_td', self.heures_td),
            data.get('heures_tp', self.heures_tp),
            data.get('semestre', self.semestre),
            data.get('type_cours', self.type_cours),
            data.get('responsable_id', self.responsable_id),
            self.id
        ))
    
    def supprimer(self):
        """Supprimer un cours"""
        query = "DELETE FROM cours WHERE id = %s"
        return self.db.execute_query(query, (self.id,))
    
    def get_charges(self):
        """Récupérer les charges d'enseignement"""
        query = """
            SELECT ce.*, p.nom, p.prenom
            FROM charges_enseignement ce
            JOIN enseignants e ON ce.enseignant_id = e.id
            JOIN personnes p ON e.id = p.id
            WHERE ce.cours_id = %s
            ORDER BY ce.date_soumission DESC
        """
        return self.db.execute_query(query, (self.id,))
    
    def save(self):
        """Sauvegarder le cours"""
        if self.id:
            return self.modifier({
                'intitule': self.intitule,
                'credits': self.credits,
                'volume_horaire': self.volume_horaire
            })
        else:
            return self.creer({
                'code': self.code,
                'intitule': self.intitule,
                'description': self.description,
                'credits': self.credits,
                'volume_horaire': self.volume_horaire,
                'semestre': self.semestre,
                'type_cours': self.type_cours,
                'departement_id': self.departement_id,
                'responsable_id': self.responsable_id
            })
    
    @staticmethod
    def get_by_code(code):
        """Récupérer un cours par son code"""
        db = DatabaseManager()
        result = db.execute_query("SELECT * FROM cours WHERE code = %s", (code,))
        if result:
            return Cours(
                id=result[0]['id'],
                code=result[0]['code'],
                intitule=result[0]['intitule'],
                credits=result[0]['credits'],
                volume_horaire=result[0]['volume_horaire'],
                semestre=result[0]['semestre'],
                type_cours=result[0]['type_cours'],
                departement_id=result[0]['departement_id'],
                responsable_id=result[0]['responsable_id'],
                description=result[0]['description']
            )
        return None
    
    @staticmethod
    def get_all():
        """Récupérer tous les cours"""
        db = DatabaseManager()
        return db.execute_query("""
            SELECT c.*, d.nom as departement_nom
            FROM cours c
            JOIN departements d ON c.departement_id = d.id
            ORDER BY c.code
        """)


class ChargeEnseignement:
    """
    Charge d'enseignement (attribution d'un cours à un enseignant)
    """
    STATUTS = ['SOUMIS', 'APPROUVE', 'REJETE', 'ANNULE']
    
    def __init__(self, id=None, enseignant_id=None, cours_id=None,
                 semestre_id=None, type_charge='COURS', volume_horaire=0,
                 date_soumission=None, statut='SOUMIS',
                 date_approbation=None, date_rejet=None,
                 motif_rejet=None, observation=None):
        self.id = id
        self.enseignant_id = enseignant_id
        self.cours_id = cours_id
        self.semestre_id = semestre_id
        self.type_charge = type_charge
        self.volume_horaire = volume_horaire
        self.date_soumission = date_soumission or datetime.now().date()
        self.statut = statut
        self.date_approbation = date_approbation
        self.date_rejet = date_rejet
        self.motif_rejet = motif_rejet
        self.observation = observation
        self.db = DatabaseManager()
    
    def soumettre(self):
        """Soumettre une charge"""
        self.statut = 'SOUMIS'
        query = """
            INSERT INTO charges_enseignement (
                enseignant_id, cours_id, semestre_id, type_charge,
                volume_horaire, date_soumission, statut
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (enseignant_id, cours_id, semestre_id) DO UPDATE SET
                date_soumission = EXCLUDED.date_soumission,
                statut = EXCLUDED.statut,
                date_approbation = NULL,
                date_rejet = NULL,
                motif_rejet = NULL
            RETURNING id
        """
        result = self.db.execute_query(query, (
            self.enseignant_id, self.cours_id, self.semestre_id,
            self.type_charge, self.volume_horaire,
            self.date_soumission, self.statut
        ))
        if result:
            self.id = result[0]['id']
        return self.id
    
    def approuver(self):
        """Approuver une charge"""
        if self.statut != 'SOUMIS':
            raise ValueError("Seule une charge soumise peut être approuvée")
        
        self.statut = 'APPROUVE'
        self.date_approbation = datetime.now().date()
        query = """
            UPDATE charges_enseignement
            SET statut = %s, date_approbation = %s, date_rejet = NULL, motif_rejet = NULL
            WHERE id = %s
        """
        return self.db.execute_query(query, (self.statut, self.date_approbation, self.id))
    
    def rejeter(self, motif):
        """Rejeter une charge"""
        if self.statut != 'SOUMIS':
            raise ValueError("Seule une charge soumise peut être rejetée")
        
        self.statut = 'REJETE'
        self.motif_rejet = motif
        self.date_rejet = datetime.now().date()
        query = """
            UPDATE charges_enseignement
            SET statut = %s, motif_rejet = %s, date_rejet = %s, date_approbation = NULL
            WHERE id = %s
        """
        return self.db.execute_query(query, (self.statut, self.motif_rejet, self.date_rejet, self.id))
    
    def est_approuvee(self):
        """Vérifier si la charge est approuvée"""
        return self.statut == 'APPROUVE'
    
    def save(self):
        """Sauvegarder la charge"""
        if self.id:
            query = """
                UPDATE charges_enseignement
                SET statut = %s, date_approbation = %s, date_rejet = %s,
                    motif_rejet = %s, observation = %s
                WHERE id = %s
            """
            return self.db.execute_query(query, (
                self.statut, self.date_approbation, self.date_rejet,
                self.motif_rejet, self.observation, self.id
            ))
        else:
            return self.soumettre()
    
    @staticmethod
    def get_by_enseignant(enseignant_id):
        """Récupérer toutes les charges d'un enseignant"""
        db = DatabaseManager()
        query = """
            SELECT ce.*, c.code, c.intitule
            FROM charges_enseignement ce
            JOIN cours c ON ce.cours_id = c.id
            WHERE ce.enseignant_id = %s
            ORDER BY ce.date_soumission DESC
        """
        return db.execute_query(query, (enseignant_id,))
    
    @staticmethod
    def get_by_cours(cours_id):
        """Récupérer toutes les charges pour un cours"""
        db = DatabaseManager()
        query = """
            SELECT ce.*, p.nom, p.prenom
            FROM charges_enseignement ce
            JOIN enseignants e ON ce.enseignant_id = e.id
            JOIN personnes p ON e.id = p.id
            WHERE ce.cours_id = %s
        """
        return db.execute_query(query, (cours_id,))