#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera o Guia Texto no Terminal a partir das aulas em tools/aulas_*.py.

  python3 tools/gerar.py comandos   -> escreve tools/comandos.txt (o que a coleta roda)
                                       e arquivos/criar-arquivos.sh
  bash tools/coleta.sh              -> roda tudo de verdade e grava _saidas-anon/
  python3 tools/gerar.py paginas    -> escreve as páginas .html e o NIVEIS do site.js
                                       usando SÓ as saídas de _saidas-anon/

Nenhuma saída é escrita à mão: toda caixa de terminal e toda pre.saida-ok
vem do JSON da coleta. Se faltar coleta, o gerador para com erro.
"""
import json, re, sys, html as _html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODO = sys.argv[1] if len(sys.argv) > 1 else "paginas"
sys.path.insert(0, str(ROOT / "tools"))
import lib_guia as L

def carregar():
    sys.path.insert(0, str(ROOT / "tools"))
    import aulas_n1, aulas_n2, aulas_n3, aulas_n4, aulas_n5
    niveis = []
    for mod in (aulas_n1, aulas_n2, aulas_n3, aulas_n4, aulas_n5):
        if mod.NIVEL["grupos"]:
            niveis.append(mod.NIVEL)
    return niveis

def gerar_criar_arquivos():
    linhas = ["#!/usr/bin/env bash",
              "# criar-arquivos.sh — cria os arquivos de exemplo do Guia Texto no Terminal",
              "# na pasta atual. Uso: mkdir -p ~/guia-texto-teste && cd ~/guia-texto-teste && bash criar-arquivos.sh",
              "# Rode de novo sempre que quiser voltar os arquivos ao original.",
              "set -e"]
    for f in sorted((ROOT / "arquivos").iterdir()):
        if f.name == "criar-arquivos.sh":
            continue
        t = f.read_text(encoding="utf-8")
        assert "FIM_DO_ARQUIVO" not in t
        linhas.append("cat > %s <<'FIM_DO_ARQUIVO'\n%sFIM_DO_ARQUIVO" % (f.name, t))
    linhas.append('echo "Arquivos de exemplo criados em $(pwd)"')
    (ROOT / "arquivos" / "criar-arquivos.sh").write_text("\n".join(linhas) + "\n", encoding="utf-8")

def main():
    L.MODO = MODO
    niveis = carregar()
    todas = [a for n in niveis for g in n["grupos"] for a in g["aulas"]]
    slugs = [a["slug"] for a in todas]
    assert len(slugs) == len(set(slugs)), "slug repetido"
    if MODO == "comandos":
        import index_pagina
        index_pagina.gerar(niveis, MODO)
        for a in todas:
            a["corpo"](); a["exercicios"](); a["missoes"]()
        txt = "".join("### %s\n%s\n\n" % (b, "\n".join(L.BLOCOS[b])) for b in L.ORDEM)
        (ROOT / "tools" / "comandos.txt").write_text(
            "# Gerado por tools/gerar.py comandos. Cada '### id' é uma caixa; cada linha, um comando.\n\n" + txt, encoding="utf-8")
        gerar_criar_arquivos()
        print("comandos: %d caixas, %d comandos" % (len(L.ORDEM), sum(len(L.BLOCOS[b]) for b in L.ORDEM)))
        return
    # NIVEIS no site.js
    js = []
    for n in niveis:
        gs = []
        for g in n["grupos"]:
            itens = ",\n".join('      [%s, %s]' % (json.dumps(a["slug"] + ".html"), json.dumps(a["menu"], ensure_ascii=False)) for a in g["aulas"])
            if g is n["grupos"][0] and n["id"] == "n1":
                itens = '      ["index.html", "Início"],\n' + itens
            gs.append('    { grupo: %s, itens: [\n%s\n    ]}' % (json.dumps(g["grupo"], ensure_ascii=False), itens))
        js.append('  { id: "%s", nome: %s, curto: %s, desc: %s, grupos: [\n%s\n  ]}' % (
            n["id"], json.dumps(n["nome"], ensure_ascii=False), json.dumps(n["curto"], ensure_ascii=False),
            json.dumps(n["desc"], ensure_ascii=False), ",\n".join(gs)))
    bloco = "var NIVEIS = [\n" + ",\n".join(js) + "\n];\n/* fim-NIVEIS */"
    p = ROOT / "assets" / "site.js"
    s = p.read_text(encoding="utf-8")
    s = re.sub(r"var NIVEIS = \[.*?/\* fim-NIVEIS \*/", lambda m: bloco, s, count=1, flags=re.S)
    p.write_text(s, encoding="utf-8")
    nmiss = 0
    for a in todas:
        h = L.pagina_aula(a)
        nmiss += h.count('class="trycmd"')
        (ROOT / (a["slug"] + ".html")).write_text(h, encoding="utf-8")
    import index_pagina
    index_pagina.gerar(niveis, MODO)
    print("páginas: %d aulas + index, %d missões" % (len(todas), nmiss))

if __name__ == "__main__":
    main()
