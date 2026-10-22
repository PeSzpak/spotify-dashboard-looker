"""Cria as views de sql/03_looker.sql e exporta cada uma para dados/looker/<nome>.csv (upload no Looker Studio).

Uso: python3 exportar.py
"""
import csv
import sqlite3
from pathlib import Path

RAIZ = Path(__file__).parent
BANCO = RAIZ / "dados" / "spotify.db"
SAIDA = RAIZ / "dados" / "looker"


def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(BANCO)
    con.executescript((RAIZ / "sql" / "03_looker.sql").read_text())
    views = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type = 'view' AND name LIKE 'looker_%'")]
    for v in views:
        cur = con.execute(f"SELECT * FROM {v}")
        arq = SAIDA / f"{v.removeprefix('looker_')}.csv"
        with open(arq, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(c[0] for c in cur.description)
            n = 0
            for linha in cur:
                w.writerow(linha)
                n += 1
        print(f"  {arq.name:20} {n:>7,} linhas  {arq.stat().st_size / 1e6:5.1f} MB")


if __name__ == "__main__":
    main()
