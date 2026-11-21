# -*- coding: utf-8 -*-
"""Nível 3 · awk, a planilha de linha de comando."""
from lib_guia import *

def aula(**k):
    return k

GAWK = '<div class="note"><strong>gawk</strong><p>As saídas desta aula são do GNU awk 5.2 (<code>gawk</code>), que o comando <code>awk</code> chama depois de <code>sudo apt install gawk</code>.</p></div>'

# ---------------------------------------------------------------- intro
def intro_corpo():
    return f"""
<h2>A ideia: padrão e ação</h2>
<p>O <code>awk</code> também lê o texto linha a linha, como o <code>sed</code>. A diferença é que ele já <strong>corta cada linha em campos</strong> (colunas) e deixa você fazer contas e decisões com eles. Um programa awk é uma lista de pares <code>padrão {{ ação }}</code>: para cada linha que casa com o padrão, a ação roda.</p>
{T("awki-basico", "awk '{print $1}' notas.txt")}
{ANAT(("awk", "o programa."), ("'{print $1}'", "o programa awk, entre aspas simples. Sem padrão, a ação vale em todas as linhas."), ("$1", "o primeiro campo da linha."), ("notas.txt", "o arquivo."))}
<hr>
<h2>1. A linha inteira: <code>$0</code></h2>
<p><code>$0</code> é a linha toda. <code>print</code> sozinho também imprime a linha toda, e o awk vira um <code>cat</code>:</p>
{T("awki-0", "awk '{print $0}' nomes.txt | head -3", "awk '{print}' frutas.txt | head -2")}
<hr>
<h2>2. Só o padrão</h2>
<p>Sem ação, o awk imprime as linhas que casam com o padrão, como o <code>grep</code>. O padrão pode ser uma regex entre barras:</p>
{T("awki-padrao", "awk '/ERRO/' log.txt")}
<hr>
<h2>3. Padrão e ação juntos</h2>
<p>Agora o poder de verdade: só nas linhas de ERRO, mostrar a hora (campo 2) e o último pedaço da mensagem:</p>
{T("awki-juntos", "awk '/ERRO/ {print $2, $NF}' log.txt")}
<p><code>$NF</code> é o último campo; a próxima aula explica por quê.</p>
{GAWK}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Chave sem fechar", "O gawk mostra a linha do programa e aponta com <code>^</code> onde se perdeu:", T("awki-erro", "awk '{print $1' notas.txt"))}
{CEN("Aspas duplas", "Com aspas duplas, o Bash troca <code>$1</code> pelo primeiro argumento do shell (vazio) antes de o awk ver. O <code>print</code> sem argumento imprime a linha inteira, e não a coluna 1:", T("awki-erro2", "awk \"{print $1}\" notas.txt | head -2"), "Use sempre aspas simples em volta do programa awk.")}
"""

def intro_ex():
    return (EX(1, "Primeira coluna", "Complete para imprimir a 1ª coluna:", "awk '{print ", "$1", "}' notas.txt", rotulo="campo") +
            EX(2, "A linha inteira", "Qual variável é a linha inteira?", "awk '{print ", "$0", "}' notas.txt", rotulo="variável") +
            MC(3, "Um programa awk é feito de pares:", ["comando e opção", "padrão { ação }", "endereço e flag", "entrada e saída"], 2) +
            MC(4, "<code>awk '/ERRO/' log.txt</code> faz o mesmo que:", ["<code>grep ERRO log.txt</code>", "<code>sed 's/ERRO//' log.txt</code>", "<code>wc -l log.txt</code>", "<code>cut -f ERRO</code>"], 1))

def intro_miss():
    return (M("awki-m1", "mostre só os nomes (1ª coluna) de <code>notas.txt</code> com o <code>awk</code>.", "awk '{print $1}' notas.txt", r"src:\bawk\b;;src:\$1;;outre:^Ana$;;outre:^Eduarda$") +
            M("awki-m2", "mostre a hora (2ª coluna) das linhas de <code>log.txt</code> com <code>AVISO</code>.", "awk '/AVISO/ {print $2}' log.txt", r"src:\bawk\b;;src:/AVISO/;;outre:^09:01:37$;;outre:^11:02:15$"))

# ---------------------------------------------------------------- campos
def campos_corpo():
    return f"""
<h2>A ideia: cada linha é uma fileira da planilha</h2>
<p>O awk corta cada linha em <strong>campos</strong>. Por padrão, o separador é “espaços e tabulações”, e vários espaços seguidos contam como um só (diferente do <code>cut</code>). Os campos se chamam <code>$1</code>, <code>$2</code>, <code>$3</code>…; <code>NF</code> (<em>number of fields</em>) é quantos campos a linha tem, e <code>$NF</code> é o último.</p>
<hr>
<h2>1. Campos separados por espaços</h2>
<p>No <code>log.txt</code>, “INFO” tem dois espaços depois, “AVISO” tem um. Para o awk, tanto faz: o nível é sempre o <code>$3</code>:</p>
{T("campos-espacos", "awk '{print $3}' log.txt | head -4", "awk '{print $1, $3}' notas.txt")}
<hr>
<h2>2. O último e o penúltimo: <code>$NF</code> e <code>$(NF-1)</code></h2>
{T("campos-nf", "awk '{print NF, $NF}' texto.txt", "awk '{print $(NF-1)}' acesso.log | head -3")}
{ANAT(("NF", "o número de campos da linha."), ("$NF", "o campo de número NF: o último."), ("$(NF-1)", "o penúltimo (o status HTTP, no acesso.log)."))}
<hr>
<h2>3. Outro separador: <code>-F</code></h2>
<p>Para CSV, diga que o separador é a vírgula com <code>-F,</code>. Para o <code>contatos.txt</code>, ponto e vírgula:</p>
{T("campos-F", "awk -F, '{print $2, $3}' vendas.csv | head -3", "awk -F';' '{print $1}' contatos.txt")}
<hr>
<h2>4. Separador com regex</h2>
<p>O <code>-F</code> aceita uma regex. Com <code>[;@]</code>, tanto o ponto e vírgula quanto a arroba separam campos, e o domínio do e-mail vira o último campo:</p>
{T("campos-regex", "awk -F'[;@]' '{print $1, $NF}' contatos.txt")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Campo negativo", "Os campos começam em <code>$1</code> (e <code>$0</code> é a linha). Um número negativo é erro fatal:", T("campos-erro", "awk '{print $(NF-5)}' notas.txt"))}
{CEN("Esqueceu o -F", "Sem <code>-F,</code>, o CSV inteiro (que não tem espaços) é um campo só, e <code>$2</code> sai vazio:", T("campos-erro2", "awk '{print $2}' vendas.csv | head -3"))}
"""

def campos_ex():
    return (EX(1, "O último", "Complete para imprimir o último campo:", "awk '{print ", "$NF", "}' texto.txt", rotulo="campo") +
            EX(2, "Separador", "Complete para usar a vírgula como separador:", "awk ", "-F,", " '{print $3}' vendas.csv", rotulo="opção") +
            MC(3, "Com o separador padrão, três espaços seguidos contam como:", ["três separadores", "um separador só", "um campo vazio", "erro"], 2) +
            MC(4, "Em <code>notas.txt</code>, o que <code>$NF</code> mostra na linha da Ana?", ["Ana", "8.5", "7.5", "4"], 3))

def campos_miss():
    return (M("campos-m1", "mostre o vendedor e o produto (2ª e 3ª colunas) de <code>vendas.csv</code>.", "awk -F, '{print $2, $3}' vendas.csv", r"src:-F;;src:\$2;;src:\$3;;outre:^Diego caneta$;;outre:^vendedor produto$") +
            M("campos-m2", "mostre o último campo de cada linha de <code>log.txt</code>.", "awk '{print $NF}' log.txt", r"src:\$NF;;outre:^pedido=1042$;;outre:^usuario=carla$;;outre:^cheio$"))

