# -*- coding: utf-8 -*-
"""Ajudantes das aulas (caixas de terminal, missões, exercícios). Usado por tools/gerar.py."""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODO = "paginas"  # o gerar.py troca
BLOCOS = {}   # id -> lista de comandos (ordem de registro)
ORDEM = []

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def registra(bid, cmds):
    if bid in BLOCOS:
        if BLOCOS[bid] != list(cmds):
            raise SystemExit("bloco repetido com comandos diferentes: " + bid)
        return
    BLOCOS[bid] = list(cmds); ORDEM.append(bid)

def coleta(bid):
    f = ROOT / "_saidas-anon" / (bid + ".json")
    if not f.exists():
        raise SystemExit("falta a coleta de " + bid + " (rode bash tools/coleta.sh)")
    d = json.loads(f.read_text(encoding="utf-8"))
    if [x["cmd"] for x in d] != BLOCOS[bid]:
        raise SystemExit("coleta desatualizada para " + bid + " (rode bash tools/coleta.sh " + bid + ")")
    return d

def saida_txt(o):
    return o[:-1] if o.endswith("\n") else o

PROIBIDO_INICIO = re.compile(r"^(\$|#>)( |$)|^[A-Z]:\\|^PS ")

def confere_linhas(bid, linhas):
    for k, l in enumerate(linhas):
        if "/tmp/" in l or "guia-texto-terminal" in l:
            raise SystemExit("saída de %s mostra caminho da máquina de coleta: %r" % (bid, l))
        if PROIBIDO_INICIO.search(l) or "«" in l:
            raise SystemExit("saída de %s tem linha que o desenhista do terminal confundiria: %r" % (bid, l))
        if k == 0 and re.match(r"^> ?", l):
            raise SystemExit("saída de %s começa com '>' (seria lida como continuação): %r" % (bid, l))

def T(bid, *cmds, notas=None, titulo=None, status=None):
    """Caixa de terminal com comandos e saídas reais. notas = {trecho_da_linha: etiqueta}."""
    registra(bid, cmds)
    if MODO != "paginas":
        return ""
    d = coleta(bid)
    notas = dict(notas or {})
    linhas = []
    for x in d:
        linhas.append("$ " + x["cmd"])
        out = saida_txt(x["out"])
        if out != "":
            ols = out.split("\n")
            confere_linhas(bid, ols)
            for l in ols:
                for trecho in list(notas):
                    if trecho in l:
                        l = l + "   « " + notas.pop(trecho)
                        break
                linhas.append(l)
    if notas:
        raise SystemExit("nota sem linha em %s: %r" % (bid, list(notas)))
    linhas.append("$")
    tit = ' data-title="%s"' % esc(titulo) if titulo else ""
    return '<pre class="term" data-cwd="~/guia-texto-teste"%s>%s</pre>' % (tit, esc("\n".join(linhas)))

def saida_de(bid):
    d = coleta(bid)
    return "\n".join(saida_txt(x["out"]) for x in d if saida_txt(x["out"]) != "")

def M(bid, tarefa, cmds, goal, script=""):
    """Missão 'cole a saída'. goal: metas separadas por ;; (src:, out:, outre:, erro:, semerro)."""
    if isinstance(cmds, str):
        cmds = [cmds]
    registra(bid, cmds)
    if MODO != "paginas":
        return ""
    saida = saida_de(bid)
    # pré-conferência: as metas out/erro/outre têm de bater com a saída real
    for meta in goal.split(";;"):
        tipo, _, val = meta.partition(":")
        if tipo in ("out", "erro") and val not in saida:
            raise SystemExit("missão %s: a saída real não tem %r\n---\n%s" % (bid, val, saida))
        if tipo == "outre" and ("\\A" in val or "\\Z" in val):
            raise SystemExit("missão %s: \\A e \\Z não existem na regex do JavaScript" % bid)
        if tipo == "outre" and not re.search(val, saida, re.M):
            raise SystemExit("missão %s: a saída real não casa com %r" % (bid, val))
        if tipo == "src" and not re.search(val, "\n".join(cmds), re.M):
            raise SystemExit("missão %s: a solução não cumpre src %r" % (bid, val))
    if not re.search(r"(^|;;)(out|outre|erro):", goal):
        raise SystemExit("missão %s precisa de meta out/outre/erro" % bid)
    if saida.strip() == "":
        raise SystemExit("missão %s sem saída real" % bid)
    sol = "\n".join(cmds)
    return "\n".join([
        '<div class="trycmd" data-goal="%s">' % esc(goal),
        '<p class="try-task"><strong>Missão:</strong> %s</p>' % tarefa,
        '<pre class="script" data-file="comandos.sh">\n%s\n</pre>' % esc(script),
        '<pre class="solucao" data-file="comandos.sh">\n%s\n</pre>' % esc(sol),
        '<pre class="saida-ok" data-file="comandos.sh" hidden>\n%s\n</pre>' % esc(saida),
        "</div>"])

