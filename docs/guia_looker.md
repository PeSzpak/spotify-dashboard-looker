# Guia de montagem no Looker Studio

Passo a passo para reproduzir no Looker Studio as 5 telas de `docs/telas/`. Os números citados servem para conferir se cada gráfico ficou certo, e todos saem do período completo (18/10/2023 a 17/02/2025).

## 1. Fontes de dados

Em **Criar → Fonte de dados → Upload de arquivo**, envie cada CSV de `dados/looker/` como uma fonte separada:

| Fonte | Arquivo | Grão (uma linha =) | Telas |
|---|---|---|---|
| `charts` | charts.csv | música × dia no Top 50 Brasil ou Global | 1, 3 |
| `artistas` | artistas.csv | artista × dia no Top 50 Brasil (feat conta para todos) | 2 |
| `artistas_resumo` | artistas_resumo.csv | artista do Top 50 Brasil | 2 |
| `musicas` | musicas.csv | música que passou pelo Top 50 Brasil | 1, 2, 3 |
| `paises` | paises.csv | país (72) com dados do Banco Mundial | 2, 4 |
| `exportacao` | exportacao.csv | música brasileira × país × mês fora do Brasil | 4 |

Na tela de campos de cada fonte, ajuste:

- `data`: tipo **Data (AAAAMMDD)**.
- `pais_cod`: tipo **Geográfico → País**.
- `internet` e todos os `pct_*`: tipo **Percentual**.
- `brasileira`, `explicita`, `feat`, `estreia`, `lancamento_recente`, `no_top10`, `um_hit_so` e `ja_estava_no_inicio`: agregação **Média**. Assim a média vira um percentual. A exceção é `estreia`, que deve usar **Soma**.

## 2. Tema e página

- **Arquivo → Configurações do relatório**: tamanho da tela personalizado **1280 × 960**.
- **Tema e layout → Personalizar**:

| Elemento | Valor |
|---|---|
| Fundo da página | `#121212` |
| Fundo dos componentes | `#1E1E1E`, borda arredondada 10 px, sem borda |
| Texto | `#FFFFFF` (principal), `#B3B3B3` (secundário) |
| Cor de destaque / série 1 | `#1DB954` (verde Spotify: **Brasil**) |
| Série 2 | `#8C8C8C` (cinza: **Global / estrangeira**) |
| Série 3 | `#509BF5` (azul: **feat / participação**) |
| Alerta | `#F59B23` (laranja) |
| Fonte dos títulos | Montserrat (negrito) |
| Fonte do corpo | Roboto |

- Em **Página → Gerenciar páginas**, crie as 5 páginas: *Panorama*, *Quem domina*, *A fórmula do hit*, *Brasil no mundo* e *Conclusões*.
- Em **Tema e layout → Layout**, ligue a **navegação por abas no topo**.
- No topo de cada página, coloque uma caixa de texto com o título (Montserrat 24) e o subtítulo (Roboto 13, `#B3B3B3`).

## 3. Campos calculados

Crie em **Recurso → Gerenciar fontes de dados → Editar → Adicionar um campo**.

**Fonte `charts`**

| Campo | Fórmula | Formato |
|---|---|---|
| Músicas distintas | `COUNT_DISTINCT(musica_id)` | Número |
| Estreias | `SUM(estreia)` | Número |
| % música brasileira | `AVG(brasileira)` | Percentual |
| % brasileira no Top 10 | `SUM(CASE WHEN posicao <= 10 THEN brasileira ELSE 0 END) / SUM(CASE WHEN posicao <= 10 THEN 1 ELSE 0 END)` | Percentual |
| % com feat | `AVG(feat)` | Percentual |
| % explícitas | `AVG(explicita)` | Percentual |
| % menos de 2min30 | `AVG(CASE WHEN duracao_min < 2.5 THEN 1 ELSE 0 END)` | Percentual |
| % lançadas há ≤ 30 dias | `AVG(lancamento_recente)` | Percentual |
| % lançadas há > 1 ano | `AVG(CASE WHEN idade_dias > 365 THEN 1 ELSE 0 END)` | Percentual |
| Duração média (min) | `AVG(duracao_min)` | Número, 2 casas |
| Valência média | `AVG(valencia)` | Número, 2 casas |

**Fonte `musicas`**

| Campo | Fórmula |
|---|---|
| Permanência média (dias) | `AVG(dias_top50)` |
| % caem em até 7 dias | `AVG(CASE WHEN dias_top50 <= 7 THEN 1 ELSE 0 END)` |
| % chegam ao Top 10 | `AVG(CASE WHEN melhor_posicao <= 10 THEN 1 ELSE 0 END)` |