# ---------------------------------------------------------------- printf
def printf_corpo():
    return f"""
<h2>A ideia: controlar a saída</h2>
<p>O <code>print</code> é rápido: imprime o que você passar e pula linha. O <code>printf</code> é preciso: você escreve um molde (<em>formato</em>) com lacunas e diz o que vai em cada uma, com largura e casas decimais. É assim que se faz relatório alinhado.</p>
<hr>
<h2>1. <code>print</code>: vírgula ou não</h2>
<p>Com vírgula entre os itens, o <code>print</code> põe um espaço (o <code>OFS</code>, da aula de variáveis). Sem vírgula, emenda tudo. Texto vai entre aspas duplas:</p>
{T("printf-print", "awk '{print $1, $2}' notas.txt | head -2", "awk '{print $1 $2}' notas.txt | head -2", "awk '{print \"Aluno:\", $1, \"- nota 1:\", $2}' notas.txt | head -2")}
<hr>
<h2>2. <code>printf</code>: o molde</h2>
<p>As lacunas mais usadas: <code>%s</code> texto, <code>%d</code> número inteiro, <code>%f</code> número com casas (<code>%.2f</code> = 2 casas). O <code>printf</code> não pula linha sozinho: o <code>\\n</code> no fim faz isso.</p>
{T("printf-molde", "awk '{printf \"%s tirou %.1f na prova 3\\n\", $1, $4}' notas.txt")}
{ANAT(("printf", "imprime com molde."), ('"%s tirou %.1f na prova 3\\n"', "o molde: texto + lacunas + quebra de linha."), ("$1", "vai na lacuna %s."), ("$4", "vai na lacuna %.1f (1 casa decimal)."))}
<hr>
<h2>3. Largura e alinhamento</h2>
<p>Um número entre o <code>%</code> e a letra é a largura. Negativo alinha à esquerda; positivo, à direita. Uma tabela bonitinha:</p>
{T("printf-largura", "awk -F, 'NR > 1 {printf \"%-8s %-8s %3d x %6.2f\\n\", $2, $3, $4, $5}' vendas.csv | head -5")}
<hr>
<h2>4. <code>%d</code> corta, <code>%.0f</code> arredonda</h2>
{T("printf-int", "awk 'BEGIN {printf \"%d %.0f %.2f %5.1f|\\n\", 7.8, 7.8, 7.8, 7.8}'")}
<p>O <code>BEGIN</code> roda antes de ler qualquer linha (aula de BEGIN e END); aqui serve para testar sem arquivo.</p>
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Lacunas demais", "Mais lacunas que valores é erro fatal no gawk:", T("printf-erro", "awk '{printf \"%s %s %s\\n\", $1}' notas.txt"))}
{CEN("Esqueceu o \\n", "Sem <code>\\n</code>, tudo sai grudado numa linha só. No terminal, até o prompt seguinte aparece colado no fim dessa linha:", T("printf-erro2", "awk '{printf \"%s \", $1}' notas.txt"))}
"""

def printf_ex():
    return (EX(1, "Duas casas", "Complete a lacuna para 2 casas decimais:", 'awk \'{printf "', "%.2f", '\\n", $2}\' notas.txt', rotulo="lacuna") +
            EX(2, "Texto", "Qual lacuna é para texto?", 'awk \'{printf "', "%s", '\\n", $1}\' notas.txt', rotulo="lacuna") +
            MC(3, "O que <code>%-8s</code> faz?", ["8 casas decimais", "texto com largura 8, alinhado à esquerda", "8 espaços antes", "corta o texto em 8 letras"], 2) +
            MC(4, "Por que a saída do <code>printf</code> às vezes sai grudada?", ["Porque ele não pula linha sem o \\n", "Porque falta a vírgula", "Porque o arquivo é CSV", "Porque precisa de -F"], 1))

def printf_miss():
    return (M("printf-m1", "com <code>printf</code>, mostre cada aluno de <code>notas.txt</code> no formato <code>Ana: 8.50</code> (nota 1 com 2 casas).", "awk '{printf \"%s: %.2f\\n\", $1, $2}' notas.txt", r"src:printf;;src:%\.2f;;outre:^Ana: 8\.50$;;outre:^Diego: 4\.00$") +
            M("printf-m2", "mostre o produto e o preço de <code>vendas.csv</code> (sem o cabeçalho) no formato <code>caderno R$ 12.50</code>.", "awk -F, 'NR > 1 {printf \"%s R$ %.2f\\n\", $3, $5}' vendas.csv", r"src:printf;;src:-F;;outre:^mochila R\$ 89\.90$;;outre:^caneta R\$ 2\.00$"))

# ---------------------------------------------------------------- padrões
def padroes_corpo():
    return f"""
<h2>A ideia: filtrar pelo conteúdo das colunas</h2>
<p>O <code>grep</code> filtra pela linha inteira. O awk filtra por <strong>coluna</strong>: “nota 1 maior que 8”, “nível igual a ERRO”, “status HTTP 500”. O padrão é qualquer condição; quando ela é verdadeira, a ação roda (ou a linha é impressa, se não houver ação).</p>
<hr>
<h2>1. Comparações</h2>
<p>Os operadores: <code>==</code> igual, <code>!=</code> diferente, <code>&gt;</code>, <code>&gt;=</code>, <code>&lt;</code>, <code>&lt;=</code>. Texto entre aspas duplas; número sem aspas:</p>
{T("pad-comp", "awk '$3 == \"ERRO\"' log.txt", "awk '$2 >= 8' notas.txt", "awk -F, '$4 > 5 {print $2, $3, $4}' vendas.csv")}
<p>Repare no cabeçalho na última saída: “quantidade” não é número, então o awk comparou <strong>como texto</strong>, e “quantidade” vem depois de “5” na ordem dos caracteres. Para tabelas com cabeçalho, junte <code>NR &gt; 1 &amp;&amp;</code> na condição.</p>
<hr>
<h2>2. Regex numa coluna: <code>~</code> e <code>!~</code></h2>
<p><code>$3 ~ /ERRO|AVISO/</code> quer dizer “o campo 3 casa com a regex”. Com <code>!~</code>, “não casa”. A regex do awk já é estendida (o <code>|</code> funciona direto):</p>
{T("pad-regex", "awk '$3 ~ /ERRO|AVISO/ {print $2, $3}' log.txt", "awk '$1 !~ /^192\\.168\\.0\\.12$/ {print $1, $9}' acesso.log | head -3")}
<hr>
<h2>3. E, ou, não: <code>&amp;&amp;</code>, <code>||</code>, <code>!</code></h2>
{T("pad-logica", "awk '$2 >= 7 && $4 >= 7' notas.txt", "awk -F, '$3 == \"mochila\" || $4 >= 10 {print $2, $3, $4}' vendas.csv")}
<hr>
<h2>4. Faixas e o número da linha</h2>
<p><code>NR</code> é o número da linha atual. <code>NR == 1</code> é o cabeçalho; <code>NR &gt; 1</code>, o resto. Dois padrões com vírgula formam uma faixa, como no sed:</p>
{T("pad-faixa", "awk 'NR == 1' vendas.csv", "awk 'NR == 2, NR == 4' notas.txt", "awk '/ERRO/, /AVISO/ {print NR\": \"$3}' log.txt")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Texto sem aspas", "Sem aspas, <code>ERRO</code> é o nome de uma variável vazia, e nenhuma linha casa:", T("pad-erro", "awk '$3 == ERRO' log.txt; echo \"código: $?\""), "Escreva <code>$3 == \"ERRO\"</code>.")}
{CEN("Um = só", "Um <code>=</code> é atribuição, não comparação: <code>$3 = \"ERRO\"</code> <strong>muda</strong> o campo 3 de todas as linhas:", T("pad-erro2", "awk '$3 = \"ERRO\"' log.txt | head -3"))}
"""

def padroes_ex():
    return (EX(1, "Igual", "Qual operador compara igualdade?", "awk '$3 ", "==", ' "ERRO"\' log.txt', rotulo="operador") +
            EX(2, "Casa com regex", "Qual operador testa uma regex num campo?", "awk '$3 ", "~", " /AVISO/' log.txt", rotulo="operador") +
            MC(3, "<code>awk 'NR &gt; 1' vendas.csv</code> mostra:", ["só o cabeçalho", "tudo menos o cabeçalho", "a última linha", "nada"], 2) +
            MC(4, "O que <code>awk '$3 = \"ERRO\"' log.txt</code> faz?", ["filtra as linhas de ERRO", "troca o campo 3 de todas as linhas por ERRO", "dá erro de sintaxe", "conta os erros"], 2))

def padroes_miss():
    return (M("pad-m1", "mostre as linhas de <code>notas.txt</code> em que a nota 1 (<code>$2</code>) é menor que 7.", "awk '$2 < 7' notas.txt", r"src:\$2\s*<\s*7;;out:Bruno 6.0 5.5 7.0;;out:Diego 4.0 6.5 5.0") +
            M("pad-m2", "do <code>acesso.log</code>, mostre o IP e o caminho (campos 1 e 7) dos pedidos com status 500 (campo 9).", "awk '$9 == 500 {print $1, $7}' acesso.log", r"src:\$9;;outre:^192\.168\.0\.20 /pagar$"))

