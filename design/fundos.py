"""Gera os fundos das 5 páginas do dashboard (estilo Power BI: o layout é uma imagem, os gráficos entram por cima).

Uso: python3 design/fundos.py   ->  design/fundos/pagina_N.png (2520x1440, exibido a 1260x720 no Looker Studio)

LAYOUT é a fonte única das posições: os mesmos retângulos dizem onde encaixar cada gráfico no relatório.
Tudo em pixels do canvas, múltiplos de 20 para casar com a grade de encaixe do Looker Studio.
"""
import subprocess
from html import escape
from pathlib import Path

RAIZ = Path(__file__).parent
SAIDA = RAIZ / "fundos"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
W, H = 1260, 720

FONTE = ("Fonte: Top Spotify Songs in 73 Countries (Kaggle) · Banco Mundial · 18/10/2023 a 17/02/2025 · "
         "SQL e código em github.com/PeSzpak/spotify-dashboard-looker")


def card(x, y, w, h, rotulo, legenda):
    return {"tipo": "card", "x": x, "y": y, "w": w, "h": h, "rotulo": rotulo, "legenda": legenda}


def painel(x, y, w, h, titulo, pergunta):
    return {"tipo": "painel", "x": x, "y": y, "w": w, "h": h, "titulo": titulo, "pergunta": pergunta}


def insight(x, y, w, h, numero, titulo, texto):
    return {"tipo": "insight", "x": x, "y": y, "w": w, "h": h, "numero": numero, "titulo": titulo, "texto": texto}


def linha_de_cards(itens, y=100, h=140):
    """Distribui n cards em 1180px com 20px de espaço (6 cards = 180px, 3 cards = 380px)."""
    n = len(itens)
    w = (1180 - 20 * (n - 1)) // n
    return [card(40 + i * (w + 20), y, w, h, r, l) for i, (r, l) in enumerate(itens)]


