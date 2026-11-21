# -*- coding: utf-8 -*-
"""Nível 5 · Projetos: juntar grep, sed, awk e jq em tarefas reais."""
from lib_guia import *

def aula(**k):
    return k

# ---------------------------------------------------------------- comandos (fora das f-strings, para não brigar com aspas)
L_STATUS = r"""awk '{print $9}' acesso.log | sort | uniq -c | sort -rn"""
L_IPS = r"""awk '{print $1}' acesso.log | sort | uniq -c | sort -rn | head -3"""
L_ERROS = r"""awk '$9 >= 400 {print $1, $7, $9}' acesso.log"""
L_5XX = r"""grep -c '" 5[0-9][0-9] ' acesso.log"""
L_JANELA = r"""sed -E 's/.*:([0-9]{2}):([0-9])[0-9]:.*/\1:\20/' acesso.log | sort | uniq -c"""
L_NIVEIS = r"""awk '{print $3}' log.txt | sort | uniq -c"""
L_ERRO_SEMSORT = r"""awk '{print $9}' acesso.log | uniq -c | head -5"""
L_M1 = r"""grep -c POST acesso.log"""
L_M2 = r"""awk '{s += $10} END {print s}' acesso.log"""

V_TOTAL = r"""awk -F, 'NR > 1 {t += $4 * $5} END {printf "%.2f\n", t}' vendas.csv"""
V_VEND = r"""awk -F, 'NR > 1 {v[$2] += $4 * $5} END {for (n in v) printf "%s %.2f\n", n, v[n]}' vendas.csv | sort -k2 -rn"""
V_PROD = r"""awk -F, 'NR > 1 {q[$3] += $4} END {for (p in q) print q[p], p}' vendas.csv | sort -rn"""
V_DIA = r"""grep '^2026-03-04' vendas.csv | awk -F, '{t += $4 * $5} END {printf "%.2f\n", t}'"""
V_VIRG = r"""awk -F, 'NR > 1 {t += $4 * $5} END {printf "%.2f\n", t}' vendas.csv | sed 's/\./,/'"""
V_ERRO = r"""awk '{t += $4 * $5} END {print t}' vendas.csv"""
V_ERRO2 = r"""awk -F, 'NR > 1 {t += $4 * $5} END {printf "%.2f\n", t}' vendas.csv | sed 's/./,/'"""
V_M1 = r"""awk -F, '$2 == "Carla" {t += $4 * $5} END {printf "%.2f\n", t}' vendas.csv"""
V_M2 = r"""awk -F, '$3 == "caneta" {q += $4} END {print q}' vendas.csv"""

J_OLHAR = r"""jq -c '.pedidos[0]' pedidos.json"""
J_PAGO_ERR = r"""bash pedidos-para-csv.sh | awk -F, '$3 == "pago" {t += $7} END {print t + 0}'"""
J_PAGO = r"""bash pedidos-para-csv.sh | tr -d '"' | awk -F, '$3 == "pago" {t += $7} END {print t + 0}'"""
J_USU = r"""jq -r '.[] | [.nome, .email // "", (.tags | join(";"))] | @csv' usuarios.json"""
J_ERRO = r"""bash pedidos-para-csv.sh produto.json"""
J_M1 = r"""bash pedidos-para-csv.sh | wc -l"""
J_M2 = r"""jq -r '.pedidos[] | [.id, .cliente, (.itens | length)] | @csv' pedidos.json"""

