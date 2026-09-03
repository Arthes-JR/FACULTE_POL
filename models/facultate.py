from database.db_manager import DatabaseManager

class Faculte:
    def __init__(self, id=None, nom=None, sigle=None, adresse=None):
        self.id = id
        self.nom = nom
        self.sigle = sigle
        self.adresse = adresse
        self.db = DatabaseManager()
    
    def get_departements(self):
        query = "SELECT * FROM departement WHERE faculte_id = %s"
        return self.db.execute_query(query, (self.id,))
    
    def save(self):
        query = """
            INSERT INTO faculte (nom, sigle, adresse) 
            VALUES (%s, %s, %s) 
            ON CONFLICT (sigle) DO UPDATE SET 
                nom = EXCLUDED.nom,
                adresse = EXCLUDED.adresse
            RETURNING id
        """
        result = self.db.execute_query(query, (self.nom, self.sigle, self.adresse))
        if result:
            self.id = result[0]['id']
        return self.id
    
    @staticmethod
    def get_all():
        db = DatabaseManager()
        return db.execute_query("SELECT * FROM faculte")
    
    @staticmethod
    def get_by_sigle(sigle):
        db = DatabaseManager()
        result = db.execute_query("SELECT * FROM faculte WHERE sigle = %s", (sigle,))
        if result:
            return Faculte(
                id=result[0]['id'],
                nom=result[0]['nom'],
                sigle=result[0]['sigle'],
                adresse=result[0]['adresse']
            )
        return None