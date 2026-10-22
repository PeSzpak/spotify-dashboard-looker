-- Views que viram as fontes de dados do Looker Studio (uma por arquivo CSV, ver exportar.py).
-- O banco inteiro tem ~300 MB e o upload de CSV do Looker aceita até 100 MB por arquivo:
-- cada view entrega só o recorte e o grão que as telas precisam.

-- 1. Top 50 diário do Brasil e do Global, desnormalizado (telas 1 e 3)
DROP VIEW IF EXISTS looker_charts;
CREATE VIEW looker_charts AS
WITH primeira_vez AS (
    SELECT pais_cod, musica_id, MIN(data) AS primeiro_dia
    FROM chart_diario WHERE pais_cod IN ('BR', 'GLOBAL') GROUP BY 1, 2
)
SELECT c.data,
       substr(c.data, 1, 7)                                            AS mes,
       CASE c.pais_cod WHEN 'BR' THEN 'Brasil' ELSE 'Global' END       AS chart,
       c.posicao,
       CASE WHEN c.posicao = 1 THEN '#1' WHEN c.posicao <= 10 THEN 'Top 2-10' ELSE 'Top 11-50' END AS faixa,
       m.musica, m.artistas, m.artista_principal,
       CASE m.brasileira WHEN 1 THEN 'Brasileira' ELSE 'Estrangeira' END AS origem_musica,
       m.brasileira,
       m.explicita,
       m.colaboracao                                                   AS feat,
       m.duracao_min,
       CAST(julianday(c.data) - julianday(m.data_lancamento) AS INTEGER) AS idade_dias,
       CASE WHEN julianday(c.data) - julianday(m.data_lancamento) <= 30 THEN 1 ELSE 0 END AS lancamento_recente,
       -- estreia: 1º dia da música no chart (o 1º dia da base não conta, ali tudo pareceria novo)
       CASE WHEN c.data = pv.primeiro_dia AND c.data > (SELECT MIN(data) FROM chart_diario) THEN 1 ELSE 0 END AS estreia,
       m.dancabilidade, m.energia, m.valencia,
       c.popularidade
FROM chart_diario c
JOIN musicas m USING (musica_id)
JOIN primeira_vez pv ON pv.pais_cod = c.pais_cod AND pv.musica_id = c.musica_id
WHERE c.pais_cod IN ('BR', 'GLOBAL');

-- 2. Artista x dia no Top 50 Brasil: feat conta para todos os artistas creditados (tela 2)
DROP VIEW IF EXISTS looker_artistas;
CREATE VIEW looker_artistas AS
SELECT c.data, substr(c.data, 1, 7) AS mes, a.artista,
       CASE a.origem_cod WHEN 'BR' THEN 'Brasileiro' ELSE 'Estrangeiro' END AS origem_artista,
       CASE ma.ordem WHEN 1 THEN 'Principal' ELSE 'Participação' END        AS papel,
       m.musica, c.posicao,
       CASE WHEN c.posicao <= 10 THEN 1 ELSE 0 END AS no_top10
FROM chart_diario c
JOIN musica_artista ma USING (musica_id)
JOIN artistas a USING (artista_id)
JOIN musicas m USING (musica_id)
WHERE c.pais_cod = 'BR';

-- 3. Uma linha por música que passou pelo Top 50 Brasil: permanência e alcance (telas 1, 2 e 4)
DROP VIEW IF EXISTS looker_musicas;
CREATE VIEW looker_musicas AS
WITH fora AS (
    SELECT musica_id, COUNT(DISTINCT pais_cod) AS paises
    FROM chart_diario WHERE pais_cod NOT IN ('BR', 'GLOBAL') GROUP BY musica_id
)
SELECT m.musica, m.artistas, m.artista_principal,
       CASE m.brasileira WHEN 1 THEN 'Brasileira' ELSE 'Estrangeira' END AS origem_musica,
       m.explicita, m.colaboracao AS feat, m.duracao_min,
       COUNT(*)                 AS dias_top50,
       SUM(c.posicao <= 10)     AS dias_top10,
       SUM(c.posicao = 1)       AS dias_no_1,
       MIN(c.posicao)           AS melhor_posicao,
       MIN(c.data)              AS entrou_em,
       MAX(c.data)              AS saiu_em,
       COALESCE(f.paises, 0)    AS paises_fora_do_brasil,
       -- quem já estava no chart no 1º dia da base tem a permanência cortada
       CASE WHEN MIN(c.data) = (SELECT MIN(data) FROM chart_diario) THEN 1 ELSE 0 END AS ja_estava_no_inicio
