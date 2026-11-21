# -*- coding: utf-8 -*-
"""Nível 1 · Base: o terreno em volta do sed, do awk e do jq."""
from lib_guia import *

# ---------------------------------------------------------------- introdução
def intro_corpo():
    return f"""
<h2>A ideia: três ferramentas para mexer em texto</h2>
<p>Quase tudo no Linux é texto: arquivos de configuração, logs, planilhas exportadas em CSV, respostas de APIs em JSON. Abrir cada arquivo num editor e mudar à mão funciona uma vez. Na décima vez, cansa. Este guia ensina três ferramentas que fazem esse trabalho <strong>sozinhas</strong>, direto no terminal:</p>
<ul>
<li><strong><code>sed</code></strong> (de <em>stream editor</em>, “editor de fluxo”): lê o texto linha a linha e <strong>edita</strong>: troca palavras, apaga linhas, insere texto.</li>
<li><strong><code>awk</code></strong> (das iniciais dos criadores, Aho, Weinberger e Kernighan): enxerga cada linha como uma <strong>tabela de colunas</strong> e faz contas, filtros e relatórios.</li>
<li><strong><code>jq</code></strong> (“JSON query”): entende <strong>JSON</strong>, o formato das APIs, e tira dele só o que você quer.</li>
</ul>
<p>Uma provinha de cada uma, com os arquivos de exemplo do guia. O <code>sed</code> trocou “rato” por “gato”, o <code>awk</code> mostrou só a primeira coluna e o <code>jq</code> pegou o nome do primeiro usuário:</p>
{T("intro-prova", "sed 's/rato/gato/' texto.txt", "awk '{print $1}' notas.txt", "jq '.[0].nome' usuarios.json",
   notas={"O gato roeu": "o sed trocou “rato” por “gato”", "Ana": "o awk mostrou a coluna 1", '"Ana Souza"': "o jq tirou um campo do JSON"})}
<p>Repare na última linha do <code>sed</code>: “Rato que é gato não volta.” O “Rato” com R maiúsculo continuou igual, e o “rato” minúsculo virou “gato”, porque o <code>s</code> diferencia maiúsculas e troca só a primeira ocorrência de cada linha. Detalhes assim são o assunto do Nível 2.</p>
<hr>
<h2>As versões usadas no guia</h2>
<p>Todas as saídas foram colhidas com estas versões. Rode os mesmos comandos aí para ver as suas:</p>
{T("intro-versoes", "sed --version | head -1", "awk --version | head -1", "jq --version")}
{ANAT(("sed --version", "pede ao programa que diga a própria versão."), ("|", "o <em>pipe</em>: manda a saída do primeiro comando para o segundo."), ("head -1", "mostra só a primeira linha (a versão vem em várias linhas)."))}
<div class="warning"><strong>gawk ou mawk?</strong>
<p>Existem vários programas chamados <code>awk</code>. O guia usa o <strong>GNU awk</strong> (<code>gawk</code>). No Ubuntu e no Debian, o <code>awk</code> que vem instalado costuma ser o <code>mawk</code>, mais simples. Quase tudo do guia funciona nos dois; quando algo é só do gawk, a aula avisa. Para ter o mesmo resultado do guia, instale o gawk com <code>sudo apt install gawk</code>: depois disso, o comando <code>awk</code> passa a chamar o gawk.</p></div>
<p>Se o seu <code>awk</code> ainda for o mawk, ele nem entende <code>--version</code>. Na máquina da coleta o mawk também estava instalado, e foi assim que ele respondeu (a versão dele se pede com <code>-W version</code>):</p>
{T("intro-mawk", "mawk --version", "mawk -W version | head -1")}
<hr>
<h2>Como as três se encaixam</h2>
<div class="table-wrap"><table class="ref">
<tr><th>Ferramenta</th><th>Pense nela como</th><th>Melhor para</th></tr>
<tr><td><code>sed</code></td><td>um “localizar e substituir” que roda sozinho</td><td>trocar textos, apagar e inserir linhas, limpar arquivos</td></tr>
<tr><td><code>awk</code></td><td>uma planilha de linha de comando</td><td>colunas, somas, médias, contagens, relatórios</td></tr>
<tr><td><code>jq</code></td><td>um tradutor de JSON</td><td>filtrar, reorganizar e converter dados JSON</td></tr>
</table></div>
<p>Antes delas, o Nível 1 revisa o terreno em volta: pastas de teste, <em>pipes</em> e redirecionamento, e as ferramentas pequenas (<code>cat</code>, <code>head</code>, <code>tail</code>, <code>wc</code>, <code>cut</code>, <code>sort</code>, <code>uniq</code>, <code>tr</code> e <code>grep</code>). Se você nunca abriu um terminal, comece pelo <a href="https://wallysondevs.github.io/guia-bash/">Guia Bash</a>, que este guia complementa.</p>
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Programa não instalado", "Se uma ferramenta não estiver instalada, o Bash avisa com esta frase. Na coleta, pedimos de propósito um programa que não existe:", T("intro-erro", "jqq --version"), "A solução é corrigir o nome ou instalar o programa: <code>sudo apt install jq</code>, por exemplo.")}
"""

def intro_ex():
    return (EX(1, "Qual ferramenta?", "Qual das três entende JSON?", "", "jq") +
            EX(2, "A versão", "Complete para ver a versão do sed:", "sed ", "--version") +
            MC(3, "O <code>awk</code> que vem no Ubuntu costuma ser:", ["o gawk", "o mawk", "o jq", "o sed"], 2) +
            MC(4, "No exemplo, por que “Rato”, na última linha, não virou “gato”?", ["O sed só lê três linhas", "O padrão era <code>rato</code> minúsculo, e o sed diferencia maiúsculas", "O arquivo estava protegido", "Faltou o <code>-i</code>"], 2))

def intro_miss():
    return (M("intro-m1", "mostre só a primeira linha da versão do <code>sed</code>.", "sed --version | head -1", r"src:\bsed --version;;src:\bhead\b;;outre:^sed \(GNU sed\) 4\.") +
            M("intro-m2", "mostre a versão do <code>jq</code>.", "jq --version", r"src:\bjq --version;;outre:^jq-1\."))

