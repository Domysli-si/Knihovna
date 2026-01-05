-- Drop database if exists (pro čisté prostředí)
DROP DATABASE IF EXISTS knihovna_db;
CREATE DATABASE knihovna_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE knihovna_db;

-- Tabulka: autori
CREATE TABLE autori (
    id INT AUTO_INCREMENT PRIMARY KEY,
    jmeno VARCHAR(100) NOT NULL,
    prijmeni VARCHAR(100) NOT NULL,
    datum_narozeni DATE,
    zeme_puvodu VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Tabulka: zanry
CREATE TABLE zanry (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nazev VARCHAR(50) NOT NULL UNIQUE,
    popis TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Tabulka: knihy
-- Obsahuje: VARCHAR (nazev, isbn), FLOAT (hodnoceni), BOOLEAN (dostupna), DATE (rok_vydani)
CREATE TABLE knihy (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nazev VARCHAR(255) NOT NULL,
    isbn VARCHAR(20) UNIQUE,
    rok_vydani INT,
    pocet_stran INT,
    hodnoceni FLOAT DEFAULT 0.0 CHECK (hodnoceni >= 0.0 AND hodnoceni <= 5.0),
    dostupna BOOLEAN DEFAULT TRUE,
    zanr_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (zanr_id) REFERENCES zanry(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- Tabulka: ctenari
CREATE TABLE ctenari (
    id INT AUTO_INCREMENT PRIMARY KEY,
    jmeno VARCHAR(100) NOT NULL,
    prijmeni VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telefon VARCHAR(20),
    registrovan_od DATE NOT NULL,
    aktivni BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Tabulka: vypujcky
-- Obsahuje: ENUM (stav), DATETIME (datum_vypujceni, datum_vraceni)
CREATE TABLE vypujcky (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kniha_id INT NOT NULL,
    ctenar_id INT NOT NULL,
    datum_vypujceni DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    datum_vraceni DATETIME,
    predpokladane_vraceni DATE NOT NULL,
    stav ENUM('active', 'returned', 'overdue') NOT NULL DEFAULT 'active',
    poznamka TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (kniha_id) REFERENCES knihy(id) ON DELETE CASCADE,
    FOREIGN KEY (ctenar_id) REFERENCES ctenari(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Vazební tabulka: knihy_autori (M:N vazba)
CREATE TABLE knihy_autori (
    kniha_id INT NOT NULL,
    autor_id INT NOT NULL,
    poradi INT DEFAULT 1,
    PRIMARY KEY (kniha_id, autor_id),
    FOREIGN KEY (kniha_id) REFERENCES knihy(id) ON DELETE CASCADE,
    FOREIGN KEY (autor_id) REFERENCES autori(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Indexy pro lepší výkon
CREATE INDEX idx_knihy_zanr ON knihy(zanr_id);
CREATE INDEX idx_vypujcky_kniha ON vypujcky(kniha_id);
CREATE INDEX idx_vypujcky_ctenar ON vypujcky(ctenar_id);
CREATE INDEX idx_vypujcky_stav ON vypujcky(stav);