P_IDS = r"""grep 'falha no pagamento' log.txt | sed -E 's/.*pedido=//'"""
P_CRUZA = r"""for id in $(grep 'falha no pagamento' log.txt | sed -E 's/.*pedido=//'); do jq -e -r --argjson id "$id" '.pedidos[] | select(.id == $id) | "\(.id) \(.cliente) \(.status)"' pedidos.json || echo "$id não está no pedidos.json"; done"""
P_JSON = r"""awk -F, 'NR > 1 {printf "{\"vendedor\":\"%s\",\"valor\":%s}\n", $2, $4 * $5}' vendas.csv | head -3"""
P_AGRUPA = r"""awk -F, 'NR > 1 {printf "{\"vendedor\":\"%s\",\"valor\":%s}\n", $2, $4 * $5}' vendas.csv | jq -s -c 'group_by(.vendedor) | map({vendedor: .[0].vendedor, total: (map(.valor) | add)})'"""
P_ERRO = r"""for id in $(grep 'falha no pagamento' log.txt | sed -E 's/.*pedido=//'); do jq -r --arg id "$id" '.pedidos[] | select(.id == $id) | .cliente' pedidos.json; done; echo fim"""
P_ERRO2 = r"""grep 'falha no pagamento' log.txt | sed -E 's/.*pedido=(\d+)$/\1/'"""
P_M1 = r"""grep -c ERRO log.txt"""
P_M2 = r"""awk -F, 'NR > 1 {printf "{\"vendedor\":\"%s\",\"valor\":%s}\n", $2, $4 * $5}' vendas.csv | jq -s 'map(select(.vendedor == "Ana") | .valor) | add'"""

# ---------------------------------------------------------------- log
def log_corpo():
    return f"""
<h2>O problema</h2>
<p>O site da papelaria grava cada visita no <code>acesso.log</code>, no formato que servidores como Apache e Nginx usam. A pergunta do chefe: <em>quantas visitas, quantos erros, quem mais acessou, e o que quebrou?</em> Vamos responder com uma ferramenta por vez e, no fim, juntar tudo num script.</p>
<hr>
<h2>1. Olhar antes de mexer</h2>
<p>Sempre comece vendo algumas linhas e contando o total:</p>
{T("plog-olhar", "head -3 acesso.log", "wc -l < acesso.log")}
<p>Separando por espaços, cada linha tem estes campos (os que o <code>awk</code> enxerga como <code>$1</code>, <code>$2</code>…):</p>
{ANAT(("$1", "o IP de quem visitou (aqui, endereços da rede de casa 192.168.0.x)."), ("$4", "data e hora, com o colchete na frente."), ("$6", "o método, com aspas na frente: \"GET ou \"POST."), ("$7", "o caminho pedido, como /index.html."), ("$9", "o status da resposta: 200 deu certo, 404 não achou, 500 erro do servidor."), ("$10", "quantos bytes foram enviados."))}
<hr>
<h2>2. Contar por status</h2>
<p>A receita clássica: <code>awk</code> tira a coluna, <code>sort</code> junta os iguais, <code>uniq -c</code> conta, e o último <code>sort -rn</code> põe os maiores no topo:</p>
{T("plog-status", L_STATUS)}
<hr>
<h2>3. Quem mais acessou</h2>
{T("plog-ips", L_IPS)}
<p>Com empate (dois IPs com 3 visitas), o <code>sort -rn</code> desempata comparando a linha inteira, também em ordem decrescente: por isso o .20 veio antes do .15.</p>
<hr>
<h2>4. Só os erros</h2>
<p>Status 400 ou mais é problema. No <code>awk</code>, um padrão numérico resolve; no <code>grep</code>, uma expressão regular que pega <code>" 5xx </code>:</p>
{T("plog-erros", L_ERROS, L_5XX)}
<hr>
<h2>5. Visitas a cada 10 minutos</h2>
<p>O <code>sed</code> recorta da hora só “hora:dezena dos minutos” e completa com 0. Depois, contar é a mesma receita:</p>
{T("plog-janela", L_JANELA)}
{ANAT((".*:", "anda até o último “:” que ainda deixa o resto casar."), ("([0-9]{2}):([0-9])[0-9]:", "guarda a hora (grupo 1) e a dezena dos minutos (grupo 2)."), ("\\1:\\20", "devolve hora, “:”, a dezena e um 0."))}
<hr>
<h2>6. O outro log: <code>log.txt</code></h2>
<p>O <code>log.txt</code> é o log do sistema da loja, com o nível na 3ª coluna:</p>
{T("plog-niveis", L_NIVEIS)}
<hr>
<h2>7. Tudo num script</h2>
<p>O arquivo <code>analisa-log.sh</code> (já está nos arquivos de exemplo) junta os passos. Ele confere se o arquivo existe antes de começar e aceita outro log como argumento:</p>
{T("plog-script", "cat analisa-log.sh", "bash analisa-log.sh")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("uniq sem sort", "O <code>uniq</code> só junta linhas iguais <strong>vizinhas</strong>. Sem o <code>sort</code> antes, a contagem sai picada, e o 200 aparece várias vezes:", T("plog-erro", L_ERRO_SEMSORT))}
{CEN("Arquivo que não existe", "O script testa o arquivo e para com uma mensagem clara (e código 1). Sem esse teste, cada <code>awk</code> do script reclamaria sozinho, como o segundo comando mostra:", T("plog-erro2", "bash analisa-log.sh nada.log; echo \"código: $?\"", "awk '{print $9}' nada.log"))}
"""