# ---------------------------------------------------------------- preparando
def prep_corpo():
    return f"""
<h2>A ideia: uma caixa de areia</h2>
<p>O <code>sed</code> e o <code>awk</code> conseguem alterar arquivos. Para treinar sem medo, todo o guia trabalha numa pasta só para isso, a <code>~/guia-texto-teste</code>, com arquivos inventados: nomes fictícios, vendas de uma papelaria, um log de sistema, JSON de usuários e pedidos. Se algo der errado, você apaga a pasta e cria de novo.</p>
<hr>
<h2>1. Criar a pasta e os arquivos</h2>
<p>Os arquivos de exemplo estão neste site, na pasta <a href="arquivos/"><code>arquivos/</code></a> (por exemplo, <a href="arquivos/vendas.csv">vendas.csv</a> e <a href="arquivos/usuarios.json">usuarios.json</a>). O jeito mais rápido é o script <a href="arquivos/criar-arquivos.sh"><code>criar-arquivos.sh</code></a>, que cria todos de uma vez, sem internet. Baixe-o (ou copie o conteúdo dele num arquivo com esse nome) e rode estes comandos:</p>
<pre class="cmd">
mkdir -p ~/guia-texto-teste
cd ~/guia-texto-teste
bash ~/Downloads/criar-arquivos.sh
</pre>
<p>Na coleta, o script foi rodado numa pasta vazia chamada <code>nova</code>, dentro da pasta de teste. Ele avisou onde criou os arquivos, e o <code>ls</code> mostrou o que apareceu:</p>
{T("prep-criar", "mkdir nova && cd nova && bash ../criar-arquivos.sh && ls")}
<div class="tip"><strong>Voltar ao original</strong><p>Rodou um <code>sed -i</code> e estragou um arquivo? Rode <code>bash criar-arquivos.sh</code> de novo dentro da pasta: ele reescreve todos os arquivos de exemplo como eram.</p></div>
<hr>
<h2>2. Conhecendo os arquivos</h2>
<p>O <code>wc -c *</code> mostra o tamanho de cada arquivo da pasta, em bytes, e o total no fim:</p>
{T("prep-ls", "wc -c *")}
<p>Os principais, por tipo:</p>
<div class="table-wrap"><table class="ref">
<tr><th>Arquivo</th><th>O que tem</th><th>Usado em</th></tr>
<tr><td><code>nomes.txt</code>, <code>frutas.txt</code></td><td>uma palavra por linha, com repetições</td><td>sort, uniq, grep</td></tr>
<tr><td><code>texto.txt</code></td><td>quatro frases com “rato”</td><td>sed</td></tr>
<tr><td><code>config.txt</code></td><td>configuração <code>chave=valor</code> com comentários</td><td>sed</td></tr>
<tr><td><code>log.txt</code>, <code>acesso.log</code></td><td>log de sistema e log de servidor web</td><td>grep, sed, awk, projetos</td></tr>
<tr><td><code>vendas.csv</code>, <code>notas.txt</code></td><td>tabelas: vendas da papelaria e notas de alunos</td><td>cut, awk</td></tr>
<tr><td><code>contatos.txt</code></td><td>nome; telefone; e-mail</td><td>sed com grupos</td></tr>
<tr><td><code>usuarios.json</code>, <code>pedidos.json</code>, <code>produto.json</code></td><td>dados em JSON</td><td>jq</td></tr>
<tr><td><code>quebrado.json</code></td><td>um JSON com erro de propósito</td><td>jq, “Quando dá errado”</td></tr>
<tr><td><code>limpa.sed</code>, <code>relatorio.awk</code></td><td>scripts prontos</td><td>sed -f, awk -f</td></tr>
</table></div>
<p>Uma espiada em dois deles:</p>
{T("prep-espiar", "cat nomes.txt", "head -3 vendas.csv")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Fora da pasta de teste", "Se você esquecer o <code>cd ~/guia-texto-teste</code>, os comandos não acham os arquivos. Na coleta, entramos de propósito numa pasta vazia:", T("prep-erro", "mkdir vazia && cd vazia && cat nomes.txt"), "“Arquivo ou diretório inexistente” quase sempre quer dizer: pasta errada ou nome digitado errado. Confira com <code>pwd</code> e <code>ls</code>.")}
"""

def prep_ex():
    return (EX(1, "Entrar na pasta", "Complete para entrar na pasta de teste:", "cd ", "~/guia-texto-teste") +
            EX(2, "Recriar os arquivos", "Complete o comando que recria os arquivos de exemplo:", "bash ", "criar-arquivos.sh") +
            MC(3, "Qual arquivo tem dados em JSON?", ["<code>vendas.csv</code>", "<code>log.txt</code>", "<code>usuarios.json</code>", "<code>nomes.txt</code>"], 3) +
            MC(4, "Por que treinar numa pasta de teste?", ["Porque o sed só funciona nela", "Para poder estragar e recriar os arquivos sem medo", "Porque é obrigatório no Linux", "Para o terminal ficar mais rápido"], 2))

def prep_miss():
    return (M("prep-m1", "liste os arquivos da pasta de teste com <code>ls</code>.", "ls", r"src:^ls\b;;out:vendas.csv;;out:usuarios.json") +
            M("prep-m2", "mostre o conteúdo de <code>nomes.txt</code>.", "cat nomes.txt", r"src:\bcat\b;;src:nomes\.txt;;outre:^Fábio$;;outre:^ana paula$"))

# ---------------------------------------------------------------- pipes
def pipes_corpo():
    return f"""
<h2>A ideia: canos entre programas</h2>
<p>As ferramentas deste guia foram feitas para trabalhar em equipe. Cada uma faz uma coisa pequena; o <strong>pipe</strong> (<code>|</code>, “cano”) liga a saída de uma na entrada da outra, e o <strong>redirecionamento</strong> (<code>&gt;</code>, <code>&gt;&gt;</code>, <code>&lt;</code>, <code>2&gt;</code>) manda a saída para um arquivo ou lê de um arquivo. O <a href="https://wallysondevs.github.io/guia-bash/">Guia Bash</a> explica tudo isso com calma; aqui vai a revisão do que você vai usar o tempo todo.</p>
<hr>
<h2>1. O pipe: <code>|</code></h2>
<p>O <code>cat</code> mostra o arquivo; com o <code>|</code>, a saída dele vai para o <code>sort</code>, que ordena. Encadeando mais um <code>|</code>, o <code>head</code> fica só com as três primeiras:</p>
{T("pipes-pipe", "cat nomes.txt | sort", "cat nomes.txt | sort | head -3")}
<p>O <code>sort</code> usou a ordem do português (<code>pt_BR.UTF-8</code>): “ana paula” veio logo depois de “Ana”, e “bruno” junto de “Bruno”. Num terminal em inglês ou com <code>LC_ALL=C</code>, as maiúsculas vêm antes das minúsculas.</p>
{ANAT(("cat nomes.txt", "escreve o arquivo na saída."), ("|", "o cano: a saída da esquerda vira a entrada da direita."), ("sort", "ordena o que chegou pelo cano."), ("| head -3", "mais um cano: fica só com as 3 primeiras linhas."))}
<hr>
<h2>2. Gravar num arquivo: <code>&gt;</code> e <code>&gt;&gt;</code></h2>
<p>O <code>&gt;</code> grava a saída num arquivo (e apaga o que havia nele). Repare que o primeiro comando não mostrou nada: a saída foi para o arquivo. O <code>&gt;&gt;</code> acrescenta no fim, sem apagar:</p>
{T("pipes-gravar", "sort nomes.txt > ordenados.txt", "head -3 ordenados.txt", "echo Gabriel >> nomes.txt", "tail -2 nomes.txt")}
<div class="warning"><strong>Cuidado com o &gt; no mesmo arquivo</strong><p><code>sort nomes.txt &gt; nomes.txt</code> <strong>apaga</strong> o arquivo: o Bash esvazia o destino antes de o <code>sort</code> começar a ler. Grave em outro arquivo, ou use o <code>-i</code> do sed (Nível 2).</p></div>
<p>Veja o estrago, de propósito, na pasta de teste:</p>
{T("pipes-estrago", "sort nomes.txt > nomes.txt", "wc -l nomes.txt")}
<hr>
<h2>3. Ler de um arquivo: <code>&lt;</code></h2>
<p>Com <code>&lt;</code>, o arquivo entra pela entrada padrão. Diferença visível no <code>wc -l</code>: com o nome como argumento, ele mostra o nome; pela entrada, só o número:</p>
{T("pipes-entrada", "wc -l nomes.txt", "wc -l < nomes.txt")}
<hr>
<h2>4. A saída de erro: <code>2&gt;</code></h2>
<p>Os programas têm duas saídas: a normal (1) e a de erros (2). O <code>&gt;</code> só desvia a normal; o <code>2&gt;</code> desvia os erros. No segundo comando, a mensagem não apareceu na tela: foi para <code>erros.txt</code>:</p>
{T("pipes-erro2", "cat nada.txt", "cat nada.txt 2> erros.txt", "cat erros.txt")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Pipe sem comando do outro lado", "Um <code>|</code> no fim da linha, sem nada depois, faz o Bash esperar a continuação. Num script (ou com <code>bash -c</code>, como na coleta), vira erro de sintaxe:", T("pipes-erro", "bash -c 'cat nomes.txt |'"), "Complete o encanamento: <code>cat nomes.txt | sort</code>.")}
"""

