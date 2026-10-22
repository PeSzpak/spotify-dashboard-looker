-- Modelo estrela: um fato (chart_diario) e as dimensões que o descrevem.
-- Uma linha do fato = "a música X estava na posição P do Top 50 do país C no dia D".

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS chart_diario;
DROP TABLE IF EXISTS musica_artista;
DROP TABLE IF EXISTS musicas;
DROP TABLE IF EXISTS artistas;
DROP TABLE IF EXISTS paises;

-- Dimensão país: códigos do Spotify integrados com o Banco Mundial pelo ISO-2
CREATE TABLE paises (
    pais_cod   TEXT PRIMARY KEY,          -- ISO-2 ('BR', 'US'…) ou 'GLOBAL'
    pais       TEXT NOT NULL,             -- nome em português
    regiao     TEXT,                      -- Banco Mundial
    renda      TEXT,                      -- Banco Mundial: Alta, Média-alta, Média-baixa
    populacao  INTEGER,                   -- Banco Mundial, 2023
    internet   REAL                       -- Banco Mundial: fração da população com internet (0-1)
);

-- Dimensão artista: origem estimada a partir de onde o artista mais acumulou dias no Top 50
CREATE TABLE artistas (
    artista_id INTEGER PRIMARY KEY,
    artista    TEXT NOT NULL UNIQUE,
    origem_cod TEXT NOT NULL              -- ISO-2 do país de origem ou 'INT' (astro global)
);

-- Dimensão música: atributos fixos da faixa
CREATE TABLE musicas (
    musica_id         TEXT PRIMARY KEY,   -- id do Spotify
    musica            TEXT NOT NULL,
    artistas          TEXT NOT NULL,      -- texto original: "Artista A, Artista B"
    artista_principal TEXT NOT NULL,
    album             TEXT,
    data_lancamento   TEXT,               -- AAAA-MM-DD
    explicita         INTEGER NOT NULL CHECK (explicita IN (0, 1)),
    colaboracao       INTEGER NOT NULL CHECK (colaboracao IN (0, 1)),  -- mais de um artista creditado
    brasileira        INTEGER NOT NULL CHECK (brasileira IN (0, 1)),   -- algum artista creditado é brasileiro
    duracao_min       REAL,
    dancabilidade     REAL,               -- 0-1, atributos de áudio do Spotify
    energia           REAL,
    valencia          REAL,               -- 0 = triste/tensa, 1 = alegre
    acustica          REAL,
    bpm               REAL
);

-- Ponte N:N entre músicas e artistas (feats)
CREATE TABLE musica_artista (
    musica_id  TEXT    NOT NULL REFERENCES musicas (musica_id),
    artista_id INTEGER NOT NULL REFERENCES artistas (artista_id),
    ordem      INTEGER NOT NULL,          -- 1 = artista principal
    PRIMARY KEY (musica_id, artista_id)
);

-- Fato: Top 50 diário por país
CREATE TABLE chart_diario (
    data         TEXT    NOT NULL,        -- AAAA-MM-DD
    pais_cod     TEXT    NOT NULL REFERENCES paises (pais_cod),
    posicao      INTEGER NOT NULL CHECK (posicao BETWEEN 1 AND 50),
    musica_id    TEXT    NOT NULL REFERENCES musicas (musica_id),
    popularidade INTEGER,                 -- 0-100 no dia da coleta (nulo quando não coletado)
    PRIMARY KEY (data, pais_cod, posicao),
    UNIQUE (data, pais_cod, musica_id)
);

CREATE INDEX ix_chart_pais_data ON chart_diario (pais_cod, data);
CREATE INDEX ix_chart_musica ON chart_diario (musica_id);
CREATE INDEX ix_ma_artista ON musica_artista (artista_id);
