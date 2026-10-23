# O que faz um hit no Brasil? — Dashboard Spotify no Looker Studio

Trabalho de **Banco de Dados II (Faculdade Senac PR)**: um Datathon em que montamos um dashboard com KPIs estratégicos no Looker Studio.

## O problema

Uma **gravadora independente brasileira** vai decidir onde investir em 2025. Ela precisa responder:

1. **Quanto espaço existe** no Top 50 do Spotify Brasil para artistas brasileiros e quanto ele se renova?
2. **Que tipo de música** chega e se mantém no topo (feat, explícita, duração, lançamento recente)?
3. **Quem domina** o mercado hoje, entre artistas e músicas, e se há espaço para novatos.
4. **Vale a pena exportar?** Para onde a música brasileira já viaja?

## As bases

| Base | Origem | O que traz |
|---|---|---|
| Top 50 diário do Spotify em 73 países + Global | [Kaggle "Top Spotify Songs in 73 Countries"](https://www.kaggle.com/datasets/asaniczka/top-spotify-songs-in-73-countries-daily-updated), via [espelho no Hugging Face](https://huggingface.co/datasets/VictorHu0602/spotifymusic_73countries) | 1,73 milhão de linhas de 18/10/2023 a 17/02/2025, com posição, música, artistas, álbum, popularidade e atributos de áudio (dançabilidade, energia, valência…) |
| Indicadores de países | [API do Banco Mundial](https://data.worldbank.org/) | região, faixa de renda, população (2023) e % da população com internet |

As duas bases se ligam pelo **código ISO do país** (`BR`, `US`, `PT`…).

## Pipeline

```
baixar_dados.sh ──► dados/brutos/          CSV de 390 MB + JSON do Banco Mundial
tratar.py       ──► dados/spotify.db       SQLite em modelo estrela (sql/01_schema.sql)
kpis.py         ──► docs/resultados_kpis.md   15 KPIs em SQL (sql/02_kpis.sql)
exportar.py     ──► dados/looker/*.csv     views para o Looker (sql/03_looker.sql)
```

```sh
./baixar_dados.sh && python3 tratar.py && python3 kpis.py && python3 exportar.py
```

Requer Python 3 com pandas. O SQLite já vem com o Python.

### Modelo de dados

```
paises (73) ◄── chart_diario (1,72 mi) ──► musicas (20,5 mil) ◄── musica_artista (33 mil) ──► artistas (10,5 mil)
pais_cod PK     data, pais_cod, posicao PK    musica_id PK          musica_id, artista_id PK      artista_id PK
+ Banco Mundial  musica_id FK, popularidade   atributos de áudio    ordem (1 = principal)         origem_cod
```

### Tratamento (o que a base tinha de errado)

| Problema | Tratamento |
|---|---|
| 3.644 linhas duplicadas: dias coletados duas vezes, com duas músicas na mesma posição | uma linha por (dia, país, posição) |
| Chart Global sem código de país, e o pandas lê "NA" (Namíbia) como nulo | `GLOBAL` explícito e `keep_default_na=False` |
| Popularidade 0 em 8,5 mil linhas e duração 0 | viram nulo (valor não coletado) |
| Feats num texto só ("A, B, C"), com nomes que têm vírgula ("Tyler, The Creator") | tabela ponte música × artista e lista de nomes protegidos |
| 12 dias sem coleta, e out/2023 e fev/2025 parciais | comparações mensais só de nov/2023 a jan/2025 |
| Base não diz a nacionalidade do artista | origem estimada pelo país onde o artista mais acumulou dias no Top 50 (com ≥ 35% dos dias), validada à mão |

A validação da origem mostrou que **rappers e MCs brasileiros como Veigh, WIU, Teto e Marina Sena passam mais dias no Top 50 de Portugal do que no do Brasil**. Por isso há uma regra: quem lidera em Portugal e também entrou no chart brasileiro conta como brasileiro. Anitta, Alok, Pabllo Vittar e o funk "montagem", que viralizou no Cazaquistão e na Arábia Saudita, entram por uma lista revisada à mão (`tratar.py`).

## Os 15 KPIs

Cada KPI é uma consulta em [`sql/02_kpis.sql`](sql/02_kpis.sql), e os resultados completos estão em [`docs/resultados_kpis.md`](docs/resultados_kpis.md).

| # | Tipo | Pergunta de negócio | Resposta | Tela |
|---|---|---|---|---|
| 1 | Volume | Quantas músicas e artistas passaram pelo Top 50 Brasil? | 663 músicas, 460 artistas | 1 |
| 2 | Volume / tempo | Quantas músicas estreiam por mês? | 22 a 67 por mês; pico em abr/2024 | 1 |
| 3 | Eficiência | Quanto do chart é música brasileira? | 96,5% do Top 50, 98,1% do Top 10, 100% do #1 | 1 |
| 4 | Eficiência | Quanto tempo uma música fica no chart? | brasileira 37 dias, estrangeira 9; 77% das estrangeiras saem em 7 dias | 3 |
| 5 | Ranking | Quem mais ocupou o chart? | Ana Castela (7,5% do chart), MC Ryan SP, Simone Mendes | 2 |
| 6 | Ranking | Quais músicas dominaram o #1? | *Let's Go 4* (68 dias), *Barbie* (46), *MTG Quem Não Quer Sou Eu* (33) | 2 |
| 7 | Eficiência | Que formato faz sucesso? | 62,5% com feat (Global 28,8%); 25,6% com menos de 2min30 (Global 12,1%) | 3 |
| 8 | Eficiência | O público quer novidade ou catálogo? | Brasil: 2,9% com mais de 1 ano, idade média de 136 dias; Global: 24,8% e 1.187 dias | 3 |
| 9 | Tempo | A participação brasileira cresce ou cai? | estável entre 93% e 99,7%; vale de nov/2024 e alta no verão | 1 |
| 10 | Ranking | Onde a música brasileira mais toca fora daqui? | Portugal 31%; depois Paraguai 2,3% e Cazaquistão 1,9% | 4 |
| 11 | Ranking | Quais músicas brasileiras mais viajaram? | *São Paulo* (The Weeknd e Anitta) em 33 países; *Alibi* (com Pabllo Vittar) em 29 | 4 |
| 12 | Eficiência | Quão concentrado é cada mercado? | Brasil: top 5 com 16,5%, 63º de 72 (Coreia do Sul 58%) | 2 |
| 13 | Eficiência | O Brasil ouve música mais dançante e alegre? | 4º país mais enérgico e 4º mais alegre; dançabilidade na média | 3 |
| 14 | Integração | Países mais conectados renovam mais o chart? | sim: 47,8 músicas a cada 30 dias com ≥ 95% de internet, contra 28,7 abaixo de 70% | 4 |
| 15 | Sazonalidade | O Natal invade o chart? | 15 a 25/12/2024: 37,5% do Global e 48,9% dos EUA, mas 0,5% do Brasil | 3 |

Os KPIs cobrem **volume** (1, 2), **eficiência** com médias e percentuais (3, 4, 7, 8, 12, 13), **rankings** (5, 6, 10, 11), **evolução temporal** (2, 9, 15) e **integração de bases** (14, com o Banco Mundial).

## Insights

1. **O mercado é brasileiro.** 96,5% do Top 50 e 100% dos dias no #1 ficaram com música brasileira. Estrangeira entra e sai: 77% caem em até 7 dias. Só *Die With A Smile* (Lady Gaga e Bruno Mars) se firmou no Top 10, com 55 dias. Junto com *The Emptiness Machine* (Linkin Park) e *APT.*, ela derrubou a participação brasileira no Top 10 para 88% em out/2024.
2. **E é aberto a novatos.** Os 5 maiores artistas têm só 16,5% do chart, o que deixa o Brasil entre os mercados menos concentrados do mundo (63º de 72). Mais da metade dos artistas (55%) emplacou uma única música.
3. **Feat é a regra.** 62,5% das posições têm 2 ou mais artistas, mais que o dobro do Global. MC Ryan SP fez 92% dos seus dias no chart como participação, e os maiores #1 juntam de 7 a 11 MCs na mesma faixa.
4. **Hit tem prazo de validade.** A idade média de uma música no chart é de 136 dias, contra 1.187 no Global. Só 2,9% têm mais de 1 ano. Quem para de lançar some.
5. **Aqui o Natal não toca, o verão sim.** No Natal de 2024, as natalinas eram 0,5% do chart brasileiro e 37,5% do Global. Já a valência (alegria) sobe de 0,61 em ago–set para 0,71 em dez–jan.
6. **Exportar = Portugal + feat.** Portugal tem 31% de música brasileira no chart, e trap e funk brasileiros fazem mais sucesso lá do que aqui. Em nenhum outro país a fatia passa de 2,3%. Toda música brasileira que chegou a 7 ou mais países foi feat com artista estrangeiro.

### Recomendações para a gravadora

- Apostar em **sertanejo e funk**, os gêneros dos 10 artistas que mais ocupam o chart, com um lançamento a cada 4 a 6 semanas.
- Lançar com **feat**: com artistas daqui para entrar no chart e com estrangeiros para exportar.
- Usar **Portugal** como primeiro mercado externo.
- Guardar as faixas mais alegres e dançantes para **novembro a janeiro**.

## O dashboard

Feito no Looker Studio com os CSVs de `dados/looker/`, em 5 telas: **Panorama**, **Quem domina**, **A fórmula do hit**, **Brasil no mundo** e **Conclusões**.

## Limitações

- **Top 50, não streams.** A base traz a posição, não o número de reproduções. Os KPIs medem *presença no chart* (dias × posições), não audiência.
- **A origem do artista é uma estimativa.** Ela é confiável para separar brasileiro de estrangeiro, porque foi validada à mão nos artistas do chart brasileiro. Não serve para medir "% de música local" em outros países: astros americanos e latinos se espalham por dezenas de charts e caem como "Internacional".
- **Gênero musical não está na base.** A recomendação de sertanejo e funk vem da leitura do ranking de artistas, não de um campo dos dados.
- **Música natalina** é identificada por palavras no título (Christmas, Navidad, Natal, Jingle, Snow…).
- **16 meses de dados.** A sazonalidade (verão, Natal) aparece em dois ciclos só.
