# -*- coding: utf-8 -*-
"""Nível 2 · sed, o editor de fluxo."""
from lib_guia import *

def aula(**k):
    return k

# ---------------------------------------------------------------- primeiros passos
def intro_corpo():
    return f"""
<h2>A ideia: uma linha de montagem</h2>
<p>O <code>sed</code> funciona como uma esteira de fábrica. Ele pega <strong>uma linha</strong> do texto, coloca num lugar de trabalho chamado <em>espaço padrão</em> (<em>pattern space</em>), aplica os comandos que você deu, <strong>imprime</strong> o resultado e passa para a próxima linha. O arquivo original não é alterado: o resultado sai na tela (a não ser que você peça o <code>-i</code>, assunto de outra aula).</p>
<p>Com um script vazio (<code>''</code>), o <code>sed</code> não muda nada e só imprime cada linha, como o <code>cat</code>:</p>
{T("sedi-vazio", "sed '' texto.txt")}
{ANAT(("sed", "o programa."), ("'...'", "o script: os comandos do sed, entre aspas simples para o Bash não mexer neles."), ("texto.txt", "o arquivo de entrada. Sem ele, o sed lê da entrada padrão (pipe)."))}
<hr>
<h2>1. Imprimir uma linha: <code>p</code></h2>
<p>O comando <code>p</code> (<em>print</em>) imprime o espaço padrão. Só que o <code>sed</code> já imprime cada linha no fim do ciclo, então <code>2p</code> faz a linha 2 aparecer <strong>duas vezes</strong>:</p>
{T("sedi-2p", "sed '2p' texto.txt", notas={"A rainha": "impressa pelo p"})}
<p>A primeira cópia da linha 2 veio do <code>p</code>; a segunda, da impressão automática do fim do ciclo.</p>
<p>Para ver só o que você pediu, desligue a impressão automática com <code>-n</code> (<em>no print</em>, “sem imprimir”):</p>
{T("sedi-n", "sed -n '2p' texto.txt", "sed -n '$p' texto.txt", "sed -n '2,3p' texto.txt")}
{ANAT(("-n", "não imprime nada sozinho."), ("2,3", "o endereço: linhas 2 a 3 (<code>$</code> é a última)."), ("p", "o comando: imprime."))}
<p>O <code>sed -n '2,3p'</code> faz o papel de um <code>head</code> e <code>tail</code> juntos: mostra um trecho do meio do arquivo.</p>
<hr>
<h2>2. Lendo do pipe</h2>
<p>Sem nome de arquivo, o <code>sed</code> trabalha no que chega pelo <code>|</code>:</p>
{T("sedi-pipe", "grep ERRO log.txt | sed -n '1p'", "echo 'Olá, Ana' | sed ''")}
<hr>
<h2>3. Vários arquivos</h2>
<p>Com mais de um arquivo, o <code>sed</code> trata tudo como um texto só, emendado. Por isso <code>$p</code> pega a última linha do último arquivo:</p>
{T("sedi-varios", "sed -n '$p' nomes.txt frutas.txt")}
<p>Para tratar cada arquivo separado, o GNU sed tem a opção <code>-s</code>:</p>
{T("sedi-s", "sed -s -n '$p' nomes.txt frutas.txt")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Comando que não existe", "Cada letra do script do sed é um comando. Uma letra desconhecida dá este erro, que diz em que caractere do script está o problema:", T("sedi-erro", "sed 'k' texto.txt"))}
{CEN("Esqueceu as aspas", "Sem aspas, o Bash troca o <code>$p</code> pelo valor da variável <code>p</code>, que não existe, ou seja, por nada. O sed recebeu <code>-n texto.txt</code> e achou que <code>texto.txt</code> era o script: o <code>t</code> é o comando de desvio do sed, e “exto.txt” virou o nome de um rótulo que não existe:", T("sedi-erro2", "sed -n $p texto.txt; echo \"código: $?\""), "Use sempre aspas simples em volta do script do sed: <code>sed -n '$p' texto.txt</code>.")}
"""

def intro_ex():
    return (EX(1, "Sem impressão automática", "Qual opção desliga a impressão automática?", "sed ", "-n", " '2p' texto.txt", rotulo="opção") +
            EX(2, "A última linha", "Qual endereço é a última linha?", "sed -n '", "$", "p' log.txt", rotulo="endereço") +
            MC(3, "O que <code>sed '2p' texto.txt</code> (sem <code>-n</code>) mostra?", ["Só a linha 2", "Todas as linhas, com a 2 repetida", "Nada", "As duas primeiras linhas"], 2) +
            MC(4, "O <code>sed</code> sem <code>-i</code> altera o arquivo?", ["Sim, sempre", "Não: o resultado só sai na tela", "Só se o arquivo for pequeno", "Só com p"], 2))

def intro_miss():
    return (M("sedi-m1", "mostre só a linha 3 de <code>texto.txt</code> com o <code>sed</code>.", "sed -n '3p' texto.txt", r"src:\bsed\b;;src:-n;;out:O rato fugiu para o mato.") +
            M("sedi-m2", "mostre as linhas 2 a 4 de <code>vendas.csv</code> com o <code>sed</code>.", "sed -n '2,4p' vendas.csv", r"src:\bsed\b;;src:2,4p;;outre:^2026-03-02,Ana,caderno,3,12\.50$;;outre:^2026-03-02,Carla,mochila,1,89\.90$"))

# ---------------------------------------------------------------- substituir
def subs_corpo():
    return f"""
<h2>A ideia: localizar e substituir</h2>
<p>O comando mais usado do <code>sed</code> é o <code>s</code> (<em>substitute</em>). Ele procura um padrão em cada linha e troca pelo texto que você mandar. É o “localizar e substituir” do editor, só que automático e para quantos arquivos você quiser.</p>
{T("subs-basico", "sed 's/rato/gato/' texto.txt")}
{ANAT(("s", "o comando de substituição."), ("/rato/", "o padrão procurado (pode ser regex)."), ("gato/", "o texto que entra no lugar."), ("texto.txt", "o arquivo."))}
<p>Duas coisas para reparar: só a <strong>primeira</strong> ocorrência de cada linha foi trocada (na última linha, o segundo “rato” continuou), e “Rato” com maiúscula não foi tocado. As <em>flags</em> da próxima aula resolvem as duas coisas.</p>
<hr>
<h2>1. Num pipe</h2>
{T("subs-pipe", "echo 'Olá, mundo' | sed 's/mundo/Ana/'", "grep tema config.txt | sed 's/claro/escuro/'")}
<hr>
<h2>2. Trocando o separador</h2>
<p>A barra <code>/</code> é só costume: o caractere logo depois do <code>s</code> vira o separador. Para trabalhar com caminhos, que têm muitas barras, use <code>#</code> ou <code>|</code> e evite escapar cada barra com <code>\\/</code>:</p>
{T("subs-sep", "echo /home/ana/docs/notas.txt | sed 's/\\/home\\/ana/~/'", "echo /home/ana/docs/notas.txt | sed 's#/home/ana#~#'")}
<hr>
<h2>3. O padrão é uma regex</h2>
<p>O que vem entre as duas primeiras barras é uma expressão regular (a <a href="regex.html">aula de regex</a> do Nível 1). Aqui, <code>[0-9]*</code> pega o número do pedido inteiro:</p>
{T("subs-regex", "grep pedido= log.txt | sed 's/pedido=[0-9]*/pedido=XXXX/'")}
<hr>
<h2>4. O <code>&amp;</code>: o pedaço que casou</h2>
<p>No texto de troca, <code>&amp;</code> significa “o que o padrão encontrou”. Dá para embrulhar o achado sem reescrevê-lo:</p>
{T("subs-e", "sed 's/[0-9][0-9]*/[&]/' notas.txt", "echo 'preço: 12.50' | sed 's/[0-9.]*$/R$ &/'")}
<p>Para um <code>&amp;</code> de verdade no texto, escreva <code>\\&amp;</code>.</p>
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Faltou a última barra", "O <code>s</code> precisa de três separadores: <code>s/padrão/troca/</code>. Faltando o último, o sed reclama:", T("subs-erro", "sed 's/rato/gato' texto.txt"))}
{CEN("Barra no meio do texto", "Se o padrão ou a troca tiver uma barra, ela fecha o comando antes da hora. Aqui o sed achou que <code>ana/</code> eram as flags:", T("subs-erro2", "echo /home/ana | sed 's//home/ana/~/'"), "Escape a barra (<code>\\/</code>) ou troque o separador: <code>s#/home/ana#~#</code>.")}
"""