def pipes_ex():
    return (EX(1, "O cano", "Complete para ordenar a saída do cat:", "cat nomes.txt ", "| sort") +
            EX(2, "Acrescentar", "Qual símbolo acrescenta no fim do arquivo, sem apagar?", "echo Gabriel ", ">>", " nomes.txt", rotulo="símbolo") +
            MC(3, "O que <code>sort nomes.txt &gt; nomes.txt</code> faz?", ["Ordena o arquivo no lugar", "Deixa o arquivo vazio", "Dá erro e não mexe em nada", "Cria uma cópia"], 2) +
            MC(4, "Para guardar só as mensagens de erro num arquivo, usamos:", ["<code>&gt;</code>", "<code>&gt;&gt;</code>", "<code>2&gt;</code>", "<code>|</code>"], 3))

def pipes_miss():
    return (M("pipes-m1", "mostre as três primeiras linhas de <code>nomes.txt</code> em ordem, juntando <code>sort</code> e <code>head</code> com um pipe.", "sort nomes.txt | head -3", r"src:\bsort\b;;src:\|\s*head;;outre:^Ana$;;outre:^ana paula$") +
            M("pipes-m2", "guarde a lista ordenada em <code>ordenados.txt</code> com <code>&gt;</code> e depois mostre a última linha desse arquivo com <code>tail -1</code>.", ["sort nomes.txt > ordenados.txt", "tail -1 ordenados.txt"], r"src:>\s*ordenados\.txt;;src:\btail\b;;outre:^Fábio$"))

# ---------------------------------------------------------------- cat head tail wc
def cht_corpo():
    return f"""
<h2>A ideia: olhar o arquivo antes de mexer</h2>
<p>Antes de editar com <code>sed</code> ou somar com <code>awk</code>, você precisa ver o arquivo: o começo, o fim, quantas linhas tem. Quatro ferramentas fazem isso: <code>cat</code> (“concatenar”: mostra tudo), <code>head</code> (“cabeça”: o começo), <code>tail</code> (“cauda”: o fim) e <code>wc</code> (<em>word count</em>: conta).</p>
<hr>
<h2>1. <code>cat</code>: o arquivo inteiro</h2>
<p>O <code>-n</code> numera as linhas, ótimo para saber em que linha está cada coisa (o <code>sed</code> usa números de linha):</p>
{T("cht-cat", "cat -n texto.txt")}
<hr>
<h2>2. <code>head</code> e <code>tail</code>: o começo e o fim</h2>
<p><code>head -n 3</code> mostra as 3 primeiras linhas; <code>tail -n 2</code>, as 2 últimas. O <code>tail -n +2</code> é diferente: mostra <strong>a partir da linha 2</strong>, ótimo para pular o cabeçalho de um CSV:</p>
{T("cht-headtail", "head -n 3 log.txt", "tail -n 2 log.txt", "tail -n +2 vendas.csv | head -n 2", notas={"2026-03-02,Ana": "a linha 1 (o cabeçalho) ficou de fora"})}
{ANAT(("tail", "o comando: o fim do arquivo."), ("-n +2", "a partir da linha 2 (com +) em vez das 2 últimas (sem +)."), ("vendas.csv", "o arquivo."))}
<hr>
<h2>3. <code>wc</code>: contar</h2>
<p>Sem opções, o <code>wc</code> mostra linhas, palavras e bytes. Com <code>-l</code>, só linhas; <code>-w</code>, só palavras; <code>-c</code>, bytes; <code>-m</code>, caracteres:</p>
{T("cht-wc", "wc texto.txt", "wc -l log.txt vendas.csv", "wc -w texto.txt")}
<p>Bytes e caracteres não são a mesma coisa. Letras acentuadas ocupam 2 bytes em UTF-8. “Fábio” tem 5 letras e 6 bytes; o <code>echo</code> ainda põe uma quebra de linha no fim. Por isso o <code>-c</code> (bytes) contou 7 e o <code>-m</code> (caracteres) contou 6:</p>
{T("cht-bytes", "echo Fábio | wc -c", "echo Fábio | wc -m")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Número inválido", "O <code>head</code> espera um número depois de <code>-n</code>. Com uma palavra no lugar, ele reclama, com a mensagem traduzida pelo próprio programa:", T("cht-erro", "head -n tres log.txt"))}
"""

def cht_ex():
    return (EX(1, "As 5 primeiras", "Complete para ver as 5 primeiras linhas de log.txt:", "head -n ", "5", " log.txt", rotulo="número") +
            EX(2, "Pular o cabeçalho", "Complete para mostrar vendas.csv a partir da linha 2:", "tail -n ", "+2", " vendas.csv") +
            EX(3, "Só linhas", "Qual opção do wc conta só as linhas?", "wc ", "-l", " log.txt", rotulo="opção") +
            MC(4, "Na coleta, <code>echo Fábio | wc -c</code> mostrou:", ["5", "6", "7", "12"], 3) +
            MC(5, "Qual opção do <code>cat</code> numera as linhas?", ["<code>-l</code>", "<code>-n</code>", "<code>-c</code>", "<code>+n</code>"], 2))

def cht_miss():
    return (M("cht-m1", "conte quantas linhas tem <code>log.txt</code> com o <code>wc</code>.", "wc -l log.txt", r"src:\bwc\b;;src:-l;;out:10 log.txt") +
            M("cht-m2", "mostre as duas últimas linhas de <code>vendas.csv</code>.", "tail -n 2 vendas.csv", r"src:\btail\b;;outre:^2026-03-05,Carla,estojo,3,15\.00$;;outre:^2026-03-05,Ana,caderno,4,12\.50$"))