# ---------------------------------------------------------------- BEGIN END
def be_corpo():
    return f"""
<h2>A ideia: antes e depois</h2>
<p>Dois padrões especiais: <code>BEGIN</code> roda <strong>uma vez antes</strong> de ler a primeira linha, e <code>END</code> roda <strong>uma vez depois</strong> da última. O <code>BEGIN</code> serve para títulos e configurações; o <code>END</code>, para totais e resumos.</p>
<hr>
<h2>1. Título e rodapé</h2>
{T("be-titulo", "awk 'BEGIN {print \"== Notas ==\"} {print $1} END {print \"== fim ==\"}' notas.txt")}
{ANAT(("BEGIN {...}", "roda antes da primeira linha."), ("{print $1}", "roda em cada linha."), ("END {...}", "roda depois da última."))}
<hr>
<h2>2. Contar no <code>END</code></h2>
<p>No <code>END</code>, o <code>NR</code> ficou com o número da última linha lida, ou seja, o total de linhas. Também dá para contar só algumas, com uma variável sua:</p>
{T("be-contar", "awk 'END {print NR, \"linhas\"}' log.txt", "awk '/ERRO/ {n++} END {print n, \"erros\"}' log.txt")}
<p><code>n++</code> soma 1 em <code>n</code>. Variáveis do awk começam vazias, que vale 0 em contas, então não precisa criar antes.</p>
<hr>
<h2>3. Só <code>BEGIN</code>: o awk como calculadora</h2>
<p>Um programa só com <code>BEGIN</code> nem espera arquivo:</p>
{T("be-calc", "awk 'BEGIN {print 2 + 3 * 4}'", "awk 'BEGIN {printf \"%.2f\\n\", 10 / 3}'", "awk 'BEGIN {print 2 ^ 10}'")}
<hr>
<h2>4. A última linha fica no <code>END</code></h2>
<p>No gawk, <code>$0</code> no <code>END</code> ainda guarda a última linha lida:</p>
{T("be-ultima", "awk 'END {print \"última:\", $0}' vendas.csv")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("BEGIN sem ação", "O <code>BEGIN</code> e o <code>END</code> sempre precisam de chaves com a ação:", T("be-erro", "awk 'BEGIN' notas.txt"))}
"""

def be_ex():
    return (EX(1, "Antes", "Qual padrão roda antes da primeira linha?", "awk '", "BEGIN", " {print \"Título\"}' notas.txt", rotulo="padrão") +
            EX(2, "Depois", "Qual padrão roda depois da última linha?", "awk '", "END", " {print NR}' notas.txt", rotulo="padrão") +
            MC(3, "<code>awk 'END {print NR}' arq</code> mostra:", ["a primeira linha", "o número de linhas", "o número de campos", "nada"], 2) +
            MC(4, "Por que <code>n++</code> funciona sem criar <code>n</code> antes?", ["Porque variáveis do awk começam vazias, que vale 0 em contas", "Porque n é especial", "Porque o BEGIN cria", "Não funciona"], 1))

def be_miss():
    return (M("be-m1", "conte quantas linhas de <code>log.txt</code> têm <code>INFO</code> e mostre <code>5 infos</code> no <code>END</code>.", "awk '/INFO/ {n++} END {print n, \"infos\"}' log.txt", r"src:END;;src:\+\+;;outre:^5 infos$") +
            M("be-m2", "mostre <code>Vendas:</code> antes, os produtos (coluna 3, sem o cabeçalho) e <code>Total de linhas: 13</code> no fim, num programa só.", "awk -F, 'BEGIN {print \"Vendas:\"} NR > 1 {print $3} END {print \"Total de linhas:\", NR}' vendas.csv", r"src:BEGIN;;src:END;;outre:^Vendas:$;;out:Total de linhas: 13"))

# ---------------------------------------------------------------- variáveis
def var_corpo():
    return f"""
<h2>A ideia: o painel de controle do awk</h2>
<p>O awk tem variáveis prontas que contam e configuram a leitura. As principais:</p>
<div class="table-wrap"><table class="ref">
<tr><th>Variável</th><th>O que guarda</th></tr>
<tr><td><code>NR</code></td><td>o número da linha (contando todos os arquivos)</td></tr>
<tr><td><code>FNR</code></td><td>o número da linha dentro do arquivo atual</td></tr>
<tr><td><code>NF</code></td><td>quantos campos a linha atual tem</td></tr>
<tr><td><code>FS</code></td><td>o separador de campos da entrada (o mesmo do <code>-F</code>)</td></tr>
<tr><td><code>OFS</code></td><td>o separador que o <code>print</code> põe entre os itens</td></tr>
<tr><td><code>FILENAME</code></td><td>o nome do arquivo que está sendo lido</td></tr>
</table></div>
<hr>
<h2>1. <code>NR</code> e <code>NF</code></h2>
{T("avar-nr", "awk '{print NR \": \" $0}' frutas.txt | head -3", "awk '{print NF \" palavras: \" $0}' texto.txt")}
<hr>
<h2>2. <code>FS</code> e <code>OFS</code></h2>
<p>Definidos no <code>BEGIN</code>, mudam a leitura e a escrita. Aqui, a entrada é CSV e a saída sai separada por <code>" | "</code>:</p>
{T("avar-fs", "awk 'BEGIN {FS = \",\"; OFS = \" | \"} {print $2, $3, $4}' vendas.csv | head -3")}
<h2>3. O truque do <code>$1 = $1</code></h2>
<p>O <code>OFS</code> só entra quando a linha é <strong>remontada</strong>. Atribuir um campo a ele mesmo força a remontagem. Assim se converte CSV em “separado por ponto e vírgula” (e o <code>1</code> sozinho no fim é um padrão sempre verdadeiro, que imprime a linha):</p>
{T("avar-truque", "awk 'BEGIN {FS = \",\"; OFS = \";\"} {$1 = $1} 1' vendas.csv | head -3", "head -1 log.txt | awk '{$1 = $1; print}'")}
<hr>
<h2>4. <code>FNR</code> e <code>FILENAME</code></h2>
<p>Com dois arquivos, <code>NR</code> continua contando e <code>FNR</code> recomeça em cada um:</p>
{T("avar-fnr", "awk '{print FILENAME, NR, FNR}' frutas.txt notas.txt | sed -n '6,9p'")}
<hr>
<h2>5. Suas variáveis e o <code>-v</code></h2>
<p>O <code>-v nome=valor</code> passa um valor do shell para o awk, sem brigar com aspas:</p>
{T("avar-v", "awk -v minimo=8 '$2 >= minimo {print $1}' notas.txt", "awk -v nivel=AVISO '$3 == nivel {print $2}' log.txt")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("-v sem valor", "O <code>-v</code> exige o formato <code>nome=valor</code>. Depois da mensagem, o gawk despeja a ajuda inteira; o <code>2&gt;&amp;1 | head -3</code> mostra só o começo:", T("avar-erro", "awk -v minimo '$2 >= minimo' notas.txt 2>&1 | head -3"))}
"""

def var_ex():
    return (EX(1, "Número da linha", "Qual variável é o número da linha?", "awk '{print ", "NR", ", $0}' frutas.txt", rotulo="variável") +
            EX(2, "Separador de saída", "Qual variável define o separador de saída?", "awk 'BEGIN {", "OFS", " = \";\"} {$1 = $1} 1' arq", rotulo="variável") +
            MC(3, "Com dois arquivos, qual variável recomeça em 1 no segundo?", ["NR", "FNR", "NF", "FS"], 2) +
            MC(4, "Para passar o valor 8 do shell para o awk como <code>minimo</code>:", ["<code>-F minimo=8</code>", "<code>-v minimo=8</code>", "<code>minimo=8 awk</code>", "<code>-n 8</code>"], 2))

def var_miss():
    return (M("avar-m1", "numere as linhas de <code>nomes.txt</code> no formato <code>1) Ana</code> usando <code>NR</code>.", "awk '{print NR \") \" $0}' nomes.txt", r"src:\bNR\b;;outre:^1\) Ana$;;outre:^9\) Fábio$") +
            M("avar-m2", "converta <code>vendas.csv</code> para separado por tabulação (<code>\\t</code>) com <code>FS</code>, <code>OFS</code> e o truque do <code>$1 = $1</code>.", "awk 'BEGIN {FS = \",\"; OFS = \"\\t\"} {$1 = $1} 1' vendas.csv", r"src:OFS;;src:\$1\s*=\s*\$1;;outre:^2026-03-05\tAna\tcaderno\t4\t12\.50$"))