LAYOUT = {
    1: {
        "titulo": "O que faz um hit no Brasil?",
        "sub": "Panorama · quanto espaço existe no Top 50 do Spotify Brasil e quanto ele se renova",
        "elementos": linha_de_cards([
            ("MÚSICAS NO TOP 50", "passaram pelo chart"),
            ("ESTREIAS", "músicas novas no período"),
            ("MÚSICA BRASILEIRA", "das posições do Top 50"),
            ("COM FEAT", "das posições têm 2+ artistas"),
            ("PERMANÊNCIA MÉDIA", "dias de uma música no chart"),
            ("ARTISTAS", "creditados, contando feats"),
        ]) + [
            painel(40, 260, 740, 420, "Quantas músicas novas entram no Top 50 por mês?",
                   "Estreias mensais · Brasil x Global · meses completos"),
            painel(800, 260, 420, 420, "Top 10 do último dia", "17/02/2025 · Top 50 Brasil"),
        ],
    },
    2: {
        "titulo": "Quem domina o Top 50 Brasil?",
        "sub": "Rankings de artistas e músicas · há espaço para artista novo?",
        "elementos": linha_de_cards([
            ("TOP 5 ARTISTAS", "da fatia do chart · média mundial 26,7%"),
            ("RANKING DE CONCENTRAÇÃO", "entre 72 países · 1º = mais concentrado"),
            ("ARTISTAS DE UM HIT SÓ", "emplacaram uma única música no período"),
        ]) + [
            painel(40, 260, 740, 420, "Top 10 artistas: dias no Top 50",
                   "Verde = artista principal · azul = participação (feat)"),
            painel(800, 260, 420, 420, "Quem dominou o #1?", "Dias no #1 e no Top 50 por música"),
        ],
    },
    3: {
        "titulo": "A fórmula do hit",
        "sub": "Formato, idade e humor das músicas que chegam e ficam no topo · Brasil x Global",
        "elementos": linha_de_cards([
            ("DURAÇÃO MÉDIA", "minutos por música · Global 3,29"),
            ("EXPLÍCITAS", "das posições do Top 50 Brasil · Global 36,8%"),
            ("LANÇADAS HÁ MAIS DE 1 ANO", "no Top 50 Brasil · Global 24,8%"),
        ]) + [
            painel(40, 260, 580, 420, "Brasil x Global: o formato do sucesso", "% das posições no Top 50"),
            painel(640, 260, 580, 420, "O humor muda com a estação?",
                   "Valência (alegria) média por mês · verão = dez a fev"),
        ],
    },
    4: {
        "titulo": "Brasil no mundo: vale a pena exportar?",
        "sub": "Onde a música brasileira toca fora daqui · Spotify cruzado com o Banco Mundial",
        "elementos": linha_de_cards([
            ("PORTUGAL", "do Top 50 português é música brasileira"),
            ("PAÍSES ALCANÇADOS", "de 71 tiveram música brasileira no Top 50"),
            ("FORA DE PORTUGAL", "maior fatia em qualquer outro país"),
        ]) + [
            painel(40, 260, 580, 420, "Onde a música brasileira toca", "% do Top 50 de cada país · Brasil fora da escala"),
            painel(640, 260, 580, 200, "Músicas brasileiras que mais viajaram", "Países onde entraram no Top 50"),
            painel(640, 480, 580, 200, "Internet x renovação do chart",
                   "% da população com internet (Banco Mundial) x músicas novas a cada 30 dias"),
        ],
    },
    5: {
        "titulo": "Conclusões",
        "sub": "O que os dados dizem para uma gravadora independente decidir onde investir",
        "elementos": [
            insight(40, 100, 380, 160, "96,5%", "O mercado é nosso",
                    "do Top 50 Brasil é música brasileira, e 100% dos dias no #1. Estrangeira entra e sai: "
                    "77% caem em até 7 dias."),
            insight(440, 100, 380, 160, "63º de 72", "Aberto a novatos",
                    "em concentração: os 5 maiores artistas têm só 16,5% do chart (Coreia do Sul: 58%). "
                    "55% dos artistas emplacaram uma única música."),
            insight(840, 100, 380, 160, "62,5%", "Feat é a regra",
                    "das posições têm 2 ou mais artistas (Global: 29%). MC Ryan SP fez 92% dos seus dias "
                    "no chart como participação."),
            insight(40, 280, 380, 160, "136 dias", "Hit tem prazo de validade",
                    "é a idade média de uma música no chart brasileiro (Global: 1.187). Só 2,9% têm mais "
                    "de 1 ano: é preciso lançar sempre."),
            insight(440, 280, 380, 160, "0,5%", "Aqui o Natal não toca",
                    "do Top 50 era natalino em 15-25/12/2024, contra 37,5% no Global. O verão sim: a "
                    "alegria média sobe de 0,61 para 0,71."),
            insight(840, 280, 380, 160, "31%", "Exportar = Portugal + feat",
                    "do Top 50 de Portugal é música brasileira; em nenhum outro país passa de 2,3%. Toda "
                    "música que chegou a 7+ países foi feat com estrangeiro."),
            {"tipo": "recomendacoes", "x": 40, "y": 460, "w": 1180, "h": 220, "itens": [
                ("Apostar em sertanejo e funk", "os gêneros dos 10 artistas que mais ocupam o chart, com um "
                 "lançamento a cada 4 a 6 semanas."),
                ("Lançar com feat", "com artistas daqui para entrar no chart e com estrangeiros para exportar."),
                ("Portugal primeiro", "trap e funk brasileiros já fazem mais sucesso lá do que aqui."),
                ("Calendário de verão", "faixas alegres e dançantes de novembro a janeiro; música de Natal "
                 "não vale o investimento."),
            ]},
        ],
    },
}

CSS = f"""
* {{ box-sizing: border-box; margin: 0; }}
body {{ width: {W}px; height: {H}px; overflow: hidden; font-family: Inter, sans-serif; color: #fff;
       background: radial-gradient(900px 420px at 0% 0%, rgba(29,185,84,.22), transparent 70%),
                   radial-gradient(700px 500px at 100% 100%, rgba(29,185,84,.07), transparent 70%), #0b0b0b; }}
.abs {{ position: absolute; }}
.marca {{ left: 40px; top: 26px; width: 40px; height: 40px; border-radius: 12px; background: #1DB954;
         display: flex; align-items: flex-end; justify-content: center; gap: 4px; padding-bottom: 10px; }}
.marca i {{ display: block; width: 5px; border-radius: 3px; background: #0b0b0b; }}
h1 {{ left: 96px; top: 22px; font: 800 26px Montserrat, sans-serif; letter-spacing: -.01em; }}
.sub {{ left: 96px; top: 58px; font-size: 13px; color: #a7a7a7; }}
.caixa {{ background: rgba(24,24,24,.92); border: 1px solid #2a2a2a; border-radius: 14px; }}
.card::before {{ content: ""; position: absolute; left: 0; top: 18px; width: 3px; height: 16px;
                background: #1DB954; border-radius: 0 3px 3px 0; }}
.rotulo {{ position: absolute; left: 18px; top: 18px; font-size: 11px; font-weight: 700; letter-spacing: .09em;
          color: #b3b3b3; }}
.legenda {{ position: absolute; left: 18px; bottom: 16px; right: 16px; font-size: 12px; color: #8a8a8a; }}
.ptitulo {{ position: absolute; left: 20px; top: 16px; font: 700 15px Montserrat, sans-serif; }}
.ppergunta {{ position: absolute; left: 20px; top: 38px; font-size: 12px; color: #9a9a9a; }}
.num {{ position: absolute; left: 20px; top: 16px; font: 800 30px Montserrat, sans-serif; color: #1DB954; }}
.ititulo {{ position: absolute; left: 20px; top: 56px; font: 700 15px Montserrat, sans-serif; }}
.itexto {{ position: absolute; left: 20px; right: 20px; top: 80px; font-size: 12.5px; line-height: 1.45; color: #c8c8c8; }}
.recs {{ background: linear-gradient(135deg, rgba(29,185,84,.18), rgba(24,24,24,.92) 60%); border-color: rgba(29,185,84,.45); }}
.recs .ptitulo {{ color: #1DB954; font-size: 17px; top: 20px; }}
.recs ol {{ position: absolute; left: 20px; right: 20px; top: 60px; list-style: none; padding: 0;
           display: grid; grid-template-columns: 1fr 1fr; gap: 18px 40px; }}
.recs li {{ display: flex; gap: 14px; font-size: 13.5px; line-height: 1.45; color: #d6d6d6; }}
.recs li b {{ color: #fff; }}
.recs .n {{ flex: 0 0 34px; height: 34px; border-radius: 50%; background: #1DB954; color: #0b0b0b;
           font: 800 16px Montserrat, sans-serif; display: grid; place-items: center; }}
.rodape {{ left: 40px; top: 692px; font-size: 10.5px; color: #6f6f6f; }}
"""