def subs_ex():
    return (EX(1, "O comando", "Complete para trocar rato por gato:", "sed '", "s/rato/gato/", "' texto.txt") +
            EX(2, "O que casou", "Qual símbolo, no texto de troca, representa o que o padrão encontrou?", "sed 's/[0-9]*/(", "&", ")/' notas.txt", rotulo="símbolo") +
            MC(3, "Sem flags, quantas ocorrências por linha o <code>s</code> troca?", ["Todas", "Só a primeira", "Só a última", "Nenhuma"], 2) +
            MC(4, "Qual comando troca <code>/home/ana</code> por <code>~</code> sem escapar barras?", ["<code>s/home/ana/~/</code>", "<code>s#/home/ana#~#</code>", "<code>s/\\home\\ana/~/</code>", "<code>y/home/~/</code>"], 2))

def subs_miss():
    return (M("subs-m1", "troque <code>claro</code> por <code>escuro</code> em <code>config.txt</code> (mostre o arquivo inteiro com a troca).", "sed 's/claro/escuro/' config.txt", r"src:\bsed\b;;src:s/claro/escuro/;;out:tema=escuro;;out:porta=8080") +
            M("subs-m2", "em <code>config.txt</code>, troque o número da porta <code>8080</code> por <code>9090</code>.", "sed 's/8080/9090/' config.txt", r"src:\bsed\b;;src:s.8080.9090.;;out:porta=9090;;out:nome=Loja da Ana"))

# ---------------------------------------------------------------- flags
def flags_corpo():
    return f"""
<h2>A ideia: ajustar o <code>s</code></h2>
<p>Depois da última barra do <code>s///</code> vêm as <strong>flags</strong>, letras que mudam o jeito da troca: todas as ocorrências, sem diferenciar maiúsculas, só a enésima, imprimir só o que mudou.</p>
<hr>
<h2>1. <code>g</code>: todas as ocorrências</h2>
<p>Sem <code>g</code> (<em>global</em>), só a primeira de cada linha muda. Com <code>g</code>, todas:</p>
{T("flags-g", "echo 'banana' | sed 's/a/A/'", "echo 'banana' | sed 's/a/A/g'")}
<hr>
<h2>2. <code>I</code>: sem diferenciar maiúsculas</h2>
<p>A flag <code>I</code> (do GNU sed; também aceita <code>i</code>) faz “rato”, “Rato” e “RATO” casarem. Juntando com <code>g</code>, a última linha de <code>texto.txt</code> finalmente troca as duas:</p>
{T("flags-i", "sed 's/rato/gato/gI' texto.txt")}
{ANAT(("s/rato/gato/", "a substituição."), ("g", "todas as ocorrências da linha."), ("I", "sem diferenciar maiúsculas de minúsculas."))}
<p>Repare: “Rato” virou “gato”, com g minúsculo, porque o texto de troca é exatamente o que você escreveu.</p>
<hr>
<h2>3. Um número: só a enésima</h2>
<p>Um número escolhe qual ocorrência trocar. Com número e <code>g</code> juntos, troca dessa em diante:</p>
{T("flags-num", "echo 'a-b-c-d' | sed 's/-/+/2'", "echo 'a-b-c-d' | sed 's/-/+/2g'")}
<hr>
<h2>4. <code>p</code> com <code>-n</code>: só as linhas que mudaram</h2>
<p>A flag <code>p</code> imprime a linha quando a troca aconteceu. Com <code>-n</code>, você vê só as linhas alteradas, ótimo para conferir antes de gravar:</p>
{T("flags-p", "sed -n 's/ERRO/FALHA/p' log.txt")}
<hr>
<h2>5. <code>w</code>: gravar as linhas alteradas</h2>
<p>A flag <code>w arquivo</code> grava num arquivo as linhas que mudaram (precisa ser a última flag):</p>
{T("flags-w", "sed -n 's/AVISO/ATENÇÃO/w avisos.txt' log.txt", "cat avisos.txt")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Flag desconhecida", "Uma letra que não é flag depois da última barra:", T("flags-erro", "sed 's/a/A/x' frutas.txt"))}
{CEN("Número zero", "As ocorrências contam a partir de 1:", T("flags-erro2", "sed 's/a/A/0' frutas.txt"))}
"""

def flags_ex():
    return (EX(1, "Todas", "Qual flag troca todas as ocorrências?", "sed 's/a/A/", "g", "' frutas.txt", rotulo="flag") +
            EX(2, "Sem maiúsculas", "Complete para trocar rato e Rato:", "sed 's/rato/gato/", ["gI", "Ig", "gi", "ig"], "' texto.txt", rotulo="flags") +
            EX(3, "A segunda", "Complete para trocar só o 2º hífen:", "echo a-b-c | sed 's/-/+/", "2", "'", rotulo="número") +
            MC(4, "Para ver só as linhas que mudaram, use:", ["<code>sed 's/a/b/g'</code>", "<code>sed -n 's/a/b/p'</code>", "<code>sed 's/a/b/w'</code>", "<code>sed -p 's/a/b/'</code>"], 2) +
            MC(5, "<code>echo a-b-c-d | sed 's/-/+/2g'</code> dá:", ["<code>a+b+c+d</code>", "<code>a-b+c+d</code>", "<code>a-b+c-d</code>", "<code>a+b-c-d</code>"], 2))

def flags_miss():
    return (M("flags-m1", "troque todos os <code>a</code> por <code>4</code> em <code>frutas.txt</code>.", "sed 's/a/4/g' frutas.txt", r"src:\bsed\b;;src:/g;;outre:^b4n4n4$;;outre:^l4r4nj4$") +
            M("flags-m2", "mostre só as linhas de <code>log.txt</code> em que <code>login</code> foi trocado por <code>ENTRADA</code>.", "sed -n 's/login/ENTRADA/p' log.txt", r"src:\bsed\b;;src:-n;;src:/p;;out:INFO  ENTRADA usuario=ana;;out:ENTRADA usuario=carla"))

