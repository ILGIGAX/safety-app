CREATE TABLE IF NOT EXISTS utenti (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    nome TEXT NOT NULL,
    cognome TEXT NOT NULL,
    data_nascita DATE NOT NULL,
    genere TEXT NOT NULL,
    motivo_iscrizione TEXT
);
