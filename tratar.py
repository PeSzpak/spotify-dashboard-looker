"""Limpa e integra o Top 50 diário do Spotify (73 países) com o Banco Mundial e carrega num banco SQLite.

Uso: python3 tratar.py
Entrada: dados/brutos/   Saída: dados/spotify.db (modelo em sql/01_schema.sql)
"""
import json
import sqlite3
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).parent
BRUTOS = RAIZ / "dados" / "brutos"
BANCO = RAIZ / "dados" / "spotify.db"

PAISES_PT = {
    "AE": "Emirados Árabes", "AR": "Argentina", "AT": "Áustria", "AU": "Austrália", "BE": "Bélgica",
    "BG": "Bulgária", "BO": "Bolívia", "BR": "Brasil", "BY": "Belarus", "CA": "Canadá", "CH": "Suíça",
    "CL": "Chile", "CO": "Colômbia", "CR": "Costa Rica", "CZ": "Tchéquia", "DE": "Alemanha",
    "DK": "Dinamarca", "DO": "República Dominicana", "EC": "Equador", "EE": "Estônia", "EG": "Egito",
    "ES": "Espanha", "FI": "Finlândia", "FR": "França", "GB": "Reino Unido", "GR": "Grécia",
    "GT": "Guatemala", "HK": "Hong Kong", "HN": "Honduras", "HU": "Hungria", "ID": "Indonésia",
    "IE": "Irlanda", "IL": "Israel", "IN": "Índia", "IS": "Islândia", "IT": "Itália", "JP": "Japão",
    "KR": "Coreia do Sul", "KZ": "Cazaquistão", "LT": "Lituânia", "LU": "Luxemburgo", "LV": "Letônia",
    "MA": "Marrocos", "MX": "México", "MY": "Malásia", "NG": "Nigéria", "NI": "Nicarágua",
    "NL": "Países Baixos", "NO": "Noruega", "NZ": "Nova Zelândia", "PA": "Panamá", "PE": "Peru",
    "PH": "Filipinas", "PK": "Paquistão", "PL": "Polônia", "PT": "Portugal", "PY": "Paraguai",
    "RO": "Romênia", "SA": "Arábia Saudita", "SE": "Suécia", "SG": "Singapura", "SK": "Eslováquia",
    "SV": "El Salvador", "TH": "Tailândia", "TR": "Turquia", "TW": "Taiwan", "UA": "Ucrânia",
    "US": "Estados Unidos", "UY": "Uruguai", "VE": "Venezuela", "VN": "Vietnã", "ZA": "África do Sul",
}
REGIOES_PT = {
    "East Asia & Pacific": "Ásia e Pacífico", "Europe & Central Asia": "Europa e Ásia Central",
    "Latin America & Caribbean": "América Latina e Caribe", "Middle East & North Africa": "Oriente Médio e Norte da África",
    "Middle East, North Africa, Afghanistan & Pakistan": "Oriente Médio e Norte da África",
    "North America": "América do Norte", "South Asia": "Sul da Ásia", "Sub-Saharan Africa": "África Subsaariana",
}
RENDA_PT = {
    "High income": "Alta", "Upper middle income": "Média-alta",
    "Lower middle income": "Média-baixa", "Low income": "Baixa",
}


def carregar_charts():
    # keep_default_na=False: sem isso o pandas lê "NA" (Namíbia) e "" como nulo
    d = pd.read_csv(BRUTOS / "top_spotify_songs_73_paises.csv", keep_default_na=False, na_values=[""])
    n0 = len(d)
    d["country"] = d["country"].fillna("GLOBAL")  # o chart Global vem sem código de país
    d["data"] = pd.to_datetime(d["snapshot_date"])

    # alguns dias foram coletados duas vezes: duas músicas na mesma posição
    d = d.sort_values(["data", "country", "daily_rank"])
    d = d.drop_duplicates(["data", "country", "spotify_id"])
    d = d.drop_duplicates(["data", "country", "daily_rank"])

    d["name"] = d["name"].fillna("(sem nome)")
    d["artists"] = d["artists"].fillna("(desconhecido)")
    d["album_name"] = d["album_name"].fillna("(sem álbum)")
    d.loc[d["duration_ms"] <= 0, "duration_ms"] = pd.NA
    d.loc[d["popularity"] <= 0, "popularity"] = pd.NA  # 0 = valor não coletado
    d["lancamento"] = pd.to_datetime(d["album_release_date"], errors="coerce")
    d["lista_artistas"] = separar_artistas(d["artists"])
    d["artista_principal"] = d["lista_artistas"].str[0]
    print(f"charts: {n0:,} linhas brutas -> {len(d):,} após remover duplicadas")
    return d