# ---------------------------------------------------------------- endereços
def end_corpo():
    return f"""
<h2>A ideia: escolher as linhas</h2>
<p>Todo comando do <code>sed</code> pode vir precedido de um <strong>endereço</strong>, que diz em quais linhas ele vale. Sem endereço, vale em todas. Os endereços servem para <code>p</code>, <code>s</code>, <code>d</code> e todos os outros.</p>
<hr>
<h2>1. Número de linha e faixa</h2>
{T("end-num", "sed '2s/caderno/CADERNO/' vendas.csv | head -3", "sed '2s/caderno/CADERNO/' vendas.csv | grep -i caderno", "sed -n '2,4p' notas.txt")}
<p>Repare no segundo comando: só a linha 2 ganhou “CADERNO”; os outros cadernos do arquivo continuaram minúsculos.</p>
{ANAT(("2", "endereço: só a linha 2."), ("s/caderno/CADERNO/", "o comando que vale nessa linha."))}
<hr>
<h2>2. A última linha: <code>$</code></h2>
{T("end-ultima", "sed -n '$p' vendas.csv", "sed '$s/carla/CARLA/' log.txt | tail -2")}
<hr>
<h2>3. Uma regex: <code>/padrão/</code></h2>
<p>Entre barras, o endereço vira “as linhas que casam com o padrão”. É o <code>grep</code> dentro do <code>sed</code>, com a vantagem de poder <strong>editar</strong> só essas linhas:</p>
{T("end-regex", "sed -n '/AVISO/p' log.txt", "sed '/ERRO/s/pagamento/PAGAMENTO/' log.txt | head -3")}
<hr>
<h2>4. Faixas com regex e misturadas</h2>
<p>Uma faixa pode começar e terminar em padrões: de uma linha com “ERRO” até a próxima com “AVISO”. Quando a faixa fecha, o sed volta a procurar o começo, por isso o trecho se repetiu a partir do ERRO seguinte. Também dá para misturar número e regex (da linha 8 até a próxima com “carla”):</p>
{T("end-faixa", "sed -n '/ERRO/,/AVISO/p' log.txt", "sed -n '8,/carla/p' log.txt")}
<hr>
<h2>5. Negação e passo</h2>
<p>O <code>!</code> depois do endereço inverte: “todas as linhas <strong>menos</strong> essas”. O GNU sed também aceita <code>início~passo</code>: <code>1~2</code> são as linhas ímpares; <code>2~2</code>, as pares:</p>
{T("end-neg", "sed -n '/INFO/!p' log.txt", "sed -n '1~2p' nomes.txt")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Linha zero", "As linhas começam em 1. O endereço 0 só é aceito no formato especial <code>0,/regex/</code>:", T("end-erro", "sed -n '0p' texto.txt"))}
{CEN("Barra sem fechar no endereço", "O endereço de regex também precisa das duas barras:", T("end-erro2", "sed -n '/ERRO p' log.txt"))}
"""

def end_ex():
    return (EX(1, "Só a linha 5", "Complete para imprimir só a linha 5:", "sed -n '", "5p", "' log.txt") +
            EX(2, "Faixa", "Complete para imprimir as linhas 2 a 6:", "sed -n '", "2,6p", "' log.txt") +
            EX(3, "Por padrão", "Complete para imprimir as linhas com ERRO:", "sed -n '", "/ERRO/p", "' log.txt") +
            MC(4, "O que <code>sed -n '/INFO/!p' log.txt</code> mostra?", ["Só as linhas com INFO", "As linhas sem INFO", "Nada", "Um erro"], 2) +
            MC(5, "No GNU sed, <code>1~2</code> significa:", ["linhas 1 e 2", "linhas ímpares", "linhas pares", "da linha 1 à 2"], 2))

def end_miss():
    return (M("end-m1", "com um endereço de regex, mostre só as linhas de <code>log.txt</code> que têm <code>logout</code> ou <code>login</code> (dica: <code>/log/</code> pega <code>log</code>in e <code>log</code>out).", "sed -n '/log/p' log.txt", r"src:\bsed\b;;src:-n;;src:/log;;out:logout usuario=ana;;out:login usuario=carla") +
            M("end-m2", "troque <code>ERRO</code> por <code>FALHA</code> só nas linhas 1 a 5 de <code>log.txt</code> (mostre o arquivo inteiro).", "sed '1,5s/ERRO/FALHA/' log.txt", r"src:\bsed\b;;src:1,5s;;out:08:17:45 FALHA;;out:10:45:20 ERRO"))

# ---------------------------------------------------------------- apagar
def del_corpo():
    return f"""
<h2>A ideia: jogar linhas fora</h2>
<p>O comando <code>d</code> (<em>delete</em>) descarta a linha: ela não é impressa e o <code>sed</code> já passa para a próxima. Junto com os endereços da aula anterior, é a forma mais rápida de limpar um arquivo: tirar comentários, linhas vazias, cabeçalho.</p>
<hr>
<h2>1. Apagar por número</h2>
{T("del-num", "sed '1d' vendas.csv | head -3", "sed '2,8d' log.txt", notas={"2026-03-02,Ana": "o cabeçalho (linha 1) sumiu"})}
<hr>
<h2>2. Apagar comentários e linhas vazias</h2>
<p>O <code>config.txt</code> tem comentários (linhas que começam com <code>#</code>) e uma linha vazia. <code>/^#/d</code> apaga as primeiras; <code>/^$/d</code>, as vazias (começo e fim colados):</p>
{T("del-config", "cat config.txt", "sed '/^#/d' config.txt", "sed '/^#/d; /^$/d' config.txt")}
{ANAT(("/^#/", "endereço: linhas que começam com #."), ("d", "apaga."), (";", "separa dois comandos."), ("/^$/d", "apaga as linhas vazias."))}
<hr>
<h2>3. Apagar tudo menos...</h2>
<p>Com <code>!</code>, o <code>d</code> apaga as linhas que <strong>não</strong> casam. <code>/ERRO/!d</code> é o mesmo que <code>grep ERRO</code>:</p>
{T("del-neg", "sed '/ERRO/!d' log.txt")}
<hr>
<h2>4. Apagar a última linha</h2>
{T("del-ultima", "sed '$d' nomes.txt")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Regex sem fechar", "No endereço <code>/^#/</code>, esquecer a barra de fechamento faz o sed achar que o <code>d</code> ainda é parte do padrão:", T("del-erro", "sed '/^#d' config.txt"))}
{CEN("O d não leva texto", "O <code>d</code> é um comando sozinho; texto depois dele vira lixo:", T("del-erro2", "sed '1d linha' vendas.csv"))}
"""

def del_ex():
    return (EX(1, "O cabeçalho", "Complete para apagar a linha 1:", "sed '", "1d", "' vendas.csv") +
            EX(2, "Linhas vazias", "Complete o endereço das linhas vazias:", "sed '", "/^$/", "d' config.txt", rotulo="endereço") +
            MC(3, "<code>sed '/ERRO/!d' log.txt</code> é parecido com:", ["<code>grep -v ERRO log.txt</code>", "<code>grep ERRO log.txt</code>", "<code>cat log.txt</code>", "<code>wc -l log.txt</code>"], 2) +
            MC(4, "Qual endereço pega as linhas de comentário que começam com <code>#</code>?", ["<code>/#$/</code>", "<code>/^#/</code>", "<code>#d</code>", "<code>/#/!</code>"], 2))

def del_miss():
    return (M("del-m1", "mostre <code>config.txt</code> sem os comentários e sem a linha vazia.", "sed '/^#/d; /^$/d' config.txt", r"src:\bsed\b;;src:\^#;;src:\^\$;;outre:^nome=Loja da Ana$;;outre:^idioma=pt-BR$") +
            M("del-m2", "apague todas as linhas de <code>log.txt</code> que têm <code>INFO</code>.", "sed '/INFO/d' log.txt", r"src:\bsed\b;;src:/INFO/d;;out:AVISO disco 85% cheio;;out:ERRO  tempo esgotado"))

