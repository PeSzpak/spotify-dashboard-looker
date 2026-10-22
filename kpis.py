"""Roda as consultas de sql/02_kpis.sql no banco e grava os resultados em docs/resultados_kpis.md.

Uso: python3 kpis.py
"""
import re
import sqlite3
from pathlib import Path

RAIZ = Path(__file__).parent
BANCO = RAIZ / "dados" / "spotify.db"
SAIDA = RAIZ / "docs" / "resultados_kpis.md"


def blocos(sql):
    """Separa o arquivo em (número, tipo, pergunta, consulta) pelos marcadores '-- @kpi N | tipo | pergunta'."""
    partes = re.split(r"^-- @kpi ", sql, flags=re.M)[1:]
    for p in partes:
        cabecalho, corpo = p.split("\n", 1)
        num, tipo, pergunta = (x.strip() for x in cabecalho.split("|"))
        yield num, tipo, pergunta, corpo.strip()


def tabela_md(cols, linhas):
    def fmt(v):
        if v is None:
            return "—"
        if isinstance(v, float):
            return f"{v:,.3f}".rstrip("0").rstrip(".").replace(",", "X").replace(".", ",").replace("X", ".")
        if isinstance(v, int):
            return f"{v:,}".replace(",", ".")
        return str(v).replace("|", "/")
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    out += ["| " + " | ".join(fmt(v) for v in linha) + " |" for linha in linhas]
    return "\n".join(out)


def main():
    con = sqlite3.connect(BANCO)
    md = ["# Resultados dos KPIs", "", "Gerado por `python3 kpis.py` a partir de `sql/02_kpis.sql`.", ""]
    for num, tipo, pergunta, consulta in blocos((RAIZ / "sql" / "02_kpis.sql").read_text()):
        cur = con.execute(consulta)
        cols = [c[0] for c in cur.description]
        linhas = cur.fetchall()
        md += [f"## KPI {num} · {tipo}", "", f"**{pergunta}**", "", tabela_md(cols, linhas), ""]
        print(f"KPI {num:>2} ok ({len(linhas)} linhas) — {pergunta}")
    SAIDA.parent.mkdir(exist_ok=True)
    SAIDA.write_text("\n".join(md))
    print(f"-> {SAIDA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