def log_ex():
    return (EX(1, "A coluna do status", "No <code>acesso.log</code>, qual campo do awk tem o status (200, 404…)?", "awk '{print ", "$9", "}' acesso.log", rotulo="campo") +
            EX(2, "Juntar antes de contar", "Complete a receita de contagem.", "awk '{print $1}' acesso.log | ", "sort", " | uniq -c", rotulo="comando") +
            MC(3, "Por que <code>uniq -c</code> precisa de <code>sort</code> antes?", ["porque o uniq só lê arquivos ordenados, senão dá erro", "porque ele só junta linhas iguais que estão vizinhas", "porque o sort apaga as linhas vazias", "não precisa"], 2) +
            MC(4, "Qual padrão do awk pega só as respostas de erro (4xx e 5xx)?", ["<code>$9 >= 400</code>", "<code>$9 == \"erro\"</code>", "<code>/erro/</code>", "<code>$1 >= 400</code>"], 1))

def log_miss():
    return (M("plog-m1", "conte quantas linhas do <code>acesso.log</code> são do método POST.", L_M1, r"src:grep;;src:POST;;outre:^3$") +
            M("plog-m2", "some a coluna de bytes (<code>$10</code>) de todas as linhas com <code>awk</code>.", L_M2, r"src:awk;;src:\$10;;outre:^30650$"))

# ---------------------------------------------------------------- vendas
def vendas_corpo():
    return f"""
<h2>O problema</h2>
<p>O <code>vendas.csv</code> tem uma venda por linha: data, vendedor, produto, quantidade e preço unitário. O pedido: <em>total geral, total por vendedor, o produto que mais saiu e um relatório com vírgula decimal, do jeito brasileiro.</em></p>
<hr>
<h2>1. Conhecer o arquivo</h2>
{T("pven-olhar", "head -3 vendas.csv", "wc -l < vendas.csv")}
<p>13 linhas: 1 cabeçalho e 12 vendas. O valor de cada venda é quantidade × preço, ou <code>$4 * $5</code> com <code>-F,</code>.</p>
<hr>
<h2>2. Total geral</h2>
<p><code>NR > 1</code> pula o cabeçalho; o <code>END</code> imprime a soma com duas casas:</p>
{T("pven-total", V_TOTAL)}
<hr>
<h2>3. Por vendedor e por produto</h2>
<p>Um array com o nome como índice acumula o total de cada um. O <code>sort -k2 -rn</code> ordena pela 2ª coluna, do maior para o menor:</p>
{T("pven-vendedor", V_VEND, V_PROD)}
<hr>
<h2>4. Um dia só</h2>
<p>O <code>grep</code> filtra as linhas do dia e o <code>awk</code> soma (aqui não há cabeçalho para pular, porque o grep já o tirou):</p>
{T("pven-dia", V_DIA)}
<hr>
<h2>5. Vírgula decimal</h2>
<p>O <code>printf</code> do awk usa ponto. Um <code>sed</code> no fim troca o ponto pela vírgula. Lembre do <code>\\.</code>: o ponto sozinho, na regex, é “qualquer caractere”:</p>
{T("pven-virgula", V_VIRG)}
<hr>
<h2>6. O relatório completo</h2>
<p>O <code>relatorio-vendas.sh</code> faz tudo numa passada só do <code>awk</code> e usa o <code>PROCINFO["sorted_in"]</code> do gawk para sair já ordenado. No fim, um <code>sed</code> troca o ponto pela vírgula só nos valores (o ponto seguido de dois dígitos no fim da linha):</p>
{T("pven-script", "cat relatorio-vendas.sh", "bash relatorio-vendas.sh")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Esqueceu o -F,", "Sem <code>-F,</code>, o awk separa por espaços. Cada linha vira um campo só, <code>$4</code> e <code>$5</code> ficam vazios e a conta dá 0, sem nenhuma mensagem de erro:", T("pven-erro", V_ERRO))}
{CEN("Ponto sem barra no sed", "Sem a barra, o <code>.</code> casa com o primeiro caractere da linha, que é o 7:", T("pven-erro2", V_ERRO2))}
"""