# ---------------------------------------------------------------- cut
def cut_corpo():
    return f"""
<h2>A ideia: recortar colunas</h2>
<p>Muitos arquivos são tabelas: cada linha é um registro e um caractere separa as colunas. No <code>vendas.csv</code>, o separador é a vírgula. O <code>cut</code> (“cortar”) recorta as colunas que você pedir. Ele é simples e rápido; quando o recorte precisar de lógica (condições, contas), o <code>awk</code> do Nível 3 entra em cena.</p>
<hr>
<h2>1. Um campo: <code>-d</code> e <code>-f</code></h2>
<p><code>-d ,</code> diz qual é o separador (<em>delimiter</em>) e <code>-f 2</code> qual campo (<em>field</em>) você quer:</p>
{T("cut-campo", "cut -d , -f 2 vendas.csv | head -4")}
{ANAT(("cut", "o comando que recorta."), ("-d ,", "o separador é a vírgula."), ("-f 2", "quero o 2º campo."), ("vendas.csv", "o arquivo."))}
<hr>
<h2>2. Vários campos e faixas</h2>
<p>Separe os campos com vírgula (<code>-f 2,4</code>) ou peça uma faixa (<code>-f 1-3</code>). O separador continua aparecendo entre os campos recortados:</p>
{T("cut-varios", "cut -d , -f 2,4 vendas.csv | head -3", "cut -d , -f 1-3 vendas.csv | tail -2")}
<hr>
<h2>3. Por posição: <code>-c</code></h2>
<p>Sem separador, dá para recortar por posição de caractere. No <code>log.txt</code>, os 10 primeiros caracteres são a data e os caracteres 12 a 19, a hora:</p>
{T("cut-c", "cut -c 1-10 log.txt | head -2", "cut -c 12-19 log.txt | head -2")}
<hr>
<h2>4. O limite do cut: espaços repetidos</h2>
<p>O <code>cut</code> trata <strong>cada</strong> separador como um corte. No <code>log.txt</code>, depois de “INFO” há dois espaços (para alinhar com “AVISO”). Com <code>-d ' '</code>, o campo 4 de uma linha INFO sai vazio:</p>
{T("cut-espacos", "head -2 log.txt | cut -d ' ' -f 4", "grep AVISO log.txt | cut -d ' ' -f 4")}
<p>Nas linhas INFO e ERRO, o campo 4 é o “nada” entre os dois espaços, e o <code>cut</code> mostrou linhas vazias. Nas linhas AVISO, que têm um espaço só, o campo 4 já é a primeira palavra da mensagem. O mesmo comando dá resultados diferentes conforme a linha.</p>
<p>O <code>awk</code> não tem esse problema: por padrão ele junta espaços repetidos. Guarde isso para o Nível 3.</p>
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Faltou dizer o quê recortar", "Sem <code>-f</code>, <code>-c</code> ou <code>-b</code>, o <code>cut</code> não sabe o que fazer:", T("cut-erro", "cut -d , vendas.csv"))}
"""

def cut_ex():
    return (EX(1, "O separador", "Complete para usar a vírgula como separador:", "cut ", "-d ,", " -f 3 vendas.csv") +
            EX(2, "O campo", "Complete para pegar o campo 5 (preço):", "cut -d , ", "-f 5", " vendas.csv") +
            MC(3, "<code>cut -c 1-10 log.txt</code> mostra:", ["as 10 primeiras linhas", "os 10 primeiros caracteres de cada linha", "o campo 10", "as linhas 1 a 10"], 2) +
            MC(4, "Por que o <code>cut -d ' '</code> se atrapalha no <code>log.txt</code>?", ["Porque o arquivo é grande", "Porque há espaços repetidos e cada um conta como corte", "Porque o cut não aceita espaço", "Porque falta o -c"], 2))

def cut_miss():
    return (M("cut-m1", "mostre só a coluna <code>produto</code> (a 3ª) de <code>vendas.csv</code>.", "cut -d , -f 3 vendas.csv", r"src:\bcut\b;;src:-f\s*3;;outre:^produto$;;outre:^mochila$") +
            M("cut-m2", "mostre as colunas vendedor e quantidade (2ª e 4ª) de <code>vendas.csv</code>.", "cut -d , -f 2,4 vendas.csv", r"src:\bcut\b;;src:2,4;;outre:^vendedor,quantidade$;;outre:^Diego,20$"))

# ---------------------------------------------------------------- sort uniq
def su_corpo():
    return f"""
<h2>A ideia: arrumar e contar repetidos</h2>
<p>O <code>sort</code> põe as linhas em ordem. O <code>uniq</code> junta linhas repetidas <strong>vizinhas</strong>. Juntos, respondem a perguntas como “quais frutas aparecem e quantas vezes?”. É uma das combinações mais usadas do terminal, e o <code>awk</code> faz a mesma conta de outro jeito no Nível 3.</p>
<hr>
<h2>1. <code>sort</code>: ordem alfabética, inversa e numérica</h2>
{T("su-sort", "sort frutas.txt", "sort -r frutas.txt | head -3")}
<p>Para números, use <code>-n</code>. Sem ele, o <code>sort</code> compara texto, e “10” vem antes de “2” (porque “1” vem antes de “2”). O <code>-t ,</code> escolhe o separador e <code>-k 4</code> a coluna da chave:</p>
{T("su-numerico", "cut -d , -f 4 vendas.csv | tail -n +2 | sort | head -4", "cut -d , -f 4 vendas.csv | tail -n +2 | sort -n | head -4", "tail -n +2 vendas.csv | sort -t , -k 4 -n -r | head -2")}
{ANAT(("sort", "ordena."), ("-t ,", "as colunas são separadas por vírgula."), ("-k 4", "a chave é a coluna 4 (quantidade)."), ("-n", "compara como número."), ("-r", "ordem inversa (do maior para o menor)."))}
<hr>
<h2>2. <code>uniq</code>: só junta vizinhos</h2>
<p>Sem ordenar antes, o <code>uniq</code> não percebe as repetições separadas: “banana” aparece três vezes na saída. Com <code>sort</code> antes, sobra uma de cada:</p>
{T("su-uniq", "uniq frutas.txt", "sort frutas.txt | uniq")}
<p>O <code>sort -u</code> faz o mesmo em um passo só.</p>
<hr>
<h2>3. Contar: <code>uniq -c</code></h2>
<p>O <code>-c</code> põe na frente quantas vezes cada linha apareceu. Um <code>sort -rn</code> no fim deixa a mais frequente em cima, o famoso “ranking”:</p>
{T("su-contar", "sort frutas.txt | uniq -c", "sort frutas.txt | uniq -c | sort -rn")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Opção que não existe", "Errar uma opção faz o programa avisar e sugerir o <code>--help</code>:", T("su-erro", "sort -x frutas.txt"))}
"""

