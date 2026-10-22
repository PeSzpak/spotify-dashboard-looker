# O que faz um hit no Brasil? — Dashboard Spotify no Looker Studio

Trabalho de **Banco de Dados II (Faculdade Senac PR)**: um Datathon em que montamos um dashboard com KPIs estratégicos no Looker Studio.

## O problema

Uma **gravadora independente brasileira** vai decidir onde investir em 2025. Ela precisa responder:

1. **Quanto espaço existe** no Top 50 do Spotify Brasil para artistas brasileiros e quanto ele se renova?
2. **Que tipo de música** chega e se mantém no topo (duração, explícita, feat, energia, lançamento recente)?
3. **Quem domina** o mercado hoje, entre artistas e músicas?
4. **Vale a pena exportar?** Em que países a música brasileira já toca, e quão "nacionalista" é cada mercado?

## As bases

| Base | Origem | O que traz |
|---|---|---|
| Top 50 diário do Spotify em 73 países + Global | [Kaggle "Top Spotify Songs in 73 Countries"](https://www.kaggle.com/datasets/asaniczka/top-spotify-songs-in-73-countries-daily-updated), via [espelho no Hugging Face](https://huggingface.co/datasets/VictorHu0602/spotifymusic_73countries) | 1,73 milhão de linhas de 18/10/2023 a 17/02/2025, com posição, música, artistas, álbum, popularidade e atributos de áudio (dançabilidade, energia, valência…) |
| Indicadores de países | [API do Banco Mundial](https://data.worldbank.org/) | região, faixa de renda, população (2023) e % da população com internet |

As duas bases se ligam pelo **código ISO do país** (`BR`, `US`, `PT`…).

## Como reproduzir

```sh
./baixar_dados.sh     # baixa as bases brutas para dados/brutos/
python3 tratar.py     # limpa, integra e gera os CSVs do Looker em dados/looker/
```