def vendas_ex():
    return (EX(1, "Valor da venda", "Com <code>-F,</code>, como calcular quantidade × preço?", "awk -F, '{print ", "$4 * $5", "}' vendas.csv", rotulo="conta") +
            EX(2, "Pular o cabeçalho", "Qual padrão pula a primeira linha?", "awk -F, '", "NR > 1", " {print $2}' vendas.csv", rotulo="padrão") +
            MC(3, "Sem <code>-F,</code>, o total das vendas deu 0 porque:", ["o awk não sabe multiplicar", "o awk separou por espaços e os campos 4 e 5 ficaram vazios", "o arquivo tem cabeçalho", "faltou o printf"], 2) +
            MC(4, "Para trocar o ponto decimal por vírgula com sed, use:", ["<code>s/./,/</code>", "<code>s/\\./,/</code>", "<code>s/,/./</code>", "<code>y/,/./</code>"], 2))

def vendas_miss():
    return (M("pven-m1", "calcule o total vendido pela Carla, com duas casas.", V_M1, r"src:awk;;src:Carla;;outre:^209\.90$") +
            M("pven-m2", "some quantas canetas foram vendidas (coluna 4).", V_M2, r"src:awk;;src:caneta;;outre:^35$"))

# ---------------------------------------------------------------- json -> csv
def jcsv_corpo():
    return f"""
<h2>O problema</h2>
<p>O sistema de pedidos exporta <code>pedidos.json</code>, mas o financeiro quer uma planilha: <em>uma linha por item, com o pedido, o cliente, o status e o subtotal.</em> Depois, ainda pedem o total só dos pedidos pagos.</p>
<hr>
<h2>1. Ver a forma do dado</h2>
{T("pjc-olhar", J_OLHAR)}
<p>Cada pedido tem uma lista <code>itens</code>. Como uma linha do CSV é um item, o pedido (pai) precisa ser guardado numa variável com <code>as $p</code>.</p>
<hr>
<h2>2. O conversor</h2>
<p>O <code>pedidos-para-csv.sh</code> escreve o cabeçalho e, para cada item, uma lista com os dados do pedido e do item, terminando em <code>@csv</code>:</p>
{T("pjc-script", "cat pedidos-para-csv.sh", "bash pedidos-para-csv.sh")}
{ANAT((".pedidos[] as $p", "para cada pedido, guarda o pedido em $p."), ("$p.itens[]", "e passa por cada item dele."), ("(.qtd * .preco)", "o subtotal, calculado na hora."), ("@csv", "vira uma linha de CSV, com aspas nos textos."))}
<hr>
<h2>3. Gravar e conferir</h2>
{T("pjc-gravar", "bash pedidos-para-csv.sh > itens.csv", "wc -l itens.csv", "cut -d, -f4,7 itens.csv")}
<hr>
<h2>4. Somar os pagos com awk</h2>
<p>O CSV do <code>@csv</code> tem aspas nos textos. Tire as aspas com <code>tr -d '"'</code> antes de comparar:</p>
{T("pjc-pago", J_PAGO)}
<p>Pedidos pagos: 1042 (25 + 10) e 1044 (15 + 6), total 56.</p>
<hr>
<h2>5. Campos nulos e listas</h2>
<p>No <code>usuarios.json</code>, a Carla não tem e-mail e as tags são uma lista. O <code>//</code> troca o null por vazio e o <code>join</code> transforma a lista em texto:</p>
{T("pjc-usuarios", J_USU)}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Comparar com as aspas lá dentro", "O campo do status é <code>\"pago\"</code>, com aspas. Comparado com <code>pago</code>, nunca é igual, e o total dá 0:", T("pjc-erro", J_PAGO_ERR))}
{CEN("Arquivo com outra forma", "O <code>produto.json</code> não tem <code>.pedidos</code>: o jq recebe null e não consegue passar por ele (“Cannot iterate over null”: não dá para percorrer null). O cabeçalho ainda saiu, porque vem antes dos pedidos; a mensagem de erro apareceu primeiro porque a saída de erro não espera na fila:", T("pjc-erro2", J_ERRO))}
"""