def su_ex():
    return (EX(1, "Numérico", "Qual opção faz o sort comparar números?", "sort ", "-n", " numeros.txt", rotulo="opção") +
            EX(2, "Contar", "Complete para contar as repetições:", "sort frutas.txt | uniq ", "-c") +
            MC(3, "Por que <code>uniq frutas.txt</code> sozinho mostrou “banana” mais de uma vez?", ["Porque o uniq só junta linhas repetidas vizinhas", "Porque o arquivo tem erro", "Porque faltou -n", "Porque o uniq diferencia acentos"], 1) +
            MC(4, "Na coleta, qual fruta ficou em primeiro em <code>sort frutas.txt | uniq -c | sort -rn</code>?", ["maçã", "uva", "banana", "laranja"], 3))

def su_miss():
    return (M("su-m1", "mostre cada fruta de <code>frutas.txt</code> uma vez só, em ordem.", "sort -u frutas.txt", r"src:\bsort\b;;outre:^laranja$;;outre:^uva$") +
            M("su-m2", "faça o ranking das frutas: quantas vezes cada uma aparece, da mais frequente para a menos.", "sort frutas.txt | uniq -c | sort -rn", r"src:uniq -c;;src:sort -rn|sort -nr;;outre:^\s+3 banana$;;outre:^\s+1 uva$"))

# ---------------------------------------------------------------- tr
def tr_corpo():
    return f"""
<h2>A ideia: trocar letra por letra</h2>
<p>O <code>tr</code> (<em>translate</em>, “traduzir”) troca caracteres: cada letra do primeiro conjunto vira a letra correspondente do segundo. Ele não lê arquivos pelo nome: o texto chega pelo pipe ou pelo <code>&lt;</code>. Para trocar <strong>palavras</strong>, use o <code>sed</code> (Nível 2).</p>
<hr>
<h2>1. Maiúsculas e minúsculas</h2>
{T("tr-maiusc", "tr 'a-z' 'A-Z' < nomes.txt | head -3", "echo 'OLÁ, MUNDO' | tr 'A-Z' 'a-z'")}
{ANAT(("tr", "o comando que troca caracteres."), ("'a-z'", "o conjunto de origem: de a até z."), ("'A-Z'", "o conjunto de destino: cada letra vira a maiúscula correspondente."), ("&lt; nomes.txt", "o texto entra pela entrada padrão."))}
<div class="warning"><strong>O tr e os acentos</strong><p>O <code>tr</code> do GNU trabalha <strong>byte a byte</strong>, e letras acentuadas ocupam 2 bytes em UTF-8. Veja na coleta: na caixa de cima, “OLÁ” virou “olÁ”, e logo abaixo “maçã e pão” virou “MAçã E PãO”. Para maiúsculas com acentos, use o <code>awk</code> (<code>toupper</code>, Nível 3) ou o <code>sed</code> com <code>\\U</code> (Nível 2).</p></div>
{T("tr-acento", "echo 'maçã e pão' | tr 'a-z' 'A-Z'")}
<hr>
<h2>2. Apagar e espremer: <code>-d</code> e <code>-s</code></h2>
<p><code>-d</code> apaga os caracteres do conjunto. <code>-s</code> (<em>squeeze</em>) espreme repetições num só, ótimo para os espaços duplos do <code>log.txt</code>:</p>
{T("tr-ds", "echo '(11) 91234-5678' | tr -d '() -'", "head -1 log.txt | tr -s ' '")}
<hr>
<h2>3. Trocar separadores</h2>
<p>Trocar a vírgula por tabulação (<code>\\t</code>) transforma o CSV em colunas alinhadas no terminal; trocar o espaço por quebra de linha (<code>\\n</code>) põe uma palavra por linha:</p>
{T("tr-sep", "head -3 vendas.csv | tr ',' '\\t'", "head -1 texto.txt | tr ' ' '\\n'")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Faltou o segundo conjunto", "Para trocar, o <code>tr</code> precisa de dois conjuntos. Com um só (e sem <code>-d</code>), ele reclama:", T("tr-erro", "echo abc | tr 'a-z'"))}
{CEN("Nome de arquivo como argumento", "O <code>tr</code> não lê arquivos pelo nome: ele entende <code>nomes.txt</code> como um terceiro conjunto:", T("tr-erro2", "tr a-z A-Z nomes.txt"), "Use <code>tr a-z A-Z &lt; nomes.txt</code>.")}
"""

def tr_ex():
    return (EX(1, "Maiúsculas", "Complete para passar para maiúsculas:", "tr 'a-z' ", "'A-Z'", " < nomes.txt") +
            EX(2, "Apagar", "Qual opção apaga os caracteres?", "echo '(11) 9999' | tr ", "-d", " '() '", rotulo="opção") +
            MC(3, "Por que <code>echo maçã | tr a-z A-Z</code> não deixa o “ç” maiúsculo?", ["Porque o tr trabalha byte a byte, e o ç tem 2 bytes", "Porque falta o -s", "Porque o terminal está em inglês", "Porque ç não tem maiúscula"], 1) +
            MC(4, "Como o <code>tr</code> recebe o texto?", ["Pelo nome do arquivo, como o cat", "Pela entrada padrão: pipe ou &lt;", "Só digitando", "Pela opção -f"], 2))

def tr_miss():
    return (M("tr-m1", "mostre <code>frutas.txt</code> em maiúsculas com o <code>tr</code>.", "tr 'a-z' 'A-Z' < frutas.txt", r"src:\btr\b;;outre:^BANANA$;;outre:^LARANJA$") +
            M("tr-m2", "pegue a 5ª linha do <code>log.txt</code> com <code>head -5 log.txt | tail -1</code> e esprema os espaços repetidos dela com o <code>tr</code>.", "head -5 log.txt | tail -1 | tr -s ' '", r"src:tr -s;;out:2026-03-02 09:05:59 INFO login usuario=bruno"))

# ---------------------------------------------------------------- grep
def grep_corpo():
    return f"""
<h2>A ideia: achar as linhas que interessam</h2>
<p>O <code>grep</code> mostra só as linhas que contêm um texto. Ele é o primo mais simples do <code>sed</code> e do <code>awk</code>: os dois também filtram linhas, mas o <code>grep</code> é o mais rápido de digitar quando só se quer <strong>ver</strong>.</p>
<hr>
<h2>1. Buscar um texto</h2>
{T("grep-basico", "grep ERRO log.txt")}
{ANAT(("grep", "o comando de busca."), ("ERRO", "o padrão procurado."), ("log.txt", "onde procurar."))}
<hr>
<h2>2. As opções do dia a dia</h2>
<p><code>-i</code> ignora maiúsculas e minúsculas; <code>-v</code> inverte (mostra as que <strong>não</strong> têm); <code>-c</code> conta; <code>-n</code> mostra o número da linha:</p>
{T("grep-opcoes", "grep -i rato texto.txt", "grep -v INFO log.txt", "grep -c ERRO log.txt", "grep -n AVISO log.txt")}
<p><code>-w</code> exige a palavra inteira, e <code>-o</code> mostra só o pedaço que casou. “ato” aparece dentro de “rato” e “mato” em 3 linhas, mas como palavra sozinha não aparece em nenhuma:</p>
{T("grep-wo", "grep -c ato texto.txt", "grep -cw ato texto.txt", "grep -o 'pedido=[0-9]*' log.txt")}
<hr>
<h2>3. Vários arquivos</h2>
<p>Com mais de um arquivo, o <code>grep</code> põe o nome na frente. O <code>-l</code> lista só os nomes dos arquivos que têm o padrão:</p>
{T("grep-varios", "grep Ana nomes.txt vendas.csv | head -4", "grep -l caderno *")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Arquivo que não existe", "O <code>grep</code> avisa, mas continua nos outros arquivos:", T("grep-erro", "grep ERRO log.txt nada.txt"))}
<div class="note"><strong>Nada encontrado não é erro na tela</strong><p>Quando não acha nada, o <code>grep</code> não escreve nada. Quem conta a história é o código de saída: <code>0</code> achou, <code>1</code> não achou, <code>2</code> erro.</p></div>
{T("grep-status", "grep FATAL log.txt; echo $?", "grep ERRO log.txt > /dev/null; echo $?")}
"""