# a base separa artistas por ", ": estes nomes têm vírgula e não podem ser quebrados
NOMES_COM_VIRGULA = ["Tyler, The Creator", "Ryu, the Runner"]

# brasileiros cujo maior público no período está fora do Brasil (revisão manual)
BRASILEIROS_NO_EXTERIOR = {
    "Anitta", "Alok", "Pabllo Vittar", "Brenno & Matheus", "Nilo", "Mc Gw", "Mc Menor Do Alvorada", "Mc Ster",
    "Bibi Babydoll", "Dj Brunin XM", "DJ MAXZZ", "DJ JL3 DA ZN", "DJ CD 011", "DJ Paulinho Mondi Da Baixa Baviera",
    "Mc Vitorioso",
}


def separar_artistas(serie):
    s = serie.copy()
    for nome in NOMES_COM_VIRGULA:
        s = s.str.replace(nome, nome.replace(", ", "\0"), regex=False)
    return s.str.split(", ").apply(lambda xs: [x.replace("\0", ", ").strip() for x in xs])


def origem_dos_artistas(d):
    """Estimativa do país de origem de cada artista, a partir de onde ele acumulou mais dias no Top 50.

    - origem = país com mais dias, se concentrar pelo menos 35% dos dias do artista; senão "INT" (astro global)
    - trap/funk brasileiro passa mais dias no Top 50 de Portugal do que no do Brasil (Veigh, WIU, Teto…):
      quem lidera em Portugal e também entrou no chart brasileiro conta como brasileiro
    - BRASILEIROS_NO_EXTERIOR corrige quem faz mais sucesso fora (Anitta, Alok, funk 'montagem' na Ásia Central)
    """
    a = d[d["country"] != "GLOBAL"][["country", "lista_artistas"]].explode("lista_artistas")
    cont = a.groupby(["lista_artistas", "country"]).size().reset_index(name="dias")
    cont.columns = ["artista", "country", "dias"]
    total = cont.groupby("artista")["dias"].sum()
    top = cont.sort_values("dias", ascending=False).drop_duplicates("artista").set_index("artista")
    origem = top["country"].where(top["dias"] / total.reindex(top.index) >= 0.35, "INT")
    no_brasil = set(cont.loc[cont["country"] == "BR", "artista"])
    origem[(origem == "PT") & origem.index.isin(no_brasil)] = "BR"
    origem[origem.index.isin(BRASILEIROS_NO_EXTERIOR)] = "BR"
    return origem


def banco_mundial():
    meta = json.load(open(BRUTOS / "wb_paises.json"))[1]
    pop = json.load(open(BRUTOS / "wb_pop.json"))[1]
    net = json.load(open(BRUTOS / "wb_net.json"))[1]
    m = pd.DataFrame(
        {"pais_cod": x["iso2Code"], "regiao_en": x["region"]["value"].strip(), "renda_en": x["incomeLevel"]["value"]}
        for x in meta
    )
    p = pd.DataFrame({"iso3": x["countryiso3code"], "pais_cod": x["country"]["id"], "populacao": x["value"]} for x in pop)
    n = pd.DataFrame({"pais_cod": x["country"]["id"], "ano": int(x["date"]), "internet": x["value"]} for x in net)
    n = n.dropna().sort_values("ano").drop_duplicates("pais_cod", keep="last")  # dado mais recente de 2019-2023
    wb = m.merge(p, on="pais_cod", how="left").merge(n[["pais_cod", "internet"]], on="pais_cod", how="left")
    wb["regiao"] = wb["regiao_en"].map(REGIOES_PT)
    wb["renda"] = wb["renda_en"].map(RENDA_PT)
    return wb[["pais_cod", "regiao", "renda", "populacao", "internet"]]