# ---------------------------------------------------------------- contas
def contas_corpo():
    return f"""
<h2>A ideia: a planilha faz contas</h2>
<p>O awk entende números: soma, subtração, multiplicação, divisão, potência e resto (<code>+ - * / ^ %</code>). Com uma variável acumulando linha a linha e um <code>END</code> para mostrar, você tem totais e médias em uma linha de comando.</p>
<hr>
<h2>1. Somar uma coluna</h2>
<p><code>total += $4</code> soma a quantidade de cada linha em <code>total</code> (o mesmo que <code>total = total + $4</code>):</p>
{T("contas-soma", "awk -F, 'NR > 1 {total += $4} END {print \"itens vendidos:\", total}' vendas.csv")}
<hr>
<h2>2. Somar uma conta</h2>
<p>O faturamento é quantidade vezes preço, linha a linha:</p>
{T("contas-fat", "awk -F, 'NR > 1 {fat += $4 * $5} END {printf \"faturamento: R$ %.2f\\n\", fat}' vendas.csv")}
{ANAT(("NR > 1", "pula o cabeçalho."), ("fat += $4 * $5", "acumula quantidade × preço."), ("END {printf ...}", "no fim, mostra com 2 casas."))}
<hr>
<h2>3. Médias</h2>
<p>A média de cada aluno (três notas) e a média da turma na prova 1:</p>
{T("contas-media", "awk '{printf \"%-8s %.2f\\n\", $1, ($2 + $3 + $4) / 3}' notas.txt", "awk '{soma += $2} END {printf \"média da prova 1: %.2f\\n\", soma / NR}' notas.txt")}
<hr>
<h2>4. Maior e menor</h2>
<p>Guarde o maior visto até agora e compare a cada linha:</p>
{T("contas-max", "awk -F, 'NR > 1 && $4 > max {max = $4; quem = $2} END {print \"maior quantidade:\", max, \"(\" quem \")\"}' vendas.csv")}
<hr>
<h2>5. Número em texto</h2>
<p>O awk converte texto em número sozinho, lendo os dígitos do começo. <code>"85%"</code> vira 85; um texto sem número vira 0:</p>
{T("contas-conv", "awk 'BEGIN {print \"85%\" + 0, \"abc\" + 0, \"3.5kg\" * 2}'")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Divisão por zero", "Dividir por zero é erro fatal. Aqui, a média das linhas de nível FATAL, que não existem no log, então <code>n</code> ficou valendo 0:", T("contas-erro", "awk '$3 == \"FATAL\" {n++; s += NF} END {print s / n}' log.txt"), "Proteja com um <code>if (n &gt; 0)</code> (aula de if e for).")}
"""

def contas_ex():
    return (EX(1, "Acumular", "Complete para somar a coluna 4 em total:", "awk -F, '{total ", "+=", " $4} END {print total}' vendas.csv", rotulo="operador") +
            EX(2, "Média", "Complete a média: soma dividida pelo número de linhas:", "awk '{s += $2} END {print s / ", "NR", "}' notas.txt", rotulo="variável") +
            MC(3, "Quanto o awk calcula para <code>\"85%\" + 0</code>?", ["0", "85", "erro", "0.85"], 2) +
            MC(4, "Por que usar <code>NR &gt; 1</code> ao somar o <code>vendas.csv</code>?", ["Para pular o cabeçalho", "Para ir mais rápido", "Porque a linha 1 é vazia", "Porque o awk exige"], 1))

def contas_miss():
    return (M("contas-m1", "some as quantidades (coluna 4) de <code>vendas.csv</code> só das canetas e mostre o total.", "awk -F, '$3 == \"caneta\" {t += $4} END {print t}' vendas.csv", r"src:\+=;;src:END;;outre:^35$") +
            M("contas-m2", "mostre a média das três notas de cada aluno de <code>notas.txt</code> com 1 casa decimal, no formato <code>Ana 8.3</code>.", "awk '{printf \"%s %.1f\\n\", $1, ($2 + $3 + $4) / 3}' notas.txt", r"src:/\s*3;;outre:^Ana 8\.3$;;outre:^Carla 9\.5$"))

# ---------------------------------------------------------------- arrays
def arrays_corpo():
    return f"""
<h2>A ideia: uma gaveta para cada nome</h2>
<p>Um <strong>array associativo</strong> é um conjunto de gavetas com etiqueta. Em vez de <code>total</code>, você usa <code>total["Ana"]</code>, <code>total["Bruno"]</code>… e a etiqueta pode vir de um campo: <code>total[$2] += $4</code>. É o jeito do awk de fazer “soma por vendedor”, “conta por IP”, a tabela dinâmica da planilha.</p>
<hr>
<h2>1. Contar por chave</h2>
<p><code>n[$3]++</code> soma 1 na gaveta do nível de cada linha. No <code>END</code>, o <code>for (k in n)</code> passa por todas as gavetas:</p>
{T("arr-contar", "awk '{n[$3]++} END {for (k in n) print k, n[k]}' log.txt")}
{ANAT(("n[$3]++", "soma 1 na gaveta com o nome do campo 3."), ("for (k in n)", "passa por cada etiqueta do array."), ("print k, n[k]", "a etiqueta e o valor da gaveta."))}
<div class="warning"><strong>A ordem do <code>for in</code> não é garantida</strong><p>O awk não promete ordem nenhuma ao percorrer o array. Para ordenar, mande para o <code>sort</code>, como abaixo, ou use o recurso do gawk da seção 4.</p></div>
<hr>
<h2>2. Somar por chave</h2>
<p>Faturamento por vendedor, ordenado do maior para o menor com o <code>sort</code>:</p>
{T("arr-somar", "awk -F, 'NR > 1 {fat[$2] += $4 * $5} END {for (v in fat) printf \"%s %.2f\\n\", v, fat[v]}' vendas.csv | sort -k2 -rn")}
<hr>
<h2>3. Contar IPs no log do servidor</h2>
{T("arr-ips", "awk '{n[$1]++} END {for (ip in n) print n[ip], ip}' acesso.log | sort -rn")}
<hr>
<h2>4. Ordem no próprio gawk: <code>PROCINFO["sorted_in"]</code></h2>
<p>Só no gawk: definir <code>PROCINFO["sorted_in"]</code> escolhe a ordem do <code>for in</code>. <code>"@ind_str_asc"</code> é etiqueta em ordem alfabética; <code>"@val_num_desc"</code>, valor numérico do maior para o menor:</p>
{T("arr-procinfo", "awk '{n[$3]++} END {PROCINFO[\"sorted_in\"] = \"@ind_str_asc\"; for (k in n) print k, n[k]}' log.txt", "awk -F, 'NR > 1 {q[$3] += $4} END {PROCINFO[\"sorted_in\"] = \"@val_num_desc\"; for (p in q) print p, q[p]}' vendas.csv")}
<hr>
<h2>5. <code>in</code> e <code>delete</code></h2>
<p><code>(chave in array)</code> testa se a gaveta existe; <code>delete array[chave]</code> apaga. O clássico “mostrar cada linha só na primeira vez” (um <code>uniq</code> que não precisa de <code>sort</code>) usa <code>!visto[$0]++</code>:</p>
{T("arr-visto", "awk '!visto[$0]++' frutas.txt", "awk -F, 'NR > 1 {v[$2]} END {print (\"Diego\" in v), (\"Zeca\" in v)}' vendas.csv")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Array usado como número", "Um array não tem valor único; imprimir o array inteiro é erro fatal:", T("arr-erro", "awk '{n[$3]++} END {print n}' log.txt"))}
"""

def arrays_ex():
    return (EX(1, "Contar", "Complete para contar por vendedor:", "awk -F, 'NR > 1 {n[", "$2", "]++} END {for (v in n) print v, n[v]}' vendas.csv", rotulo="campo") +
            EX(2, "Percorrer", "Complete o laço que passa pelas etiquetas:", "END {for (k ", "in", " n) print k}", rotulo="palavra") +
            MC(3, "O <code>for (k in n)</code> devolve as chaves em que ordem?", ["alfabética", "na ordem em que apareceram", "nenhuma ordem garantida", "numérica"], 3) +
            MC(4, "O que <code>awk '!visto[$0]++' frutas.txt</code> faz?", ["conta as frutas", "mostra cada linha só na primeira vez que aparece", "apaga o arquivo", "ordena"], 2))