def grep_ex():
    return (EX(1, "Ignorar maiúsculas", "Complete para achar rato, Rato ou RATO:", "grep ", "-i", " rato texto.txt", rotulo="opção") +
            EX(2, "Inverter", "Complete para mostrar as linhas que NÃO têm INFO:", "grep ", "-v", " INFO log.txt", rotulo="opção") +
            EX(3, "Contar", "Complete para contar as linhas com ERRO:", "grep ", "-c", " ERRO log.txt", rotulo="opção") +
            MC(4, "O que o <code>grep</code> mostra quando não encontra nada?", ["Uma mensagem de erro", "Nada (e sai com código 1)", "O arquivo inteiro", "A palavra “vazio”"], 2) +
            MC(5, "Para ver só o trecho que casou, e não a linha toda, use:", ["<code>-c</code>", "<code>-n</code>", "<code>-o</code>", "<code>-l</code>"], 3))

def grep_miss():
    return (M("grep-m1", "mostre as linhas de <code>log.txt</code> com AVISO, com o número da linha.", "grep -n AVISO log.txt", r"src:\bgrep\b;;src:-n;;out:4:2026-03-02 09:01:37 AVISO estoque baixo produto=caderno;;out:9:") +
            M("grep-m2", "conte quantas linhas de <code>log.txt</code> têm a palavra <code>login</code>.", "grep -c login log.txt", r"src:\bgrep\b;;src:-c;;outre:^3$"))

# ---------------------------------------------------------------- regex
def regex_corpo():
    return f"""
<h2>A ideia: padrões em vez de textos fixos</h2>
<p>Uma <strong>expressão regular</strong> (regex) descreve um <em>formato</em> de texto: “uma linha que começa com 2026”, “um número de 4 dígitos”, “ERRO ou AVISO”. O <code>grep</code>, o <code>sed</code> e o <code>awk</code> falam regex, então esta aula vale para os três. Os exemplos usam o <code>grep</code> por ser o mais curto.</p>
<hr>
<h2>1. Âncoras: <code>^</code> e <code>$</code></h2>
<p><code>^</code> é o começo da linha; <code>$</code>, o fim. <code>^O</code> pega as linhas que começam com O; <code>to\\.$</code>, as que terminam com “to.” (a barra faz o ponto valer como ponto de verdade). Vieram “resto.” e “mato.”:</p>
{T("regex-ancoras", "grep '^O' texto.txt", "grep 'to\\.$' texto.txt")}
<hr>
<h2>2. Curingas: <code>.</code>, <code>*</code> e classes <code>[ ]</code></h2>
<div class="table-wrap"><table class="ref">
<tr><th>Peça</th><th>Casa com</th></tr>
<tr><td><code>.</code></td><td>qualquer caractere (um só)</td></tr>
<tr><td><code>*</code></td><td>o anterior repetido 0 ou mais vezes</td></tr>
<tr><td><code>[abc]</code></td><td>um caractere entre a, b ou c</td></tr>
<tr><td><code>[0-9]</code></td><td>um dígito</td></tr>
<tr><td><code>[^0-9]</code></td><td>um caractere que <strong>não</strong> é dígito</td></tr>
<tr><td><code>\\.</code></td><td>um ponto de verdade (a barra tira o poder especial)</td></tr>
</table></div>
{T("regex-curingas", "grep 'r.to' texto.txt", "grep -o 'pedido=[0-9][0-9]*' log.txt", "grep '^[BC]' nomes.txt")}
<hr>
<h2>3. Regex estendida: <code>grep -E</code></h2>
<p>Com <code>-E</code>, ganham poder especial <code>+</code> (1 ou mais), <code>?</code> (0 ou 1), <code>{{n}}</code> (exatamente n vezes), <code>|</code> (ou) e os parênteses de agrupamento. Na regex básica, eles precisariam de barra invertida (<code>\\+</code>, <code>\\|</code>):</p>
{T("regex-estendida", "grep -E 'ERRO|AVISO' log.txt", "grep -oE '[0-9]{4}-[0-9]{4}' contatos.txt", "grep -oE '[a-z]+@[a-z.]+' contatos.txt")}
{ANAT(("grep -E", "regex estendida."), ("[0-9]{4}", "quatro dígitos seguidos."), ("-", "um hífen literal."), ("[0-9]{4}", "mais quatro dígitos."))}
<div class="tip"><strong>Básica ou estendida?</strong><p>No <code>sed</code>, a estendida se liga com <code>-E</code>, igual ao grep. No <code>awk</code>, a regex já é estendida por padrão. No <code>jq</code>, as funções <code>test</code> e <code>match</code> usam a regex do Oniguruma, parecida com a estendida.</p></div>
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Colchete sem fechar", "Uma classe aberta e não fechada é um erro na regex:", T("regex-erro", "grep '[0-9' log.txt"))}
{CEN("Esqueceu o -E", "Sem <code>-E</code>, o <code>|</code> é um caractere comum: o grep procurou o texto literal “ERRO|AVISO” e não achou nada (código de saída 1):", T("regex-erro2", "grep 'ERRO|AVISO' log.txt; echo $?"))}
"""

def regex_ex():
    return (EX(1, "Começo da linha", "Qual símbolo marca o começo da linha?", "grep '", "^", "2026' log.txt", rotulo="símbolo") +
            EX(2, "Fim da linha", "Qual símbolo marca o fim da linha?", "grep 'a", "$", "' nomes.txt", rotulo="símbolo") +
            EX(3, "Estendida", "Complete para usar regex estendida:", "grep ", "-E", " 'ERRO|AVISO' log.txt", rotulo="opção") +
            MC(4, "O que <code>[0-9]{3}</code> casa (com <code>-E</code>)?", ["o texto “0-9” três vezes", "três dígitos seguidos", "um dígito até 3", "nada"], 2) +
            MC(5, "Para casar um ponto de verdade, escreva:", ["<code>.</code>", "<code>\\.</code>", "<code>[.]*</code>", "<code>^.</code>"], 2))