def ANAT(*pares):
    return '<dl class="anatomy">' + "".join("<dt>%s</dt><dd>%s</dd>" % (esc(a), b) for a, b in pares) + "</dl>"

def REF(linhas, cab=("Você digita", "O que faz")):
    h = '<div class="table-wrap"><table class="ref">\n<tr><th>%s</th><th>%s</th></tr>\n' % cab
    for a, b in linhas:
        h += "<tr><td><code>%s</code></td><td>%s</td></tr>\n" % (esc(a), b)
    return h + "</table></div>"

def EX(n, titulo, texto, antes, resposta, depois="", rotulo="resposta"):
    resp = "|".join(r.replace("|", "\\|") for r in ([resposta] if isinstance(resposta, str) else resposta))
    return ('<div class="exercise"><h3>%d. %s</h3><p>%s</p><div class="ex-code">%s<input data-answer="%s" aria-label="%s">%s</div></div>'
            % (n, titulo, texto, esc(antes), esc(resp), esc(rotulo), esc(depois)))

_mc = [0]
def MC(n, pergunta, opcoes, certa):
    _mc[0] += 1
    nome = "q%d" % n
    h = '<div class="mc" data-answer="%d"><p class="mc-q">%d. %s</p>\n' % (certa, n, pergunta)
    h += "\n".join('<label><input type="radio" name="%s"> %s</label>' % (nome, o) for o in opcoes)
    return h + "</div>"

def caixa(cls, titulo, corpo):
    return '<div class="%s"><strong>%s</strong>\n%s</div>' % (cls, titulo, corpo)

def CEN(titulo, texto, term, depois=""):
    return '<div class="cenario"><strong>%s</strong>\n<p>%s</p>\n%s\n%s</div>' % (titulo, texto, term, ("<p>%s</p>" % depois) if depois else "")

PASTA = ('<p class="pasta-teste">Todas as saídas desta aula foram colhidas de verdade num Linux (Debian 13, com GNU Bash 5.2, '
         'GNU sed 4.9, GNU awk 5.2 e jq 1.7) em português (<code>pt_BR.UTF-8</code>), dentro da pasta de teste '
         '<code>~/guia-texto-teste</code> com os <a href="preparando.html">arquivos de exemplo</a>. Antes de cada caixa a pasta foi '
         'recriada do zero, então um comando que altera arquivo numa caixa não afeta a seguinte.</p>')

HEAD = '''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="assets/style.css">
<script>try{{var t=localStorage.getItem("tema");if(t)document.documentElement.setAttribute("data-theme",t)}}catch(e){{}}</script>
</head>
<body>
<div class="layout">
<nav class="sidebar" id="sidebar" aria-label="Tópicos"></nav>
<main class="main">
<div class="content">

<div class="pager"></div>

'''
FOOT = '''

<div class="pager"></div>

</div>
</main>
</div>
<script src="assets/site.js"></script>
</body>
</html>
'''

def pagina_aula(a):
    corpo = []
    corpo.append("<h1>%s</h1>" % a["h1"])
    corpo.append('<p class="intro">%s</p>' % a["intro"])
    corpo.append('<div class="note"><strong>Você vai aprender</strong><ul>\n%s\n</ul></div>' % "\n".join("<li>%s</li>" % x for x in a["aprender"]))
    if a.get("pasta", True):
        corpo.append(PASTA)
    corpo.append("<hr>")
    corpo.append(a["corpo"]())
    if a.get("ref"):
        corpo.append("<hr>\n<h2>Referência rápida</h2>\n" + REF(a["ref"]))
    corpo.append("<hr>\n<h2>Exercícios</h2>\n" + a["exercicios"]())
    corpo.append("<hr>\n<h2>Missões</h2>\n<p>Rode na sua pasta <code>~/guia-texto-teste</code> (com os arquivos de exemplo originais) e cole o que o terminal respondeu. O botão <strong>Conferir</strong> compara com o que a saída real precisa ter.</p>\n" + a["missoes"]())
    corpo.append("<hr>\n<h2>Resumo</h2>\n<ul>\n%s\n</ul>" % "\n".join("<li>%s</li>" % x for x in a["resumo"]))
    return HEAD.format(title=esc(a["title"] + " | Guia Texto no Terminal"), desc=esc(a["desc"])) + "\n\n".join(corpo) + FOOT