# ---------------------------------------------------------------- inserir
def ins_corpo():
    return f"""
<h2>A ideia: acrescentar linhas inteiras</h2>
<p>Três comandos colocam texto novo: <code>i</code> (<em>insert</em>) insere <strong>antes</strong> da linha, <code>a</code> (<em>append</em>) acrescenta <strong>depois</strong> e <code>c</code> (<em>change</em>) <strong>troca</strong> a linha inteira. No GNU sed, o texto pode vir na mesma linha do comando.</p>
<hr>
<h2>1. <code>i</code>: antes</h2>
<p>Um cabeçalho novo para o <code>nomes.txt</code>:</p>
{T("ins-i", "sed '1i NOMES' nomes.txt | head -3")}
{ANAT(("1", "o endereço: a linha 1."), ("i", "inserir antes."), ("NOMES", "o texto da linha nova."))}
<hr>
<h2>2. <code>a</code>: depois</h2>
<p>Acrescentar uma configuração depois da linha do <code>debug</code>, e uma linha no fim do arquivo (<code>$a</code>):</p>
{T("ins-a", "sed '/^debug/a log=sim' config.txt", "sed '$a Gabriel' nomes.txt | tail -2")}
<hr>
<h2>3. <code>c</code>: trocar a linha inteira</h2>
<p>Diferente do <code>s</code>, que troca um pedaço, o <code>c</code> joga fora a linha toda e põe outra:</p>
{T("ins-c", "sed '/^porta=/c porta=9090' config.txt")}
<hr>
<h2>4. A forma clássica, com barra invertida</h2>
<p>O padrão POSIX pede o texto na linha de baixo, depois de <code>\\</code>. Num script de uma linha, o GNU sed aceita <code>i\\texto</code> também. Você vai ver muito essa forma em scripts antigos:</p>
{T("ins-classico", "sed '2i\\--- divisória ---' texto.txt")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Comando sem texto", "O <code>a</code>, o <code>i</code> e o <code>c</code> precisam do texto que vão colocar:", T("ins-erro", "sed '1a' nomes.txt"))}
"""

def ins_ex():
    return (EX(1, "Antes", "Qual comando insere antes da linha?", "sed '1", "i", " TÍTULO' nomes.txt", rotulo="comando") +
            EX(2, "Depois da última", "Complete para acrescentar depois da última linha:", "sed '", "$a", " FIM' nomes.txt") +
            MC(3, "Qual a diferença entre <code>c</code> e <code>s</code>?", ["Nenhuma", "O <code>c</code> troca a linha inteira; o <code>s</code>, um pedaço", "O <code>s</code> troca a linha inteira", "O <code>c</code> apaga a linha"], 2) +
            MC(4, "<code>sed '/^debug/a log=sim' config.txt</code> põe <code>log=sim</code>:", ["antes da linha do debug", "depois da linha do debug", "no lugar da linha do debug", "no fim do arquivo"], 2))

def ins_miss():
    return (M("ins-m1", "insira a linha <code>FRUTAS</code> antes da primeira linha de <code>frutas.txt</code>.", "sed '1i FRUTAS' frutas.txt", r"src:\bsed\b;;src:1i;;outre:^FRUTAS\nbanana$") +
            M("ins-m2", "troque a linha inteira do <code>tema</code> em <code>config.txt</code> por <code>tema=escuro</code>, usando o comando <code>c</code>.", "sed '/^tema/c tema=escuro' config.txt", r"src:\bsed\b;;src:c\s*\\?tema=escuro;;out:tema=escuro;;out:idioma=pt-BR"))

# ---------------------------------------------------------------- -i
def inplace_corpo():
    return f"""
<h2>A ideia: gravar a mudança no próprio arquivo</h2>
<p>Até aqui, o <code>sed</code> só mostrou o resultado na tela. A opção <code>-i</code> (<em>in-place</em>, “no lugar”) <strong>grava</strong> a mudança no arquivo. É poderosa e perigosa: não tem “desfazer”. Por isso, a regra do guia é <strong>só usar <code>-i</code> na pasta de teste</strong> e, de preferência, com backup.</p>
<div class="warning"><strong>Confira antes de gravar</strong><p>Rode o comando <strong>sem</strong> <code>-i</code> primeiro e olhe a saída. Só quando estiver certo, acrescente o <code>-i</code>. Se estragar, recrie os arquivos com <code>bash criar-arquivos.sh</code>.</p></div>
<hr>
<h2>1. <code>-i</code>: gravar</h2>
<p>Repare que o <code>sed -i</code> não mostra nada na tela. O resultado está no arquivo:</p>
{T("inp-i", "sed -i 's/claro/escuro/' config.txt", "grep tema config.txt")}
<hr>
<h2>2. <code>-i.bak</code>: gravar com backup</h2>
<p>Com um sufixo colado no <code>-i</code>, o <code>sed</code> guarda uma cópia do original antes de gravar:</p>
{T("inp-bak", "sed -i.bak 's/8080/9090/' config.txt", "ls config.txt*", "grep porta config.txt config.txt.bak")}
{ANAT(("-i.bak", "grava no arquivo e guarda o original como config.txt.bak."), ("s/8080/9090/", "a mudança."), ("config.txt", "o arquivo alterado."))}
<p>Para desfazer, basta trazer o backup de volta: <code>mv config.txt.bak config.txt</code>.</p>
<hr>
<h2>3. Vários arquivos de uma vez</h2>
<p>O <code>-i</code> vale para todos os arquivos da linha, cada um gravado separadamente. Aqui, “Ana” virou “Aninha” nos dois de uma vez (e “ana paula”, minúsculo, ficou como estava):</p>
{T("inp-varios", "sed -i 's/Ana/Aninha/' nomes.txt vendas.csv", "grep -c Aninha nomes.txt vendas.csv")}
<hr>
<h2>4. O cuidado com o <code>-n</code></h2>
<p><code>-n</code> com <code>-i</code> grava <strong>só o que foi impresso</strong>. Esquecer o <code>p</code> deixa o arquivo vazio:</p>
{T("inp-n", "sed -n -i 's/ERRO/FALHA/' log.txt", "wc -l log.txt")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("-i sem arquivo", "O <code>-i</code> precisa de um arquivo para gravar; não funciona com pipe:", T("inp-erro", "echo teste | sed -i 's/t/T/'"))}
{CEN("-in não é -i -n", "O que vem colado no <code>-i</code> é o sufixo do backup. <code>-in</code> não liga o <code>-n</code>: cria um backup com sufixo <code>n</code>:", T("inp-erro2", "sed -in 's/uva/UVA/' frutas.txt", "ls frutas*"), "Escreva <code>-n -i</code> separados, ou <code>-ni</code>.")}
"""

def inplace_ex():
    return (EX(1, "Gravar", "Qual opção grava a mudança no arquivo?", "sed ", "-i", " 's/a/b/' frutas.txt", rotulo="opção") +
            EX(2, "Com backup", "Complete para guardar o original como .bak:", "sed ", "-i.bak", " 's/a/b/' frutas.txt") +
            MC(3, "O que <code>sed -i</code> mostra na tela quando dá certo?", ["O arquivo alterado", "Nada", "Só as linhas alteradas", "Uma mensagem de sucesso"], 2) +
            MC(4, "<code>sed -in 's/a/b/' frutas.txt</code>:", ["liga -i e -n", "grava e cria o backup <code>frutas.txtn</code>", "dá erro", "só mostra na tela"], 2))