def jcsv_ex():
    return (EX(1, "Guardar o pai", "Complete para guardar cada pedido em <code>$p</code>.", "jq '.pedidos[] ", "as $p", " | $p.itens[] | .produto' pedidos.json", rotulo="trecho") +
            EX(2, "Sem aspas", "Qual comando apaga as aspas do CSV antes do awk?", "bash pedidos-para-csv.sh | ", "tr -d '\"'", " | awk -F, '{print $3}'", rotulo="comando") +
            MC(3, "Por que <code>$3 == \"pago\"</code> no awk deu 0 no CSV do <code>@csv</code>?", ["porque o awk não lê CSV", "porque o campo é <code>\"pago\"</code>, com as aspas", "porque o status está na coluna 2", "porque faltou o -r no jq"], 2) +
            MC(4, "Para um campo null virar texto vazio no CSV:", ["<code>.email // \"\"</code>", "<code>.email | @csv</code>", "<code>.email[]</code>", "<code>del(.email)</code>"], 1))

def jcsv_miss():
    return (M("pjc-m1", "conte quantas linhas o <code>pedidos-para-csv.sh</code> escreve (cabeçalho incluído).", J_M1, r"src:pedidos-para-csv;;src:wc -l;;outre:^7$") +
            M("pjc-m2", "faça um CSV com o id, o cliente e quantos itens cada pedido tem.", J_M2, r"src:@csv;;src:length;;out:1042,\"Bruno\",2;;out:1045,\"Ana\",1"))

# ---------------------------------------------------------------- pipeline
def pipe_corpo():
    return f"""
<h2>O problema</h2>
<p>O log do sistema (<code>log.txt</code>) diz que dois pagamentos falharam. Quem eram esses clientes? A resposta está no <code>pedidos.json</code>. E, de quebra, o chefe quer o total por vendedor em JSON, para mandar a outro sistema. É hora de juntar <code>grep</code>, <code>sed</code>, <code>awk</code> e <code>jq</code>.</p>
<hr>
<h2>1. Tirar os números dos pedidos do log</h2>
<p><code>grep</code> acha as linhas; <code>sed</code> apaga tudo até <code>pedido=</code>, sobrando só o número:</p>
{T("ppl-ids", P_IDS)}
<hr>
<h2>2. Procurar cada pedido no JSON</h2>
<p>Um <code>for</code> passa por cada número e o <code>jq</code> procura o pedido com <code>--argjson</code> (o id é número). Com <code>-e</code>, o jq sai com erro quando não acha nada, e o <code>||</code> avisa:</p>
{T("ppl-cruza", P_CRUZA)}
<p>O pedido 1047 está no log, mas não no <code>pedidos.json</code>: uma pista de que a exportação está desatualizada. Achar isso à mão, num log grande, levaria muito mais tempo.</p>
<hr>
<h2>3. De CSV para JSON</h2>
<p>Agora o caminho contrário. O <code>awk</code> escreve um objeto JSON por linha (as aspas do JSON vão com <code>\\"</code> dentro do printf):</p>
{T("ppl-json", P_JSON)}
<p>E o <code>jq -s</code> junta todos numa lista, agrupa por vendedor e soma:</p>
{T("ppl-agrupa", P_AGRUPA)}
<hr>
<h2>4. O painel</h2>
<p>O <code>painel.sh</code> é o projeto final: cada linha usa a ferramenta certa para o arquivo certo, e o resultado é um resumo da loja inteira:</p>
{T("ppl-painel", "cat painel.sh", "bash painel.sh")}
<hr>
<h2>Qual ferramenta, quando?</h2>
<div class="table-wrap"><table class="ref">
<tr><th>Tarefa</th><th>Ferramenta</th></tr>
<tr><td>achar linhas</td><td><code>grep</code></td></tr>
<tr><td>trocar ou recortar texto numa linha</td><td><code>sed</code></td></tr>
<tr><td>colunas, contas, contagens, relatórios</td><td><code>awk</code></td></tr>
<tr><td>qualquer coisa em JSON</td><td><code>jq</code></td></tr>
<tr><td>ordenar e contar repetidos</td><td><code>sort</code> e <code>uniq -c</code></td></tr>
</table></div>
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("--arg em vez de --argjson", "Com <code>--arg</code>, o id vira o texto <code>\"1042\"</code>, que nunca é igual ao número 1042 do JSON. Não sai nada e nenhum erro aparece, só o “fim”:", T("ppl-erro", P_ERRO))}
{CEN("\\d no sed", "O <code>sed</code> não conhece <code>\\d</code> (isso é do Perl e do Python). A regex não casa e a linha sai inteira, sem troca. Use <code>[0-9]</code>:", T("ppl-erro2", P_ERRO2))}
"""

