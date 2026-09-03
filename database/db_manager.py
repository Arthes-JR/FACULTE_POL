import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.connection = None
            cls._instance.cursor = None
        return cls._instance
    
    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                database=os.getenv('DB_NAME', 'gestion_faculte'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', 'postgres'),
                port=os.getenv('DB_PORT', '5432')
            )
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            print("✅ Connexion à PostgreSQL établie")
            return True
        except Exception as e:
            print(f"❌ Erreur de connexion: {e}")
            return False
    
    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            if query.strip().upper().startswith('SELECT'):
                return self.cursor.fetchall()
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Erreur: {e}")
            self.connection.rollback()
            return None
    
    def create_database(self):
        """Créer la base de données si elle n'existe pas"""
        try:
            db_name = os.getenv('DB_NAME', 'gestion_faculte')
            
            # Se connecter à la base 'postgres' par défaut
            conn = psycopg2.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                database='postgres',
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', 'postgres'),
                port=os.getenv('DB_PORT', '5432')
            )
            conn.autocommit = True
            cursor = conn.cursor()
            
            # Vérifier si la base existe
            cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
            exists = cursor.fetchone()
            
            if not exists:
                cursor.execute(f"CREATE DATABASE {db_name}")
                print(f"✅ Base de données '{db_name}' créée")
            else:
                print(f"✅ Base de données '{db_name}' existe déjà")
            
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Erreur création base: {e}")
            return False
    
    def create_tables(self):
        tables = [
            """
            CREATE TABLE IF NOT EXISTS personne (
                id SERIAL PRIMARY KEY,
                nom VARCHAR(100) NOT NULL,
                prenom VARCHAR(100) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                telephone VARCHAR(20),
                type_personne VARCHAR(50) NOT NULL
            )
            """,
            
            """
            CREATE TABLE IF NOT EXISTS etudiant (
                id INTEGER PRIMARY KEY REFERENCES personne(id),
                matricule VARCHAR(50) UNIQUE NOT NULL,
                filiere VARCHAR(100),
                annee_etude INTEGER
            )
            """,
            
            """
            CREATE TABLE IF NOT EXISTS enseignant (
                id INTEGER PRIMARY KEY REFERENCES personne(id),
                specialite VARCHAR(200),
                date_embauche DATE,
                statut VARCHAR(50)
            )
            """,
            
            """
            CREATE TABLE IF NOT EXISTS professeur (
                id INTEGER PRIMARY KEY REFERENCES enseignant(id),
                grade VARCHAR(50)
            )
            """,
            
            """
            CREATE TABLE IF NOT EXISTS doyen (
                id INTEGER PRIMARY KEY REFERENCES professeur(id),
                date_debut_mandat DATE,
                faculte_id INTEGER
            )
            """,
            
            """
            CREATE TABLE IF NOT EXISTS faculte (
                id SERIAL PRIMARY KEY,
                nom VARCHAR(200) NOT NULL,
                sigle VARCHAR(10) UNIQUE NOT NULL,
                adresse VARCHAR(255)
            )
            """,
            
            """
            CREATE TABLE IF NOT EXISTS departement (
                id SERIAL PRIMARY KEY,
                nom VARCHAR(200) NOT NULL,
                code VARCHAR(20) UNIQUE NOT NULL,
                faculte_id INTEGER REFERENCES faculte(id)
            )
            """,
            
            """
            CREATE TABLE IF NOT EXISTS cours (
                id SERIAL PRIMARY KEY,
                code VARCHAR(20) UNIQUE NOT NULL,
                intitule VARCHAR(200) NOT NULL,
                credits INTEGER DEFAULT 0,
                heures INTEGER DEFAULT 0,
                departement_id INTEGER REFERENCES departement(id)
            )
            """,
            
            """
            CREATE TABLE IF NOT EXISTS charge_enseignement (
                id SERIAL PRIMARY KEY,
                enseignant_id INTEGER REFERENCES enseignant(id),
                cours_id INTEGER REFERENCES cours(id),
                date_soumission DATE NOT NULL,
                statut VARCHAR(20) DEFAULT 'SOUMIS',
                date_approbation DATE,
                motif_rejet TEXT
            )
            """,
            
            """
            CREATE TABLE IF NOT EXISTS note (
                id SERIAL PRIMARY KEY,
                etudiant_id INTEGER REFERENCES etudiant(id),
                cours_id INTEGER REFERENCES cours(id),
                valeur DECIMAL(5,2),
                date_evaluation DATE
            )
            """
        ]
        
        for query in tables:
            self.execute_query(query)
        print("✅ Tables créées")
        return True
    
    def seed_data(self):
        data = [
            """
            INSERT INTO personne (nom, prenom, email, telephone, type_personne) 
            VALUES ('Mvumbi', 'Jean-Pierre', 'doyen@unikin.com', '+243812345678', 'PROFESSEUR')
            ON CONFLICT (email) DO NOTHING
            """,
            
            """
            INSERT INTO personne (nom, prenom, email, telephone, type_personne) 
            VALUES ('Kalonji', 'David', 'etudiant@unikin.com', '+243812345679', 'ETUDIANT')
            ON CONFLICT (email) DO NOTHING
            """,
            
            """
            INSERT INTO personne (nom, prenom, email, telephone, type_personne) 
            VALUES ('Lukusa', 'Pierre', 'professeur@unikin.com', '+243812345680', 'ENSEIGNANT')
            ON CONFLICT (email) DO NOTHING
            """,
            
            """
            INSERT INTO faculte (nom, sigle, adresse) 
            VALUES ('Faculté de Droit', 'FD', 'Kinshasa, RDC')
            ON CONFLICT (sigle) DO NOTHING
            """,
            
            """
            INSERT INTO faculte (nom, sigle, adresse) 
            VALUES ('Faculté de Médecine', 'FM', 'Kinshasa, RDC')
            ON CONFLICT (sigle) DO NOTHING
            """
        ]
        
        for query in data:
            self.execute_query(query)
        print("✅ Données initiales insérées")
        return True