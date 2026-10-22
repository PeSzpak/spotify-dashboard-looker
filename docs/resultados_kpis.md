# Resultados dos KPIs

Gerado por `python3 kpis.py` a partir de `sql/02_kpis.sql`.

## KPI 1 · Volume

**Quantas músicas e artistas diferentes passaram pelo Top 50 Brasil no período?**

| musicas_distintas | artistas_distintos | dias_coletados |
|---|---|---|
| 663 | 460 | 477 |

## KPI 2 · Volume / Tempo

**Quantas músicas estreiam por mês no Top 50, no Brasil e no Global?**

| mes | estreias_brasil | estreias_global | dias_coletados |
|---|---|---|---|
| 2023-11 | 22 | 46 | 30 |
| 2023-12 | 30 | 56 | 31 |
| 2024-01 | 26 | 37 | 31 |
| 2024-02 | 35 | 43 | 29 |
| 2024-03 | 52 | 66 | 29 |
| 2024-04 | 67 | 66 | 30 |
| 2024-05 | 46 | 36 | 31 |
| 2024-06 | 37 | 28 | 30 |
| 2024-07 | 28 | 37 | 31 |
| 2024-08 | 45 | 41 | 31 |
| 2024-09 | 39 | 28 | 30 |
| 2024-10 | 36 | 39 | 31 |
| 2024-11 | 34 | 49 | 27 |
| 2024-12 | 36 | 38 | 24 |
| 2025-01 | 31 | 32 | 31 |

## KPI 3 · Eficiência

**Quanto do Top 50 é ocupado por música brasileira, no Top 50, no Top 10 e no #1?**

| chart | pct_top50 | pct_top10 | pct_no_1 |
|---|---|---|---|
| Brasil | 96,5 | 98,1 | 100 |
| Portugal | 31 | 29,6 | 31,7 |
| Global | 0,9 | 0,2 | 0 |

## KPI 4 · Eficiência

**Quanto tempo uma música fica no Top 50 Brasil? Brasileiras duram mais?**

| musica | musicas | media_dias | pct_saem_em_ate_7_dias | pct_ficam_90_dias_ou_mais | pct_chegam_ao_top10 |
|---|---|---|---|---|---|
| Estrangeira | 95 | 8,8 | 76,8 | 2,1 | 10,5 |
| Brasileira | 518 | 36,9 | 33,8 | 12,7 | 34,9 |

## KPI 5 · Ranking

**Quais os 10 artistas que mais ocuparam o Top 50 Brasil (dias somando todas as músicas)?**

| artista | dias_no_chart | musicas | dias_no_top10 | pct_do_chart |
|---|---|---|---|---|
| Ana Castela | 1.783 | 33 | 446 | 7,5 |
| MC Ryan SP | 1.277 | 26 | 277 | 5,4 |
| Simone Mendes | 1.110 | 19 | 252 | 4,7 |
| Luan Pereira | 1.072 | 19 | 335 | 4,5 |
| Henrique & Juliano | 1.071 | 19 | 136 | 4,5 |
| Murilo Huff | 1.031 | 11 | 106 | 4,3 |
| MC Tuto | 924 | 11 | 403 | 3,9 |
| Zé Neto & Cristiano | 890 | 11 | 258 | 3,7 |
| MC PH | 835 | 18 | 259 | 3,5 |
| Mc IG | 779 | 22 | 233 | 3,3 |

## KPI 6 · Ranking

**Quais músicas dominaram o #1 do Brasil?**