def html_elemento(e):
    pos = f'style="left:{e["x"]}px;top:{e["y"]}px;width:{e["w"]}px;height:{e["h"]}px"'
    if e["tipo"] == "card":
        return (f'<div class="abs caixa card" {pos}><div class="rotulo">{escape(e["rotulo"])}</div>'
                f'<div class="legenda">{escape(e["legenda"])}</div></div>')
    if e["tipo"] == "painel":
        return (f'<div class="abs caixa" {pos}><div class="ptitulo">{escape(e["titulo"])}</div>'
                f'<div class="ppergunta">{escape(e["pergunta"])}</div></div>')
    if e["tipo"] == "insight":
        return (f'<div class="abs caixa card" {pos}><div class="num">{escape(e["numero"])}</div>'
                f'<div class="ititulo">{escape(e["titulo"])}</div><div class="itexto">{escape(e["texto"])}</div></div>')
    itens = "".join(f'<li><span class="n">{i}</span><span><b>{escape(t)}:</b> {escape(d)}</span></li>'
                    for i, (t, d) in enumerate(e["itens"], 1))
    return (f'<div class="abs caixa recs" {pos}><div class="ptitulo">Recomendações para a gravadora</div>'
            f'<ol>{itens}</ol></div>')


def html_pagina(p):
    corpo = "".join(html_elemento(e) for e in p["elementos"])
    barras = "".join(f'<i style="height:{h}px"></i>' for h in (10, 18, 13, 22))
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&family=Montserrat:wght@700;800&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<div class="abs marca">{barras}</div><h1 class="abs">{escape(p["titulo"])}</h1><div class="abs sub">{escape(p["sub"])}</div>
{corpo}<div class="abs rodape">{escape(FONTE)}</div></body></html>"""


def checar_grade():
    """Toda caixa precisa cair na grade de 20px e dentro do canvas, senão os gráficos não encaixam."""
    for n, p in LAYOUT.items():
        for e in p["elementos"]:
            for k in ("x", "y", "w", "h"):
                assert e[k] % 20 == 0, f"página {n}: {e.get('titulo') or e.get('rotulo')} {k}={e[k]} fora da grade"
            assert e["x"] + e["w"] <= W - 40 and e["y"] + e["h"] <= H - 40, f"página {n}: caixa fora da margem"


def main():
    checar_grade()
    SAIDA.mkdir(parents=True, exist_ok=True)
    tmp = SAIDA / "_html"
    tmp.mkdir(exist_ok=True)
    for n, p in LAYOUT.items():
        arq = tmp / f"pagina_{n}.html"
        arq.write_text(html_pagina(p))
        png = SAIDA / f"pagina_{n}.png"
        subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", f"--window-size={W},{H}",
                        "--force-device-scale-factor=2", "--virtual-time-budget=8000",
                        f"--screenshot={png}", arq.as_uri()], check=True, capture_output=True)
        print(f"  página {n} -> {png.relative_to(RAIZ.parent)}")
        for e in p["elementos"]:
            if e["tipo"] in ("card", "painel"):
                print(f"     {e['tipo']:6} x={e['x']:4} y={e['y']:3} w={e['w']:4} h={e['h']:3}  {e.get('titulo') or e.get('rotulo')}")


if __name__ == "__main__":
    main()
