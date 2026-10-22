-- KPIs estratégicos: cada consulta responde a uma pergunta de negócio da gravadora.
-- Comparações mensais usam só os meses completos (nov/2023 a jan/2025): out/2023 e fev/2025 são parciais.
-- Rode com: python3 kpis.py  (gera docs/resultados_kpis.md)

-- @kpi 1 | Volume | Quantas músicas e artistas diferentes passaram pelo Top 50 Brasil no período?
SELECT COUNT(DISTINCT c.musica_id)  AS musicas_distintas,
       COUNT(DISTINCT ma.artista_id) AS artistas_distintos,
       COUNT(DISTINCT c.data)        AS dias_coletados
FROM chart_diario c
JOIN musica_artista ma USING (musica_id)
WHERE c.pais_cod = 'BR';

-- @kpi 2 | Volume / Tempo | Quantas músicas estreiam por mês no Top 50, no Brasil e no Global?
-- estreia = primeiro dia de uma música naquele chart; ajustado pelos dias coletados no mês
WITH estreias AS (
    SELECT pais_cod, musica_id, MIN(data) AS primeiro_dia
    FROM chart_diario
    WHERE pais_cod IN ('BR', 'GLOBAL')
    GROUP BY pais_cod, musica_id
),
dias AS (
    SELECT pais_cod, substr(data, 1, 7) AS mes, COUNT(DISTINCT data) AS dias
    FROM chart_diario WHERE pais_cod IN ('BR', 'GLOBAL') GROUP BY 1, 2
)
SELECT d.mes,
       SUM(CASE WHEN e.pais_cod = 'BR' THEN 1 ELSE 0 END)     AS estreias_brasil,
       SUM(CASE WHEN e.pais_cod = 'GLOBAL' THEN 1 ELSE 0 END) AS estreias_global,
       MAX(CASE WHEN d.pais_cod = 'BR' THEN d.dias END)       AS dias_coletados
FROM dias d
LEFT JOIN estreias e ON e.pais_cod = d.pais_cod AND substr(e.primeiro_dia, 1, 7) = d.mes
WHERE d.mes BETWEEN '2023-11' AND '2025-01'
GROUP BY d.mes
ORDER BY d.mes;

-- @kpi 3 | Eficiência | Quanto do Top 50 é ocupado por música brasileira, no Top 50, no Top 10 e no #1?
SELECT p.pais AS chart,
       ROUND(100.0 * AVG(m.brasileira), 1)                                             AS pct_top50,
       ROUND(100.0 * AVG(CASE WHEN c.posicao <= 10 THEN m.brasileira END), 1)          AS pct_top10,
       ROUND(100.0 * AVG(CASE WHEN c.posicao = 1 THEN m.brasileira END), 1)            AS pct_no_1
FROM chart_diario c
JOIN musicas m USING (musica_id)
JOIN paises p USING (pais_cod)
WHERE c.pais_cod IN ('BR', 'GLOBAL', 'PT')
GROUP BY p.pais
ORDER BY pct_top50 DESC;

-- @kpi 4 | Eficiência | Quanto tempo uma música fica no Top 50 Brasil? Brasileiras duram mais?
WITH permanencia AS (
    SELECT c.musica_id, m.brasileira, COUNT(*) AS dias, MIN(c.posicao) AS melhor
    FROM chart_diario c JOIN musicas m USING (musica_id)
    WHERE c.pais_cod = 'BR'
      AND c.musica_id NOT IN (SELECT musica_id FROM chart_diario   -- ignora quem já estava no 1º dia
                              WHERE pais_cod = 'BR' AND data = (SELECT MIN(data) FROM chart_diario))
    GROUP BY c.musica_id
)
SELECT CASE brasileira WHEN 1 THEN 'Brasileira' ELSE 'Estrangeira' END AS musica,
       COUNT(*)                                                      AS musicas,
       ROUND(AVG(dias), 1)                                           AS media_dias,
       ROUND(100.0 * AVG(dias <= 7), 1)                              AS pct_saem_em_ate_7_dias,
       ROUND(100.0 * AVG(dias >= 90), 1)                             AS pct_ficam_90_dias_ou_mais,
       ROUND(100.0 * AVG(melhor <= 10), 1)                           AS pct_chegam_ao_top10
FROM permanencia
GROUP BY brasileira;

-- @kpi 5 | Ranking | Quais os 10 artistas que mais ocuparam o Top 50 Brasil (dias somando todas as músicas)?
SELECT a.artista,
       COUNT(*)                                       AS dias_no_chart,
       COUNT(DISTINCT c.musica_id)                    AS musicas,
       SUM(c.posicao <= 10)                           AS dias_no_top10,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM chart_diario WHERE pais_cod = 'BR'), 1) AS pct_do_chart
