"""Gera os mockups das telas do dashboard com os dados reais do banco (referência para montar no Looker Studio).

Uso: python3 layout/telas.py   ->  layout/html/tela_N.html e docs/telas/tela_N.png
"""
import json
import sqlite3
import subprocess
from pathlib import Path

RAIZ = Path(__file__).parent.parent
BANCO = RAIZ / "dados" / "spotify.db"
HTML = RAIZ / "layout" / "html"
PNG = RAIZ / "docs" / "telas"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
LARGURA, ALTURA = 1280, 960

VERDE, CINZA, AZUL, LARANJA = "#1DB954", "#8C8C8C", "#509BF5", "#F59B23"
MESES_COMPLETOS = "substr(data, 1, 7) BETWEEN '2023-11' AND '2025-01'"
ABAS = ["Panorama", "Quem domina", "A fórmula do hit", "Brasil no mundo", "Conclusões"]

con = sqlite3.connect(BANCO)


def q(sql):
    return con.execute(sql).fetchall()


def um(sql):
    return q(sql)[0][0]


def pct(x, casas=1):
    return f"{100 * x:.{casas}f}%".replace(".", ",")


def num(x):
    return f"{x:,.0f}".replace(",", ".")


def mes_curto(m):
    nomes = "jan fev mar abr mai jun jul ago set out nov dez".split()
    return f"{nomes[int(m[5:7]) - 1]}/{m[2:4]}"


# ---------------------------------------------------------------- componentes

def card(titulo, valor, detalhe="", cor=VERDE):
    return f"""<div class="card kpi"><div class="kt">{titulo}</div>
    <div class="kv" style="color:{cor}">{valor}</div><div class="kd">{detalhe}</div></div>"""


def grafico(id_, titulo, pergunta, area):
    return f"""<div class="card" style="grid-area:{area}"><div class="gt">{titulo}</div>
    <div class="gp">{pergunta}</div><div class="plot" id="{id_}"></div></div>"""


def tabela(titulo, pergunta, cols, linhas, area, barra=None):
    """barra = índice da coluna numérica que ganha uma barra verde proporcional."""
    maxv = max((l[barra] for l in linhas), default=1) if barra is not None else 1
    corpo = ""
    for l in linhas:
        tds = ""
        for i, v in enumerate(l):
            if i == barra:
                tds += (f'<td class="num"><div class="bar"><span style="width:{100 * v / maxv:.0f}%"></span>'
                        f"<b>{num(v)}</b></div></td>")
            elif isinstance(v, (int, float)):
                tds += f'<td class="num">{num(v)}</td>'
            else:
                tds += f"<td>{v}</td>"
        corpo += f"<tr>{tds}</tr>"
    cab = "".join(f"<th>{c}</th>" for c in cols)
    return f"""<div class="card" style="grid-area:{area}"><div class="gt">{titulo}</div><div class="gp">{pergunta}</div>
    <table><thead><tr>{cab}</tr></thead><tbody>{corpo}</tbody></table></div>"""


def filtros(*nomes):
    return "".join(f'<div class="filtro"><span>{n}</span><i>▾</i></div>' for n in nomes)


def pagina(n, titulo, subtitulo, filtros_html, corpo, grid, figs):
    abas = "".join(f'<a class="{"on" if i == n else ""}">{a}</a>' for i, a in enumerate(ABAS, 1))
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Tela {n}</title>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/plotly.js-dist-min@2.35.2/plotly.min.js"></script>
<style>
* {{ box-sizing: border-box; }}
body {{ margin: 0; width: {LARGURA}px; height: {ALTURA}px; background: #121212; color: #fff;
       font-family: Roboto, sans-serif; overflow: hidden; }}
header {{ display: flex; align-items: center; gap: 18px; padding: 18px 28px 0; }}
.logo {{ width: 38px; height: 38px; border-radius: 50%; background: {VERDE}; display: grid; place-items: center; }}
.logo i {{ display: block; width: 18px; height: 3px; background: #121212; border-radius: 3px; margin: 2.5px 0;
          transform: rotate(-8deg); }}