def inplace_miss():
    return (M("inp-m1", "troque <code>sim</code> por <code>nao</code> no <code>debug</code> de <code>config.txt</code> com <code>-i</code> e depois mostre a linha com <code>grep debug config.txt</code>.", ["sed -i 's/debug=sim/debug=nao/' config.txt", "grep debug config.txt"], r"src:sed -i;;src:\bgrep\b;;outre:^debug=nao$") +
            M("inp-m2", "com <code>-i.bak</code>, troque <code>uva</code> por <code>kiwi</code> em <code>frutas.txt</code> e liste os arquivos <code>frutas*</code>.", ["sed -i.bak 's/uva/kiwi/' frutas.txt", "ls frutas*"], r"src:-i\.bak;;src:\bls\b;;out:frutas.txt.bak"))

# ---------------------------------------------------------------- -E e grupos
def ext_corpo():
    return f"""
<h2>A ideia: lembrar pedaços e reorganizar</h2>
<p>Com parênteses, a regex <strong>guarda</strong> o que casou em cada grupo. No texto de troca, <code>\\1</code> é o primeiro grupo, <code>\\2</code> o segundo, e assim por diante. Com isso dá para inverter nome e sobrenome, mudar o formato de datas e extrair pedaços. Com <code>-E</code> (regex estendida), os parênteses e o <code>+</code> funcionam sem barra invertida.</p>
<hr>
<h2>1. <code>-E</code>: regex estendida</h2>
<p>Sem <code>-E</code>, <code>+</code> é um caractere comum, e o sed procurou um “+” no texto e não achou nada. Com <code>-E</code>, <code>[0-9]+</code> é “um ou mais dígitos”:</p>
{T("ext-e", "echo 'pedido 1042' | sed 's/[0-9]+/N/'", "echo 'pedido 1042' | sed -E 's/[0-9]+/N/'")}
<hr>
<h2>2. Grupos e <code>\\1</code></h2>
<p>Inverter “Nome Sobrenome” para “Sobrenome, Nome” no <code>contatos.txt</code>:</p>
{T("ext-grupos", "sed -E 's/^([A-Za-z]+) ([A-Za-z]+);.*/\\2, \\1/' contatos.txt")}
{ANAT(("^([A-Za-z]+)", "grupo 1: a primeira palavra (o nome)."), (" ", "o espaço entre as duas."), ("([A-Za-z]+)", "grupo 2: o sobrenome."), (";.*", "o resto da linha (vai embora)."), ("\\2, \\1", "a troca: sobrenome, vírgula, nome."))}
<hr>
<h2>3. Mudando o formato da data</h2>
<p>De <code>2026-03-02</code> (ano-mês-dia) para <code>02/03/2026</code>, no começo de cada linha do log:</p>
{T("ext-data", "sed -E 's/^([0-9]{4})-([0-9]{2})-([0-9]{2})/\\3\\/\\2\\/\\1/' log.txt | head -3", "sed -E 's#^([0-9]{4})-([0-9]{2})-([0-9]{2})#\\3/\\2/\\1#' log.txt | head -3")}
<p>As duas linhas fazem o mesmo; a segunda usa <code>#</code> como separador e fica mais legível.</p>
<hr>
<h2>4. Extrair um pedaço</h2>
<p>Casando a linha inteira e devolvendo só um grupo, o <code>sed</code> extrai: aqui, só o e-mail de cada contato:</p>
{T("ext-extrair", "sed -E 's/.*;(.*)$/\\1/' contatos.txt")}
<hr>
<h2>5. Maiúsculas e minúsculas: <code>\\U</code>, <code>\\L</code>, <code>\\u</code></h2>
<p>O GNU sed tem códigos especiais na troca: <code>\\U</code> passa para maiúsculas até o fim (ou até <code>\\E</code>), <code>\\L</code> para minúsculas e <code>\\u</code> só a próxima letra. Diferente do <code>tr</code>, funciona com acentos:</p>
{T("ext-case", "sed -E 's/^(.)/\\u\\1/' nomes.txt", "echo 'maçã e pão' | sed 's/.*/\\U&/'")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("\\1 sem grupo", "Sem <code>-E</code>, os parênteses são caracteres comuns, e não existe grupo 1:", T("ext-erro", "sed 's/(rato)/[\\1]/' texto.txt"), "Use <code>-E</code> (ou escreva <code>\\(rato\\)</code> na regex básica).")}
"""

def ext_ex():
    return (EX(1, "Regex estendida", "Qual opção liga a regex estendida no sed?", "sed ", "-E", " 's/[0-9]+/N/' log.txt", rotulo="opção") +
            EX(2, "O segundo grupo", "Complete para devolver só o segundo grupo:", "sed -E 's/(a+)(b+)/", "\\2", "/'") +
            MC(3, "No texto de troca, <code>\\1</code> significa:", ["a linha 1", "o que casou no primeiro grupo de parênteses", "a primeira letra", "uma barra e um 1"], 2) +
            MC(4, "Qual comando deixa tudo em maiúsculas, com acentos?", ["<code>tr a-z A-Z</code>", "<code>sed 's/.*/\\U&amp;/'</code>", "<code>sed 'y/a-z/A-Z/'</code>", "<code>sed -U</code>"], 2))

def ext_miss():
    return (M("ext-m1", "com <code>sed -E</code> e grupos, mostre só os nomes completos (o que vem antes do primeiro <code>;</code>) de <code>contatos.txt</code>.", "sed -E 's/^([^;]+);.*/\\1/' contatos.txt", r"src:sed -E;;src:\\1;;outre:^Ana Souza$;;outre:^Diego Rocha$") +
            M("ext-m2", "mude a data de <code>vendas.csv</code> de <code>2026-03-02</code> para <code>02/03/2026</code> em todas as linhas.", "sed -E 's#^([0-9]{4})-([0-9]{2})-([0-9]{2})#\\3/\\2/\\1#' vendas.csv", r"src:sed -E;;src:\\3;;out:02/03/2026,Ana,caderno;;out:05/03/2026,Ana,caderno,4,12.50"))

# ---------------------------------------------------------------- vários comandos
def varios_corpo():
    return f"""
<h2>A ideia: uma receita com vários passos</h2>
<p>Um script do <code>sed</code> pode ter vários comandos. Eles rodam em ordem, <strong>na mesma linha</strong>, antes de ela ser impressa. Há três jeitos de juntar: várias opções <code>-e</code>, o ponto e vírgula <code>;</code> e as chaves <code>{{ }}</code> para agrupar comandos sob um endereço. Quando a receita cresce, ela vai para um arquivo e roda com <code>-f</code>.</p>
<hr>
<h2>1. <code>-e</code> e <code>;</code></h2>
{T("var-e", "sed -e 's/rato/gato/g' -e 's/Rato/Gato/' texto.txt", "sed 's/rato/gato/g; s/Rato/Gato/' texto.txt")}
<p>As duas formas deram o mesmo resultado. A ordem importa: cada comando trabalha no resultado do anterior.</p>
<hr>
<h2>2. Chaves: vários comandos num endereço</h2>
<p>Só nas linhas de ERRO: trocar ERRO por FALHA e espremer os dois espaços num só:</p>
{T("var-chaves", "sed '/ERRO/{s/ERRO/FALHA/; s/  / /}' log.txt | head -3")}
{ANAT(("/ERRO/", "endereço: as linhas com ERRO."), ("{", "começa o grupo."), ("s/ERRO/FALHA/", "1º comando do grupo."), ("; s/  / /", "2º comando: dois espaços viram um."), ("}", "fecha o grupo."))}
<hr>
<h2>3. Um script em arquivo: <code>-f</code></h2>
<p>O arquivo <code>limpa.sed</code> dos exemplos tem três comandos, um por linha, e comentários com <code>#</code>. O <code>-f</code> (<em>file</em>) lê o script do arquivo:</p>
{T("var-f", "cat limpa.sed", "sed -f limpa.sed config.txt")}
<div class="tip"><strong>Script executável</strong><p>Se a primeira linha do arquivo for <code>#!/usr/bin/sed -f</code> e ele tiver permissão de execução (<code>chmod +x</code>), dá para rodar como <code>./limpa.sed config.txt</code>.</p></div>
<hr>
<h2>4. Comandos que param: <code>q</code></h2>
<p>O <code>q</code> (<em>quit</em>) imprime a linha atual e encerra o sed. <code>3q</code> é um <code>head -3</code>; com um endereço de regex, para no primeiro achado:</p>
{T("var-q", "sed '3q' log.txt", "sed -n '/ERRO/{p;q}' log.txt")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Chave sem fechar", "Abriu <code>{</code>, tem de fechar com <code>}</code>:", T("var-erro", "sed '/ERRO/{s/ERRO/FALHA/' log.txt"))}
{CEN("Script que não existe", "O <code>-f</code> precisa de um arquivo de script que exista:", T("var-erro2", "sed -f nada.sed config.txt"))}
"""

