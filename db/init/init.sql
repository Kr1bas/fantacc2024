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
    ('aeronautica', 'Accademia Aeronautica di Pozzuoli', '/static/web/loghi/aeronautica'),
    ('unibo', 'Alma Mater Studiorum - Università di Bologna', '/static/web/loghi/unibo'),
    ('c3t', 'Centro di Competenza in Cybersecurity Toscano', '/static/web/loghi/c3t'),
    ('esercito', 'Comando per la Formazione e Scuola di Applicazione dell Esercito - Torino', '/static/web/loghi/esercito'),
    ('unibz', 'Libera Università di Bolzano', '/static/web/loghi/unibz'),
    ('poliba', 'Politecnico di Bari', '/static/web/loghi/poliba'),
    ('polimi', 'Politecnico di Milano', '/static/web/loghi/polimi'),
    ('polito', 'Politecnico di Torino', '/static/web/loghi/polito'),
    ('unirm1', 'Sapienza Università di Roma', '/static/web/loghi/unirm1'),
    ('unive', 'Università Ca Foscari Venezia', '/static/web/loghi/unive'),
    ('unicampus', 'Università Campus Bio-Medico di Roma', '/static/web/loghi/unicampus'),
    ('unicampania', 'Università degli Studi della Campania Luigi Vanvitelli', '/static/web/loghi/unicampania'),
    ('univaq', 'Università degli Studi dell Aquila', '/static/web/loghi/univaq'),
    ('uninsubria', 'Università degli Studi dell Insubria', '/static/web/loghi/uninsubria'),
    ('uniba', 'Università degli Studi di Bari Aldo Moro', '/static/web/loghi/uniba'),
    ('unibs', 'Università degli Studi di Brescia', '/static/web/loghi/unibs'),
    ('unica', 'Università degli Studi di Cagliari', '/static/web/loghi/unica'),
    ('unicam', 'Università degli Studi di Camerino', '/static/web/loghi/unicam'),
    ('unict', 'Università degli Studi di Catania', '/static/web/loghi/unict'),
    ('unife', 'Università degli Studi di Ferrara', '/static/web/loghi/unife'),
    ('unige', 'Università degli Studi di Genova', '/static/web/loghi/unige'),
    ('unime', 'Università degli Studi di Messina', '/static/web/loghi/unime'),
    ('unimi', 'Università degli Studi di Milano', '/static/web/loghi/unimi'),
    ('unimib', 'Università degli Studi di Milano-Bicocca', '/static/web/loghi/unimib'),
    ('unipd', 'Università degli Studi di Padova', '/static/web/loghi/unipd'),
    ('unipa', 'Università degli Studi di Palermo', '/static/web/loghi/unipa'),
    ('unipr', 'Università degli Studi di Parma', '/static/web/loghi/unipr'),
    ('unipg', 'Università degli Studi di Perugia', '/static/web/loghi/unipg'),
    ('unirm2', 'Università degli Studi di Roma Tor Vergata', '/static/web/loghi/unirm2'),
    ('unisa', 'Università degli Studi di Salerno', '/static/web/loghi/unisa'),
    ('unitn', 'Università degli Studi di Trento', '/static/web/loghi/unitn'),
    ('uniud', 'Università degli Studi di Udine', '/static/web/loghi/uniud'),
    ('univr', 'Università degli Studi di Verona', '/static/web/loghi/univr'),
    ('unich', 'Università degli Studi "Gabriele d Annunzio" di Chieti-Pescara', '/static/web/loghi/unich'),
    ('unirm3', 'Università degli Studi Roma Tre', '/static/web/loghi/unirm3'),
    ('unical', 'Università della Calabria', '/static/web/loghi/unical'),
    ('unisalento', 'Università del Salento', '/static/web/loghi/unisalento'),
    ('unimore', 'Università di Modena e Reggio Emilia', '/static/web/loghi/unimore'),
    ('napoli', 'Università di Napoli', '/static/web/loghi/napoli'),
    ('unipi', 'Università di Pisa', '/static/web/loghi/unipi'),
    ('unito', 'Università di Torino', '/static/web/loghi/unito'),
    ('unirc', 'Università Mediterranea di Reggio Calabria', '/static/web/loghi/unirc'),
    ('univpm', 'Università Politecnica delle Marche', '/static/web/loghi/univpm');