FROM chart_diario c
JOIN musica_artista ma USING (musica_id)
JOIN artistas a USING (artista_id)
WHERE c.pais_cod = 'BR'
GROUP BY a.artista
ORDER BY dias_no_chart DESC
LIMIT 10;

-- @kpi 6 | Ranking | Quais músicas dominaram o #1 do Brasil?
SELECT m.musica, m.artistas,
       SUM(c.posicao = 1)  AS dias_no_1,
       COUNT(*)            AS dias_no_top50,
       MIN(c.data)         AS entrou_em
FROM chart_diario c
JOIN musicas m USING (musica_id)
WHERE c.pais_cod = 'BR'
GROUP BY c.musica_id
HAVING dias_no_1 > 0
ORDER BY dias_no_1 DESC
LIMIT 10;

-- @kpi 7 | Eficiência | Que formato de música faz sucesso: feat, explícita, duração? (Brasil x Global)
SELECT p.pais AS chart,
       ROUND(100.0 * AVG(m.colaboracao), 1)  AS pct_com_feat,
       ROUND(100.0 * AVG(m.explicita), 1)    AS pct_explicitas,
       ROUND(AVG(m.duracao_min), 2)          AS duracao_media_min,
       ROUND(100.0 * AVG(m.duracao_min < 2.5), 1) AS pct_menos_de_2min30
FROM chart_diario c
JOIN musicas m USING (musica_id)
JOIN paises p USING (pais_cod)
WHERE c.pais_cod IN ('BR', 'GLOBAL')
GROUP BY p.pais;

-- @kpi 8 | Eficiência | O público quer novidade ou catálogo? Idade das músicas no chart
SELECT p.pais AS chart,
       ROUND(100.0 * AVG(julianday(c.data) - julianday(m.data_lancamento) <= 30), 1)  AS pct_lancadas_ha_30_dias,
       ROUND(100.0 * AVG(julianday(c.data) - julianday(m.data_lancamento) > 365), 1)  AS pct_com_mais_de_1_ano,
       CAST(AVG(julianday(c.data) - julianday(m.data_lancamento)) AS INTEGER)         AS idade_media_dias
FROM chart_diario c
JOIN musicas m USING (musica_id)
JOIN paises p USING (pais_cod)
WHERE c.pais_cod IN ('BR', 'GLOBAL') AND m.data_lancamento IS NOT NULL
GROUP BY p.pais;

-- @kpi 9 | Tempo | A participação brasileira no Top 50 Brasil cresce ou cai mês a mês?
SELECT substr(c.data, 1, 7)                  AS mes,
       ROUND(100.0 * AVG(m.brasileira), 1)   AS pct_brasileira,
       ROUND(100.0 * AVG(m.explicita), 1)    AS pct_explicitas,
       ROUND(AVG(m.duracao_min), 2)          AS duracao_media_min,
       ROUND(AVG(m.valencia), 3)             AS valencia_media
FROM chart_diario c
JOIN musicas m USING (musica_id)
WHERE c.pais_cod = 'BR' AND substr(c.data, 1, 7) BETWEEN '2023-11' AND '2025-01'
GROUP BY mes
ORDER BY mes;

-- @kpi 10 | Ranking | Em quais países a música brasileira mais toca (exportação)?
SELECT p.pais, p.regiao,
       ROUND(100.0 * AVG(m.brasileira), 2)            AS pct_musica_brasileira,
       COUNT(DISTINCT CASE WHEN m.brasileira = 1 THEN c.musica_id END) AS musicas_brasileiras
FROM chart_diario c
JOIN musicas m USING (musica_id)
JOIN paises p USING (pais_cod)
WHERE c.pais_cod NOT IN ('BR', 'GLOBAL')
GROUP BY p.pais
HAVING musicas_brasileiras > 0
ORDER BY pct_musica_brasileira DESC
LIMIT 10;

-- @kpi 11 | Ranking | Quais músicas brasileiras mais viajaram (número de países onde entraram no Top 50)?
-- agrupa por nome + artistas: a mesma música pode ter mais de um id no Spotify (single e álbum)
SELECT m.musica, m.artistas,
       COUNT(DISTINCT c.pais_cod)        AS paises_fora_do_brasil,
       GROUP_CONCAT(DISTINCT c.pais_cod) AS onde
FROM chart_diario c
JOIN musicas m USING (musica_id)
WHERE m.brasileira = 1 AND c.pais_cod NOT IN ('BR', 'GLOBAL')
GROUP BY m.musica, m.artistas
ORDER BY paises_fora_do_brasil DESC
LIMIT 10;