| musica | artistas | dias_no_1 | dias_no_top50 | entrou_em |
|---|---|---|---|---|
| Let's Go 4 | Dj GBR, Mc IG, MC Ryan SP, MC PH, Mc Davi, Mc Luki, Mc Don Juan, Mc Kadu, TrapLaudo, MC GP, MC GH do 7 | 68 | 202 | 2023-10-18 |
| Barbie | MC Tuto, DJ Glenner | 46 | 110 | 2024-10-21 |
| MTG QUEM NÃO QUER SOU EU | DJ TOPO | 33 | 173 | 2024-05-16 |
| DEJA VU | Luan Santana, Ana Castela | 24 | 96 | 2023-12-10 |
| Oh Garota Eu Quero Você Só Pra Mim | Oruam, Zé Felipe, MC Tuto, Dj Lc da Roça, MC K9, Mc Rodrigo do CN, mc pl alves | 20 | 60 | 2024-12-20 |
| Digitando | Gustavo Moura & Rafael | 19 | 103 | 2024-03-31 |
| Saveiro | Kaique e Felipe, Luan Pereira | 16 | 149 | 2024-08-04 |
| THE BOX MEDLEY FUNK 2 | THE BOX, Mc Brinquedo, MC Cebezinho, MC Tuto, Mc Laranjinha | 16 | 217 | 2024-04-30 |
| Só Fé | Grelo | 15 | 80 | 2024-08-06 |
| Diz Aí Qual é o Plano? | Mc IG, MC Ryan SP, Oruam, MC GH do 7, MC GP, MC Nego Micha, MC PH, Mc Luki, Mc Poze do Rodo, Murillo e LT no Beat, TrapLaudo | 13 | 92 | 2024-03-23 |

## KPI 7 · Eficiência

**Que formato de música faz sucesso: feat, explícita, duração? (Brasil x Global)**

| chart | pct_com_feat | pct_explicitas | duracao_media_min | pct_menos_de_2min30 |
|---|---|---|---|---|
| Brasil | 62,5 | 25,4 | 3,09 | 25,6 |
| Global | 28,8 | 36,8 | 3,29 | 12,1 |

## KPI 8 · Eficiência

**O público quer novidade ou catálogo? Idade das músicas no chart**

| chart | pct_lancadas_ha_30_dias | pct_com_mais_de_1_ano | idade_media_dias |
|---|---|---|---|
| Brasil | 20,2 | 2,9 | 136 |
| Global | 20,9 | 24,8 | 1.187 |

## KPI 9 · Tempo

**A participação brasileira no Top 50 Brasil cresce ou cai mês a mês?**

| mes | pct_brasileira | pct_explicitas | duracao_media_min | valencia_media |
|---|---|---|---|---|
| 2023-11 | 98,1 | 26 | 3,03 | 0,649 |
| 2023-12 | 99,7 | 24 | 3,01 | 0,61 |
| 2024-01 | 99,5 | 21,8 | 3,01 | 0,632 |
| 2024-02 | 98,6 | 23 | 3,09 | 0,659 |
| 2024-03 | 96,3 | 31,4 | 3,18 | 0,651 |
| 2024-04 | 95,5 | 35,3 | 3,29 | 0,655 |
| 2024-05 | 95,7 | 32,2 | 3,13 | 0,644 |
| 2024-06 | 95,6 | 29,7 | 3,09 | 0,621 |
| 2024-07 | 97,8 | 21,9 | 2,93 | 0,631 |
| 2024-08 | 95 | 16,4 | 2,95 | 0,61 |
| 2024-09 | 93,7 | 28,4 | 3,07 | 0,608 |
| 2024-10 | 94 | 25,6 | 3,11 | 0,638 |
| 2024-11 | 93,2 | 26,4 | 3,12 | 0,691 |
| 2024-12 | 96,6 | 20,8 | 3,22 | 0,71 |
| 2025-01 | 97,5 | 21,2 | 3,07 | 0,711 |

## KPI 10 · Ranking

**Em quais países a música brasileira mais toca (exportação)?**

| pais | regiao | pct_musica_brasileira | musicas_brasileiras |
|---|---|---|---|
| Portugal | Europa e Ásia Central | 31,04 | 146 |
| Paraguai | América Latina e Caribe | 2,3 | 9 |
| Cazaquistão | Europa e Ásia Central | 1,86 | 6 |
| Arábia Saudita | Oriente Médio e Norte da África | 1,63 | 11 |
| Luxemburgo | Europa e Ásia Central | 1,41 | 32 |
| Uruguai | América Latina e Caribe | 1,29 | 7 |
| Eslováquia | Europa e Ásia Central | 1,22 | 4 |
| Argentina | América Latina e Caribe | 1,15 | 3 |
| Ucrânia | Europa e Ásia Central | 1,12 | 6 |
| Alemanha | Europa e Ásia Central | 1,01 | 3 |

## KPI 11 · Ranking