**Fonte `paises`**

| Campo | Fórmula |
|---|---|
| % brasileira (escala até 5%) | `CASE WHEN pct_musica_brasileira > 0.05 THEN 0.05 ELSE pct_musica_brasileira END` |

**Fonte `artistas`**: renomeie a métrica *Contagem de registros* para **Dias no chart**.

## 4. Filtros reutilizáveis

Crie em **Recurso → Gerenciar filtros**:

| Filtro | Fonte | Condição |
|---|---|---|
| Só Brasil | charts | Incluir `chart` = Brasil |
| Meses completos | charts | Excluir `mes` em (2023-10, 2025-02) *(meses com coleta parcial)* |
| Permanência completa | musicas | Incluir `ja_estava_no_inicio` = 0 *(quem já estava no chart no 1º dia tem a permanência cortada)* |
| Último dia | charts | Incluir `data` = 20250217 |

---

## Tela 1 · Panorama

> Pergunta: *quanto espaço existe no Top 50 Brasil e quanto ele se renova?*

**Controles (topo):**
- **Controle de período** sobre `data`.
- **Lista suspensa** de `origem_musica`.

**Linha de 6 scorecards** (filtro *Só Brasil*; os números conferem com o período completo):

| Card | Fonte | Métrica | Confere |
|---|---|---|---|
| Músicas no Top 50 | charts | Músicas distintas | 663 |
| Artistas | artistas | `COUNT_DISTINCT(artista)` | 460 |
| Estreias | charts | Estreias | 613 |
| Música brasileira | charts | % música brasileira | 96,5% |
| Permanência média | musicas (filtro *Permanência completa*) | Permanência média (dias) | 32,6 |
| Com feat | charts | % com feat (azul) | 62,5% |

**Gráficos:**

1. **Estreias por mês**: gráfico de colunas.
   - Fonte `charts`, filtro *Meses completos*.
   - Dimensão `mes`, detalhamento `chart`, métrica *Estreias*.
   - Cores: Brasil verde, Global cinza.
2. **Participação da música brasileira**: gráfico de linhas.
   - Fonte `charts`, filtros *Só Brasil* e *Meses completos*.
   - Dimensão `mes`, métricas *% música brasileira* (verde, 3 px) e *% brasileira no Top 10* (branco, pontilhada).
   - Eixo Y de 85% a 100%.
   - Adicione uma caixa de texto sobre out/24: *"Die With A Smile (Lady Gaga e Bruno Mars)"*.
3. **Top do último dia**: tabela.
   - Fonte `charts`, filtros *Só Brasil* e *Último dia*.
   - Dimensões `posicao`, `musica` e `artistas`.
   - Ordenar por `posicao` crescente, 6 linhas.

Agrupe os scorecards (selecione e use **Organizar → Agrupar**) para que o controle de período filtre todos de uma vez.

## Tela 2 · Quem domina

> Pergunta: *quem são os donos do chart? Há espaço para artista novo?*

**Controles:**
- **Controle de período** sobre `data` (fonte `artistas`).
- **Listas suspensas** de `origem_artista` e `papel`.

**Scorecards:**

| Card | Fonte | Configuração | Confere |
|---|---|---|---|
| Concentração | paises | `pct_top5_artistas`, filtro `pais_cod` = BR | 16,5% |
| Média mundial (texto do card) | paises | `AVG(pct_top5_artistas)` | 26,7% |
| Ranking de concentração | paises | `ranking_concentracao`, filtro `pais_cod` = BR | 63 (de 72) |
| Artistas de um hit só | artistas_resumo | `AVG(um_hit_so)` | 55% |

**Gráficos:**

1. **Top 10 artistas**: gráfico de barras horizontais **empilhadas**.
   - Fonte `artistas`.
   - Dimensão `artista`, detalhamento `papel`, métrica *Dias no chart*.
   - Ordenar por *Dias no chart* decrescente, 10 barras.
   - Cores: Principal verde, Participação azul.
   - Confere: Ana Castela 1.783 e MC Ryan SP 1.277, sendo 92% como feat.
2. **Quem dominou o #1**: tabela com barras.
   - Fonte `musicas`.
   - Dimensões `musica` e `artistas`, métricas `dias_top50` e `dias_no_1` (exibir como **barra**, verde).
   - Filtro `dias_no_1` > 0, ordenar por `dias_no_1` decrescente, 8 linhas.
   - Confere: *Let's Go 4* tem 68 dias no #1.

