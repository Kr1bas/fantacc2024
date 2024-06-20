-- Create table "sedi"
CREATE TABLE sedi (
    id_sede INT AUTO_INCREMENT PRIMARY KEY,
    tag_sede VARCHAR(20) NOT NULL,
    full_name_sede VARCHAR(100) NOT NULL,
    logo_sede VARCHAR(50)
);

-- Create table "bonus"
CREATE TABLE bonus (
    id_bonus INT AUTO_INCREMENT PRIMARY KEY,
    description_bonus VARCHAR(255) NOT NULL,
    value_bonus INT
);

-- Create table "teams"
CREATE TABLE teams (
    id_team INT AUTO_INCREMENT PRIMARY KEY,
    name_team VARCHAR(100) NOT NULL,
    captain_team INT,
    uni2_team INT,
    uni3_team INT,
    uni4_team INT,
    uni5_team INT,
    FOREIGN KEY (captain_team) REFERENCES sedi(id_sede),
    FOREIGN KEY (uni2_team) REFERENCES sedi(id_sede),
    FOREIGN KEY (uni3_team) REFERENCES sedi(id_sede),
    FOREIGN KEY (uni4_team) REFERENCES sedi(id_sede),
    FOREIGN KEY (uni5_team) REFERENCES sedi(id_sede)
);

-- Create table "players"
CREATE TABLE players (
    id_player INT AUTO_INCREMENT PRIMARY KEY,
    name_player VARCHAR(100) NOT NULL,
    sede_player INT,
    password_player CHAR(64),
    team_player INT,
    FOREIGN KEY (sede_player) REFERENCES sedi(id_sede),
    FOREIGN KEY (team_player) REFERENCES teams(id_team)
);
-- Create table "points"
CREATE TABLE points (
    id_point INT AUTO_INCREMENT PRIMARY KEY,
    bonus_id_point INT,
    sede_id_point INT,
    multiplier_point INT,
    FOREIGN KEY (bonus_id_point) REFERENCES bonus(id_bonus),
    FOREIGN KEY (sede_id_point) REFERENCES sedi(id_sede)
);

-- Create table "teams"
CREATE TABLE rickrolls (
    id_rr INT AUTO_INCREMENT PRIMARY KEY,
    user_rr INT,
    FOREIGN KEY (user_rr) REFERENCES players(id_player)
);

INSERT INTO sedi (tag_sede, full_name_sede, logo_sede)
VALUES
    ('aeronautica', 'Accademia Aeronautica di Pozzuoli', '/static/web/loghi/aeronautica.png'),
    ('unibo', 'Alma Mater Studiorum - Università di Bologna', '/static/web/loghi/unibo.png'),
    ('c3t', 'Centro di Competenza in Cybersecurity Toscano', '/static/web/loghi/c3t.png'),
    ('esercito', 'Comando per la Formazione e Scuola di Applicazione dell Esercito - Torino', '/static/web/loghi/esercito.png'),
    ('unibz', 'Libera Università di Bolzano', '/static/web/loghi/unibz.png'),
    ('poliba', 'Politecnico di Bari', '/static/web/loghi/poliba.png'),
    ('polimi', 'Politecnico di Milano', '/static/web/loghi/polimi.png'),
    ('polito', 'Politecnico di Torino', '/static/web/loghi/polito.png'),
    ('unirm1', 'Sapienza Università di Roma', '/static/web/loghi/unirm1.png'),
    ('unive', 'Università Ca Foscari Venezia', '/static/web/loghi/unive.png'),
    ('unicampus', 'Università Campus Bio-Medico di Roma', '/static/web/loghi/unicampus.png'),
    ('unicampania', 'Università degli Studi della Campania Luigi Vanvitelli', '/static/web/loghi/unicampania.png'),
    ('univaq', 'Università degli Studi dell Aquila', '/static/web/loghi/univaq.png'),
    ('uninsubria', 'Università degli Studi dell Insubria', '/static/web/loghi/uninsubria.png'),
    ('uniba', 'Università degli Studi di Bari Aldo Moro', '/static/web/loghi/uniba.png'),
    ('unibs', 'Università degli Studi di Brescia', '/static/web/loghi/unibs.png'),
    ('unica', 'Università degli Studi di Cagliari', '/static/web/loghi/unica.png'),
    ('unicam', 'Università degli Studi di Camerino', '/static/web/loghi/unicam.png'),
    ('unict', 'Università degli Studi di Catania', '/static/web/loghi/unict.png'),
    ('unife', 'Università degli Studi di Ferrara', '/static/web/loghi/unife.png'),
    ('unige', 'Università degli Studi di Genova', '/static/web/loghi/unige.png'),
    ('unime', 'Università degli Studi di Messina', '/static/web/loghi/unime.png'),
    ('unimi', 'Università degli Studi di Milano', '/static/web/loghi/unimi.png'),
    ('unimib', 'Università degli Studi di Milano-Bicocca', '/static/web/loghi/unimib.png'),
    ('unipd', 'Università degli Studi di Padova', '/static/web/loghi/unipd.png'),
    ('unipa', 'Università degli Studi di Palermo', '/static/web/loghi/unipa.png'),
    ('unipr', 'Università degli Studi di Parma', '/static/web/loghi/unipr.png'),
    ('unipg', 'Università degli Studi di Perugia', '/static/web/loghi/unipg.png'),
    ('unirm2', 'Università degli Studi di Roma Tor Vergata', '/static/web/loghi/unirm2.png'),
    ('unisa', 'Università degli Studi di Salerno', '/static/web/loghi/unisa.png'),
    ('unitn', 'Università degli Studi di Trento', '/static/web/loghi/unitn.png'),
    ('uniud', 'Università degli Studi di Udine', '/static/web/loghi/uniud.png'),
    ('univr', 'Università degli Studi di Verona', '/static/web/loghi/univr.png'),
    ('unich', 'Università degli Studi "Gabriele d Annunzio" di Chieti-Pescara', '/static/web/loghi/unich.png'),
    ('unirm3', 'Università degli Studi Roma Tre', '/static/web/loghi/unirm3.png'),
    ('unical', 'Università della Calabria', '/static/web/loghi/unical.png'),
    ('unisalento', 'Università del Salento', '/static/web/loghi/unisalento.png'),
    ('unimore', 'Università di Modena e Reggio Emilia', '/static/web/loghi/unimore.png'),
    ('napoli', 'Università di Napoli', '/static/web/loghi/napoli.png'),
    ('unipi', 'Università di Pisa', '/static/web/loghi/unipi.png'),
    ('unito', 'Università di Torino', '/static/web/loghi/unito.png'),
    ('unirc', 'Università Mediterranea di Reggio Calabria', '/static/web/loghi/unirc.png'),
    ('univpm', 'Università Politecnica delle Marche', '/static/web/loghi/univpm.png');


