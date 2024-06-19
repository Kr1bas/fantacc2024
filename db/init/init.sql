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
    value_bonus SMALLINT
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
    multiplier_point DECIMAL(5,2),
    FOREIGN KEY (bonus_id_point) REFERENCES bonus(id_bonus),
    FOREIGN KEY (sede_id_point) REFERENCES sedi(id_sede)
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
    ("Bonus 1",10),
    ("Bonus 2",20),
    ("Malus 1",-10),
    ("Malus 2",-20);

INSERT INTO players(name_player,sede_player,password_player)
VALUES
    ("kribas",22,"2fd00cf24f5ba14b500948d6564e67ab0dab42200c86984c3c416412f03a1acb")