def regex_miss():
    return (M("regex-m1", "mostre as linhas de <code>nomes.txt</code> que terminam com a letra <code>a</code>.", "grep 'a$' nomes.txt", r"src:\bgrep\b;;src:a\$;;outre:^Carla$;;outre:^Eduarda$") +
            M("regex-m2", "com <code>grep -oE</code>, tire só os telefones (formato <code>(11) 91234-5678</code>) de <code>contatos.txt</code>.", r"grep -oE '\([0-9]{2}\) [0-9]{5}-[0-9]{4}' contatos.txt", r"src:grep -oE|grep -Eo;;out:(11) 91234-5678;;out:(41) 97654-3210"))

NIVEL = {"id": "n1", "nome": "Nível 1 · Base", "curto": "Base", "desc": "O terreno em volta: pipes, filtros pequenos, grep e regex", "grupos": [
    {"grupo": "Começando", "aulas": [
        dict(slug="introducao", menu="O que são sed, awk e jq", title="O que são sed, awk e jq", h1='O que são <span class="hl">sed</span>, <span class="hl">awk</span> e <span class="hl">jq</span>',
             desc="Introdução ao Guia Texto no Terminal: para que servem o sed, o awk e o jq, as versões usadas no guia e a diferença entre gawk e mawk.",
             intro="Três ferramentas pequenas, presentes em quase todo Linux, fazem o trabalho pesado com texto: editar, somar colunas e entender JSON. Esta aula apresenta as três, com uma provinha real de cada uma.",
             aprender=["Para que serve cada ferramenta: <code>sed</code>, <code>awk</code> e <code>jq</code>.", "Como ver as versões instaladas.", "Por que o guia usa o <code>gawk</code> e o que muda no <code>mawk</code>."],
             corpo=intro_corpo, exercicios=intro_ex, missoes=intro_miss,
             ref=[("sed --version", "mostra a versão do sed."), ("awk --version", "mostra a versão do awk (no gawk)."), ("mawk -W version", "a versão do mawk."), ("jq --version", "mostra a versão do jq."), ("sudo apt install gawk jq", "instala o gawk e o jq no Debian/Ubuntu.")],
             resumo=["<code>sed</code> edita texto, <code>awk</code> trabalha com colunas e contas, <code>jq</code> entende JSON.", "O guia usa GNU sed 4.9, GNU awk 5.2 e jq 1.7, com saídas reais em pt_BR.", "Se o seu <code>awk</code> for o mawk, instale o gawk para acompanhar o guia."]),
        dict(slug="preparando", menu="A pasta de teste e os arquivos de exemplo", title="A pasta de teste e os arquivos de exemplo", h1='A pasta de teste e os <span class="hl">arquivos de exemplo</span>',
             desc="Como criar a pasta ~/guia-texto-teste com os arquivos de exemplo do guia (nomes, vendas, log, JSON) e voltar tudo ao original.",
             intro="Antes de editar e filtrar, você precisa de algo para editar. Esta aula cria a pasta de treino e apresenta os arquivos inventados que aparecem em todas as aulas.",
             aprender=["Criar a pasta <code>~/guia-texto-teste</code> com o script <code>criar-arquivos.sh</code>.", "O que tem em cada arquivo de exemplo.", "Como voltar os arquivos ao original."],
             corpo=prep_corpo, exercicios=prep_ex, missoes=prep_miss,
             ref=[("mkdir -p ~/guia-texto-teste", "cria a pasta de teste."), ("cd ~/guia-texto-teste", "entra nela."), ("bash criar-arquivos.sh", "cria (ou recria) os arquivos de exemplo."), ("ls -l", "lista os arquivos com tamanho.")],
             resumo=["Treine sempre em <code>~/guia-texto-teste</code>.", "O <code>criar-arquivos.sh</code> recria todos os arquivos de exemplo, sem internet.", "“Arquivo ou diretório inexistente” costuma ser pasta errada."]),
        dict(slug="pipes", menu="Pipes e redirecionamento", title="Pipes e redirecionamento (|, >, >>, <, 2>)", h1='Pipes e redirecionamento (<span class="hl">|</span>, <span class="hl">&gt;</span>, <span class="hl">&lt;</span>)',
             desc="Revisão de pipes e redirecionamento no Bash para usar com sed, awk e jq: |, >, >>, < e 2>, com saídas reais.",
             intro="O sed, o awk e o jq brilham quando encadeados com outros comandos. Esta aula revisa os canos e os desvios de saída que aparecem em todo o guia.",
             aprender=["O pipe <code>|</code>, que liga um comando no outro.", "Gravar com <code>&gt;</code> e acrescentar com <code>&gt;&gt;</code>.", "Ler com <code>&lt;</code> e desviar erros com <code>2&gt;</code>."],
             corpo=pipes_corpo, exercicios=pipes_ex, missoes=pipes_miss,
             ref=[("cmd1 | cmd2", "a saída de cmd1 entra em cmd2."), ("cmd > arq", "grava a saída em arq (apaga o que havia)."), ("cmd >> arq", "acrescenta no fim de arq."), ("cmd < arq", "lê a entrada de arq."), ("cmd 2> arq", "grava as mensagens de erro em arq.")],
             resumo=["<code>|</code> encadeia comandos; é assim que sed, awk e jq trabalham juntos.", "<code>&gt;</code> apaga o destino antes; nunca redirecione para o mesmo arquivo que está lendo.", "Erros saem por outro canal, desviado com <code>2&gt;</code>."]),
    ]},
    {"grupo": "Ferramentas de apoio", "aulas": [
        dict(slug="cat-head-tail-wc", menu="cat, head, tail e wc", title="Olhando arquivos: cat, head, tail e wc", h1='Olhando arquivos: <span class="hl">cat</span>, <span class="hl">head</span>, <span class="hl">tail</span> e <span class="hl">wc</span>',
             desc="Ver o arquivo inteiro, o começo, o fim e contar linhas, palavras e bytes com cat, head, tail e wc, com saídas reais.",
             intro="Antes de editar, olhe. Estas quatro ferramentas mostram o arquivo inteiro, só o começo, só o fim, e contam linhas e palavras.",
             aprender=["<code>cat -n</code> para ver com números de linha.", "<code>head</code>, <code>tail</code> e o truque <code>tail -n +2</code>.", "<code>wc</code> e a diferença entre bytes e caracteres."],
             corpo=cht_corpo, exercicios=cht_ex, missoes=cht_miss,
             ref=[("cat -n arq", "mostra com números de linha."), ("head -n 3 arq", "as 3 primeiras linhas."), ("tail -n 2 arq", "as 2 últimas linhas."), ("tail -n +2 arq", "da linha 2 em diante."), ("wc -l arq", "conta linhas."), ("wc -w / -c / -m", "palavras / bytes / caracteres.")],
             resumo=["<code>head</code> e <code>tail</code> mostram começo e fim; <code>tail -n +2</code> pula o cabeçalho.", "<code>wc -l</code> conta linhas.", "Acento ocupa 2 bytes: <code>wc -c</code> e <code>wc -m</code> podem dar números diferentes."]),
        dict(slug="cut", menu="Recortando colunas (cut)", title="Recortando colunas (cut)", h1='Recortando colunas (<span class="hl">cut</span>)',
             desc="O comando cut: recortar campos de um CSV com -d e -f, faixas, posições com -c e o problema dos espaços repetidos.",
             intro="Num CSV, cada linha é um registro e a vírgula separa as colunas. O <code>cut</code> recorta só as colunas que você quer.",
             aprender=["Recortar campos com <code>-d</code> e <code>-f</code>.", "Pedir vários campos e faixas.", "Recortar por posição com <code>-c</code>, e o limite do cut com espaços repetidos."],
             corpo=cut_corpo, exercicios=cut_ex, missoes=cut_miss,
             ref=[("cut -d , -f 2 arq", "o 2º campo, separado por vírgula."), ("cut -d , -f 2,4 arq", "os campos 2 e 4."), ("cut -d , -f 1-3 arq", "os campos 1 a 3."), ("cut -c 1-10 arq", "os caracteres 1 a 10 de cada linha.")],
             resumo=["<code>-d</code> é o separador, <code>-f</code> os campos.", "<code>-c</code> recorta por posição.", "Com espaços repetidos, prefira o <code>awk</code>."]),
        dict(slug="sort-uniq", menu="Ordenando e contando (sort e uniq)", title="Ordenando e contando repetidos (sort e uniq)", h1='Ordenando e contando (<span class="hl">sort</span> e <span class="hl">uniq</span>)',
             desc="sort alfabético, inverso e numérico, por coluna com -t e -k; uniq, uniq -c e o ranking sort | uniq -c | sort -rn.",
             intro="Ordenar e contar repetições responde muita pergunta: qual fruta mais aparece, qual venda foi maior. O <code>sort</code> e o <code>uniq</code> fazem isso juntos.",
             aprender=["<code>sort</code>, <code>-r</code>, <code>-n</code> e a ordenação por coluna.", "Por que o <code>uniq</code> precisa do <code>sort</code> antes.", "O ranking com <code>uniq -c</code> e <code>sort -rn</code>."],
             corpo=su_corpo, exercicios=su_ex, missoes=su_miss,
             ref=[("sort arq", "ordem alfabética."), ("sort -r arq", "ordem inversa."), ("sort -n arq", "ordem numérica."), ("sort -t , -k 4 -n arq", "pela coluna 4 do CSV, como número."), ("sort -u arq", "ordena e tira repetidos."), ("sort arq | uniq -c", "conta repetições.")],
             resumo=["<code>sort -n</code> para números; sem ele, “10” vem antes de “2”.", "<code>uniq</code> só junta repetidos vizinhos: ordene antes.", "<code>sort | uniq -c | sort -rn</code> é o ranking clássico."]),
        dict(slug="tr", menu="Trocando caracteres (tr)", title="Trocando caracteres (tr)", h1='Trocando caracteres (<span class="hl">tr</span>)',
             desc="O comando tr: maiúsculas e minúsculas, apagar com -d, espremer com -s, trocar separadores e o limite com acentos em UTF-8.",
             intro="O <code>tr</code> troca caracteres um por um: minúsculas por maiúsculas, vírgulas por tabulações. Rápido e simples, com uma pegadinha nos acentos.",
             aprender=["Trocar conjuntos de caracteres.", "Apagar (<code>-d</code>) e espremer repetições (<code>-s</code>).", "Por que o <code>tr</code> não entende acentos."],
             corpo=tr_corpo, exercicios=tr_ex, missoes=tr_miss,
             ref=[("tr 'a-z' 'A-Z' < arq", "minúsculas para maiúsculas."), ("tr -d '() -'", "apaga esses caracteres."), ("tr -s ' '", "espreme espaços repetidos."), ("tr ',' '\\t'", "troca vírgula por tabulação.")],
             resumo=["O <code>tr</code> lê da entrada padrão, nunca pelo nome do arquivo.", "<code>-d</code> apaga, <code>-s</code> espreme.", "Com acentos, use <code>awk</code> ou <code>sed</code>."]),
        dict(slug="grep", menu="Procurando linhas (grep)", title="Procurando linhas (grep)", h1='Procurando linhas (<span class="hl">grep</span>)',
             desc="O grep básico: buscar texto, -i, -v, -c, -n, -w, -o, vários arquivos, -l e o código de saída.",
             intro="Antes de editar com o sed, quase sempre a gente procura. O <code>grep</code> mostra só as linhas que contêm um texto.",
             aprender=["Buscar um texto num arquivo.", "As opções <code>-i</code>, <code>-v</code>, <code>-c</code>, <code>-n</code>, <code>-w</code> e <code>-o</code>.", "Buscar em vários arquivos e ler o código de saída."],
             corpo=grep_corpo, exercicios=grep_ex, missoes=grep_miss,
             ref=[("grep texto arq", "linhas com texto."), ("grep -i", "ignora maiúsculas."), ("grep -v", "linhas sem o texto."), ("grep -c", "conta as linhas."), ("grep -n", "mostra o número da linha."), ("grep -o", "só o trecho que casou."), ("grep -l texto *", "só os nomes dos arquivos.")],
             resumo=["<code>grep</code> filtra linhas; <code>-v</code> inverte.", "<code>-c</code> conta e <code>-n</code> numera.", "Código de saída: 0 achou, 1 não achou, 2 erro."]),
        dict(slug="regex", menu="Expressões regulares básicas", title="Expressões regulares básicas (^, $, ., *, [ ], -E)", h1='Expressões <span class="hl">regulares</span> básicas',
             desc="Regex para grep, sed e awk: âncoras ^ e $, ponto, asterisco, classes [ ], regex estendida com grep -E, +, {n} e |.",
             intro="Expressões regulares descrevem formatos de texto. Elas são a língua comum do grep, do sed e do awk, então valem para o resto do guia.",
             aprender=["Âncoras <code>^</code> e <code>$</code>.", "Curingas <code>.</code> e <code>*</code> e classes <code>[ ]</code>.", "Regex estendida (<code>-E</code>) com <code>+</code>, <code>{n}</code> e <code>|</code>."],
             corpo=regex_corpo, exercicios=regex_ex, missoes=regex_miss,
             ref=[("^texto", "linha que começa com texto."), ("texto$", "linha que termina com texto."), (".", "qualquer caractere."), ("[0-9]", "um dígito."), ("x*", "x repetido 0 ou mais vezes."), ("-E 'a+'", "a, 1 ou mais vezes (estendida)."), ("-E 'a|b'", "a ou b (estendida)."), ("-E '[0-9]{4}'", "4 dígitos (estendida).")],
             resumo=["<code>^</code> e <code>$</code> prendem no começo e no fim.", "<code>[ ]</code> é um caractere de uma lista; <code>.</code> é qualquer um.", "Para <code>+</code>, <code>?</code>, <code>{n}</code> e <code>|</code>, use <code>-E</code>."]),
    ]},
]}