def varios_ex():
    return (EX(1, "Separador", "Qual caractere separa dois comandos na mesma string?", "sed 's/a/b/", ";", " s/c/d/' arq", rotulo="caractere") +
            EX(2, "Script em arquivo", "Qual opção lê o script de um arquivo?", "sed ", "-f", " limpa.sed config.txt", rotulo="opção") +
            MC(3, "Em <code>sed '/ERRO/{s/a/b/; s/c/d/}'</code>, os dois <code>s</code> valem:", ["em todas as linhas", "só nas linhas com ERRO", "só na primeira linha", "em nenhuma"], 2) +
            MC(4, "<code>sed '3q' log.txt</code> faz o mesmo que:", ["<code>tail -3</code>", "<code>head -3</code>", "<code>wc -l</code>", "<code>sed '3d'</code>"], 2))

def varios_miss():
    return (M("var-m1", "rode o script <code>limpa.sed</code> no <code>config.txt</code>.", "sed -f limpa.sed config.txt", r"src:sed -f limpa\.sed;;out:porta = 8080;;out:idioma = pt-BR") +
            M("var-m2", "com chaves, só nas linhas de <code>log.txt</code> com <code>AVISO</code>, troque <code>AVISO</code> por <code>ATENCAO</code> e <code>disco</code> por <code>DISCO</code>; mostre só essas linhas (use <code>-n</code> e <code>p</code> dentro das chaves).", "sed -n '/AVISO/{s/AVISO/ATENCAO/; s/disco/DISCO/; p}' log.txt", r"src:\{;;src:\};;out:ATENCAO DISCO 85% cheio;;out:ATENCAO estoque baixo"))

# ---------------------------------------------------------------- y e hold
def hold_corpo():
    return f"""
<h2>A ideia: duas ferramentas a mais</h2>
<p>Esta aula fecha o <code>sed</code> com dois recursos menos usados, mas que resolvem problemas que o <code>s</code> não resolve bem: o <code>y</code>, que troca caractere por caractere (como o <code>tr</code>), e o <strong>espaço reserva</strong> (<em>hold space</em>), uma segunda área de trabalho onde o <code>sed</code> guarda texto entre uma linha e outra.</p>
<hr>
<h2>1. <code>y</code>: trocar letras</h2>
<p><code>y/origem/destino/</code> troca cada caractere da origem pelo da mesma posição no destino. Diferente do <code>tr</code>, o GNU sed entende acentos em UTF-8, então serve para tirar acentos:</p>
{T("hold-y", "echo 'maçã e pão' | sed 'y/áãçé/aace/'", "sed 'y/abc/ABC/' frutas.txt | head -3")}
<p>O <code>y</code> não aceita faixas: <code>y/a-z/A-Z/</code> trocaria só “a”, “-” e “z”. Para maiúsculas, use <code>s/.*/\\U&amp;/</code>.</p>
<hr>
<h2>2. O espaço reserva: <code>h</code>, <code>H</code>, <code>g</code>, <code>G</code>, <code>x</code></h2>
<div class="table-wrap"><table class="ref">
<tr><th>Comando</th><th>O que faz</th></tr>
<tr><td><code>h</code></td><td>copia o espaço padrão para o reserva (apaga o que havia lá)</td></tr>
<tr><td><code>H</code></td><td>acrescenta o espaço padrão no reserva, com uma quebra de linha antes</td></tr>
<tr><td><code>g</code></td><td>copia o reserva para o espaço padrão</td></tr>
<tr><td><code>G</code></td><td>acrescenta o reserva no espaço padrão, com uma quebra de linha antes</td></tr>
<tr><td><code>x</code></td><td>troca os dois de lugar</td></tr>
</table></div>
<p>O exemplo mais simples: <code>G</code> sozinho acrescenta o reserva, que está vazio, a cada linha. Resultado: uma linha em branco depois de cada linha (espaçamento duplo):</p>
{T("hold-G", "sed G texto.txt")}
<hr>
<h2>3. Juntar todas as linhas numa só</h2>
<p><code>H</code> vai acumulando cada linha no reserva; na última (<code>$</code>), o <code>x</code> traz tudo de volta, o <code>s</code> troca as quebras de linha (<code>\\n</code>) por vírgulas e o <code>p</code> imprime:</p>
{T("hold-juntar", "sed -n 'H; ${x; s/\\n/, /g; s/^, //; p}' frutas.txt")}
{ANAT(("H", "em toda linha: guarda no reserva."), ("$", "na última linha..."), ("x", "traz o reserva para o espaço padrão."), ("s/\\n/, /g", "quebras de linha viram vírgulas."), ("s/^, //", "tira a vírgula do começo."), ("p", "imprime."))}
<hr>
<h2>4. Inverter a ordem das linhas</h2>
<p>O clássico “<code>tac</code> feito com sed”: cada linha nova recebe as anteriores embaixo (<code>G</code>), o total vai para o reserva (<code>h</code>) e só a última linha imprime:</p>
{T("hold-tac", "sed -n '1!G; h; $p' texto.txt")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Tamanhos diferentes no y", "Origem e destino do <code>y</code> precisam ter o mesmo número de caracteres:", T("hold-erro", "sed 'y/abc/xy/' frutas.txt"))}
"""

def hold_ex():
    return (EX(1, "Trocar letras", "Complete para trocar a por 4 e e por 3:", "sed '", "y/ae/43/", "' frutas.txt") +
            EX(2, "Linha em branco", "Qual comando sozinho põe uma linha em branco depois de cada linha?", "sed ", "G", " texto.txt", rotulo="comando") +
            MC(3, "O que o <code>h</code> faz?", ["Imprime ajuda", "Copia o espaço padrão para o espaço reserva", "Apaga a linha", "Junta as linhas"], 2) +
            MC(4, "Por que <code>y/a-z/A-Z/</code> não passa tudo para maiúsculas?", ["Porque o y não aceita faixas: troca só a, - e z", "Porque falta o g", "Porque o y só funciona com números", "Porque precisa de -E"], 1))