h1 {{ margin: 0; font: 800 24px Montserrat, sans-serif; letter-spacing: -.01em; }}
.sub {{ color: #B3B3B3; font-size: 13px; margin-top: 2px; }}
.filtros {{ margin-left: auto; display: flex; gap: 10px; }}
.filtro {{ display: flex; gap: 22px; align-items: center; background: #242424; border: 1px solid #333;
          border-radius: 20px; padding: 7px 14px; font-size: 12.5px; color: #ddd; }}
.filtro i {{ font-style: normal; color: {VERDE}; }}
nav {{ display: flex; gap: 6px; padding: 14px 28px 0; border-bottom: 1px solid #282828; }}
nav a {{ padding: 8px 14px 10px; font: 600 13px Montserrat, sans-serif; color: #8c8c8c; border-bottom: 3px solid transparent; }}
nav a.on {{ color: #fff; border-color: {VERDE}; }}
main {{ display: grid; gap: 14px; padding: 16px 28px 20px; height: {ALTURA - 132}px; {grid} }}
.card {{ background: #1E1E1E; border-radius: 10px; padding: 14px 16px; min-height: 0; display: flex; flex-direction: column; }}
.kpi {{ justify-content: center; }}
.kt {{ font-size: 12px; color: #B3B3B3; text-transform: uppercase; letter-spacing: .06em; font-weight: 500; }}
.kv {{ font: 800 32px Montserrat, sans-serif; margin: 6px 0 2px; }}
.kd {{ font-size: 12px; color: #8c8c8c; line-height: 1.35; }}
.gt {{ font: 700 15px Montserrat, sans-serif; }}
.gp {{ font-size: 12px; color: #8c8c8c; margin: 3px 0 4px; font-style: italic; }}
.plot {{ flex: 1; min-height: 0; }}
table {{ width: 100%; border-collapse: collapse; font-size: 12.5px; margin-top: 6px; }}
th {{ text-align: left; color: #8c8c8c; font-weight: 500; padding: 6px 6px; border-bottom: 1px solid #333; font-size: 11.5px; }}
td {{ padding: 6.5px 6px; border-bottom: 1px solid #2a2a2a; color: #e6e6e6; }}
td.num {{ text-align: right; font-variant-numeric: tabular-nums; }}
td small {{ color: #8c8c8c; }}
.bar {{ position: relative; height: 20px; min-width: 120px; }}
.bar span {{ position: absolute; left: 0; top: 2px; bottom: 2px; background: {VERDE}55; border-radius: 3px; }}
.bar b {{ position: relative; line-height: 20px; padding-right: 4px; font-weight: 700; }}
.insight {{ border-left: 4px solid {VERDE}; }}
.insight p {{ margin: 6px 0 0; font-size: 13px; line-height: 1.5; color: #ddd; }}
.insight strong {{ color: {VERDE}; }}
</style></head><body>
<header><div class="logo"><div><i></i><i></i><i></i></div></div>
<div><h1>{titulo}</h1><div class="sub">{subtitulo}</div></div><div class="filtros">{filtros_html}</div></header>
<nav>{abas}</nav><main>{corpo}</main>
<script>
const BASE = {{paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)',
  font:{{family:'Roboto', color:'#B3B3B3', size:12}}, margin:{{l:44, r:12, t:8, b:34}},
  xaxis:{{gridcolor:'#2a2a2a', linecolor:'#333', zeroline:false}}, yaxis:{{gridcolor:'#2a2a2a', zeroline:false}},
  legend:{{orientation:'h', y:1.12, x:0, font:{{color:'#ddd'}}}}, hoverlabel:{{bgcolor:'#282828'}}}};
function merge(a, b) {{ for (const k in b) a[k] = (typeof b[k] === 'object' && !Array.isArray(b[k]) && a[k]) ? merge({{...a[k]}}, b[k]) : b[k]; return a; }}
const FIGS = {json.dumps(figs, ensure_ascii=False)};
for (const [id, f] of Object.entries(FIGS))
  Plotly.newPlot(id, f.data, merge(JSON.parse(JSON.stringify(BASE)), f.layout || {{}}), {{displayModeBar:false, staticPlot:true}});
</script></body></html>"""


# ---------------------------------------------------------------- tela 1: panorama

def tela1():
    musicas = um("SELECT COUNT(DISTINCT musica_id) FROM chart_diario WHERE pais_cod='BR'")
    artistas = um("""SELECT COUNT(DISTINCT artista_id) FROM chart_diario JOIN musica_artista USING (musica_id)
                     WHERE pais_cod='BR'""")
    estreias = um("""SELECT COUNT(*) FROM (SELECT musica_id, MIN(data) d FROM chart_diario WHERE pais_cod='BR'
                     GROUP BY 1) WHERE d > (SELECT MIN(data) FROM chart_diario)""")
    pct_br = um("SELECT AVG(brasileira) FROM chart_diario JOIN musicas USING (musica_id) WHERE pais_cod='BR'")
    perman = um("""SELECT AVG(n) FROM (SELECT COUNT(*) n FROM chart_diario WHERE pais_cod='BR' GROUP BY musica_id
                   HAVING MIN(data) > (SELECT MIN(data) FROM chart_diario))""")
    feat = um("SELECT AVG(colaboracao) FROM chart_diario JOIN musicas USING (musica_id) WHERE pais_cod='BR'")

    est = q(f"""WITH e AS (SELECT pais_cod, musica_id, MIN(data) d FROM chart_diario
                           WHERE pais_cod IN ('BR','GLOBAL') GROUP BY 1, 2)
               SELECT substr(d, 1, 7) m, SUM(pais_cod='BR'), SUM(pais_cod='GLOBAL') FROM e
               WHERE substr(d, 1, 7) BETWEEN '2023-11' AND '2025-01' GROUP BY m ORDER BY m""")
    part = q(f"""SELECT substr(data, 1, 7) m, 100 * AVG(brasileira), 100 * AVG(CASE WHEN posicao <= 10 THEN brasileira END)
                FROM chart_diario JOIN musicas USING (musica_id) WHERE pais_cod='BR' AND {MESES_COMPLETOS}
                GROUP BY m ORDER BY m""")
    top = q("""SELECT posicao, musica, artistas FROM chart_diario JOIN musicas USING (musica_id)
               WHERE pais_cod='BR' AND data=(SELECT MAX(data) FROM chart_diario) AND posicao <= 6 ORDER BY posicao""")
    top = [(f"#{p}", f"{m}<br><small>{a if len(a) < 48 else a[:46] + '…'}</small>") for p, m, a in top]

    x = [mes_curto(r[0]) for r in est]
    figs = {
        "g_estreias": {"data": [
            {"type": "bar", "name": "Brasil", "x": x, "y": [r[1] for r in est], "marker": {"color": VERDE}},
            {"type": "bar", "name": "Global", "x": x, "y": [r[2] for r in est], "marker": {"color": CINZA}},
        ], "layout": {"barmode": "group", "bargap": .25}},
        "g_part": {"data": [
            {"type": "scatter", "mode": "lines+markers", "name": "Top 50", "x": x, "y": [r[1] for r in part],
             "line": {"color": VERDE, "width": 3}},
            {"type": "scatter", "mode": "lines", "name": "Top 10", "x": x, "y": [r[2] for r in part],
             "line": {"color": "#fff", "width": 1.5, "dash": "dot"}},
        ], "layout": {"yaxis": {"range": [85, 101], "ticksuffix": "%"}, "annotations": [
            {"x": x.index("out/24"), "y": part[x.index("out/24")][2], "text": "Die With A Smile<br>(Lady Gaga e Bruno Mars)",
             "ax": -90, "ay": 10, "font": {"color": "#fff", "size": 11}, "arrowcolor": "#888", "align": "right"}]}},
    }
    corpo = (
        card("Músicas no Top 50", num(musicas), "passaram pelo chart")
        + card("Artistas", num(artistas), "creditados, contando feats")
        + card("Estreias", num(estreias), f"≈ {estreias / 16:.0f} músicas novas por mês")
        + card("Música brasileira", pct(pct_br), "do Top 50 Brasil, dia a dia")
        + card("Permanência média", f"{perman:.0f} dias".replace(".", ","), "de uma música no Top 50")
        + card("Com feat", pct(feat), "das posições têm 2+ artistas", AZUL)
        + grafico("g_estreias", "Estreias por mês", "Quantas músicas novas entram no Top 50 a cada mês?", "a")
        + grafico("g_part", "Participação da música brasileira", "O espaço do artista nacional cresce ou encolhe?", "b")
        + tabela("Top do último dia", "17/02/2025 · Brasil", ["#", "Música"], top, "c")
    )
    grid = ("grid-template-columns: repeat(6, 1fr); grid-template-rows: 118px 1fr 1fr;"
            "grid-template-areas: '. . . . . .' 'a a a a c c' 'b b b b c c';")
    return pagina(1, "O que faz um hit no Brasil?", "Top 50 diário do Spotify · 18/10/2023 a 17/02/2025",
                  filtros("Período: tudo", "Chart: Brasil", "Origem: todas"), corpo, grid, figs)


# ---------------------------------------------------------------- tela 2: quem domina

def tela2():
    art = q("""SELECT a.artista, SUM(ma.ordem = 1), SUM(ma.ordem > 1), COUNT(DISTINCT c.musica_id)
               FROM chart_diario c JOIN musica_artista ma USING (musica_id) JOIN artistas a USING (artista_id)
               WHERE c.pais_cod='BR' GROUP BY a.artista ORDER BY COUNT(*) DESC LIMIT 10""")[::-1]
    n1 = q("""SELECT musica, artistas, SUM(posicao = 1) d1, COUNT(*) FROM chart_diario JOIN musicas USING (musica_id)
              WHERE pais_cod='BR' GROUP BY musica_id HAVING d1 > 0 ORDER BY d1 DESC LIMIT 8""")
    n1 = [(f"{m}<br><small>{a if len(a) < 44 else a[:42] + '…'}</small>", d50, d1) for m, a, d1, d50 in n1]
    conc = dict(q("""WITH d AS (SELECT c.pais_cod, ma.artista_id, COUNT(*) n FROM chart_diario c
                     JOIN musica_artista ma USING (musica_id) WHERE ma.ordem = 1 GROUP BY 1, 2),
                     r AS (SELECT pais_cod, n, ROW_NUMBER() OVER (PARTITION BY pais_cod ORDER BY n DESC) p,
                           SUM(n) OVER (PARTITION BY pais_cod) t FROM d)
                     SELECT pais_cod, 1.0 * SUM(n) / MAX(t) FROM r WHERE p <= 5 GROUP BY pais_cod"""))
    media = sum(v for k, v in conc.items() if k != "GLOBAL") / (len(conc) - 1)
    ordem = sorted((v for k, v in conc.items() if k != "GLOBAL"), reverse=True)
    pos_br = ordem.index(conc["BR"]) + 1
    um_hit = um("""SELECT AVG(n = 1) FROM (SELECT ma.artista_id, COUNT(DISTINCT musica_id) n FROM chart_diario
                   JOIN musica_artista ma USING (musica_id) WHERE pais_cod='BR' GROUP BY 1)""")

    figs = {"g_art": {"data": [
        {"type": "bar", "orientation": "h", "name": "Principal", "y": [r[0] for r in art],
         "x": [r[1] for r in art], "marker": {"color": VERDE}},
        {"type": "bar", "orientation": "h", "name": "Feat", "y": [r[0] for r in art],
         "x": [r[2] for r in art], "marker": {"color": AZUL}},
    ], "layout": {"barmode": "stack", "margin": {"l": 140}, "xaxis": {"title": {"text": "dias no Top 50"}}}}}
    corpo = (
        card("Concentração", pct(conc["BR"]), f"do chart com os 5 maiores artistas · média mundial {pct(media)}")
        + card("Ranking de concentração", f"{pos_br}º de 72", "um dos mercados MENOS concentrados do mundo", AZUL)
        + card("Artistas de um hit só", pct(um_hit, 0), "emplacaram só 1 música no período", LARANJA)
        + grafico("g_art", "Top 10 artistas no Top 50 Brasil",
                  "Quem mais ocupou o chart? (dias somando todas as músicas)", "a")
        + tabela("Quem dominou o #1", "Quais músicas ficaram mais dias no topo?",
                 ["Música", "Dias no Top 50", "Dias no #1"], n1, "b", barra=2)
    )
    grid = ("grid-template-columns: repeat(3, 1fr); grid-template-rows: 118px 1fr;"
            "grid-template-areas: '. . .' 'a a b';")
    return pagina(2, "Quem domina o Top 50 Brasil", "Rankings de artistas e músicas · feats contam para todos os artistas",
                  filtros("Período: tudo", "Origem do artista: todas", "Papel: todos"), corpo, grid, figs)


# ---------------------------------------------------------------- tela 3: a fórmula do hit

def tela3():
    formato = {r[0]: r[1:] for r in q("""
        SELECT pais_cod, 100 * AVG(colaboracao), 100 * AVG(explicita), 100 * AVG(duracao_min < 2.5),
               100 * AVG(julianday(data) - julianday(data_lancamento) <= 30),
               100 * AVG(julianday(data) - julianday(data_lancamento) > 365), AVG(duracao_min)
        FROM chart_diario JOIN musicas USING (musica_id) WHERE pais_cod IN ('BR','GLOBAL') GROUP BY 1""")}
    rotulos = ["Com feat", "Explícitas", "Menos de 2min30", "Lançadas há ≤ 30 dias", "Lançadas há > 1 ano"]
    perm = {r[0]: r[1:] for r in q("""
        WITH p AS (SELECT musica_id, COUNT(*) n, MIN(posicao) mp FROM chart_diario WHERE pais_cod='BR'
                   GROUP BY 1 HAVING MIN(data) > (SELECT MIN(data) FROM chart_diario))
        SELECT brasileira, AVG(n), 100 * AVG(n <= 7), 100 * AVG(mp <= 10), COUNT(*)
        FROM p JOIN musicas USING (musica_id) GROUP BY 1""")}
    val = q(f"""SELECT substr(data, 1, 7) m, AVG(CASE WHEN pais_cod='BR' THEN valencia END),
                       AVG(CASE WHEN pais_cod='GLOBAL' THEN valencia END)
                FROM chart_diario JOIN musicas USING (musica_id) WHERE pais_cod IN ('BR','GLOBAL') AND {MESES_COMPLETOS}
                GROUP BY m ORDER BY m""")
    x = [mes_curto(r[0]) for r in val]
    figs = {
        "g_formato": {"data": [
            {"type": "bar", "name": "Brasil", "x": rotulos, "y": formato["BR"][:5], "marker": {"color": VERDE},
             "text": [f"{v:.0f}%" for v in formato["BR"][:5]], "textposition": "outside"},
            {"type": "bar", "name": "Global", "x": rotulos, "y": formato["GLOBAL"][:5], "marker": {"color": CINZA},
             "text": [f"{v:.0f}%" for v in formato["GLOBAL"][:5]], "textposition": "outside"},
        ], "layout": {"barmode": "group", "yaxis": {"ticksuffix": "%", "range": [0, 75]}}},
        "g_perm": {"data": [
            {"type": "bar", "orientation": "h", "y": ["Estrangeira", "Brasileira"], "x": [perm[0][0], perm[1][0]],
             "marker": {"color": [CINZA, VERDE]}, "text": [f"{perm[0][0]:.0f} dias", f"{perm[1][0]:.0f} dias"],
             "textposition": "outside"},
        ], "layout": {"margin": {"l": 92}, "xaxis": {"range": [0, 48]}, "yaxis": {"ticksuffix": "  "}, "showlegend": False}},
        "g_val": {"data": [
            {"type": "scatter", "mode": "lines+markers", "name": "Brasil", "x": x, "y": [r[1] for r in val],
             "line": {"color": VERDE, "width": 3}},
            {"type": "scatter", "mode": "lines+markers", "name": "Global", "x": x, "y": [r[2] for r in val],
             "line": {"color": CINZA, "width": 2}},
        ], "layout": {"yaxis": {"range": [0.4, 0.75]}, "shapes": [
            {"type": "rect", "xref": "x", "yref": "paper", "x0": 0.5, "x1": 3.5, "y0": 0, "y1": 1,
             "fillcolor": LARANJA, "opacity": .08, "line": {"width": 0}},
            {"type": "rect", "xref": "x", "yref": "paper", "x0": 12.5, "x1": 14.5, "y0": 0, "y1": 1,
             "fillcolor": LARANJA, "opacity": .08, "line": {"width": 0}}], "annotations": [
            {"x": 1, "y": val[1][2], "text": "Natal: canções natalinas<br>tomam o Global", "ax": 60, "ay": 78, "bgcolor": "#1E1E1E",
             "font": {"color": "#ddd", "size": 11}, "arrowcolor": "#888"}]}},
    }
    dur = formato["BR"][5]
    corpo = (
        card("Duração média no Brasil", f"{int(dur)}:{round(dur % 1 * 60):02d}", f"Global: {int(formato['GLOBAL'][5])}:{round(formato['GLOBAL'][5] % 1 * 60):02d} min")
        + card("Estrangeiras que caem em 1 semana", pct(perm[0][1] / 100, 0), f"brasileiras: {pct(perm[1][1] / 100, 0)}", CINZA)
        + card("Chegam ao Top 10", pct(perm[1][2] / 100, 0), f"das brasileiras que entram · estrangeiras: {pct(perm[0][2] / 100, 0)}")
        + grafico("g_formato", "Brasil x Global: o formato do sucesso",
                  "Feat, explícita, duração e idade: o que o Top 50 de cada um tem?", "a")
        + grafico("g_perm", "Permanência média no Top 50 Brasil", "Quanto tempo uma música dura no chart?", "b")
        + grafico("g_val", "Valência (alegria) média por mês",
                  "O humor do chart muda com a estação? Faixas laranja = verão no Brasil (dez a fev)", "c")
    )
    grid = ("grid-template-columns: repeat(3, 1fr); grid-template-rows: 118px 1fr 1fr;"
            "grid-template-areas: '. . .' 'a a b' 'c c c';")
    return pagina(3, "A fórmula do hit", "Formato, idade e humor das músicas · Brasil x Global",
                  filtros("Período: tudo", "Chart: Brasil e Global", "Faixa: Top 50"), corpo, grid, figs)


# ---------------------------------------------------------------- tela 4: Brasil no mundo

def iso3():
    meta = json.load(open(RAIZ / "dados" / "brutos" / "wb_paises.json"))[1]
    return {**{x["iso2Code"]: x["id"] for x in meta}, "TW": "TWN"}


def tela4():
    paises = q("""SELECT c.pais_cod, p.pais, 100 * AVG(m.brasileira), p.internet,
                         COUNT(DISTINCT c.musica_id) * 30.0 / COUNT(DISTINCT c.data), p.populacao
                  FROM chart_diario c JOIN musicas m USING (musica_id) JOIN paises p USING (pais_cod)
                  WHERE c.pais_cod <> 'GLOBAL' GROUP BY c.pais_cod""")
    m3 = iso3()
    fora = [r for r in paises if r[0] != "BR"]
    viajaram = q("""SELECT musica, artistas, COUNT(DISTINCT pais_cod) n FROM chart_diario JOIN musicas USING (musica_id)
                    WHERE brasileira = 1 AND pais_cod NOT IN ('BR','GLOBAL') GROUP BY musica, artistas
                    ORDER BY n DESC LIMIT 7""")
    viajaram = [(f"{m}<br><small>{a}</small>", n) for m, a, n in viajaram]
    n_paises = um("""SELECT COUNT(DISTINCT pais_cod) FROM chart_diario JOIN musicas USING (musica_id)
                     WHERE brasileira = 1 AND pais_cod NOT IN ('BR','GLOBAL')""")
    pt = next(r for r in paises if r[0] == "PT")
    com_net = [r for r in paises if r[3] is not None]
    figs = {
        "g_mapa": {"data": [{
            "type": "choropleth", "locations": [m3[r[0]] for r in fora], "z": [min(r[2], 5) for r in fora],
            "text": [f"{r[1]}: {r[2]:.1f}%" for r in fora], "hoverinfo": "text", "zmin": 0, "zmax": 5,
            "colorscale": [[0, "#2a2a2a"], [0.2, "#1a5c33"], [1, VERDE]], "marker": {"line": {"color": "#121212", "width": .4}},
            "colorbar": {"ticksuffix": "%", "len": .8, "thickness": 10, "tickvals": [0, 1, 2, 3, 4, 5],
                         "ticktext": ["0%", "1%", "2%", "3%", "4%", "5%+"], "tickfont": {"color": "#B3B3B3"}},
        }], "layout": {"margin": {"l": 0, "r": 0, "t": 0, "b": 0}, "geo": {
            "bgcolor": "rgba(0,0,0,0)", "showframe": False, "showcoastlines": False, "projection": {"type": "natural earth"},
            "showland": True, "landcolor": "#1a1a1a", "showcountries": True, "countrycolor": "#121212",
            "lataxis": {"range": [-58, 82]}}}},
        "g_net": {"data": [
            {"type": "scatter", "mode": "markers", "name": "Países", "x": [100 * r[3] for r in com_net if r[0] != "BR"],
             "y": [r[4] for r in com_net if r[0] != "BR"], "text": [r[1] for r in com_net if r[0] != "BR"],
             "marker": {"color": CINZA, "size": 8, "opacity": .75}},
            {"type": "scatter", "mode": "markers+text", "name": "Brasil", "x": [100 * r[3] for r in com_net if r[0] == "BR"],
             "y": [r[4] for r in com_net if r[0] == "BR"], "text": ["Brasil"], "textposition": "top center",
             "textfont": {"color": VERDE}, "marker": {"color": VERDE, "size": 13}},
        ], "layout": {"showlegend": False, "xaxis": {"title": {"text": "% da população com internet (Banco Mundial)"},
                                                     "ticksuffix": "%"},
                      "yaxis": {"title": {"text": "músicas distintas / 30 dias"}}, "margin": {"l": 50, "b": 44}}},
    }
    corpo = (
        card("Países com música brasileira", f"{n_paises} de 71", "no Top 50 em algum dia do período")
        + card("Portugal", pct(pt[2] / 100), "do Top 50 português é música brasileira", VERDE)
        + card("Fora de Portugal", "≤ 2,3%", "em nenhum outro país passa disso", LARANJA)
        + grafico("g_mapa", "Onde a música brasileira toca",
                  "% do Top 50 de cada país ocupado por música brasileira (Portugal = 31%, escala cortada em 5%)", "a")
        + tabela("Músicas brasileiras que mais viajaram", "Em quantos países entraram no Top 50?",
                 ["Música", "Países"], viajaram, "b", barra=1)
        + grafico("g_net", "Internet x renovação do chart",
                  "Países mais conectados trocam mais de música? (Spotify + Banco Mundial)", "c")
    )
    grid = ("grid-template-columns: repeat(3, 1fr); grid-template-rows: 118px 1fr 1fr;"
            "grid-template-areas: '. . .' 'a a b' 'c c b';")
    return pagina(4, "Brasil no mundo", "Exportação da música brasileira e comparação entre 72 países",
                  filtros("Região: todas", "Renda: todas", "Mês: tudo"), corpo, grid, figs)


# ---------------------------------------------------------------- tela 5: conclusões

def tela5():
    itens = [
        ("96,5%", "O mercado é nosso", "do Top 50 Brasil é música brasileira, e <strong>100%</strong> dos dias no #1. "
         "Estrangeira entra e sai: <strong>77%</strong> caem em até 7 dias."),
        ("63º de 72", "E é aberto a novatos", "em concentração: os 5 maiores artistas têm só <strong>16,5%</strong> do chart "
         "(Coreia do Sul: 58%). <strong>55%</strong> dos artistas emplacaram uma única música."),
        ("62,5%", "Feat é a regra", "das posições têm 2+ artistas (Global: 29%). MC Ryan SP fez <strong>92%</strong> "
         "dos seus dias no chart como participação."),
        ("136 dias", "Hit tem prazo de validade", "é a idade média de uma música no chart brasileiro (Global: 1.187). "
         "Só <strong>2,9%</strong> têm mais de 1 ano: é preciso lançar sempre."),
        ("0,5%", "Aqui o Natal não toca", "do Top 50 Brasil eram músicas natalinas em 15-25/12/2024, contra "
         "<strong>37,5%</strong> no Global e 49% nos EUA. O verão sim: a alegria sobe de <strong>0,61 para 0,71</strong>."),
        ("31%", "Exportar = Portugal + feat", "do Top 50 de Portugal é música brasileira; em nenhum outro país passa de "
         "<strong>2,3%</strong>. Toda música que chegou a 7+ países foi <strong>feat com estrangeiro</strong>."),
    ]
    recs = [
        "Apostar em <strong>sertanejo e funk</strong>, os gêneros dos 10 artistas que mais ocupam o chart, "
        "com um lançamento a cada 4 a 6 semanas.",
        "Lançar com <strong>feat</strong>: com artistas daqui para entrar no chart e com estrangeiros para exportar.",
        "Usar <strong>Portugal</strong> como primeiro mercado externo. Trap e funk já fazem mais sucesso lá do que aqui.",
        "Guardar as faixas mais alegres e dançantes para <strong>novembro a janeiro</strong>. Não vale investir em música de Natal.",
    ]
    cards = "".join(f'''<div class="card insight"><div class="big">{n}</div><div class="gt">{t}</div><p>{p}</p></div>'''
                    for n, t, p in itens)
    lis = "".join(f"<li>{r}</li>" for r in recs)
    corpo = cards + f"""<div class="card" style="grid-column: 1 / -1; background:#1DB95418; border:1px solid #1DB95455">
      <div class="gt" style="color:{VERDE}; font-size:17px">Recomendações para a gravadora</div>
      <ol style="margin:8px 0 0; padding-left:22px; font-size:15px; line-height:1.8; color:#eee">{lis}</ol></div>
      <style>.big {{ font: 800 40px Montserrat, sans-serif; color: {VERDE}; margin-bottom: 4px; }}
      .insight {{ justify-content: center; padding: 18px 22px; }} .insight .gt {{ font-size: 17px; }} .insight p {{ font-size: 14px; }}</style>"""
    grid = "grid-template-columns: repeat(3, 1fr); grid-template-rows: 1fr 1fr auto;"
    return pagina(5, "Conclusões", "O que os dados dizem para a gravadora", "", corpo, grid, {})


def main():
    HTML.mkdir(parents=True, exist_ok=True)
    PNG.mkdir(parents=True, exist_ok=True)
    for i, tela in enumerate([tela1, tela2, tela3, tela4, tela5], 1):
        arq = HTML / f"tela_{i}.html"
        arq.write_text(tela())
        png = PNG / f"tela_{i}.png"
        subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", f"--window-size={LARGURA},{ALTURA}",
                        "--virtual-time-budget=20000", f"--screenshot={png}", arq.as_uri()],
                       check=True, capture_output=True)
        print(f"  tela {i} -> {png.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