INSERT INTO bonus (description_bonus, value_bonus)
VALUES
    ("Bonus First blood: La tua squadra fa un first blood durante la demo (raddoppia durante la nazionale)",10),
    ("Bonus Gabibbo: Qualcuno della tua squadra posta una foto con abbigliamento a tema gabibbo.",10),
    ("Malus: La tua squadra arriva dopo il NopTeam durante la demo (raddoppia durante la nazionale)",-5),
    ("Bonus: La tua squadra fa il meme migliore dell'anno",20),
    ("Bonus: La tua squadra mema durante la presentazione delle vuln o dei workshop (vale 1 volta, solo nel canale meme-ctf o generale nazionale)",10),
    ("Bonus: il primo nazionale fa parte della tua squadra",50),
    ("Bonus: Qualcuno della tua squadra nomina uomo d'acciao o topolino o il gabibbo o sistema paese durante la presentazione",30),
    ("Bonus: La tua università è sponsorizzata da: NordVPN e/o altre VPN",20),
    ("Malus: Chiami uno dei tuoi tool 'La proxy'",-20),
    ("Bonus La tua squadra fa ridere Gaspare durante la presentazione delle vuln o dei workshop. Raddoppia se si tocca il naso",15),
    ("Malus: Manca un membro della squadra alla nazionale (si ripete per ogni membro mancante)",-10),
    ("Bonus: la tua squadra si presenta alla nazionale con la maglia del team",20),
    ("Bonus: trovi una unintended alla A/D",25),
    ("Bonus batti 5: La tua squadra batte il 5 a qualcuno degli sponsor durante la presentazione",50),
    ("Bonus: La tua squadra ringrazia lo staff, il pubblico e gli sponsor durante la presentazione",10),
    ("Bonus: Baci al pubblico durante la presentazione",15),
    ("Bonus fantaCc: La tua squadra nomina fantacyberchallenge durante la presentazione",25),
    ("Malus: qualcuno rickrolla la tua squadra",-25),
    ("Bonus classifica: prendi punti in base alla classifica della finale nazionale (10 punti per ogni posto)",10),
    ("Bonus: Fiore vero o finto tra i capelli veri o finti durante la presentazione",10),
    ("Malus Mirco: Indossi un cappello durante la gara (diventa bonus se è a tema gabibbo o è un bucket hat)",-10),
    ("Malus: Sbaglia a pronunciare una parola durante la presentazione (una sola volta)",-25),
    ("Bonus Mascotte: porti una mascotte alla nazionale (diventa malus se è la stessa del 2023)",30),
    ("Malus: Discorso e/o battute di carattere discriminatorio in chat",-20),
    ("Malus veneta: La tua squadra bestemmia sul discord",-25),
    ("Malus: la tua squadra si  becca una backdoor alla A/d",-25),
    ("Bonus: miglior nome team nel fantaCC",25);

INSERT INTO players(name_player,sede_player,password_player)
VALUES
    ("Kribas",22,"2fd00cf24f5ba14b500948d6564e67ab0dab42200c86984c3c416412f03a1acb")