def pipe_ex():
    return (EX(1, "Id como número", "Qual opção passa o id ao jq como número?", "jq ", "--argjson", " id 1042 '.pedidos[] | select(.id == $id)' pedidos.json", rotulo="opção") +
            EX(2, "Juntar a entrada", "Qual opção do jq junta todos os objetos numa lista?", "awk … | jq ", "-s", " 'length'", rotulo="opção") +
            MC(3, "No sed, para casar um dígito, use:", ["<code>\\d</code>", "<code>[0-9]</code>", "<code>%d</code>", "<code>#</code>"], 2) +
            MC(4, "Para contar quantas vezes cada IP aparece num log, a melhor dupla é:", ["<code>jq</code> e <code>sed</code>", "<code>awk</code> para a coluna e <code>sort | uniq -c</code>", "<code>grep -c</code> sozinho", "<code>cat</code> e <code>tr</code>"], 2))

def pipe_miss():
    return (M("ppl-m1", "conte quantas linhas de nível ERRO o <code>log.txt</code> tem.", P_M1, r"src:grep;;src:ERRO;;outre:^3$") +
            M("ppl-m2", "transforme o <code>vendas.csv</code> em JSON com awk e use o jq para somar só as vendas da Ana.", P_M2, r"src:awk;;src:jq -s;;outre:^277\.3$"))