def hold_miss():
    return (M("hold-m1", "com o <code>y</code>, tire os acentos de <code>frutas.txt</code> (troque <code>ç</code> por <code>c</code> e <code>ã</code> por <code>a</code>).", "sed 'y/çã/ca/' frutas.txt", r"src:\by/;;outre:^maca$;;outre:^laranja$") +
            M("hold-m2", "inverta a ordem das linhas de <code>nomes.txt</code> com o espaço reserva.", "sed -n '1!G; h; $p' nomes.txt", r"src:\bG\b;;src:\bh\b;;outre:^Fábio\nCarla\nEduarda"))

NIVEL = {"id": "n2", "nome": "Nível 2 · sed", "curto": "sed", "desc": "O editor de fluxo: imprimir, trocar, apagar e inserir", "grupos": [
    {"grupo": "Primeiros passos", "aulas": [
        aula(slug="sed-intro", menu="Como o sed funciona (p e -n)", title="Como o sed funciona: p e -n", h1='Como o <span class="hl">sed</span> funciona (<span class="hl">p</span> e <span class="hl">-n</span>)',
             desc="Primeiros passos com o GNU sed: o ciclo linha a linha, o comando p, a opção -n, ler do pipe e de vários arquivos.",
             intro="O <code>sed</code> lê o texto linha por linha, aplica seus comandos e imprime. Entender esse ciclo explica quase tudo que ele faz, inclusive as surpresas.",
             aprender=["O ciclo do sed e o espaço padrão.", "O comando <code>p</code> e a opção <code>-n</code>.", "Ler do pipe e de vários arquivos (<code>-s</code>)."],
             corpo=intro_corpo, exercicios=intro_ex, missoes=intro_miss,
             ref=[("sed '' arq", "imprime o arquivo como está."), ("sed -n '2p' arq", "só a linha 2."), ("sed -n '2,4p' arq", "linhas 2 a 4."), ("sed -n '$p' arq", "a última linha."), ("cmd | sed ...", "trabalha na saída de outro comando."), ("sed -s -n '$p' a b", "a última linha de cada arquivo.")],
             resumo=["O sed lê uma linha, aplica os comandos e imprime; o arquivo não muda.", "<code>-n</code> desliga a impressão automática; <code>p</code> imprime.", "Aspas simples em volta do script, sempre."]),
        aula(slug="sed-substituir", menu="Substituindo (s///)", title="Substituindo texto com sed (s///)", h1='Substituindo (<span class="hl">s///</span>)',
             desc="O comando s do sed: localizar e substituir, trocar o separador, usar regex no padrão e o & no texto de troca, com erros reais.",
             intro="O <code>s</code> é o comando mais famoso do <code>sed</code>: localiza um padrão e troca por outro texto, linha por linha.",
             aprender=["A forma <code>s/padrão/troca/</code>.", "Trocar o separador para lidar com barras.", "Usar regex no padrão e <code>&amp;</code> na troca."],
             corpo=subs_corpo, exercicios=subs_ex, missoes=subs_miss,
             ref=[("sed 's/a/b/' arq", "troca o 1º a por b em cada linha."), ("sed 's#/x#/y#' arq", "o mesmo, com # de separador."), ("sed 's/[0-9]*/N/' arq", "padrão com regex."), ("sed 's/x/[&]/' arq", "& é o que casou.")],
             resumo=["<code>s/padrão/troca/</code> troca a primeira ocorrência de cada linha.", "O separador pode ser qualquer caractere: <code>s#a#b#</code>.", "<code>&amp;</code> repete o que o padrão encontrou."]),
        aula(slug="sed-flags", menu="Flags do s (g, I, número, p, w)", title="Flags do s no sed: g, I, número, p e w", h1='Flags do s (<span class="hl">g</span>, <span class="hl">I</span>, <span class="hl">p</span>…)',
             desc="As flags do comando s do sed: g para todas as ocorrências, I sem diferenciar maiúsculas, um número para a enésima, p com -n e w para gravar.",
             intro="As letras depois da última barra do <code>s///</code> mudam o jeito da troca. Com elas você troca todas as ocorrências, ignora maiúsculas e vê só o que mudou.",
             aprender=["<code>g</code> e <code>I</code>.", "Um número para trocar só a enésima ocorrência.", "<code>p</code> com <code>-n</code> e <code>w</code>."],
             corpo=flags_corpo, exercicios=flags_ex, missoes=flags_miss,
             ref=[("s/a/b/g", "todas as ocorrências."), ("s/a/b/I", "sem diferenciar maiúsculas (GNU)."), ("s/a/b/2", "só a 2ª ocorrência."), ("s/a/b/2g", "da 2ª em diante."), ("sed -n 's/a/b/p'", "só as linhas alteradas."), ("s/a/b/w arq", "grava as linhas alteradas em arq.")],
             resumo=["<code>g</code> troca todas; <code>I</code> ignora maiúsculas.", "Um número escolhe a ocorrência.", "<code>-n</code> + <code>p</code> mostra só o que mudou."]),
    ]},
    {"grupo": "Escolhendo e mudando linhas", "aulas": [
        aula(slug="sed-enderecos", menu="Endereços (linha, faixa, regex)", title="Endereços no sed: linha, faixa, $, regex e !", h1='Endereços (<span class="hl">linha</span>, <span class="hl">faixa</span>, <span class="hl">/regex/</span>)',
             desc="Endereços do sed: número de linha, faixas, a última linha $, endereços de regex, faixas com regex, negação ! e passo 1~2.",
             intro="Endereços dizem em quais linhas um comando vale. Com eles, o <code>sed</code> edita só a linha 3, só as linhas com ERRO, ou tudo menos o cabeçalho.",
             aprender=["Número de linha, faixa e <code>$</code>.", "Endereços de regex e faixas entre padrões.", "Negação com <code>!</code> e passo com <code>~</code>."],
             corpo=end_corpo, exercicios=end_ex, missoes=end_miss,
             ref=[("3p", "a linha 3."), ("2,5p", "linhas 2 a 5."), ("$p", "a última linha."), ("/ERRO/p", "linhas com ERRO."), ("/A/,/B/p", "de uma linha com A até a próxima com B."), ("/INFO/!p", "linhas sem INFO."), ("1~2p", "linhas ímpares (GNU).")],
             resumo=["Sem endereço, o comando vale em todas as linhas.", "<code>/regex/</code> escolhe as linhas pelo conteúdo.", "<code>!</code> inverte o endereço."]),
        aula(slug="sed-apagar", menu="Apagando linhas (d)", title="Apagando linhas com sed (d)", h1='Apagando linhas (<span class="hl">d</span>)',
             desc="O comando d do sed: apagar por número, faixa, regex, comentários, linhas vazias, a última linha e tudo menos um padrão.",
             intro="O <code>d</code> joga a linha fora. Junto com os endereços, limpa arquivos: comentários, linhas vazias, cabeçalhos.",
             aprender=["Apagar por número e faixa.", "Apagar comentários e linhas vazias.", "Apagar tudo menos as linhas que interessam."],
             corpo=del_corpo, exercicios=del_ex, missoes=del_miss,
             ref=[("1d", "apaga a linha 1."), ("2,8d", "apaga as linhas 2 a 8."), ("$d", "apaga a última."), ("/^#/d", "apaga comentários."), ("/^$/d", "apaga linhas vazias."), ("/ERRO/!d", "apaga tudo que não tem ERRO.")],
             resumo=["<code>d</code> descarta a linha e pula para a próxima.", "<code>/^#/d; /^$/d</code> limpa um arquivo de configuração.", "<code>/padrão/!d</code> funciona como o <code>grep</code>."]),
        aula(slug="sed-inserir", menu="Inserindo e trocando linhas (i, a, c)", title="Inserindo e trocando linhas com sed (i, a, c)", h1='Inserindo e trocando linhas (<span class="hl">i</span>, <span class="hl">a</span>, <span class="hl">c</span>)',
             desc="Os comandos i, a e c do sed: inserir antes, acrescentar depois, trocar a linha inteira, e a forma clássica com barra invertida.",
             intro="Para colocar linhas novas ou trocar uma linha inteira, o <code>sed</code> tem três comandos: <code>i</code>, <code>a</code> e <code>c</code>.",
             aprender=["<code>i</code>: inserir antes de uma linha.", "<code>a</code>: acrescentar depois.", "<code>c</code>: trocar a linha inteira."],
             corpo=ins_corpo, exercicios=ins_ex, missoes=ins_miss,
             ref=[("1i texto", "insere antes da linha 1."), ("$a texto", "acrescenta depois da última."), ("/x/a texto", "depois de cada linha com x."), ("/x/c texto", "troca as linhas com x por texto.")],
             resumo=["<code>i</code> antes, <code>a</code> depois, <code>c</code> no lugar.", "O texto vem logo depois do comando (GNU) ou depois de <code>\\</code>.", "O <code>c</code> troca a linha inteira, não um pedaço."]),
        aula(slug="sed-in-place", menu="Editando o arquivo (-i e backup)", title="Editando o próprio arquivo com sed -i (e backup)", h1='Editando o arquivo (<span class="hl">-i</span> e backup)',
             desc="sed -i para gravar as mudanças no arquivo, -i.bak para guardar backup, vários arquivos, o perigo do -n e o erro do -in.",
             intro="A opção <code>-i</code> grava a mudança no próprio arquivo. Útil e perigosa: esta aula mostra como usar com segurança, sempre na pasta de teste.",
             aprender=["Gravar no arquivo com <code>-i</code>.", "Guardar o original com <code>-i.bak</code>.", "As armadilhas: <code>-n</code> com <code>-i</code> e o <code>-in</code>."],
             corpo=inplace_corpo, exercicios=inplace_ex, missoes=inplace_miss,
             ref=[("sed -i 's/a/b/' arq", "grava a troca em arq."), ("sed -i.bak 's/a/b/' arq", "grava e guarda arq.bak."), ("mv arq.bak arq", "desfaz, trazendo o backup de volta."), ("sed -n -i '/x/p' arq", "deixa no arquivo só as linhas com x.")],
             resumo=["Teste sem <code>-i</code>, confira, e só então grave.", "<code>-i.bak</code> guarda o original.", "<code>-n -i</code> sem <code>p</code> esvazia o arquivo."]),
    ]},
    {"grupo": "sed avançado", "aulas": [
        aula(slug="sed-grupos", menu="Regex estendida e grupos (-E, \\1)", title="sed -E, grupos e \\1: reorganizando texto", h1='Regex estendida e grupos (<span class="hl">-E</span>, <span class="hl">\\1</span>)',
             desc="sed -E com regex estendida, grupos de captura e \\1 para inverter nomes, mudar o formato de datas, extrair pedaços e \\U, \\L, \\u do GNU sed.",
             intro="Parênteses guardam pedaços do que casou, e <code>\\1</code>, <code>\\2</code> os devolvem na ordem que você quiser. É assim que o <code>sed</code> reorganiza texto.",
             aprender=["A regex estendida com <code>-E</code>.", "Grupos <code>( )</code> e referências <code>\\1</code>, <code>\\2</code>.", "<code>\\U</code>, <code>\\L</code> e <code>\\u</code> para maiúsculas e minúsculas."],
             corpo=ext_corpo, exercicios=ext_ex, missoes=ext_miss,
             ref=[("sed -E 's/[0-9]+/N/'", "regex estendida."), ("sed -E 's/(a) (b)/\\2 \\1/'", "inverte dois grupos."), ("sed -E 's/.*;(.*)/\\1/'", "extrai o último campo."), ("sed 's/.*/\\U&/'", "tudo em maiúsculas (GNU)."), ("sed -E 's/^(.)/\\u\\1/'", "primeira letra maiúscula (GNU).")],
             resumo=["<code>-E</code> deixa <code>( )</code>, <code>+</code> e <code>{n}</code> funcionarem sem barra.", "<code>\\1</code> devolve o primeiro grupo.", "<code>\\U</code> e <code>\\L</code> mudam a caixa, com acentos."]),
        aula(slug="sed-varios", menu="Vários comandos e scripts (-e, ;, {}, -f)", title="Vários comandos e scripts no sed: -e, ;, {} e -f", h1='Vários comandos e scripts (<span class="hl">-e</span>, <span class="hl">{ }</span>, <span class="hl">-f</span>)',
             desc="Juntar comandos no sed com -e, ponto e vírgula e chaves, rodar scripts .sed com -f e encerrar com q.",
             intro="Um script do <code>sed</code> pode ter vários comandos, agrupados por endereço e guardados num arquivo. Esta aula mostra como montar essas receitas.",
             aprender=["Juntar comandos com <code>-e</code> e <code>;</code>.", "Agrupar comandos sob um endereço com <code>{ }</code>.", "Rodar um arquivo de script com <code>-f</code> e parar com <code>q</code>."],
             corpo=varios_corpo, exercicios=varios_ex, missoes=varios_miss,
             ref=[("sed -e 'cmd1' -e 'cmd2'", "dois comandos."), ("sed 'cmd1; cmd2'", "o mesmo, com ;."), ("sed '/x/{cmd1; cmd2}'", "dois comandos só nas linhas com x."), ("sed -f script.sed arq", "lê o script de um arquivo."), ("sed '3q'", "para depois da linha 3.")],
             resumo=["Os comandos rodam em ordem, na mesma linha.", "<code>{ }</code> agrupa comandos sob um endereço.", "Receitas grandes vão para um arquivo <code>.sed</code> e rodam com <code>-f</code>."]),
        aula(slug="sed-y-hold", menu="y e o espaço reserva (h, G, x)", title="sed: o comando y e o espaço reserva (h, H, G, x)", h1='O <span class="hl">y</span> e o espaço reserva (<span class="hl">h</span>, <span class="hl">G</span>, <span class="hl">x</span>)',
             desc="O comando y do sed para trocar caracteres (com acentos) e o hold space: h, H, g, G e x para juntar linhas, espaçamento duplo e inverter a ordem.",
             intro="Para fechar o <code>sed</code>: o <code>y</code>, que troca letra por letra, e o espaço reserva, a memória do sed entre uma linha e outra.",
             aprender=["Trocar caracteres com <code>y</code> (e tirar acentos).", "Os comandos do espaço reserva: <code>h</code>, <code>H</code>, <code>g</code>, <code>G</code> e <code>x</code>.", "Juntar linhas e inverter a ordem do arquivo."],
             corpo=hold_corpo, exercicios=hold_ex, missoes=hold_miss,
             ref=[("y/abc/xyz/", "troca a→x, b→y, c→z."), ("sed G", "espaçamento duplo."), ("sed -n 'H; ${x; s/\\n/,/g; p}'", "junta as linhas (começa com vírgula)."), ("sed -n '1!G; h; $p'", "inverte a ordem das linhas.")],
             resumo=["O <code>y</code> troca caracteres um a um e entende acentos.", "O espaço reserva guarda texto entre as linhas.", "<code>G</code>, <code>h</code> e <code>x</code> fazem truques que o <code>s</code> sozinho não faz."]),
    ]},
]}