-- @kpi 12 | Eficiência | Quão concentrado é cada mercado? Fatia do chart ocupada pelos 5 maiores artistas
WITH dias_artista AS (
    SELECT c.pais_cod, ma.artista_id, COUNT(*) AS dias
    FROM chart_diario c JOIN musica_artista ma USING (musica_id)
    WHERE ma.ordem = 1                      -- só o artista principal, para não contar feat duas vezes
    GROUP BY c.pais_cod, ma.artista_id
),
ranking AS (
    SELECT pais_cod, dias,
           ROW_NUMBER() OVER (PARTITION BY pais_cod ORDER BY dias DESC) AS pos,
           SUM(dias) OVER (PARTITION BY pais_cod)                       AS total
    FROM dias_artista
)
SELECT p.pais, p.renda,
       ROUND(100.0 * SUM(dias) / MAX(total), 1)  AS pct_top5_artistas,
       RANK() OVER (ORDER BY 1.0 * SUM(dias) / MAX(total) DESC) AS posicao_entre_73
FROM ranking r JOIN paises p USING (pais_cod)
WHERE pos <= 5
GROUP BY p.pais
ORDER BY pct_top5_artistas DESC;

-- @kpi 13 | Eficiência | O Brasil escuta música mais dançante, enérgica e alegre que o resto do mundo?
WITH perfil AS (
    SELECT c.pais_cod,
           AVG(m.dancabilidade) AS danca, AVG(m.energia) AS energia, AVG(m.valencia) AS valencia
    FROM chart_diario c JOIN musicas m USING (musica_id)
    WHERE c.pais_cod <> 'GLOBAL'
    GROUP BY c.pais_cod
),
posicoes AS (
    SELECT pais_cod, danca, energia, valencia,
           RANK() OVER (ORDER BY danca DESC)    AS rank_danca,
           RANK() OVER (ORDER BY energia DESC)  AS rank_energia,
           RANK() OVER (ORDER BY valencia DESC) AS rank_valencia
    FROM perfil
)
SELECT 'Brasil' AS pais, ROUND(danca, 3) AS dancabilidade, rank_danca, ROUND(energia, 3) AS energia, rank_energia,
       ROUND(valencia, 3) AS valencia, rank_valencia
FROM posicoes WHERE pais_cod = 'BR'
UNION ALL
SELECT 'Média dos 72 países', ROUND(AVG(danca), 3), NULL, ROUND(AVG(energia), 3), NULL, ROUND(AVG(valencia), 3), NULL
FROM perfil;

-- @kpi 14 | Integração | Países mais conectados renovam mais o chart? (Banco Mundial x Spotify)
WITH renovacao AS (
    SELECT pais_cod, 1.0 * COUNT(DISTINCT musica_id) / COUNT(DISTINCT data) * 30 AS musicas_novas_por_30_dias
    FROM chart_diario WHERE pais_cod <> 'GLOBAL' GROUP BY pais_cod
)
SELECT CASE WHEN p.internet >= 0.95 THEN '1. 95% ou mais'
            WHEN p.internet >= 0.85 THEN '2. 85% a 95%'
            WHEN p.internet >= 0.70 THEN '3. 70% a 85%'
            ELSE '4. menos de 70%' END            AS populacao_com_internet,
       COUNT(*)                                   AS paises,
       ROUND(AVG(r.musicas_novas_por_30_dias), 1) AS musicas_distintas_por_30_dias,
       GROUP_CONCAT(p.pais_cod)                   AS exemplos
FROM renovacao r JOIN paises p USING (pais_cod)
WHERE p.internet IS NOT NULL
GROUP BY 1
ORDER BY 1;

-- @kpi 15 | Sazonalidade | O Natal invade o chart? % do Top 50 com música natalina de 15 a 25/12/2024
-- natalina = título com palavra de Natal (Christmas, Navidad, Natal, Jingle, Santa, Snow…)
WITH periodo AS (
    SELECT c.pais_cod, m.musica,
           (m.musica LIKE '%Christmas%' OR m.musica LIKE '%Navidad%' OR m.musica LIKE '%Natal%'
            OR m.musica LIKE '%Jingle%' OR m.musica LIKE '%Santa %' OR m.musica LIKE '%Snow%'
            OR m.musica LIKE '%Wonderful Time%' OR m.musica LIKE '%Weihnacht%' OR m.musica LIKE '%Noël%') AS natalina
    FROM chart_diario c JOIN musicas m USING (musica_id)
    WHERE c.data BETWEEN '2024-12-15' AND '2024-12-25'
),
ranking AS (
    SELECT p.pais,
           ROUND(100.0 * AVG(natalina), 1)                    AS pct_natalinas,
           COUNT(DISTINCT CASE WHEN natalina THEN musica END)  AS musicas_natalinas,
           RANK() OVER (ORDER BY AVG(natalina) DESC)           AS posicao_entre_73
    FROM periodo JOIN paises p USING (pais_cod)
    GROUP BY p.pais
)
SELECT * FROM ranking
WHERE pais IN ('Brasil', 'Global', 'Estados Unidos', 'Alemanha', 'Reino Unido', 'Portugal', 'México', 'Argentina')
   OR posicao_entre_73 <= 3
ORDER BY pct_natalinas DESC;
