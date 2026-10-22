#!/bin/sh
# Baixa as bases brutas para dados/brutos/ (não versionadas: o CSV do Spotify tem ~390 MB)
set -e
cd "$(dirname "$0")"
mkdir -p dados/brutos
B=dados/brutos

# 1. Top 50 diário do Spotify em 73 países + Global (out/2023 a fev/2025)
#    Espelho no Hugging Face do dataset "Top Spotify Songs in 73 Countries (Daily Updated)" do Kaggle
curl -L -o $B/top_spotify_songs_73_paises.csv \
  https://huggingface.co/datasets/VictorHu0602/spotifymusic_73countries/resolve/main/Top_spotify_songs.csv

# 2. Banco Mundial: metadados dos países, população (2023) e % da população com internet
curl -s -o $B/wb_paises.json "https://api.worldbank.org/v2/country?format=json&per_page=400"
curl -s -o $B/wb_pop.json "https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?format=json&date=2023&per_page=400"
curl -s -o $B/wb_net.json "https://api.worldbank.org/v2/country/all/indicator/IT.NET.USER.ZS?format=json&date=2019:2023&per_page=2000"
