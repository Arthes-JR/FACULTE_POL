#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test de connexion à PostgreSQL
"""

import psycopg2
import os
from dotenv import load_dotenv

def test_connection():
    """
    Tester la connexion à PostgreSQL
    """
    print("=" * 60)
    print("🔌 TEST DE CONNEXION À POSTGRESQL")
    print("=" * 60)
    
    # Charger les variables d'environnement
    load_dotenv()
    
    # Récupérer les paramètres de connexion
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'database': os.getenv('DB_NAME', 'gestion_faculte'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'postgres'),
        'port': os.getenv('DB_PORT', '5432')
    }
    
    print("\n📋 Paramètres de connexion:")
    print(f"   Host: {config['host']}")
    print(f"   Port: {config['port']}")
    print(f"   Base de données: {config['database']}")
    print(f"   Utilisateur: {config['user']}")
    print(f"   Mot de passe: {'*' * len(config['password'])}")
    
    try:
        print("\n🔄 Tentative de connexion...")
        
        # Établir la connexion
        conn = psycopg2.connect(
            host=config['host'],
            database=config['database'],
            user=config['user'],
            password=config['password'],
            port=config['port'],
            connect_timeout=10
        )
        
        print("✅ Connexion établie avec succès !")
        
        # Créer un curseur
        cursor = conn.cursor()
        
        # Récupérer la version
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"\n📌 Version PostgreSQL:")
        print(f"   {version[0]}")
        
        # Afficher les bases de données
        cursor.execute("""
            SELECT datname, pg_database_size(datname) as size 
            FROM pg_database 
            ORDER BY datname;
        """)
        databases = cursor.fetchall()
        
        print("\n📂 Bases de données:")
        print("-" * 50)
        for db in databases:
            size_mb = round(db[1] / (1024 * 1024), 2) if db[1] else 0
            print(f"   {db[0]:<20} - {size_mb} MB")
        
        # Vérifier si la base gestion_faculte existe
        cursor.execute("""
            SELECT 1 FROM pg_database WHERE datname = 'gestion_faculte';
        """)
        db_exists = cursor.fetchone()
        
        if db_exists:
            print("\n✅ La base 'gestion_faculte' existe déjà.")
        else:
            print("\n⚠️ La base 'gestion_faculte' n'existe pas encore.")
        
        # Afficher les tables si la base existe
        if db_exists:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()
            
            if tables:
                print(f"\n📊 Tables dans 'gestion_faculte' ({len(tables)} tables):")
                print("-" * 50)
                for table in tables:
                    print(f"   - {table[0]}")
            else:
                print("\n📊 Aucune table trouvée dans 'gestion_faculte'.")
        
        # Fermer la connexion
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ TEST DE CONNEXION RÉUSSI !")
        print("=" * 60)
        
        return True
        
    except psycopg2.OperationalError as e:
        print("\n❌ ERREUR DE CONNEXION !")
        print(f"   {str(e)}")
        print("\n📌 Vérifiez:")
        print("   1. PostgreSQL est-il installé ?")
        print("   2. Le service PostgreSQL est-il démarré ?")
        print("   3. Les identifiants dans le fichier .env sont-ils corrects ?")
        return False
        
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        return False


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🔄 TEST DE CONNEXION POSTGRESQL")
    print("=" * 60)
    
    # Tester la connexion
    test_connection()
    
    print("\n" + "=" * 60)
    print("🔚 FIN DU TEST")
    print("=" * 60)