def arrays_miss():
    return (M("arr-m1", "conte quantas vendas (linhas) cada vendedor teve em <code>vendas.csv</code>, ordenando o resultado com <code>sort</code>.", "awk -F, 'NR > 1 {n[$2]++} END {for (v in n) print v, n[v]}' vendas.csv | sort", r"src:\[\$2\]\+\+;;src:for \(;;outre:^Ana 4$;;outre:^Diego 2$") +
            M("arr-m2", "some a quantidade vendida por produto (coluna 3) e mostre <code>produto total</code>, em ordem alfabética.", "awk -F, 'NR > 1 {q[$3] += $4} END {for (p in q) print p, q[p]}' vendas.csv | sort", r"src:\[\$3\]\s*\+=;;outre:^caderno 15$;;outre:^caneta 35$;;outre:^mochila 4$"))

# ---------------------------------------------------------------- strings
def str_corpo():
    return f"""
<h2>A ideia: mexer dentro do texto</h2>
<p>O awk tem funções prontas para medir, cortar, procurar e trocar texto. No gawk, em <code>pt_BR.UTF-8</code>, elas contam <strong>letras</strong>, não bytes, então acentos funcionam direito.</p>
<div class="table-wrap"><table class="ref">
<tr><th>Função</th><th>O que faz</th></tr>
<tr><td><code>length(s)</code></td><td>o tamanho de <code>s</code> (sem argumento: da linha)</td></tr>
<tr><td><code>substr(s, i, n)</code></td><td><code>n</code> letras de <code>s</code> a partir da posição <code>i</code> (começa em 1)</td></tr>
<tr><td><code>toupper(s)</code> / <code>tolower(s)</code></td><td>maiúsculas / minúsculas</td></tr>
<tr><td><code>index(s, t)</code></td><td>a posição de <code>t</code> dentro de <code>s</code> (0 se não tem)</td></tr>
<tr><td><code>split(s, a, sep)</code></td><td>quebra <code>s</code> no array <code>a</code>; devolve quantos pedaços</td></tr>
<tr><td><code>sub(re, t, s)</code> / <code>gsub(re, t, s)</code></td><td>troca a primeira / todas as ocorrências (como o <code>s</code> do sed)</td></tr>
</table></div>
<hr>
<h2>1. <code>length</code>, <code>substr</code> e maiúsculas</h2>
{T("str-len", "awk '{print length($0), $0}' nomes.txt | head -5", "awk '{print substr($1, 1, 3)}' notas.txt", "awk '{print toupper($0)}' frutas.txt | head -2")}
<p>“maçã” virou “MAÇÃ”, com acentos: diferente do <code>tr</code> do Nível 1.</p>
<hr>
<h2>2. <code>index</code> e <code>split</code></h2>
<p><code>split</code> quebra o campo da data em ano, mês e dia:</p>
{T("str-split", "awk -F, 'NR == 2 {n = split($1, d, \"-\"); print n, \"pedaços:\", d[3] \"/\" d[2] \"/\" d[1]}' vendas.csv", "awk '{print index($0, \"@\"), $0}' contatos.txt | head -2")}
<hr>
<h2>3. <code>sub</code> e <code>gsub</code></h2>
<p>Como o <code>s</code> do sed, mas dentro do awk e podendo mirar um campo só. Sem o terceiro argumento, trocam na linha inteira (<code>$0</code>):</p>
{T("str-gsub", "awk '{gsub(/rato/, \"gato\"); print}' texto.txt", "awk -F';' '{sub(/@.*/, \"\", $3); print $1 \" -> \" $3}' contatos.txt")}
<hr>
<h2>4. Juntando tudo</h2>
<p>Primeira letra maiúscula em cada nome de <code>nomes.txt</code>:</p>
{T("str-capital", "awk '{print toupper(substr($0, 1, 1)) substr($0, 2)}' nomes.txt")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Função sem argumento", "O <code>substr</code> precisa de pelo menos o texto e a posição:", T("str-erro", "awk '{print substr($1)}' notas.txt"))}
"""

def str_ex():
    return (EX(1, "Tamanho", "Qual função mede o tamanho do texto?", "awk '{print ", "length", "($1)}' notas.txt", rotulo="função") +
            EX(2, "Todas as ocorrências", "Qual função troca todas as ocorrências?", "awk '{", "gsub", "(/a/, \"4\"); print}' frutas.txt", rotulo="função") +
            MC(3, "Em <code>substr(\"banana\", 2, 3)</code>, o resultado é:", ["ban", "ana", "nan", "anan"], 2) +
            MC(4, "No gawk em UTF-8, <code>toupper(\"maçã\")</code> dá:", ["MAçã", "MAÇÃ", "maçã", "erro"], 2))

def str_miss():
    return (M("str-m1", "mostre <code>frutas.txt</code> em maiúsculas com a função <code>toupper</code>.", "awk '{print toupper($0)}' frutas.txt", r"src:toupper;;outre:^MAÇÃ$;;outre:^LARANJA$") +
            M("str-m2", "com <code>gsub</code>, troque todos os <code>-</code> das datas de <code>vendas.csv</code> por <code>/</code> (mostre o arquivo todo).", "awk '{gsub(/-/, \"/\"); print}' vendas.csv", r"src:gsub;;out:2026/03/02,Ana,caderno;;outre:^data,vendedor,produto,quantidade,preco$"))

# ---------------------------------------------------------------- controle
def ctrl_corpo():
    return f"""
<h2>A ideia: decisões e repetições</h2>
<p>Dentro das chaves, o awk é uma linguagem de programação completa, com sintaxe parecida com a do C e do JavaScript: <code>if</code>/<code>else</code> para decidir, <code>for</code> e <code>while</code> para repetir, <code>next</code> para pular para a próxima linha e <code>exit</code> para parar.</p>
<hr>
<h2>1. <code>if</code> e <code>else</code></h2>
<p>A condição vai entre parênteses. Aprovado com média 7 ou mais:</p>
{T("ctrl-if", "awk '{m = ($2 + $3 + $4) / 3; if (m >= 7) print $1, \"aprovado\"; else print $1, \"reprovado\"}' notas.txt")}
<p>Com mais de um comando por ramo, use chaves. E há o operador ternário, <code>condição ? a : b</code>, para escolher um valor:</p>
{T("ctrl-ternario", "awk '{m = ($2 + $3 + $4) / 3; printf \"%-8s %4.1f %s\\n\", $1, m, (m >= 7 ? \"ok\" : \"recuperação\")}' notas.txt")}
<hr>
<h2>2. <code>for</code>: percorrer os campos</h2>
<p>O <code>for (i = 2; i &lt;= NF; i++)</code> passa por cada campo a partir do 2º. Aqui, a maior nota de cada aluno:</p>
{T("ctrl-for", "awk '{max = $2; for (i = 3; i <= NF; i++) if ($i > max) max = $i; print $1, max}' notas.txt")}
{ANAT(("max = $2", "começa com a primeira nota."), ("for (i = 3; i <= NF; i++)", "i vai de 3 até o último campo."), ("if ($i > max) max = $i", "$i é o campo de número i."), ("print $1, max", "nome e maior nota."))}
<hr>
<h2>3. <code>while</code></h2>
{T("ctrl-while", "awk 'BEGIN {i = 1; while (i <= 5) {printf \"%d \", i * i; i++}; print \"\"}'")}
<hr>
<h2>4. <code>next</code> e <code>exit</code></h2>
<p><code>next</code> abandona a linha atual e vai para a próxima (aqui, pula comentários e linhas vazias). <code>exit</code> encerra o programa (indo para o <code>END</code>, se houver):</p>
{T("ctrl-next", "awk '/^#/ || /^$/ {next} {print \"config:\", $0}' config.txt", "awk '$3 == \"ERRO\" {print \"primeiro erro na linha\", NR; exit}' log.txt")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("if sem parênteses", "A condição do <code>if</code> precisa de parênteses:", T("ctrl-erro", "awk '{if $2 > 7 print $1}' notas.txt"))}
"""

def ctrl_ex():
    return (EX(1, "Senão", "Complete o ramo do “senão”:", "if (m >= 7) print \"ok\"; ", "else", " print \"não\"", rotulo="palavra") +
            EX(2, "Pular linha", "Qual comando pula para a próxima linha?", "awk '/^#/ {", "next", "} {print}' config.txt", rotulo="comando") +
            MC(3, "No <code>for (i = 2; i &lt;= NF; i++)</code>, <code>$i</code> é:", ["a variável i", "o campo de número i", "sempre o campo 2", "o número de campos"], 2) +
            MC(4, "O que o <code>exit</code> faz?", ["apaga o arquivo", "encerra o programa (ainda rodando o END, se houver)", "pula a linha", "sai do terminal"], 2))