**Quais músicas brasileiras mais viajaram (número de países onde entraram no Top 50)?**

| musica | artistas | paises_fora_do_brasil | onde |
|---|---|---|---|
| São Paulo (feat. Anitta) | The Weeknd, Anitta | 33 | AE,AT,AU,BE,BG,CA,CH,CZ,DE,DK,EE,FR,GB,GR,HU,IS,IT,LT,LU,LV,NL,PL,PT,RO,SA,SK,UA,FI,IE,NO,SE,SG,KZ |
| Alibi (with Pabllo Vittar & Yseult) | Sevdaliza, Pabllo Vittar, Yseult | 29 | RO,PT,BG,EE,CH,HU,LT,LV,SG,SK,AT,FR,PL,UA,BY,KZ,LU,MY,PA,DE,BE,CZ,SA,AE,NO,IT,GR,MA,CA |
| BELLAKEO | Peso Pluma, Anitta | 17 | MX,BO,GT,EC,PE,SV,HN,PY,NI,CL,CR,PA,VE,US,PT,CO,RO |
| Alegría | Tiago PZK, Anitta, Emilia | 7 | AR,UY,EE,CO,ES,CL,PY |
| Funk Rave | Anitta | 5 | LV,EE,PA,UY,LU |
| LET'S GET FKD UP | Alok, Mondello'G, CERES, Tribbs | 5 | AT,DE,SK,CZ,CH |
| Automotivo Bibi Fogosa | Bibi Babydoll, Dj Brunin XM, KZA Produções | 4 | BY,KZ,SA,UA |
| Digitando | Gustavo Moura & Rafael | 4 | HK,IS,DO,SA |
| Tengo | Juliette | 4 | PA,LV,PT,LU |
| MONTAGEM - PR FUNK | S3BZS, Mc Gw, Mc Menor Do Alvorada | 3 | KZ,SA,UA |

## KPI 12 · Eficiência

**Quão concentrado é cada mercado? Fatia do chart ocupada pelos 5 maiores artistas**

| pais | renda | pct_top5_artistas | posicao_entre_73 |
|---|---|---|---|
| Coreia do Sul | Alta | 58,2 | 1 |
| Hong Kong | Alta | 47,5 | 2 |
| Hungria | Alta | 47,3 | 3 |
| Colômbia | Média-alta | 43,1 | 4 |
| Japão | Alta | 42,5 | 5 |
| Islândia | Alta | 40,6 | 6 |
| Israel | Alta | 39,2 | 7 |
| Chile | Alta | 37,1 | 8 |
| Paquistão | Média-baixa | 36,7 | 9 |
| Costa Rica | Alta | 36,6 | 10 |
| Índia | Média-baixa | 35,6 | 11 |
| México | Média-alta | 35,5 | 12 |
| República Dominicana | Média-alta | 35,3 | 13 |
| Venezuela | Média-baixa | 35,1 | 14 |
| El Salvador | Média-alta | 34,7 | 15 |
| Marrocos | Média-baixa | 33,7 | 16 |
| Equador | Média-alta | 33,6 | 17 |
| Panamá | Alta | 33,5 | 18 |
| Bolívia | Média-baixa | 32,1 | 19 |
| Turquia | Média-alta | 31,7 | 20 |
| Nigéria | Média-baixa | 31,5 | 21 |
| Grécia | Alta | 31,1 | 22 |
| Peru | Média-alta | 31 | 23 |
| Guatemala | Média-alta | 30,7 | 24 |
| Honduras | Média-baixa | 30,7 | 25 |
| Nicarágua | Média-baixa | 30 | 26 |
| Paraguai | Média-alta | 28,7 | 27 |
| Romênia | Alta | 28,6 | 28 |
| Singapura | Alta | 28,1 | 29 |
| Uruguai | Alta | 28,1 | 30 |
| Cazaquistão | Média-alta | 28 | 31 |
| Tchéquia | Alta | 27,5 | 32 |
| Egito | Média-baixa | 27,4 | 33 |
| Lituânia | Alta | 26,7 | 34 |
| Eslováquia | Alta | 25,9 | 35 |
| Argentina | Média-alta | 25,5 | 36 |
| Vietnã | Média-alta | 25,4 | 37 |
| Estados Unidos | Alta | 25,2 | 38 |
| Austrália | Alta | 24,8 | 39 |
| Canadá | Alta | 23,8 | 40 |
| Itália | Alta | 23,7 | 41 |
| Irlanda | Alta | 23,5 | 42 |
| Bulgária | Alta | 22,6 | 43 |
| Espanha | Alta | 22,2 | 44 |
| Ucrânia | Média-alta | 22,1 | 45 |
| Belarus | Média-alta | 22 | 46 |
| Emirados Árabes | Alta | 21,9 | 47 |
| Arábia Saudita | Alta | 21,9 | 48 |
| Portugal | Alta | 21,8 | 49 |
| Finlândia | Alta | 21,5 | 50 |
| Tailândia | Média-alta | 21,4 | 51 |
| França | Alta | 21 | 52 |
| Taiwan | Alta | 21 | 53 |
| Filipinas | Média-alta | 20,9 | 54 |
| Reino Unido | Alta | 20,8 | 55 |
| Malásia | Média-alta | 20,8 | 56 |
| Indonésia | Média-alta | 20,3 | 57 |
| Global | — | 20,3 | 58 |
| Estônia | Alta | 19,5 | 59 |
| Nova Zelândia | Alta | 19 | 60 |
| Dinamarca | Alta | 18,4 | 61 |
| Suécia | Alta | 17,8 | 62 |
| Polônia | Alta | 16,8 | 63 |
| Brasil | Média-alta | 16,5 | 64 |
| Letônia | Alta | 15,7 | 65 |
| África do Sul | Média-alta | 14,6 | 66 |
| Bélgica | Alta | 14 | 67 |
| Países Baixos | Alta | 13,6 | 68 |
| Alemanha | Alta | 12,8 | 69 |
| Luxemburgo | Alta | 12,5 | 70 |
| Noruega | Alta | 12,2 | 71 |
| Suíça | Alta | 12,1 | 72 |
| Áustria | Alta | 10,2 | 73 |