NIVEL = {"id": "n5", "nome": "Nível 5 · Projetos", "curto": "Projetos", "desc": "Tarefas reais juntando grep, sed, awk e jq", "grupos": [
    {"grupo": "Projetos", "aulas": [
        aula(slug="projeto-log", menu="Analisar um log de acesso", title="Projeto: analisar um log de acesso com awk, sort e uniq", h1='Projeto: analisar um <span class="hl">log</span>',
             desc="Projeto prático: contar visitas, status, IPs e erros de um log de acesso com awk, grep, sed, sort e uniq, e juntar tudo num script.",
             intro="Logs são o texto que mais aparece na vida de quem cuida de sistemas. Neste projeto, um log de site vira um relatório, passo a passo.",
             aprender=["Ler os campos de um log de acesso.", "Contar por status e por IP com <code>sort | uniq -c</code>.", "Montar um script de relatório que confere o arquivo."],
             corpo=log_corpo, exercicios=log_ex, missoes=log_miss,
             ref=[("awk '{print $9}' acesso.log", "a coluna do status."), ("… | sort | uniq -c | sort -rn", "conta e ordena."), ("awk '$9 >= 400' acesso.log", "só os erros."), ("bash analisa-log.sh", "o relatório completo.")],
             resumo=["Olhe o arquivo antes de escrever o comando.", "<code>sort | uniq -c | sort -rn</code> é a receita de contagem.", "Um script deve conferir a entrada antes de começar."]),
        aula(slug="projeto-vendas", menu="Relatório de vendas (CSV)", title="Projeto: relatório de vendas de um CSV com awk e sed", h1='Projeto: relatório de <span class="hl">vendas</span>',
             desc="Projeto prático: totais por vendedor, por produto e por dia de um CSV de vendas com awk, e vírgula decimal com sed.",
             intro="Planilha exportada em CSV é rotina em qualquer empresa. Este projeto tira do <code>vendas.csv</code> um relatório pronto para mandar ao chefe.",
             aprender=["Somar e agrupar colunas de CSV com <code>awk</code>.", "Filtrar um dia com <code>grep</code>.", "Formatar valores com vírgula decimal usando <code>sed</code>."],
             corpo=vendas_corpo, exercicios=vendas_ex, missoes=vendas_miss,
             ref=[("awk -F, 'NR > 1 {t += $4 * $5}'", "soma o valor das vendas."), ("v[$2] += …", "acumula por vendedor."), ("sort -k2 -rn", "ordena pela 2ª coluna, números, do maior."), ("sed 's/\\./,/'", "ponto vira vírgula.")],
             resumo=["<code>-F,</code> e <code>NR > 1</code> em todo CSV com cabeçalho.", "Array com índice de texto agrupa.", "Ponto na regex precisa de <code>\\.</code>."]),
        aula(slug="projeto-json-csv", menu="De JSON para planilha", title="Projeto: converter JSON em CSV com jq e somar com awk", h1='Projeto: de <span class="hl">JSON</span> para planilha',
             desc="Projeto prático: transformar pedidos.json em CSV com uma linha por item usando jq, tratar null e listas, e somar com awk.",
             intro="Dados de API chegam em JSON; o financeiro quer planilha. Este projeto faz a ponte com o <code>jq</code> e confere o resultado com <code>awk</code>.",
             aprender=["Uma linha de CSV por item, com <code>as $p</code>.", "Tratar <code>null</code> e listas na hora de exportar.", "Somar o CSV gerado com <code>awk</code>, sem cair nas aspas."],
             corpo=jcsv_corpo, exercicios=jcsv_ex, missoes=jcsv_miss,
             ref=[(".pedidos[] as $p | $p.itens[]", "item com o pedido à mão."), ("[…] | @csv", "uma linha CSV."), ('.email // ""', "null vira vazio."), ("tr -d '\"'", "tira as aspas antes do awk.")],
             resumo=["Pense em “uma linha é o quê?” antes de escrever o filtro.", "<code>@csv</code> põe aspas nos textos: lembre disso no awk.", "Teste o conversor com um arquivo de outra forma."]),
        aula(slug="projeto-pipeline", menu="Tudo junto: grep, sed, awk e jq", title="Projeto final: grep, sed, awk e jq no mesmo pipeline", h1='Projeto final: <span class="hl">tudo junto</span>',
             desc="Projeto final: cruzar um log de texto com um JSON, converter CSV em JSON com awk e jq, e montar um painel em Bash.",
             intro="O projeto final cruza os três tipos de arquivo da loja: log de texto, CSV e JSON. Cada ferramenta faz a parte em que é melhor.",
             aprender=["Levar dados do texto para o <code>jq</code> com um <code>for</code>.", "Escrever JSON com <code>awk</code> e agrupar com <code>jq -s</code>.", "Escolher a ferramenta certa para cada tarefa."],
             corpo=pipe_corpo, exercicios=pipe_ex, missoes=pipe_miss,
             ref=[("for id in $(…); do jq … ; done", "um jq por item."), ("jq -e … || echo …", "avisa quando não acha."), ("awk '{printf \"{…}\\n\"}' | jq -s", "texto vira lista JSON."), ("bash painel.sh", "o resumo da loja.")],
             resumo=["Cada ferramenta tem seu forte: grep acha, sed troca, awk conta, jq entende JSON.", "Número e texto são diferentes no jq: <code>--argjson</code> para números.", "O <code>sed</code> usa <code>[0-9]</code>, não <code>\\d</code>."]),
    ]},
]}