def ctrl_miss():
    return (M("ctrl-m1", "para cada aluno de <code>notas.txt</code>, mostre o nome e <code>passou</code> se a nota 3 (<code>$4</code>) for 7 ou mais, senão <code>ficou</code>.", "awk '{if ($4 >= 7) print $1, \"passou\"; else print $1, \"ficou\"}' notas.txt", r"src:\bif\b;;src:\belse\b;;outre:^Ana passou$;;outre:^Diego ficou$") +
            M("ctrl-m2", "com um <code>for</code> pelos campos, some as três notas de cada aluno e mostre <code>nome soma</code>.", "awk '{s = 0; for (i = 2; i <= NF; i++) s += $i; print $1, s}' notas.txt", r"src:\bfor\b;;outre:^Ana 25$;;outre:^Carla 28\.5$"))

# ---------------------------------------------------------------- scripts
def scr_corpo():
    return f"""
<h2>A ideia: programas awk em arquivo</h2>
<p>Quando o programa passa de uma linha, fica ruim de digitar entre aspas. Coloque-o num arquivo <code>.awk</code> e rode com <code>-f</code>. Dentro do arquivo não precisa de aspas simples, dá para quebrar linhas, indentar e comentar com <code>#</code>.</p>
<hr>
<h2>1. <code>-f</code>: rodar um arquivo</h2>
<p>O <code>relatorio.awk</code> dos exemplos calcula o faturamento por vendedor:</p>
{T("scr-f", "cat relatorio.awk", "awk -f relatorio.awk vendas.csv | sort")}
{ANAT(("awk", "o programa."), ("-f relatorio.awk", "lê o programa awk do arquivo."), ("vendas.csv", "o arquivo de dados."))}
<hr>
<h2>2. Script executável</h2>
<p>Com a primeira linha <code>#!/usr/bin/awk -f</code> e permissão de execução, o arquivo vira um comando. Na coleta, o script foi criado com <code>printf</code> para caber numa linha:</p>
{T("scr-exec", "printf '#!/usr/bin/awk -f\\n{ print NR \": \" $1 }\\n' > numera.awk", "chmod +x numera.awk", "./numera.awk notas.txt")}
<hr>
<h2>3. <code>-v</code> com <code>-f</code></h2>
<p>O <code>-v</code> passa valores para o script, que fica reaproveitável: o mesmo filtro para níveis diferentes:</p>
{T("scr-v", "printf '$3 == nivel { print $2, $4 }\\n' > filtra.awk", "awk -v nivel=ERRO -f filtra.awk log.txt", "awk -v nivel=AVISO -f filtra.awk log.txt")}
<hr>
<h2>4. Funções</h2>
<p>No awk você pode criar funções com <code>function nome(parâmetros) {{ ... }}</code>. Aqui, uma que formata dinheiro:</p>
{T("scr-funcao", "awk -F, 'function reais(v) {return sprintf(\"R$ %.2f\", v)} NR > 1 {print $3, reais($4 * $5)}' vendas.csv | head -3")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Script que não existe", "O <code>-f</code> precisa de um arquivo que exista:", T("scr-erro", "awk -f nada.awk notas.txt"))}
"""

def scr_ex():
    return (EX(1, "Ler de arquivo", "Qual opção lê o programa de um arquivo?", "awk ", "-f", " relatorio.awk vendas.csv", rotulo="opção") +
            EX(2, "A primeira linha", "Complete a primeira linha de um script awk executável:", "#!/usr/bin/awk ", "-f") +
            MC(3, "Dentro de um arquivo <code>.awk</code>, o programa:", ["precisa de aspas simples", "não precisa de aspas e pode ter várias linhas", "só pode ter uma linha", "precisa começar com BEGIN"], 2) +
            MC(4, "Como se cria uma função no awk?", ["<code>def f(x):</code>", "<code>function f(x) { ... }</code>", "<code>func f</code>", "<code>sub f</code>"], 2))

def scr_miss():
    return (M("scr-m1", "rode o <code>relatorio.awk</code> no <code>vendas.csv</code> e ordene o resultado com <code>sort</code>.", "awk -f relatorio.awk vendas.csv | sort", r"src:-f relatorio\.awk;;outre:^Ana\s+R\$\s+277\.30$;;outre:^Diego\s+R\$\s+65\.00$") +
            M("scr-m2", "use o <code>-v</code> para filtrar as linhas de <code>notas.txt</code> cuja nota 1 é maior que um <code>limite</code> de 7, mostrando só o nome.", "awk -v limite=7 '$2 > limite {print $1}' notas.txt", r"src:-v limite=7;;outre:^Ana$;;outre:^Carla$"))

# ---------------------------------------------------------------- CSV
def csv_corpo():
    return f"""
<h2>A ideia: CSV de verdade</h2>
<p>CSV (<em>comma-separated values</em>) é o formato que as planilhas exportam. Na maioria das vezes, <code>-F,</code> resolve, como você viu. O problema aparece quando um campo tem vírgula dentro, protegido por aspas: <code>"Souza, Ana"</code>. Esta aula junta o que você aprendeu num fluxo de CSV e mostra o limite do <code>-F,</code>.</p>
<hr>
<h2>1. Cabeçalho, filtro e total</h2>
<p>O roteiro comum: pular o cabeçalho, filtrar, calcular e escrever outro CSV. Aqui, só as vendas da Ana, com uma coluna nova de total:</p>
{T("csv-roteiro", "awk -F, 'BEGIN {OFS = \",\"} NR == 1 {print $1, $3, \"total\"; next} $2 == \"Ana\" {print $1, $3, $4 * $5}' vendas.csv")}
<hr>
<h2>2. Usando os nomes das colunas</h2>
<p>Lendo o cabeçalho num array, dá para pedir a coluna pelo nome, e o script continua funcionando se as colunas mudarem de lugar:</p>
{T("csv-nomes", "awk -F, 'NR == 1 {for (i = 1; i <= NF; i++) col[$i] = i; next} {print $col[\"produto\"], $col[\"preco\"]}' vendas.csv | head -3")}
<hr>
<h2>3. O problema da vírgula dentro do campo</h2>
<p>Com <code>-F,</code>, a vírgula de dentro das aspas também corta, e o campo 2 sai pela metade:</p>
{T("csv-problema", "echo '7,\"Souza, Ana\",28' | awk -F, '{print $2}'")}
<p>O gawk tem a variável <code>FPAT</code>, que descreve <strong>como é um campo</strong> em vez de como é o separador: “ou uma sequência sem vírgulas, ou algo entre aspas”:</p>
{T("csv-fpat", "echo '7,\"Souza, Ana\",28' | awk -v FPAT='([^,]*)|(\"[^\"]*\")' '{print $2; print NF, \"campos\"}'")}
<div class="warning"><strong>Só no gawk</strong><p>O <code>FPAT</code> é do gawk. O mawk ignora a variável e continua separando por espaços: na coleta, ele devolveu o campo 2 errado. (O gawk 5.3, mais novo que o deste guia, ainda ganhou a opção <code>--csv</code>.)</p></div>
{T("csv-mawk", "echo '7,\"Souza, Ana\",28' | mawk -v FPAT='([^,]*)|(\"[^\"]*\")' '{print $2}'")}
<hr>
<h2>4. CSV para tabela legível</h2>
{T("csv-tabela", "awk -F, '{printf \"%-11s %-9s %-8s %10s %6s\\n\", $1, $2, $3, $4, $5}' vendas.csv | head -5")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Fim de linha do Windows", "Um CSV salvo no Windows tem <code>\\r</code> antes de cada quebra de linha. O último campo carrega esse caractere invisível e a comparação falha. Na coleta, criamos uma linha assim com <code>printf</code>; o <code>$3 == \"28\"</code> deu falso:", T("csv-erro", "printf '7,Ana,28\\r\\n' | awk -F, '{print ($3 == \"28\") ? \"igual\" : \"diferente\"}'"), "Limpe antes com <code>sed 's/\\r$//'</code> ou, no awk, <code>sub(/\\r$/, \"\")</code>.")}
"""

def csv_ex():
    return (EX(1, "Pular o cabeçalho", "Complete para pular a primeira linha:", "awk -F, '", "NR > 1", " {print $2}' vendas.csv", rotulo="padrão") +
            EX(2, "Campo como padrão", "Qual variável do gawk descreve como é um campo?", "awk -v ", "FPAT", "='([^,]*)|(\"[^\"]*\")'", rotulo="variável") +
            MC(3, "Por que <code>-F,</code> falha em <code>\"Souza, Ana\"</code>?", ["Porque a vírgula dentro das aspas também corta", "Porque o nome tem espaço", "Porque falta o OFS", "Não falha"], 1) +
            MC(4, "Qual problema o <code>\\r</code> de arquivos do Windows causa?", ["Nenhum", "O último campo carrega um caractere invisível e comparações falham", "O awk não abre o arquivo", "As linhas somem"], 2))

