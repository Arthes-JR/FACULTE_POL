-- ============================================================
-- SYSTÈME DE GESTION DE FACULTÉ - UNIKIN
-- Script de création des tables
-- ============================================================

-- MODULE 1 : PERSONNES
-- ============================================================

CREATE TABLE IF NOT EXISTS personnes (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    date_naissance DATE,
    lieu_naissance VARCHAR(100),
    sexe CHAR(1) CHECK (sexe IN ('M', 'F')),
    nationalite VARCHAR(50) DEFAULT 'Congolaise',
    email VARCHAR(255) UNIQUE NOT NULL,
    telephone VARCHAR(20),
    adresse VARCHAR(255),
    type_personne VARCHAR(50) NOT NULL CHECK (type_personne IN ('ETUDIANT', 'ENSEIGNANT', 'PERSONNEL', 'AUTRE')),
    photo VARCHAR(255),
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MODULE 2 : ÉTUDIANTS
-- ============================================================

CREATE TABLE IF NOT EXISTS etudiants (
    id INTEGER PRIMARY KEY REFERENCES personnes(id) ON DELETE CASCADE,
    matricule VARCHAR(50) UNIQUE NOT NULL,
    filiere VARCHAR(100),
    annee_etude INTEGER,
    promotion_id INTEGER,
    regime VARCHAR(50) DEFAULT 'PRESENTIEL' CHECK (regime IN ('PRESENTIEL', 'A_DISTANCE', 'MIXTE')),
    statut VARCHAR(50) DEFAULT 'INSCRIT' CHECK (statut IN ('INSCRIT', 'SUSPENDU', 'EXCLU', 'DIPLOME')),
    date_premiere_inscription DATE,
    lieu_residence VARCHAR(255),
    contact_urgence VARCHAR(100),
    email_personnel VARCHAR(255),
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MODULE 3 : ENSEIGNANTS
-- ============================================================

CREATE TABLE IF NOT EXISTS enseignants (
    id INTEGER PRIMARY KEY REFERENCES personnes(id) ON DELETE CASCADE,
    matricule VARCHAR(50) UNIQUE NOT NULL,
    specialite VARCHAR(200),
    qualification VARCHAR(100) CHECK (qualification IN ('ASSISTANT', 'CHEF_TRAVAUX', 'MAITRE_ASSISTANT', 'MAITRE_CONFERENCE', 'PROFESSEUR')),
    grade VARCHAR(50),
    date_embauche DATE,
    statut VARCHAR(50) DEFAULT 'PERMANENT' CHECK (statut IN ('PERMANENT', 'TEMPORAIRE', 'VISITEUR', 'VACATAIRE')),
    domaine_recherche TEXT,
    h_index INTEGER DEFAULT 0,
    publications_count INTEGER DEFAULT 0,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MODULE 4 : PERSONNEL ADMINISTRATIF
-- ============================================================

CREATE TABLE IF NOT EXISTS personnel_administratif (
    id INTEGER PRIMARY KEY REFERENCES personnes(id) ON DELETE CASCADE,
    matricule VARCHAR(50) UNIQUE NOT NULL,
    fonction VARCHAR(100),
    service VARCHAR(100),
    categorie VARCHAR(50) CHECK (categorie IN ('PERMANENT', 'CONTRACTUEL', 'VACATAIRE')),
    date_entree DATE,
    date_sortie DATE,
    supervision_id INTEGER REFERENCES personnel_administratif(id),
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MODULE 5 : APPARITEURS
-- ============================================================

CREATE TABLE IF NOT EXISTS appariteurs (
    id INTEGER PRIMARY KEY REFERENCES personnel_administratif(id) ON DELETE CASCADE,
    zone_affectation VARCHAR(100),
    tournee VARCHAR(50),
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MODULE 6 : COMPTABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS comptables (
    id INTEGER PRIMARY KEY REFERENCES personnel_administratif(id) ON DELETE CASCADE,
    numero_agrement VARCHAR(50),
    qualification VARCHAR(100),
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MODULE 7 : FACULTES
-- ============================================================

CREATE TABLE IF NOT EXISTS facultes (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    nom VARCHAR(200) NOT NULL,
    sigle VARCHAR(10) UNIQUE NOT NULL,
    adresse VARCHAR(255),
    telephone VARCHAR(20),
    email VARCHAR(255),
    site_web VARCHAR(255),
    doyen_id INTEGER REFERENCES enseignants(id),
    secretaire_id INTEGER REFERENCES personnel_administratif(id),
    date_creation DATE,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MODULE 8 : DEPARTEMENTS
-- ============================================================

CREATE TABLE IF NOT EXISTS departements (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    nom VARCHAR(200) NOT NULL,
    sigle VARCHAR(10) UNIQUE,
    faculte_id INTEGER NOT NULL REFERENCES facultes(id) ON DELETE CASCADE,
    chef_id INTEGER REFERENCES enseignants(id),
    description TEXT,
    date_creation DATE,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(code, faculte_id)
);

-- MODULE 9 : ANNEES ACADEMIQUES
-- ============================================================

CREATE TABLE IF NOT EXISTS annees_academiques (
    id SERIAL PRIMARY KEY,
    libelle VARCHAR(50) UNIQUE NOT NULL,
    debut DATE NOT NULL,
    fin DATE NOT NULL,
    statut VARCHAR(20) DEFAULT 'EN_COURS' CHECK (statut IN ('PREVUE', 'EN_COURS', 'TERMINEE', 'CLOTUREE')),
    date_ouverture_inscriptions DATE,
    date_cloture_inscriptions DATE,
    date_debut_cours DATE,
    date_fin_cours DATE,
    date_debut_examens DATE,
    date_fin_examens DATE,
    date_debut_deliberations DATE,
    date_fin_deliberations DATE,
    is_active BOOLEAN DEFAULT FALSE,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MODULE 10 : SEMESTRES
-- ============================================================

CREATE TABLE IF NOT EXISTS semestres (
    id SERIAL PRIMARY KEY,
    annee_academique_id INTEGER NOT NULL REFERENCES annees_academiques(id) ON DELETE CASCADE,
    numero SMALLINT NOT NULL CHECK (numero IN (1, 2, 3, 4, 5, 6)),
    intitule VARCHAR(100) NOT NULL,
    debut DATE NOT NULL,
    fin DATE NOT NULL,
    date_debut_cours DATE,
    date_fin_cours DATE,
    date_debut_examens DATE,
    date_fin_examens DATE,
    is_current BOOLEAN DEFAULT FALSE,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(annee_academique_id, numero)
);

-- MODULE 11 : PROMOTIONS
-- ============================================================

CREATE TABLE IF NOT EXISTS promotions (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    nom VARCHAR(200) NOT NULL,
    niveau VARCHAR(50) NOT NULL CHECK (niveau IN ('L1', 'L2', 'L3', 'M1', 'M2', 'D1', 'D2', 'D3')),
    departement_id INTEGER NOT NULL REFERENCES departements(id) ON DELETE CASCADE,
    annee_academique_id INTEGER NOT NULL REFERENCES annees_academiques(id),
    capacite INTEGER DEFAULT 0,
    effectif INTEGER DEFAULT 0,
    responsable_id INTEGER REFERENCES enseignants(id),
    date_creation DATE,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(nom, departement_id, annee_academique_id)
);

-- MODULE 12 : COURS
-- ============================================================

CREATE TABLE IF NOT EXISTS cours (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    intitule VARCHAR(200) NOT NULL,
    description TEXT,
    credits INTEGER DEFAULT 0 CHECK (credits >= 0),
    volume_horaire INTEGER DEFAULT 0 CHECK (volume_horaire >= 0),
    heures_cours INTEGER DEFAULT 0,
    heures_td INTEGER DEFAULT 0,
    heures_tp INTEGER DEFAULT 0,
    semestre INTEGER CHECK (semestre IN (1, 2, 3, 4, 5, 6)),
    type_cours VARCHAR(50) CHECK (type_cours IN ('FONDAMENTAL', 'COMPLEMENTAIRE', 'OPTIONNEL', 'LIBRE')),
    departement_id INTEGER NOT NULL REFERENCES departements(id) ON DELETE CASCADE,
    responsable_id INTEGER REFERENCES enseignants(id),
    prerequis TEXT,
    objectifs TEXT,
    contenu TEXT,
    modalites_evaluation TEXT,
    bibliographie TEXT,
    est_actif BOOLEAN DEFAULT TRUE,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MODULE 13 : CHARGES ENSEIGNEMENT
-- ============================================================

CREATE TABLE IF NOT EXISTS charges_enseignement (
    id SERIAL PRIMARY KEY,
    enseignant_id INTEGER NOT NULL REFERENCES enseignants(id) ON DELETE CASCADE,
    cours_id INTEGER NOT NULL REFERENCES cours(id) ON DELETE CASCADE,
    semestre_id INTEGER NOT NULL REFERENCES semestres(id),
    type_charge VARCHAR(50) CHECK (type_charge IN ('COURS', 'TD', 'TP', 'ENCADREMENT', 'AUTRE')),
    volume_horaire INTEGER DEFAULT 0,
    date_debut DATE,
    date_fin DATE,
    statut VARCHAR(20) DEFAULT 'SOUMIS' CHECK (statut IN ('SOUMIS', 'APPROUVE', 'REJETE', 'ANNULE')),
    date_soumission DATE,
    date_approbation DATE,
    date_rejet DATE,
    motif_rejet TEXT,
    observation TEXT,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(enseignant_id, cours_id, semestre_id)
);

-- MODULE 14 : EVALUATIONS
-- ============================================================

CREATE TABLE IF NOT EXISTS evaluations (
    id SERIAL PRIMARY KEY,
    cours_id INTEGER NOT NULL REFERENCES cours(id) ON DELETE CASCADE,
    semestre_id INTEGER NOT NULL REFERENCES semestres(id),
    type_evaluation VARCHAR(50) CHECK (type_evaluation IN ('CONTINUE', 'SESSION1', 'SESSION2', 'RATTRAPAGE', 'RECHARGEMENT', 'AUTRE')),
    intitule VARCHAR(200),
    coefficient DECIMAL(5,2) DEFAULT 1.0,
    ponderation DECIMAL(5,2) DEFAULT 100,
    date_evaluation DATE,
    duree INTEGER,
    salle VARCHAR(100),
    responsable_id INTEGER REFERENCES enseignants(id),
    est_publie BOOLEAN DEFAULT FALSE,
    date_publication DATE,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MODULE 15 : NOTES
-- ============================================================

CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY,
    etudiant_id INTEGER NOT NULL REFERENCES etudiants(id) ON DELETE CASCADE,
    evaluation_id INTEGER NOT NULL REFERENCES evaluations(id) ON DELETE CASCADE,
    valeur DECIMAL(5,2) CHECK (valeur >= 0 AND valeur <= 20),
    valeur_ponderee DECIMAL(5,2),
    appreciation VARCHAR(100),
    date_saisie TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    enseignant_saisie_id INTEGER REFERENCES enseignants(id),
    est_valide BOOLEAN DEFAULT FALSE,
    date_validation DATE,
    validateur_id INTEGER REFERENCES enseignants(id),
    observation TEXT,
    UNIQUE(etudiant_id, evaluation_id)
);

-- MODULE 16 : DOSSIERS INSCRIPTION
-- ============================================================

CREATE TABLE IF NOT EXISTS dossiers_inscription (
    id SERIAL PRIMARY KEY,
    etudiant_id INTEGER NOT NULL REFERENCES etudiants(id) ON DELETE CASCADE,
    promotion_id INTEGER NOT NULL REFERENCES promotions(id),
    semestre_id INTEGER REFERENCES semestres(id),
    date_soumission DATE NOT NULL,
    date_validation DATE,
    statut VARCHAR(50) DEFAULT 'SOUMIS' CHECK (statut IN ('SOUMIS', 'COMPLET', 'VALIDATION_EN_COURS', 'VALIDE', 'REJETE', 'ANNULE')),
    type_inscription VARCHAR(50) CHECK (type_inscription IN ('NOUVELLE', 'REINSCRIPTION', 'REORIENTATION', 'AUTRE')),
    mode_paiement VARCHAR(50) CHECK (mode_paiement IN ('ESPECES', 'VIREMENT', 'MOBILE_MONEY', 'AUTRE')),
    montant DECIMAL(10,2),
    commentaire TEXT,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MODULE 17 : PAIEMENTS
-- ============================================================

CREATE TABLE IF NOT EXISTS paiements (
    id SERIAL PRIMARY KEY,
    reference VARCHAR(50) UNIQUE NOT NULL,
    etudiant_id INTEGER NOT NULL REFERENCES etudiants(id) ON DELETE CASCADE,
    dossier_id INTEGER REFERENCES dossiers_inscription(id),
    montant DECIMAL(10,2) NOT NULL,
    devise VARCHAR(10) DEFAULT 'USD',
    date_paiement DATE NOT NULL,
    mode_paiement VARCHAR(50) CHECK (mode_paiement IN ('ESPECES', 'VIREMENT', 'MOBILE_MONEY', 'OM', 'AUTRE')),
    reference_transaction VARCHAR(100),
    statut VARCHAR(50) DEFAULT 'EN_ATTENTE' CHECK (statut IN ('EN_ATTENTE', 'CONFIRME', 'VALIDE', 'ANNULE', 'REMBOURSE')),
    date_confirmation DATE,
    confirmateur_id INTEGER REFERENCES personnel_administratif(id),
    commentaire TEXT,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MODULE 18 : JURYS
-- ============================================================

CREATE TABLE IF NOT EXISTS jurys (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    intitule VARCHAR(200) NOT NULL,
    type_jury VARCHAR(50) CHECK (type_jury IN ('SOUTENANCE', 'DELIBERATION', 'RECHARGEMENT', 'AUTRE')),
    faculte_id INTEGER REFERENCES facultes(id) ON DELETE CASCADE,
    departement_id INTEGER REFERENCES departements(id) ON DELETE CASCADE,
    president_id INTEGER REFERENCES enseignants(id),
    rapporteur_id INTEGER REFERENCES enseignants(id),
    date_constitution DATE,
    date_prevue DATE,
    date_reelle DATE,
    lieu VARCHAR(255),
    statut VARCHAR(50) DEFAULT 'CONSTITUE' CHECK (statut IN ('CONSTITUE', 'EN_SEANCE', 'TERMINE', 'ANNULE')),
    resultat TEXT,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MODULE 19 : MEMBRES JURY
-- ============================================================

CREATE TABLE IF NOT EXISTS membres_jury (
    id SERIAL PRIMARY KEY,
    jury_id INTEGER NOT NULL REFERENCES jurys(id) ON DELETE CASCADE,
    enseignant_id INTEGER NOT NULL REFERENCES enseignants(id) ON DELETE CASCADE,
    fonction VARCHAR(50) CHECK (fonction IN ('PRESIDENT', 'RAPPORTEUR', 'MEMBRE', 'OBSERVATEUR', 'SECRETAIRE')),
    ordre SMALLINT DEFAULT 0,
    date_designation DATE,
    observation TEXT,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(jury_id, enseignant_id)
);

-- MODULE 20 : DELIBERATIONS
-- ============================================================

CREATE TABLE IF NOT EXISTS deliberations (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    jury_id INTEGER REFERENCES jurys(id) ON DELETE SET NULL,
    semestre_id INTEGER NOT NULL REFERENCES semestres(id),
    promotion_id INTEGER REFERENCES promotions(id),
    date_deliberation DATE,
    heure_debut TIME,
    heure_fin TIME,
    lieu VARCHAR(255),
    process_verbal TEXT,
    decision_globale TEXT,
    statut VARCHAR(50) DEFAULT 'PREVUE' CHECK (statut IN ('PREVUE', 'EN_COURS', 'TERMINEE', 'ANNULEE')),
    date_validation DATE,
    validateur_id INTEGER REFERENCES enseignants(id),
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MODULE 21 : PALMARES
-- ============================================================

CREATE TABLE IF NOT EXISTS palmares (
    id SERIAL PRIMARY KEY,
    deliberation_id INTEGER NOT NULL REFERENCES deliberations(id) ON DELETE CASCADE,
    promotion_id INTEGER REFERENCES promotions(id),
    date_publication DATE,
    rang_etudiant INTEGER,
    moyenne DECIMAL(5,2),
    mention VARCHAR(50) CHECK (mention IN ('PASSABLE', 'ASSEZ_BIEN', 'BIEN', 'TRES_BIEN', 'DISTINCTION', 'AUCUNE')),
    decision VARCHAR(100) CHECK (decision IN ('ADMIS', 'ECHOUE', 'SUSPENDU', 'REORIENTE', 'EXCLU')),
    observation TEXT,
    est_officiel BOOLEAN DEFAULT FALSE,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MODULE 22 : LABORATOIRES
-- ============================================================

CREATE TABLE IF NOT EXISTS laboratoires (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    nom VARCHAR(200) NOT NULL,
    sigle VARCHAR(20),
    type_laboratoire VARCHAR(50) CHECK (type_laboratoire IN ('RECHERCHE', 'ENSEIGNEMENT', 'MIXTE')),
    departement_id INTEGER REFERENCES departements(id) ON DELETE CASCADE,
    responsable_id INTEGER REFERENCES enseignants(id),
    localisation VARCHAR(255),
    description TEXT,
    budget_annuel DECIMAL(15,2),
    date_creation DATE,
    statut VARCHAR(50) DEFAULT 'ACTIF' CHECK (statut IN ('ACTIF', 'INACTIF', 'EN_RENOVATION')),
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MODULE 23 : DOCUMENTS OFFICIELS
-- ============================================================

CREATE TABLE IF NOT EXISTS documents_officiels (
    id SERIAL PRIMARY KEY,
    etudiant_id INTEGER NOT NULL REFERENCES etudiants(id) ON DELETE CASCADE,
    type_document VARCHAR(50) NOT NULL CHECK (type_document IN ('ATESTATION', 'RELEVE', 'DIPLOME', 'CERTIFICAT', 'CARTE_ETUDIANT', 'AUTRE')),
    intitule VARCHAR(200),
    numero VARCHAR(50) UNIQUE,
    contenu TEXT,
    chemin_fichier VARCHAR(255),
    date_generation DATE NOT NULL,
    date_signature DATE,
    signataire_id INTEGER REFERENCES enseignants(id),
    est_signe BOOLEAN DEFAULT FALSE,
    est_valide BOOLEAN DEFAULT FALSE,
    date_validation DATE,
    validateur_id INTEGER REFERENCES personnel_administratif(id),
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- INDEX POUR OPTIMISER LES PERFORMANCES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_personnes_email ON personnes(email);
CREATE INDEX IF NOT EXISTS idx_personnes_type ON personnes(type_personne);
CREATE INDEX IF NOT EXISTS idx_etudiants_matricule ON etudiants(matricule);
CREATE INDEX IF NOT EXISTS idx_etudiants_promotion ON etudiants(promotion_id);
CREATE INDEX IF NOT EXISTS idx_enseignants_matricule ON enseignants(matricule);
CREATE INDEX IF NOT EXISTS idx_facultes_sigle ON facultes(sigle);
CREATE INDEX IF NOT EXISTS idx_departements_faculte ON departements(faculte_id);
CREATE INDEX IF NOT EXISTS idx_cours_code ON cours(code);
CREATE INDEX IF NOT EXISTS idx_cours_departement ON cours(departement_id);
CREATE INDEX IF NOT EXISTS idx_notes_etudiant ON notes(etudiant_id);
CREATE INDEX IF NOT EXISTS idx_paiements_etudiant ON paiements(etudiant_id);
CREATE INDEX IF NOT EXISTS idx_paiements_reference ON paiements(reference);
CREATE INDEX IF NOT EXISTS idx_dossiers_etudiant ON dossiers_inscription(etudiant_id);

-- ============================================================
-- DONNÉES DE TEST
-- ============================================================

INSERT INTO personnes (nom, prenom, email, telephone, type_personne) 
VALUES ('Mvumbi', 'Jean-Pierre', 'doyen.fd@unikin.com', '+243812345678', 'ENSEIGNANT')
ON CONFLICT (email) DO NOTHING;

INSERT INTO personnes (nom, prenom, email, telephone, type_personne) 
VALUES ('Lukusa', 'Pierre', 'professeur@unikin.com', '+243812345680', 'ENSEIGNANT')
ON CONFLICT (email) DO NOTHING;

INSERT INTO personnes (nom, prenom, email, telephone, type_personne) 
VALUES ('Kalonji', 'David', 'etudiant@unikin.com', '+243812345681', 'ETUDIANT')
ON CONFLICT (email) DO NOTHING;

INSERT INTO facultes (code, nom, sigle, adresse) 
VALUES ('FD', 'Faculté de Droit', 'FD', 'Kinshasa, RDC')
ON CONFLICT (sigle) DO NOTHING;