## KPI 13 · Eficiência

**O Brasil escuta música mais dançante, enérgica e alegre que o resto do mundo?**

| pais | dancabilidade | rank_danca | energia | rank_energia | valencia | rank_valencia |
|---|---|---|---|---|---|---|
| Brasil | 0,678 | 42 | 0,709 | 4 | 0,65 | 4 |
| Média dos 72 países | 0,68 | — | 0,649 | — | 0,55 | — |

## KPI 14 · Integração

**Países mais conectados renovam mais o chart? (Banco Mundial x Spotify)**

| populacao_com_internet | paises | musicas_distintas_por_30_dias | exemplos |
|---|---|---|---|
| 1. 95% ou mais | 17 | 47,8 | AE,AT,AU,CH,DK,ES,GB,HK,IE,IS,KR,LU,MY,NL,NO,SA,SE |
| 2. 85% a 95% | 31 | 42,3 | AR,BE,BY,CA,CL,CR,CZ,DE,DO,EE,FI,FR,GR,HU,IL,IT,JP,KZ,LT,LV,MA,NZ,PL,PT,RO,SG,SK,TH,TR,US,UY |
| 3. 70% a 85% | 14 | 31,3 | BG,BO,BR,CO,EC,EG,MX,PE,PH,PY,UA,VE,VN,ZA |
| 4. menos de 70% | 9 | 28,7 | GT,HN,ID,IN,NG,NI,PA,PK,SV |

## KPI 15 · Sazonalidade

**O Natal invade o chart? % do Top 50 com música natalina de 15 a 25/12/2024**

| pais | pct_natalinas | musicas_natalinas | posicao_entre_73 |
|---|---|---|---|
| Áustria | 53,3 | 37 | 1 |
| Irlanda | 52 | 33 | 2 |
| Reino Unido | 51,8 | 32 | 3 |
| Estados Unidos | 48,9 | 35 | 6 |
| Alemanha | 47,8 | 31 | 7 |
| Global | 37,5 | 31 | 12 |
| Portugal | 20,2 | 30 | 25 |
| México | 0,9 | 5 | 55 |
| Brasil | 0,5 | 3 | 58 |
| Argentina | 0,2 | 1 | 63 |