## Tela 3 · A fórmula do hit

> Pergunta: *que tipo de música chega e fica no topo?*

**Controles:**
- **Controle de período** (fonte `charts`).
- **Lista suspensa** de `faixa`: #1, Top 2-10, Top 11-50.

**Scorecards:**

| Card | Fonte | Configuração | Confere |
|---|---|---|---|
| Duração média no Brasil | charts | *Duração média (min)*, filtro *Só Brasil* | 3,09 min ≈ 3:05 |
| Estrangeiras que caem em 1 semana | musicas | *% caem em até 7 dias*, filtros *Permanência completa* e `origem_musica` = Estrangeira | 77% |
| Chegam ao Top 10 | musicas | *% chegam ao Top 10*, filtros *Permanência completa* e `origem_musica` = Brasileira | 35% |

**Gráficos:**

1. **Brasil × Global: o formato do sucesso**: gráfico de colunas agrupadas.
   - Fonte `charts`, dimensão `chart`.
   - Métricas *% com feat*, *% explícitas*, *% menos de 2min30*, *% lançadas há ≤ 30 dias* e *% lançadas há > 1 ano*.
   - Mostre os rótulos de dados.
   - No Looker, os grupos ficam por chart (Brasil | Global) e as cores por métrica. Para um visual igual ao do mockup, use um gráfico por métrica, lado a lado.
   - Confere: feat 62,5% × 28,8%; mais de 1 ano 2,9% × 24,8%.
2. **Permanência média**: barras horizontais.
   - Fonte `musicas`, filtro *Permanência completa*.
   - Dimensão `origem_musica`, métrica *Permanência média (dias)*.
   - Confere: brasileira 36,9 e estrangeira 8,8.
3. **Valência por mês**: gráfico de linhas.
   - Fonte `charts`, filtro *Meses completos*.
   - Dimensão `mes`, detalhamento `chart`, métrica *Valência média*.
   - Eixo Y de 0,4 a 0,75.
   - Adicione retângulos laranja translúcidos (10%) sobre dez–fev (verão) e uma caixa de texto em dez/23: *"Natal: canções natalinas tomam o Global"*.

## Tela 4 · Brasil no mundo

> Pergunta: *vale a pena exportar? Para onde?*

**Controles:** **Listas suspensas** de `regiao` e `renda` (fonte `paises`) e de `mes` (fonte `exportacao`).

**Scorecards:**

| Card | Fonte | Configuração | Confere |
|---|---|---|---|
| Países com música brasileira | exportacao | `COUNT_DISTINCT(pais_cod)` | 58 (de 71) |
| Portugal | paises | `pct_musica_brasileira`, filtro `pais_cod` = PT | 31,0% |
| Fora de Portugal | paises | `MAX(pct_musica_brasileira)`, filtro excluir `pais_cod` em (BR, PT) | 2,3% |

**Gráficos:**

1. **Onde a música brasileira toca**: mapa geográfico (*Geo chart*).
   - Fonte `paises`, dimensão `pais_cod`, métrica *% brasileira (escala até 5%)*.
   - Cores: mínimo `#2A2A2A`, máximo `#1DB954`. Sem escala cortada, Portugal deixa o resto do mapa sem diferença de cor.
2. **Músicas brasileiras que mais viajaram**: tabela com barras.
   - Fonte `exportacao`.
   - Dimensões `musica` e `artistas`, métrica `COUNT_DISTINCT(pais_cod)` renomeada para *Países* (exibir como barra).
   - Ordenar decrescente, 7 linhas.
   - Confere: *São Paulo* (The Weeknd e Anitta) chegou a 33 países.
3. **Internet × renovação do chart**: gráfico de dispersão (*bolhas*).
   - Fonte `paises`, dimensão `pais`.
   - X = `internet`, Y = `musicas_por_30_dias`, tamanho = `populacao`.
   - Destaque o Brasil com uma caixa de texto ou um filtro de cor.

## Tela 5 · Conclusões

Use 6 caixas de texto no estilo "cartão", com fundo `#1E1E1E` e borda esquerda verde de 4 px. Cada uma tem um número grande (Montserrat 40, verde), um título e duas linhas de explicação, como em `docs/telas/tela_5.png`. Embaixo, um retângulo `#1DB95418` traz as 4 recomendações. Os textos estão no README, na seção **Insights**.