def csv_miss():
    return (M("csv-m1", "a partir de <code>vendas.csv</code>, gere um CSV só com <code>vendedor,total</code> (quantidade × preço) das linhas de <code>mochila</code>, com cabeçalho.", "awk -F, 'BEGIN {OFS = \",\"; print \"vendedor,total\"} $3 == \"mochila\" {print $2, $4 * $5}' vendas.csv", r"src:OFS;;outre:^vendedor,total$;;outre:^Ana,179\.8$;;outre:^Bruno,89\.9$") +
            M("csv-m2", "use o <code>FPAT</code> para mostrar o nome (campo 2) de <code>echo '9,\"Lima, Bruno\",35'</code>.", "echo '9,\"Lima, Bruno\",35' | awk -v FPAT='([^,]*)|(\"[^\"]*\")' '{print $2}'", r"src:FPAT;;outre:^\"Lima, Bruno\"$"))

NIVEL = {"id": "n3", "nome": "Nível 3 · awk", "curto": "awk", "desc": "Colunas, contas, contagens e relatórios", "grupos": [
    {"grupo": "Primeiros passos", "aulas": [
        aula(slug="awk-intro", menu="Como o awk funciona (padrão { ação })", title="Como o awk funciona: padrão e ação", h1='Como o <span class="hl">awk</span> funciona (padrão { ação })',
             desc="Primeiros passos com o awk (gawk): padrão e ação, $0, $1, filtros com regex e os erros mais comuns.",
             intro="O <code>awk</code> lê o texto linha a linha e já corta cada linha em colunas. Com um padrão e uma ação, ele filtra e reorganiza em uma linha de comando.",
             aprender=["A estrutura <code>padrão {{ ação }}</code>.".replace("{{", "{").replace("}}", "}"), "<code>$0</code>, <code>$1</code> e o <code>print</code>.", "Filtrar com regex, com e sem ação."],
             corpo=intro_corpo, exercicios=intro_ex, missoes=intro_miss,
             ref=[("awk '{print $1}' arq", "a 1ª coluna."), ("awk '{print}' arq", "a linha toda (como cat)."), ("awk '/x/' arq", "as linhas com x (como grep)."), ("awk '/x/ {print $2}' arq", "a 2ª coluna das linhas com x.")],
             resumo=["Um programa awk é uma lista de <code>padrão { ação }</code>.", "<code>$0</code> é a linha; <code>$1</code>, <code>$2</code>… as colunas.", "Programa awk sempre entre aspas simples."]),
        aula(slug="awk-campos", menu="Campos, $NF e -F", title="Campos no awk: $1, $NF e o separador -F", h1='Campos, <span class="hl">$NF</span> e <span class="hl">-F</span>',
             desc="Campos no awk: separação por espaços, NF e $NF, $(NF-1), -F para CSV e separador com regex.",
             intro="Cada linha vira uma fileira de planilha. Esta aula mostra como o awk corta os campos, como pegar o último e como trocar o separador.",
             aprender=["Como o awk separa campos por espaços.", "<code>NF</code>, <code>$NF</code> e <code>$(NF-1)</code>.", "Trocar o separador com <code>-F</code>, inclusive com regex."],
             corpo=campos_corpo, exercicios=campos_ex, missoes=campos_miss,
             ref=[("$1, $2...", "os campos."), ("NF", "quantos campos."), ("$NF", "o último campo."), ("$(NF-1)", "o penúltimo."), ("awk -F, ...", "separador vírgula."), ("awk -F'[;@]' ...", "separador ; ou @.")],
             resumo=["Espaços repetidos contam como um separador só.", "<code>$NF</code> é o último campo.", "<code>-F</code> troca o separador, e aceita regex."]),
        aula(slug="awk-printf", menu="print e printf", title="print e printf no awk: formatando a saída", h1='<span class="hl">print</span> e <span class="hl">printf</span>',
             desc="print e printf no awk: vírgula e concatenação, lacunas %s %d %f, casas decimais, largura e alinhamento.",
             intro="O <code>print</code> é rápido; o <code>printf</code> é preciso. Com ele você controla casas decimais, largura e alinhamento: relatórios bonitos.",
             aprender=["<code>print</code> com e sem vírgula.", "O molde do <code>printf</code>: <code>%s</code>, <code>%d</code>, <code>%.2f</code>.", "Largura e alinhamento de colunas."],
             corpo=printf_corpo, exercicios=printf_ex, missoes=printf_miss,
             ref=[("print $1, $2", "com espaço entre os dois."), ("print $1 $2", "emendados."), ('printf "%s\\n", $1', "texto + quebra de linha."), ('printf "%.2f\\n", $2', "número com 2 casas."), ('printf "%-8s|\\n", $1', "largura 8, à esquerda."), ('printf "%5d\\n", $4', "inteiro, largura 5, à direita.")],
             resumo=["Vírgula no <code>print</code> põe o separador de saída.", "<code>printf</code> não pula linha sem <code>\\n</code>.", "<code>%-8s</code> e <code>%6.2f</code> alinham colunas."]),
        aula(slug="awk-padroes", menu="Padrões e condições", title="Padrões e condições no awk", h1='Padrões e <span class="hl">condições</span>',
             desc="Padrões no awk: comparações por coluna, ~ e !~ com regex, &&, ||, !, NR e faixas de linhas.",
             intro="O awk filtra por coluna: nota maior que 8, nível igual a ERRO, status 500. Esta aula mostra todas as formas de escrever essas condições.",
             aprender=["Comparações: <code>==</code>, <code>!=</code>, <code>&gt;</code>, <code>&lt;</code>.", "Regex numa coluna com <code>~</code> e <code>!~</code>.", "Combinar com <code>&amp;&amp;</code>, <code>||</code> e usar <code>NR</code>."],
             corpo=padroes_corpo, exercicios=padroes_ex, missoes=padroes_miss,
             ref=[('$3 == "ERRO"', "campo 3 igual a ERRO."), ("$2 >= 8", "campo 2 maior ou igual a 8."), ("$3 ~ /A|B/", "campo 3 casa com a regex."), ("$1 !~ /x/", "campo 1 não casa."), ("a && b", "as duas condições."), ("a || b", "uma ou outra."), ("NR > 1", "tudo menos a 1ª linha.")],
             resumo=["Texto entre aspas duplas; número sem aspas.", "<code>~</code> testa regex num campo.", "<code>==</code> compara; <code>=</code> atribui."]),
    ]},
    {"grupo": "Contas e variáveis", "aulas": [
        aula(slug="awk-begin-end", menu="BEGIN e END", title="BEGIN e END no awk", h1='<span class="hl">BEGIN</span> e <span class="hl">END</span>',
             desc="Os padrões BEGIN e END do awk: títulos, rodapés, contagens no fim e o awk como calculadora.",
             intro="<code>BEGIN</code> roda antes de tudo; <code>END</code>, depois de tudo. São os lugares do título, das configurações e dos totais.",
             aprender=["Título e rodapé com <code>BEGIN</code> e <code>END</code>.", "Contar linhas e ocorrências no <code>END</code>.", "Usar o awk como calculadora."],
             corpo=be_corpo, exercicios=be_ex, missoes=be_miss,
             ref=[("BEGIN {...}", "antes da 1ª linha."), ("END {...}", "depois da última."), ("END {print NR}", "conta as linhas."), ("/x/ {n++} END {print n}", "conta as linhas com x."), ("awk 'BEGIN {print 2+3}'", "calculadora.")],
             resumo=["<code>BEGIN</code> e <code>END</code> rodam uma vez cada.", "No <code>END</code>, <code>NR</code> é o total de linhas.", "Variáveis começam vazias (0 em contas)."]),
        aula(slug="awk-variaveis", menu="Variáveis (NR, NF, FS, OFS, -v)", title="Variáveis do awk: NR, NF, FS, OFS, FNR e -v", h1='Variáveis (<span class="hl">NR</span>, <span class="hl">NF</span>, <span class="hl">FS</span>, <span class="hl">OFS</span>)',
             desc="Variáveis embutidas do awk: NR, FNR, NF, FS, OFS, FILENAME, o truque $1=$1 e o -v para passar valores do shell.",
             intro="O awk tem um painel de variáveis prontas: o número da linha, quantos campos, os separadores. Esta aula mostra cada uma e como passar as suas com <code>-v</code>.",
             aprender=["<code>NR</code>, <code>FNR</code>, <code>NF</code> e <code>FILENAME</code>.", "<code>FS</code>, <code>OFS</code> e o truque <code>$1 = $1</code>.", "Passar valores do shell com <code>-v</code>."],
             corpo=var_corpo, exercicios=var_ex, missoes=var_miss,
             ref=[("NR", "nº da linha (total)."), ("FNR", "nº da linha no arquivo atual."), ("NF", "nº de campos."), ('BEGIN {FS = ","}', "o mesmo que -F,."), ('BEGIN {OFS = ";"} {$1 = $1} 1', "remonta a linha com ;."), ("-v x=10", "cria a variável x com 10.")],
             resumo=["<code>NR</code> conta linhas; <code>NF</code>, campos.", "<code>OFS</code> só aparece quando a linha é remontada.", "<code>-v</code> traz valores do shell sem brigar com aspas."]),
        aula(slug="awk-contas", menu="Somas, médias e máximos", title="Somas, médias e máximos com awk", h1='Somas, <span class="hl">médias</span> e máximos',
             desc="Contas no awk: somar colunas, faturamento, médias por linha e da coluna, maior valor e conversão de texto em número.",
             intro="Total vendido, média da turma, maior venda: com uma variável acumulando e um <code>END</code>, o awk faz as contas da planilha.",
             aprender=["Somar uma coluna e uma conta.", "Médias por linha e da coluna inteira.", "Achar o maior valor e entender a conversão de texto em número."],
             corpo=contas_corpo, exercicios=contas_ex, missoes=contas_miss,
             ref=[("{t += $4} END {print t}", "soma a coluna 4."), ("{t += $4 * $5}", "soma uma conta."), ("END {print t / NR}", "média."), ("$4 > max {max = $4}", "guarda o maior."), ("+ - * / ^ %", "os operadores.")],
             resumo=["<code>x += valor</code> acumula.", "Média = soma / quantidade (cuidado com zero).", "Texto vira número lendo os dígitos do começo."]),
        aula(slug="awk-arrays", menu="Arrays associativos (contagens)", title="Arrays associativos no awk: contar e somar por chave", h1='Arrays <span class="hl">associativos</span>',
             desc="Arrays associativos no awk: contar e somar por chave, for in, ordenar com sort ou PROCINFO sorted_in (gawk), in, delete e !visto[$0]++.",
             intro="Um array associativo tem uma gaveta para cada etiqueta. É assim que o awk faz soma por vendedor e contagem por IP, a tabela dinâmica do terminal.",
             aprender=["Contar e somar por chave.", "Percorrer com <code>for (k in a)</code> e ordenar.", "<code>in</code>, <code>delete</code> e o truque <code>!visto[$0]++</code>."],
             corpo=arrays_corpo, exercicios=arrays_ex, missoes=arrays_miss,
             ref=[("n[$1]++", "conta por campo 1."), ("t[$2] += $4", "soma por campo 2."), ("for (k in n) print k, n[k]", "percorre (sem ordem garantida)."), ('PROCINFO["sorted_in"] = "@ind_str_asc"', "ordem alfabética (gawk)."), ("(k in n)", "a chave existe?"), ("!visto[$0]++", "cada linha só na 1ª vez.")],
             resumo=["<code>a[chave]</code> cria a gaveta na hora.", "O <code>for in</code> não tem ordem: use <code>sort</code> ou <code>PROCINFO</code>.", "<code>!visto[$0]++</code> tira repetidos sem ordenar."]),
    ]},
    {"grupo": "Programando em awk", "aulas": [
        aula(slug="awk-strings", menu="Funções de texto", title="Funções de texto no awk: length, substr, toupper, split, gsub", h1='Funções de <span class="hl">texto</span>',
             desc="Funções de string do awk: length, substr, toupper, tolower, index, split, sub e gsub, com acentos no gawk.",
             intro="Medir, cortar, procurar e trocar dentro do texto: o awk tem funções prontas para tudo isso, e no gawk elas entendem acentos.",
             aprender=["<code>length</code>, <code>substr</code>, <code>toupper</code> e <code>tolower</code>.", "<code>index</code> e <code>split</code>.", "<code>sub</code> e <code>gsub</code>."],
             corpo=str_corpo, exercicios=str_ex, missoes=str_miss,
             ref=[("length($1)", "tamanho do campo 1."), ("substr($1, 1, 3)", "3 letras a partir da 1ª."), ("toupper($0)", "maiúsculas."), ('index($0, "@")', "posição do @."), ('split($1, d, "-")', "quebra em d[1], d[2]..."), ('gsub(/a/, "b")', "troca todas na linha.")],
             resumo=["As funções do gawk contam letras, não bytes.", "<code>split</code> devolve quantos pedaços e enche um array.", "<code>sub</code> e <code>gsub</code> são o <code>s</code> do sed dentro do awk."]),
        aula(slug="awk-controle", menu="if, for, while, next e exit", title="if, for, while, next e exit no awk", h1='<span class="hl">if</span>, <span class="hl">for</span> e <span class="hl">while</span>',
             desc="Estruturas de controle do awk: if/else, ternário, for pelos campos, while, next e exit.",
             intro="Dentro das chaves, o awk é uma linguagem completa. Esta aula mostra decisões e repetições, com exemplos de notas e logs.",
             aprender=["<code>if</code>/<code>else</code> e o ternário.", "<code>for</code> pelos campos e <code>while</code>.", "<code>next</code> e <code>exit</code>."],
             corpo=ctrl_corpo, exercicios=ctrl_ex, missoes=ctrl_miss,
             ref=[("if (c) a; else b", "decide."), ("c ? x : y", "escolhe um valor."), ("for (i = 1; i <= NF; i++)", "percorre os campos."), ("while (c) {...}", "repete enquanto c."), ("next", "vai para a próxima linha."), ("exit", "encerra (roda o END).")],
             resumo=["A condição do <code>if</code> vai entre parênteses.", "<code>$i</code> é o campo de número i.", "<code>next</code> pula a linha; <code>exit</code> encerra."]),
        aula(slug="awk-scripts", menu="Scripts awk (-f), -v e funções", title="Scripts awk em arquivo (-f), -v e funções", h1='Scripts awk (<span class="hl">-f</span>), -v e funções',
             desc="Programas awk em arquivo com -f, scripts executáveis com #!/usr/bin/awk -f, -v com scripts e funções definidas pelo usuário.",
             intro="Quando o programa cresce, ele vai para um arquivo <code>.awk</code>. Esta aula mostra como rodar, como tornar executável, como parametrizar e como criar funções.",
             aprender=["Rodar um arquivo com <code>-f</code>.", "Script executável com <code>#!/usr/bin/awk -f</code>.", "Parâmetros com <code>-v</code> e funções com <code>function</code>."],
             corpo=scr_corpo, exercicios=scr_ex, missoes=scr_miss,
             ref=[("awk -f prog.awk arq", "roda o programa do arquivo."), ("#!/usr/bin/awk -f", "1ª linha do script executável."), ("awk -v x=1 -f prog.awk arq", "passa x para o script."), ("function f(a) {return a*2}", "cria uma função.")],
             resumo=["Arquivo <code>.awk</code>: sem aspas, com comentários e várias linhas.", "<code>-v</code> deixa o script reaproveitável.", "<code>function</code> cria funções suas."]),
        aula(slug="awk-csv", menu="CSV com awk (e o FPAT do gawk)", title="CSV com awk: cabeçalho, colunas por nome e FPAT", h1='CSV com <span class="hl">awk</span>',
             desc="Trabalhar com CSV no awk: pular cabeçalho, gerar CSV, colunas pelo nome, vírgula dentro de aspas com FPAT (gawk) e o \\r do Windows.",
             intro="CSV é o formato das planilhas. Esta aula junta o que você aprendeu num fluxo completo e mostra o limite do <code>-F,</code> com campos entre aspas.",
             aprender=["Filtrar e gerar CSV com cabeçalho.", "Pedir colunas pelo nome.", "Campos com vírgula dentro: o <code>FPAT</code> do gawk."],
             corpo=csv_corpo, exercicios=csv_ex, missoes=csv_miss,
             ref=[("awk -F, 'NR > 1 ...'", "pula o cabeçalho."), ("BEGIN {OFS = \",\"}", "saída em CSV."), ("col[$i] = i", "mapa nome → número da coluna."), ("-v FPAT='([^,]*)|(\"[^\"]*\")'", "campos com aspas (gawk)."), ("sub(/\\r$/, \"\")", "tira o \\r do Windows.")],
             resumo=["<code>-F,</code> resolve CSV simples.", "Vírgula dentro de aspas pede o <code>FPAT</code> do gawk.", "Arquivo do Windows? Tire o <code>\\r</code> antes."]),
    ]},
]}