def main():
    d = carregar_charts()
    origem = origem_dos_artistas(d)
    brasileiros = set(origem[origem == "BR"].index)

    paises = pd.DataFrame({"pais_cod": sorted(d["country"].unique())})
    paises["pais"] = paises["pais_cod"].map({**PAISES_PT, "GLOBAL": "Global"})
    paises = paises.merge(banco_mundial(), on="pais_cod", how="left")
    paises.loc[paises["pais_cod"] == "TW", ["regiao", "renda"]] = ["Ásia e Pacífico", "Alta"]  # fora do Banco Mundial
    paises["internet"] = (paises["internet"] / 100).round(4)

    # atributos da faixa são fixos: fica a primeira ocorrência de cada música
    u = d.drop_duplicates("spotify_id")
    musicas = pd.DataFrame({
        "musica_id": u["spotify_id"], "musica": u["name"], "artistas": u["artists"],
        "artista_principal": u["artista_principal"], "album": u["album_name"],
        "data_lancamento": u["lancamento"].dt.strftime("%Y-%m-%d"),
        "explicita": u["is_explicit"].astype(int),
        "colaboracao": (u["lista_artistas"].str.len() > 1).astype(int),
        # música brasileira = pelo menos um artista creditado é brasileiro (pega feats e o funk produzido lá fora)
        "brasileira": u["lista_artistas"].apply(lambda xs: int(any(x in brasileiros for x in xs))),
        "duracao_min": (u["duration_ms"] / 60000).round(2),
        "dancabilidade": u["danceability"], "energia": u["energy"], "valencia": u["valence"],
        "acustica": u["acousticness"], "bpm": u["tempo"].round(1),
    })

    ponte = u[["spotify_id", "lista_artistas"]].explode("lista_artistas")
    ponte["ordem"] = ponte.groupby(level=0).cumcount() + 1
    ponte = ponte.drop_duplicates(["spotify_id", "lista_artistas"])
    artistas = pd.DataFrame({"artista": sorted(ponte["lista_artistas"].unique())})
    artistas["artista_id"] = range(1, len(artistas) + 1)
    artistas["origem_cod"] = artistas["artista"].map(origem).fillna("INT")  # só no chart Global
    ponte = ponte.merge(artistas[["artista", "artista_id"]], left_on="lista_artistas", right_on="artista")
    ponte = ponte.rename(columns={"spotify_id": "musica_id"})[["musica_id", "artista_id", "ordem"]]

    chart = pd.DataFrame({
        "data": d["data"].dt.strftime("%Y-%m-%d"), "pais_cod": d["country"], "posicao": d["daily_rank"],
        "musica_id": d["spotify_id"], "popularidade": d["popularity"],
    })

    BANCO.unlink(missing_ok=True)
    con = sqlite3.connect(BANCO)
    con.executescript((RAIZ / "sql" / "01_schema.sql").read_text())
    for nome, df in [("paises", paises), ("artistas", artistas[["artista_id", "artista", "origem_cod"]]),
                     ("musicas", musicas), ("musica_artista", ponte), ("chart_diario", chart)]:
        df.to_sql(nome, con, if_exists="append", index=False)
        print(f"  {nome:15} {len(df):>9,} linhas")
    con.commit()
    erros = con.execute("PRAGMA foreign_key_check").fetchall()
    assert not erros, f"chaves estrangeiras quebradas: {erros[:5]}"
    con.execute("VACUUM")
    con.close()
    print(f"período: {d['data'].min():%d/%m/%Y} a {d['data'].max():%d/%m/%Y}, {d['data'].nunique()} dias com coleta")
    print(f"banco: {BANCO.relative_to(RAIZ)} ({BANCO.stat().st_size / 1e6:.0f} MB)")


if __name__ == "__main__":
    main()