FROM chart_diario c
JOIN musicas m USING (musica_id)
LEFT JOIN fora f USING (musica_id)
WHERE c.pais_cod = 'BR'
GROUP BY c.musica_id;

-- 4. Os 72 países + Banco Mundial, com os indicadores comparativos (tela 4)
DROP VIEW IF EXISTS looker_paises;
CREATE VIEW looker_paises AS
WITH base AS (
    SELECT c.pais_cod,
           COUNT(*)                         AS linhas,
           COUNT(DISTINCT c.data)           AS dias,
           COUNT(DISTINCT c.musica_id)      AS musicas_distintas,
           AVG(m.brasileira)                AS pct_musica_brasileira,
           COUNT(DISTINCT CASE WHEN m.brasileira = 1 THEN c.musica_id END) AS musicas_brasileiras,
           AVG(m.explicita)                 AS pct_explicitas,
           AVG(m.colaboracao)               AS pct_feat,
           AVG(m.duracao_min)               AS duracao_media,
           AVG(m.dancabilidade)             AS dancabilidade,
           AVG(m.energia)                   AS energia,
           AVG(m.valencia)                  AS valencia
    FROM chart_diario c JOIN musicas m USING (musica_id)
    WHERE c.pais_cod <> 'GLOBAL'
    GROUP BY c.pais_cod
),
top5 AS (
    SELECT pais_cod, SUM(dias) * 1.0 / MAX(total) AS pct_top5_artistas
    FROM (
        SELECT c.pais_cod, COUNT(*) AS dias,
               ROW_NUMBER() OVER (PARTITION BY c.pais_cod ORDER BY COUNT(*) DESC) AS pos,
               SUM(COUNT(*)) OVER (PARTITION BY c.pais_cod) AS total
        FROM chart_diario c JOIN musica_artista ma USING (musica_id)
        WHERE ma.ordem = 1 AND c.pais_cod <> 'GLOBAL'
        GROUP BY c.pais_cod, ma.artista_id
    )
    WHERE pos <= 5
    GROUP BY pais_cod
)
SELECT p.pais_cod, p.pais, p.regiao, p.renda, p.populacao, p.internet,
       b.musicas_distintas,
       ROUND(b.musicas_distintas * 30.0 / b.dias, 1) AS musicas_por_30_dias,
       ROUND(b.pct_musica_brasileira, 4) AS pct_musica_brasileira,
       b.musicas_brasileiras,
       ROUND(t.pct_top5_artistas, 4)     AS pct_top5_artistas,
       ROUND(b.pct_explicitas, 4)        AS pct_explicitas,
       ROUND(b.pct_feat, 4)              AS pct_feat,
       ROUND(b.duracao_media, 2)         AS duracao_media,
       ROUND(b.dancabilidade, 3)         AS dancabilidade,
       ROUND(b.energia, 3)               AS energia,
       ROUND(b.valencia, 3)              AS valencia
FROM base b
JOIN paises p USING (pais_cod)
JOIN top5 t USING (pais_cod);

-- 5. Música brasileira fora do Brasil: país x música x mês (tela 4, mapa e tabela)
DROP VIEW IF EXISTS looker_exportacao;
CREATE VIEW looker_exportacao AS
SELECT p.pais_cod, p.pais, p.regiao,
       substr(c.data, 1, 7) AS mes,
       m.musica, m.artistas,
       COUNT(*)             AS dias_no_top50,
       MIN(c.posicao)       AS melhor_posicao
FROM chart_diario c
JOIN musicas m USING (musica_id)
JOIN paises p USING (pais_cod)
WHERE m.brasileira = 1 AND c.pais_cod NOT IN ('BR', 'GLOBAL')
GROUP BY p.pais_cod, mes, m.musica, m.artistas;
