USE knihovna_db;

-- View 1: Přehled aktuálně vypůjčených knih s informacemi o čtenáři
CREATE OR REPLACE VIEW v_aktualni_vypujcky AS
SELECT 
    v.id AS vypujcka_id,
    k.nazev AS kniha_nazev,
    k.isbn,
    CONCAT(c.jmeno, ' ', c.prijmeni) AS ctenar_jmeno,
    c.email AS ctenar_email,
    c.telefon AS ctenar_telefon,
    v.datum_vypujceni,
    v.predpokladane_vraceni,
    DATEDIFF(CURDATE(), v.predpokladane_vraceni) AS dny_po_terminu,
    v.stav
FROM vypujcky v
JOIN knihy k ON v.kniha_id = k.id
JOIN ctenari c ON v.ctenar_id = c.id
WHERE v.stav IN ('active', 'overdue')
ORDER BY v.datum_vypujceni DESC;

-- View 2: Statistiky knih - agregovaná data ze tří tabulek
CREATE OR REPLACE VIEW v_statistiky_knih AS
SELECT 
    k.id AS kniha_id,
    k.nazev AS kniha_nazev,
    z.nazev AS zanr,
    COUNT(v.id) AS pocet_vypujcek,
    COUNT(CASE WHEN v.stav = 'active' THEN 1 END) AS aktivnich_vypujcek,
    COUNT(CASE WHEN v.stav = 'returned' THEN 1 END) AS vraceno,
    MAX(v.datum_vypujceni) AS posledni_vypujcka,
    k.hodnoceni,
    k.dostupna
FROM knihy k
LEFT JOIN zanry z ON k.zanr_id = z.id
LEFT JOIN vypujcky v ON k.id = v.kniha_id
GROUP BY k.id, k.nazev, z.nazev, k.hodnoceni, k.dostupna
ORDER BY pocet_vypujcek DESC;
