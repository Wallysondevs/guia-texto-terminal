# -*- coding: utf-8 -*-
"""Nível 4 · jq, o canivete do JSON."""
from lib_guia import *

def aula(**k):
    return k

INGLES = '<div class="note"><strong>Mensagens do jq em inglês</strong><p>O jq não tem tradução: mesmo num Linux em português, as mensagens de erro saem em inglês. Elas aparecem aqui exatamente como o jq escreveu, com a explicação em português.</p></div>'

# ---------------------------------------------------------------- intro
def intro_corpo():
    return f"""
<h2>A ideia: JSON é texto com estrutura</h2>
<p>JSON é o formato das APIs e de muitos arquivos de configuração: <strong>objetos</strong> entre chaves (<code>{{"nome": "caderno"}}</code>), <strong>listas</strong> (arrays) entre colchetes (<code>["azul", "verde"]</code>), textos entre aspas, números, <code>true</code>, <code>false</code> e <code>null</code>. O <code>sed</code> e o <code>awk</code> enxergam JSON como linhas soltas; o <code>jq</code> entende a estrutura e navega por ela.</p>
<hr>
<h2>1. O filtro <code>.</code>: mostrar bonito</h2>
<p>O programa mais simples do jq é <code>.</code> (“a entrada inteira”). Ele lê o JSON e devolve formatado, com recuo:</p>
{T("jqi-ponto", "cat produto.json", "jq . produto.json")}
{ANAT(("jq", "o programa."), ("'.'", "o filtro: a entrada inteira, sem mudança."), ("produto.json", "o arquivo JSON."))}
<p>Na sua tela, o jq ainda pinta as chaves, os textos e os números com cores diferentes. A coleta foi gravada sem terminal, por isso as caixas do guia não têm cor.</p>
<hr>
<h2>2. <code>-c</code>: tudo numa linha</h2>
<p>O contrário: <code>-c</code> (<em>compact</em>) devolve cada resultado numa linha só, ótimo para passar adiante num pipe:</p>
{T("jqi-c", "jq -c . usuarios.json | cut -c 1-70")}
<hr>
<h2>3. Do pipe</h2>
<p>Como as outras ferramentas, o jq lê do <code>|</code>. Na vida real, a entrada costuma vir de uma API, com <code>curl -s https://… | jq .</code>. Neste guia, tudo é local: os arquivos fazem o papel da resposta da API.</p>
{T("jqi-pipe", "echo '{\"loja\": \"Papelaria\", \"aberta\": true}' | jq .", "cat pedidos.json | jq -c '.loja'")}
{INGLES}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("JSON quebrado", "O <code>quebrado.json</code> termina no meio, sem fechar a chave. O jq diz onde a leitura parou (“Unfinished JSON term at EOF”: termo JSON inacabado no fim do arquivo):", T("jqi-erro", "jq . quebrado.json"))}
{CEN("Esqueceu o filtro", "Com arquivo, o jq precisa do filtro antes do nome. Sem ele, o jq acha que <code>produto.json</code> é o programa e lê <code>produto</code> como o nome de uma função sem argumentos (<code>produto/0</code>) que não existe (“is not defined”: não está definida):", T("jqi-erro2", "jq produto.json"))}
"""

def intro_ex():
    return (EX(1, "A entrada inteira", "Qual filtro devolve a entrada inteira, formatada?", "jq '", ".", "' produto.json", rotulo="filtro") +
            EX(2, "Compacto", "Qual opção põe cada resultado numa linha?", "jq ", "-c", " . usuarios.json", rotulo="opção") +
            MC(3, "Em JSON, o que fica entre colchetes <code>[ ]</code>?", ["um objeto", "uma lista (array)", "um texto", "um comentário"], 2) +
            MC(4, "As mensagens de erro do jq saem:", ["em português, como as do sed", "em inglês, porque o jq não tem tradução", "em espanhol", "não existem"], 2))

def intro_miss():
    return (M("jqi-m1", "mostre <code>produto.json</code> formatado com o filtro <code>.</code>.", "jq . produto.json", r"src:\bjq\b;;out:\"estoque\": {;;out:\"deposito\": 120") +
            M("jqi-m2", "mostre <code>pedidos.json</code> compacto, numa linha só.", "jq -c . pedidos.json", r"src:jq -c;;outre:^\{\"loja\":\"Papelaria da Ana\",\"atualizado\":\"2026-03-05\""))

# ---------------------------------------------------------------- campos
def campos_corpo():
    return f"""
<h2>A ideia: um caminho até o dado</h2>
<p>Num objeto JSON, cada valor tem uma chave. Em jq, <code>.chave</code> pega o valor dessa chave. Para descer em objetos dentro de objetos, emende: <code>.estoque.loja</code>. É como um endereço: rua, número, apartamento.</p>
<hr>
<h2>1. Um campo</h2>
{T("jqc-um", "jq '.nome' produto.json", "jq '.preco' produto.json", "jq '.cores' produto.json")}
<p>Repare: o texto veio <strong>com aspas</strong>, porque o jq devolve JSON. A aula de <code>-r</code> mostra como tirar as aspas.</p>
<hr>
<h2>2. Campos aninhados</h2>
{T("jqc-aninhado", "jq '.estoque' produto.json", "jq '.estoque.deposito' produto.json", "jq '.pedidos[0].itens[0].produto' pedidos.json")}
{ANAT((".pedidos", "a lista de pedidos."), ("[0]", "o primeiro pedido."), (".itens[0]", "o primeiro item dele."), (".produto", "o nome do produto."))}
<hr>
<h2>3. Vários campos de uma vez</h2>
<p>A vírgula produz vários resultados, um depois do outro:</p>
{T("jqc-virgula", "jq '.nome, .preco, .estoque.loja' produto.json")}
<hr>
<h2>4. Campo que não existe: <code>null</code></h2>
<p>Pedir uma chave que não existe não é erro: o jq devolve <code>null</code> (“nada”). A aula de null mostra como tratar isso.</p>
{T("jqc-null", "jq '.peso' produto.json")}
<hr>
<h2>5. Chaves com caracteres especiais</h2>
<p>Se a chave tiver espaço, hífen ou acento, use aspas: <code>."nome da chave"</code>, ou a forma de colchetes <code>.["nome da chave"]</code>:</p>
{T("jqc-especial", "echo '{\"data-de-entrega\": \"2026-03-10\"}' | jq '.\"data-de-entrega\"'", "echo '{\"data-de-entrega\": \"2026-03-10\"}' | jq '.[\"data-de-entrega\"]'")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Entrar num número", "<code>.estoque.loja</code> é o número 40. Pedir uma chave dentro de um número é erro (“Cannot index number with string &quot;x&quot;”: não dá para indexar um número com o texto “x”):", T("jqc-erro", "jq '.estoque.loja.x' produto.json"))}
{CEN("Hífen sem aspas", "Sem aspas, o jq lê <code>.data-de-entrega</code> como uma conta: <code>.data</code> menos <code>de</code> menos <code>entrega</code>, e <code>de</code> não é uma função conhecida:", T("jqc-erro2", "echo '{\"data-de-entrega\": \"x\"}' | jq '.data-de-entrega'"))}
"""

def campos_ex():
    return (EX(1, "Um campo", "Complete para pegar o preço:", "jq '", ".preco", "' produto.json", rotulo="filtro") +
            EX(2, "Aninhado", "Complete para pegar o estoque da loja:", "jq '.estoque", ".loja", "' produto.json", rotulo="filtro") +
            MC(3, "O que o jq devolve para uma chave que não existe?", ["um erro", "<code>null</code>", "<code>0</code>", "nada, nem uma linha"], 2) +
            MC(4, "Como pegar a chave <code>data-de-entrega</code>?", ["<code>.data-de-entrega</code>", "<code>.\"data-de-entrega\"</code>", "<code>.data_de_entrega</code>", "<code>$data-de-entrega</code>"], 2))

def campos_miss():
    return (M("jqc-m1", "mostre o estoque do depósito de <code>produto.json</code>.", "jq '.estoque.deposito' produto.json", r"src:\.estoque\.deposito;;outre:^120$") +
            M("jqc-m2", "mostre o nome da loja e a data de atualização de <code>pedidos.json</code>, num filtro com vírgula.", "jq '.loja, .atualizado' pedidos.json", r"src:\.loja\s*,\s*\.atualizado;;outre:^\"Papelaria da Ana\"$;;outre:^\"2026-03-05\"$"))

# ---------------------------------------------------------------- arrays
def arr_corpo():
    return f"""
<h2>A ideia: listas e o “para cada”</h2>
<p>Muito JSON é uma lista de coisas parecidas: usuários, pedidos, produtos. Com <code>[n]</code> você pega um item pela posição (começando em 0). Com <code>[]</code>, sem número, o jq <strong>abre a lista</strong> e devolve cada item separado, e o que vier depois vale para cada um.</p>
<hr>
<h2>1. Posição: <code>.[0]</code>, <code>.[-1]</code></h2>
<p>O <code>usuarios.json</code> é uma lista. <code>.[0]</code> é o primeiro; <code>.[-1]</code>, o último:</p>
{T("jqa-pos", "jq '.[0]' usuarios.json", "jq '.[-1].nome' usuarios.json")}
<hr>
<h2>2. Fatias: <code>.[1:3]</code></h2>
<p>Do item 1 até antes do 3 (ou seja, o 2º e o 3º), devolvidos como lista:</p>
{T("jqa-fatia", "jq -c '.[1:3]' produto.json", "jq -c '.cores[1:]' produto.json", "jq -c '.cores[:2]' produto.json")}
<p>O primeiro comando deu erro: o <code>produto.json</code> é um objeto, não uma lista, e objeto não tem fatia. Nos dois seguintes, aplicada a <code>.cores</code>, que é lista, funciona: <code>[1:]</code> é “do 1 até o fim” e <code>[:2]</code>, “do começo até antes do 2”.</p>
<hr>
<h2>3. <code>.[]</code>: cada item</h2>
<p>O <code>.[]</code> devolve cada item da lista, um por resultado. Emendando <code>.nome</code>, sai o nome de cada um:</p>
{T("jqa-cada", "jq '.cores[]' produto.json", "jq '.[].nome' usuarios.json", "jq '.pedidos[].cliente' pedidos.json")}
{ANAT((".pedidos", "a lista de pedidos."), ("[]", "abre a lista: um resultado por pedido."), (".cliente", "de cada pedido, o cliente."))}
<hr>
<h2>4. Listas dentro de listas</h2>
<p>Cada pedido tem uma lista de itens. Dois <code>[]</code> abrem as duas camadas e dão todos os produtos de todos os pedidos:</p>
{T("jqa-dupla", "jq '.pedidos[].itens[].produto' pedidos.json")}
<hr>
<h2>5. <code>.[]</code> num objeto</h2>
<p>Num objeto, <code>.[]</code> devolve os <strong>valores</strong> (sem as chaves):</p>
{T("jqa-objeto", "jq '.estoque[]' produto.json")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Número num objeto", "<code>[0]</code> só funciona em listas. Num objeto, é erro (“Cannot index object with number”: não dá para indexar um objeto com número):", T("jqa-erro", "jq '.[0]' produto.json"))}
{CEN("Abrir um texto", "<code>[]</code> abre listas e objetos, não textos (“Cannot iterate over string”: não dá para percorrer um texto):", T("jqa-erro2", "jq '.nome[]' produto.json"))}
"""

def arr_ex():
    return (EX(1, "O primeiro", "Complete para pegar o primeiro usuário:", "jq '.", "[0]", "' usuarios.json", rotulo="índice") +
            EX(2, "Cada item", "Complete para devolver cada cor separada:", "jq '.cores", "[]", "' produto.json", rotulo="filtro") +
            MC(3, "Em jq, a primeira posição de uma lista é:", ["1", "0", "-1", "a"], 2) +
            MC(4, "<code>.[-1]</code> pega:", ["o primeiro item", "o último item", "nada", "todos menos o último"], 2))

def arr_miss():
    return (M("jqa-m1", "mostre a cidade de cada usuário de <code>usuarios.json</code>.", "jq '.[].cidade' usuarios.json", r"src:\.\[\]\.cidade;;outre:^\"Rio de Janeiro\"$;;outre:^\"Belo Horizonte\"$") +
            M("jqa-m2", "mostre o <code>id</code> de cada pedido de <code>pedidos.json</code>.", "jq '.pedidos[].id' pedidos.json", r"src:\.pedidos\[\]\.id;;outre:^1042$;;outre:^1045$"))

# ---------------------------------------------------------------- select
def sel_corpo():
    return f"""
<h2>A ideia: o pipe de dentro e o filtro</h2>
<p>Dentro do programa jq também existe <code>|</code>: a saída de um filtro vira a entrada do próximo, igual ao pipe do Bash. E o <code>select(condição)</code> deixa passar só os itens em que a condição é verdadeira, o <code>grep</code> do JSON.</p>
<hr>
<h2>1. O <code>|</code> do jq</h2>
<p><code>.[] | .nome</code> é o mesmo que <code>.[].nome</code>: abra a lista e, de cada item, pegue o nome. Com o pipe fica mais fácil de ler quando o caminho cresce:</p>
{T("jqs-pipe", "jq '.[] | .nome' usuarios.json", "jq '.pedidos[] | .itens[] | .produto' pedidos.json | sort -u")}
<hr>
<h2>2. <code>select</code>: filtrar</h2>
<p>Só os usuários ativos; só os maiores de 30; só os de São Paulo:</p>
{T("jqs-select", "jq '.[] | select(.ativo) | .nome' usuarios.json", "jq '.[] | select(.idade > 30) | .nome' usuarios.json", "jq '.[] | select(.cidade == \"São Paulo\") | .nome' usuarios.json")}
{ANAT((".[]", "cada usuário."), ("select(.idade > 30)", "deixa passar só quem tem idade maior que 30."), (".nome", "dos que passaram, o nome."))}
<hr>
<h2>3. <code>and</code>, <code>or</code>, <code>not</code></h2>
{T("jqs-logica", "jq '.[] | select(.ativo and .idade < 30) | .nome' usuarios.json", "jq '.pedidos[] | select(.status == \"pago\" or .status == \"pendente\") | .id' pedidos.json", "jq '.[] | select(.ativo | not) | .nome' usuarios.json")}
<hr>
<h2>4. Regex: <code>test</code></h2>
<p><code>test("regex")</code> é verdadeiro se o texto casa. Com <code>"i"</code> no segundo argumento, sem diferenciar maiúsculas:</p>
{T("jqs-test", "jq '.[] | select(.nome | test(\"^[AB]\")) | .nome' usuarios.json", "jq '.[] | select(.cidade | test(\"paulo\"; \"i\")) | .id' usuarios.json")}
<hr>
<h2>5. Filtrar dentro de listas</h2>
<p>Os pedidos que têm pelo menos um item de caneta, usando <code>any</code>:</p>
{T("jqs-any", "jq '.pedidos[] | select(any(.itens[]; .produto == \"caneta\")) | .cliente' pedidos.json")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("select sem parênteses", "A condição do <code>select</code> vai entre parênteses. Sem eles, o jq procura uma função <code>select</code> sem argumentos (<code>select/0</code>), que não existe:", T("jqs-erro", "jq '.[] | select .ativo' usuarios.json"))}
{CEN("Um = só", "Em jq, comparar é <code>==</code>. Um <code>=</code> só é atribuição: o resultado dela é um objeto, que conta como verdadeiro, então <strong>todos</strong> passaram no filtro (e a cidade nem mudou na saída, porque o <code>select</code> devolve o item original):", T("jqs-erro2", "jq -c '.[] | select(.cidade = \"Recife\") | {nome, cidade}' usuarios.json"))}
"""

def sel_ex():
    return (EX(1, "Filtrar", "Qual função deixa passar só os itens em que a condição é verdadeira?", "jq '.[] | ", "select", "(.ativo)' usuarios.json", rotulo="função") +
            EX(2, "Comparar", "Qual operador compara igualdade?", "select(.status ", "==", " \"pago\")", rotulo="operador") +
            MC(3, "<code>.[] | .nome</code> é o mesmo que:", ["<code>.nome[]</code>", "<code>.[].nome</code>", "<code>.nome</code>", "<code>[.nome]</code>"], 2) +
            MC(4, "Para testar uma regex num texto, use:", ["<code>grep</code>", "<code>test(\"regex\")</code>", "<code>~ /regex/</code>", "<code>=~</code>"], 2))

def sel_miss():
    return (M("jqs-m1", "mostre o <code>id</code> dos pedidos com status <code>pago</code> em <code>pedidos.json</code>.", "jq '.pedidos[] | select(.status == \"pago\") | .id' pedidos.json", r"src:select;;src:pago;;outre:^1042$;;outre:^1044$") +
            M("jqs-m2", "mostre o nome dos usuários com idade menor que 30.", "jq '.[] | select(.idade < 30) | .nome' usuarios.json", r"src:select\(\.idade\s*<\s*30\);;outre:^\"Ana Souza\"$;;outre:^\"Carla Dias\"$"))

# ---------------------------------------------------------------- map
def map_corpo():
    return f"""
<h2>A ideia: trabalhar com a lista inteira</h2>
<p>O <code>.[]</code> desmonta a lista em itens soltos. Às vezes você quer continuar com uma <strong>lista</strong>: transformar cada item e receber a lista de volta. Para isso existe o <code>map</code>. E há funções que olham a lista toda: <code>length</code> (tamanho), <code>keys</code> (chaves), <code>add</code> (soma), <code>min</code>, <code>max</code>.</p>
<hr>
<h2>1. <code>map</code></h2>
<p><code>map(.nome)</code> devolve uma lista só com os nomes. É o mesmo que <code>[.[] | .nome]</code>, os colchetes juntando os resultados numa lista:</p>
{T("jqm-map", "jq -c 'map(.nome)' usuarios.json", "jq -c '[.[] | .nome]' usuarios.json", "jq -c 'map(.idade + 1)' usuarios.json")}
<hr>
<h2>2. <code>length</code></h2>
<p>Tamanho de uma lista, número de chaves de um objeto, letras de um texto:</p>
{T("jqm-length", "jq 'length' usuarios.json", "jq '.pedidos | length' pedidos.json", "jq '.[] | .tags | length' usuarios.json", "jq '.nome | length' produto.json")}
<hr>
<h2>3. <code>keys</code> e <code>has</code></h2>
<p><code>keys</code> lista as chaves de um objeto (em ordem alfabética); <code>has("chave")</code> diz se ela existe:</p>
{T("jqm-keys", "jq -c 'keys' produto.json", "jq -c '.[0] | keys' usuarios.json", "jq 'has(\"preco\"), has(\"peso\")' produto.json")}
<hr>
<h2>4. <code>add</code>, <code>min</code>, <code>max</code> e a média</h2>
<p><code>add</code> soma os itens de uma lista. Com <code>length</code>, dá a média:</p>
{T("jqm-add", "jq 'map(.idade) | add' usuarios.json", "jq 'map(.idade) | add / length' usuarios.json", "jq 'map(.idade) | min, max' usuarios.json")}
{ANAT(("map(.idade)", "lista com as idades: [28,35,22,41]."), ("add", "soma: 126."), ("/ length", "divide pela quantidade: 4."))}
<hr>
<h2>5. <code>map</code> com <code>select</code></h2>
<p>Dentro do <code>map</code>, o <code>select</code> filtra e a lista volta menor. Quantos usuários ativos?</p>
{T("jqm-mapsel", "jq 'map(select(.ativo)) | length' usuarios.json", "jq -c '.pedidos | map(select(.status != \"cancelado\") | .id)' pedidos.json")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("keys de um texto", "Texto não tem chaves (“has no keys”):", T("jqm-erro", "jq '.nome | keys' produto.json"))}
{CEN("map num objeto", "No jq 1.7, <code>map</code> num objeto passa pelos valores; aqui, os valores 40 e 120 não têm o campo <code>nome</code> (“Cannot index number”):", T("jqm-erro2", "jq 'map(.nome)' <<< '{\"a\": 40, \"b\": 120}'"))}
"""

def map_ex():
    return (EX(1, "Transformar a lista", "Qual função aplica um filtro a cada item e devolve uma lista?", "jq '", "map", "(.nome)' usuarios.json", rotulo="função") +
            EX(2, "Somar", "Qual função soma os itens da lista?", "jq 'map(.idade) | ", "add", "' usuarios.json", rotulo="função") +
            MC(3, "<code>map(.nome)</code> é o mesmo que:", ["<code>.[].nome</code>", "<code>[.[] | .nome]</code>", "<code>.nome[]</code>", "<code>keys</code>"], 2) +
            MC(4, "Na coleta, quanto deu <code>map(.idade) | add / length</code>?", ["126", "31.5", "4", "41"], 2))

def map_miss():
    return (M("jqm-m1", "mostre quantos pedidos existem em <code>pedidos.json</code>.", "jq '.pedidos | length' pedidos.json", r"src:length;;outre:^4$") +
            M("jqm-m2", "mostre a lista (compacta) com o e-mail de cada usuário, usando <code>map</code>.", "jq -c 'map(.email)' usuarios.json", r"src:map\(\.email\);;out:[\"ana@exemplo.com\",\"bruno@exemplo.com\",null,\"diego@exemplo.com\"]"))

# ---------------------------------------------------------------- -r e strings
def str_corpo():
    return f"""
<h2>A ideia: sair do JSON para texto</h2>
<p>O jq devolve JSON: textos aparecem entre aspas. Isso é ótimo para mandar para outro programa que lê JSON, mas ruim para ler ou para passar ao <code>sort</code>, ao <code>awk</code> e a um script. A opção <code>-r</code> (<em>raw</em>, “cru”) tira as aspas. E as strings do jq têm truques próprios: interpolação, <code>join</code>, maiúsculas, <code>split</code>.</p>
<hr>
<h2>1. <code>-r</code>: sem aspas</h2>
{T("jqr-r", "jq '.[].nome' usuarios.json", "jq -r '.[].nome' usuarios.json")}
<p>Sem aspas, a saída combina com as ferramentas dos níveis anteriores:</p>
{T("jqr-combo", "jq -r '.[].cidade' usuarios.json | sort | uniq -c")}
<hr>
<h2>2. Interpolação: <code>\\( )</code></h2>
<p>Dentro de um texto do jq, <code>\\(filtro)</code> é trocado pelo resultado do filtro, como o <code>$variavel</code> do Bash:</p>
{T("jqr-interp", "jq -r '.[] | \"\\(.nome) tem \\(.idade) anos e mora em \\(.cidade)\"' usuarios.json")}
{ANAT(('"..."', "um texto do jq, entre aspas duplas."), ("\\(.nome)", "troca pelo nome do item."), ("\\(.idade)", "números entram sem conversão."))}
<hr>
<h2>3. <code>join</code>, <code>split</code>, maiúsculas</h2>
{T("jqr-join", "jq -r '.cores | join(\", \")' produto.json", "jq -r '.[] | \"\\(.nome): \\(.tags | join(\"/\"))\"' usuarios.json", "jq -c 'split(\" \")' <<< '\"Ana Souza\"'", "jq -r '.[].nome | ascii_upcase' usuarios.json")}
<p>O <code>ascii_upcase</code> só mexe nas letras sem acento (por isso o nome tem “ascii”). Para acentos, passe o resultado para o <code>sed 's/.*/\\U&amp;/'</code> ou o <code>awk</code>.</p>
<hr>
<h2>4. Juntar textos com <code>+</code></h2>
<p><code>+</code> emenda textos. Números precisam virar texto antes, com <code>tostring</code>:</p>
{T("jqr-mais", "jq -r '.[] | .nome + \" (\" + (.idade | tostring) + \")\"' usuarios.json")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Texto + número", "Sem o <code>tostring</code>, somar texto com número é erro (“string and number cannot be added”: texto e número não podem ser somados):", T("jqr-erro", "jq -r '.[0] | .nome + \" - \" + .idade' usuarios.json"))}
"""

def str_ex():
    return (EX(1, "Sem aspas", "Qual opção tira as aspas dos textos?", "jq ", "-r", " '.[].nome' usuarios.json", rotulo="opção") +
            EX(2, "Juntar a lista", "Qual função junta uma lista de textos com um separador?", "jq -r '.cores | ", "join", "(\", \")' produto.json", rotulo="função") +
            MC(3, "Dentro de um texto do jq, <code>\\(.nome)</code>:", ["é um erro", "é trocado pelo valor de .nome", "imprime “.nome”", "é um comentário"], 2) +
            MC(4, "Para emendar um número num texto com <code>+</code>, antes use:", ["<code>tonumber</code>", "<code>tostring</code>", "<code>-r</code>", "<code>join</code>"], 2))

def str_miss():
    return (M("jqr-m1", "mostre o nome de cada cliente de <code>pedidos.json</code>, sem aspas.", "jq -r '.pedidos[].cliente' pedidos.json", r"src:jq -r;;outre:^Bruno$;;outre:^Ana$") +
            M("jqr-m2", "com interpolação, mostre cada pedido no formato <code>Pedido 1042: pago</code>.", "jq -r '.pedidos[] | \"Pedido \\(.id): \\(.status)\"' pedidos.json", r"src:\\\(;;out:Pedido 1042: pago;;out:Pedido 1045: cancelado"))

# ---------------------------------------------------------------- objetos
def obj_corpo():
    return f"""
<h2>A ideia: montar o JSON que você quer</h2>
<p>Além de extrair, o jq <strong>constrói</strong>: <code>{{ }}</code> monta objetos e <code>[ ]</code> monta listas. É assim que se tira só o necessário de uma resposta grande de API, se renomeia campos e se calcula campos novos.</p>
<hr>
<h2>1. Objetos com campos escolhidos</h2>
<p><code>{{nome, cidade}}</code> é um atalho para <code>{{nome: .nome, cidade: .cidade}}</code>:</p>
{T("jqo-atalho", "jq -c '.[] | {nome, cidade}' usuarios.json")}
<hr>
<h2>2. Renomear e calcular</h2>
<p>Do lado esquerdo do <code>:</code>, o nome novo; do direito, qualquer filtro:</p>
{T("jqo-calc", "jq -c '.pedidos[] | {pedido: .id, cliente, itens: (.itens | length), total: (.itens | map(.qtd * .preco) | add)}' pedidos.json")}
{ANAT(("pedido: .id", "renomeia id para pedido."), ("cliente", "mantém o cliente."), ("itens: (.itens | length)", "um campo calculado: quantos itens."), ("total: (... | add)", "soma de qtd × preço."))}
<hr>
<h2>3. Montar listas com <code>[ ]</code></h2>
<p>Colchetes em volta de um filtro juntam todos os resultados numa lista:</p>
{T("jqo-lista", "jq -c '[.[] | select(.ativo) | .id]' usuarios.json", "jq -c '{loja, clientes: [.pedidos[].cliente]}' pedidos.json")}
<hr>
<h2>4. Chave calculada: <code>(expr): valor</code></h2>
<p>Com parênteses, a <strong>chave</strong> também vem de um filtro. Com <code>add</code>, os objetos pequenos viram um só, um “dicionário” de nome para idade:</p>
{T("jqo-chave", "jq -c '.[] | {(.nome): .idade}' usuarios.json", "jq -c 'map({(.nome): .idade}) | add' usuarios.json")}
<hr>
<h2>5. Mudar um campo e manter o resto</h2>
<p><code>.campo = valor</code> devolve o objeto inteiro com o campo trocado; <code>+=</code> soma; <code>del(.campo)</code> remove:</p>
{T("jqo-mudar", "jq -c '.preco = 13.9' produto.json", "jq -c '.estoque.loja += 10 | del(.cores)' produto.json")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Faltou o dois-pontos", "Dentro de <code>{{ }}</code>, cada campo é <code>chave: valor</code> ou só o nome do campo. Um filtro solto quebra a sintaxe:", T("jqo-erro", "jq '.[] | {nome .idade}' usuarios.json"))}
"""

def obj_ex():
    return (EX(1, "Atalho", "Complete para montar um objeto só com nome e idade:", "jq -c '.[] | ", "{nome, idade}", "' usuarios.json") +
            EX(2, "Juntar em lista", "Qual símbolo junta todos os resultados numa lista?", "jq -c '", "[", ".[].nome]' usuarios.json", rotulo="símbolo") +
            MC(3, "<code>{nome}</code> é o mesmo que:", ["<code>{\"nome\"}</code>", "<code>{nome: .nome}</code>", "<code>.nome</code>", "<code>[.nome]</code>"], 2) +
            MC(4, "O que <code>del(.cores)</code> faz?", ["apaga o arquivo", "devolve o objeto sem o campo cores", "esvazia a lista de cores", "dá erro"], 2))

def obj_miss():
    return (M("jqo-m1", "monte, para cada usuário, um objeto compacto só com <code>id</code> e <code>email</code>.", "jq -c '.[] | {id, email}' usuarios.json", r"src:\{id,\s*email\};;out:{\"id\":1,\"email\":\"ana@exemplo.com\"};;out:{\"id\":3,\"email\":null}") +
            M("jqo-m2", "monte uma lista (compacta) com os <code>id</code> dos pedidos.", "jq -c '[.pedidos[].id]' pedidos.json", r"src:\[\.pedidos\[\]\.id\];;out:[1042,1043,1044,1045]"))

# ---------------------------------------------------------------- ordenar
def ord_corpo():
    return f"""
<h2>A ideia: ordenar e agrupar sem sair do JSON</h2>
<p>O <code>sort</code> do terminal ordena linhas. No JSON, você quer ordenar objetos por um campo, agrupar por cidade, achar o mais velho. O jq tem funções para isso, todas trabalhando sobre uma <strong>lista</strong>.</p>
<hr>
<h2>1. <code>sort_by</code> e <code>reverse</code></h2>
{T("jqord-sort", "jq -r 'sort_by(.idade) | .[] | \"\\(.idade) \\(.nome)\"' usuarios.json", "jq -r 'sort_by(.idade) | reverse | .[0].nome' usuarios.json")}
{ANAT(("sort_by(.idade)", "ordena a lista pela idade, da menor para a maior."), ("| reverse", "inverte a lista."), ("| .[0].nome", "o primeiro da lista invertida: o mais velho."))}
<hr>
<h2>2. <code>min_by</code> e <code>max_by</code></h2>
{T("jqord-minmax", "jq -r 'min_by(.idade).nome, max_by(.idade).nome' usuarios.json")}
<hr>
<h2>3. <code>group_by</code>: agrupar</h2>
<p><code>group_by(.cidade)</code> devolve uma lista de grupos (cada grupo é uma lista). Com um <code>map</code>, cada grupo vira um resumo:</p>
{T("jqord-group", "jq -c 'group_by(.cidade) | map({cidade: .[0].cidade, pessoas: length})' usuarios.json")}
<p>O mesmo nos pedidos: quantos pedidos por status:</p>
{T("jqord-status", "jq -r '.pedidos | group_by(.status) | .[] | \"\\(.[0].status): \\(length)\"' pedidos.json")}
<hr>
<h2>4. <code>unique</code> e <code>unique_by</code></h2>
<p><code>unique</code> tira repetidos de uma lista simples (e ordena); <code>unique_by</code> fica com um item por valor do campo:</p>
{T("jqord-unique", "jq -c '[.pedidos[].itens[].produto] | unique' pedidos.json", "jq -c 'unique_by(.cidade) | map(.nome)' usuarios.json")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("sort_by num objeto", "As funções de ordenar são para listas. Num objeto, o <code>sort_by</code> passa pelos valores e tenta pegar <code>.loja</code> de cada um; no primeiro, o texto “caderno”, já quebra:", T("jqord-erro", "jq 'sort_by(.loja)' produto.json"))}
{CEN("Esqueceu de juntar", "<code>.[].idade</code> são números soltos, não uma lista. O <code>sort</code> recebe um número de cada vez (“cannot be sorted, as it is not an array”: não pode ser ordenado, porque não é uma lista):", T("jqord-erro2", "jq '.[].idade | sort' usuarios.json"), "Junte numa lista antes: <code>[.[].idade] | sort</code>.")}
"""

def ord_ex():
    return (EX(1, "Ordenar por campo", "Complete para ordenar por idade:", "jq '", "sort_by", "(.idade)' usuarios.json", rotulo="função") +
            EX(2, "Agrupar", "Qual função agrupa por um campo?", "jq '", "group_by", "(.cidade)' usuarios.json", rotulo="função") +
            MC(3, "O que <code>group_by(.cidade)</code> devolve?", ["um objeto cidade → pessoas", "uma lista de listas, uma por cidade", "um número", "as cidades sem repetição"], 2) +
            MC(4, "Para achar o usuário mais velho:", ["<code>max(.idade)</code>", "<code>max_by(.idade)</code>", "<code>sort</code>", "<code>.idade | max</code>"], 2))

def ord_miss():
    return (M("jqord-m1", "mostre os nomes dos usuários (sem aspas) em ordem de idade, do mais velho para o mais novo.", "jq -r 'sort_by(.idade) | reverse | .[].nome' usuarios.json", r"src:sort_by\(\.idade\);;src:reverse;;outre:^Diego Rocha\nBruno Lima\nAna Souza\nCarla Dias$") +
            M("jqord-m2", "liste (compacto, sem repetição) todas as cidades dos usuários.", "jq -c '[.[].cidade] | unique' usuarios.json", r"src:unique;;out:[\"Belo Horizonte\",\"Rio de Janeiro\",\"São Paulo\"]"))

# ---------------------------------------------------------------- csv
def csv_corpo():
    return f"""
<h2>A ideia: do JSON para a planilha</h2>
<p>Os formatadores <code>@csv</code> e <code>@tsv</code> transformam uma <strong>lista</strong> em uma linha de CSV (separada por vírgula, com textos entre aspas) ou TSV (separada por tabulação). Com <code>-r</code>, a linha sai pronta para gravar num arquivo e abrir na planilha.</p>
<hr>
<h2>1. <code>@csv</code></h2>
<p>Para cada usuário, monte uma lista com os campos na ordem das colunas e passe por <code>@csv</code>:</p>
{T("jqcsv-csv", "jq -r '.[] | [.id, .nome, .cidade, .idade] | @csv' usuarios.json")}
{ANAT((".[]", "cada usuário."), ("[.id, .nome, .cidade, .idade]", "uma lista: as colunas, na ordem."), ("@csv", "vira uma linha de CSV."), ("-r", "sem as aspas externas do JSON."))}
<hr>
<h2>2. Com cabeçalho</h2>
<p>A vírgula do jq produz primeiro a lista do cabeçalho, depois as linhas:</p>
{T("jqcsv-cab", "jq -r '[\"id\", \"nome\", \"email\"], (.[] | [.id, .nome, .email]) | @csv' usuarios.json")}
<p>Repare: o <code>email</code> nulo da Carla virou um campo vazio.</p>
<hr>
<h2>3. <code>@tsv</code></h2>
<p>TSV usa tabulação e não põe aspas: ótimo para o <code>awk</code> e para o <code>column</code>:</p>
{T("jqcsv-tsv", "jq -r '.pedidos[] | [.id, .cliente, .status] | @tsv' pedidos.json", "jq -r '.pedidos[] | [.id, .cliente, .status] | @tsv' pedidos.json | awk -F'\\t' '$3 == \"pago\" {print $2}'")}
<hr>
<h2>4. Uma linha por item de pedido</h2>
<p>Para listas dentro de listas, guarde o pai numa variável com <code>as $p</code> e abra os filhos:</p>
{T("jqcsv-itens", "jq -r '.pedidos[] as $p | $p.itens[] | [$p.id, $p.cliente, .produto, .qtd, .preco] | @csv' pedidos.json")}
<hr>
<h2>5. Gravar e conferir</h2>
{T("jqcsv-gravar", "jq -r '.[] | [.id, .nome, .cidade] | @csv' usuarios.json > usuarios.csv", "wc -l usuarios.csv", "awk -F, '{print $2}' usuarios.csv")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("@csv num objeto", "O <code>@csv</code> só aceita listas (“cannot be csv-formatted, only array”: não pode virar CSV, só lista):", T("jqcsv-erro", "jq -r '.[0] | @csv' usuarios.json"))}
{CEN("Lista dentro da linha", "Cada coluna tem de ser um valor simples. A lista de <code>tags</code> não cabe numa célula (“is not valid in a csv row”: não vale numa linha de CSV):", T("jqcsv-erro2", "jq -r '.[0] | [.nome, .tags] | @csv' usuarios.json"), "Junte antes: <code>(.tags | join(\";\"))</code>.")}
"""

def csv_ex():
    return (EX(1, "CSV", "Qual formatador gera CSV?", "jq -r '.[] | [.id, .nome] | ", "@csv", "' usuarios.json", rotulo="formatador") +
            EX(2, "TSV", "Qual formatador separa por tabulação?", "jq -r '.[] | [.id, .nome] | ", "@tsv", "' usuarios.json", rotulo="formatador") +
            MC(3, "O que o <code>@csv</code> recebe?", ["um objeto", "uma lista de valores simples", "um texto", "qualquer coisa"], 2) +
            MC(4, "Por que usar <code>-r</code> com <code>@csv</code>?", ["Para ordenar", "Para a linha sair sem as aspas externas do JSON", "Para ir mais rápido", "Não precisa"], 2))

def csv_miss():
    return (M("jqcsv-m1", "gere um CSV com <code>id</code> e <code>status</code> de cada pedido de <code>pedidos.json</code>.", "jq -r '.pedidos[] | [.id, .status] | @csv' pedidos.json", r"src:@csv;;src:-r;;outre:^1042,\"pago\"$;;outre:^1045,\"cancelado\"$") +
            M("jqcsv-m2", "gere um TSV com <code>nome</code> e <code>idade</code> de cada usuário.", "jq -r '.[] | [.nome, .idade] | @tsv' usuarios.json", r"src:@tsv;;outre:^Ana Souza\t28$;;outre:^Diego Rocha\t41$"))

# ---------------------------------------------------------------- arg
def arg_corpo():
    return f"""
<h2>A ideia: valores de fora para dentro do filtro</h2>
<p>Em scripts, o valor do filtro (a cidade, o status, a idade mínima) costuma vir de uma variável do shell. Colar a variável dentro das aspas do jq dá dor de cabeça com aspas e é inseguro. O jq tem opções próprias: <code>--arg</code> passa um <strong>texto</strong>, <code>--argjson</code> passa um <strong>valor JSON</strong> (número, true, lista…). Dentro do filtro, eles viram <code>$nome</code>.</p>
<hr>
<h2>1. <code>--arg</code>: um texto</h2>
{T("jqarg-arg", "jq -r --arg cidade 'São Paulo' '.[] | select(.cidade == $cidade) | .nome' usuarios.json", "status=pago; jq -c --arg s \"$status\" '[.pedidos[] | select(.status == $s) | .id]' pedidos.json")}
{ANAT(("--arg cidade 'São Paulo'", "cria $cidade com o texto São Paulo."), ("select(.cidade == $cidade)", "usa a variável no filtro."))}
<hr>
<h2>2. <code>--argjson</code>: um número</h2>
<p>O <code>--arg</code> sempre cria <strong>texto</strong>. Comparar idade (número) com texto não dá o que você espera: no jq, todo número é “menor” que qualquer texto, e o filtro não devolveu ninguém. Com <code>--argjson</code>, o 30 é número de verdade:</p>
{T("jqarg-json", "jq -r --arg min 30 '.[] | select(.idade > $min) | .nome' usuarios.json", "jq -r --argjson min 30 '.[] | select(.idade > $min) | .nome' usuarios.json")}
<hr>
<h2>3. <code>-n</code> e <code>-s</code></h2>
<p><code>-n</code> (<em>null input</em>) roda o filtro sem ler entrada nenhuma: bom para criar JSON do zero. <code>-s</code> (<em>slurp</em>, “engolir”) junta todas as entradas numa lista só:</p>
{T("jqarg-ns", "jq -n --arg nome Ana --argjson idade 28 '{nome: $nome, idade: $idade}'", "jq -c '.nome' produto.json usuarios.json 2>&1 | head -2", "jq -s 'length' produto.json pedidos.json")}
<p>No segundo comando, o jq aplicou <code>.nome</code> em cada arquivo: no <code>produto.json</code> deu “caderno” e no <code>usuarios.json</code> (uma lista) deu erro. A mensagem de erro apareceu primeiro porque a saída de erro não espera na fila. No terceiro, com <code>-s</code>, os dois arquivos viraram uma lista de 2 itens.</p>
<hr>
<h2>4. Variáveis de ambiente: <code>$ENV</code></h2>
<p>Variáveis de ambiente também estão disponíveis, em <code>$ENV</code> (ou <code>env</code>):</p>
{T("jqarg-env", "LOJA_CIDADE=Recife jq -n -r '$ENV.LOJA_CIDADE'")}
<div class="tip"><strong>O padrão com APIs</strong><p>Na vida real: <code>curl -s https://api.exemplo.com/pedidos | jq -r --arg s pago '.pedidos[] | select(.status == $s) | .id'</code>. O guia não acessa a internet; o <code>cat pedidos.json |</code> faz o papel do <code>curl</code>.</p></div>
{T("jqarg-api", "cat pedidos.json | jq -r --arg s pago '.pedidos[] | select(.status == $s) | .id'")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Variável não criada", "Usar <code>$cidade</code> sem o <code>--arg</code> é erro de compilação (“$cidade is not defined”: $cidade não foi definida):", T("jqarg-erro", "jq '.[] | select(.cidade == $cidade)' usuarios.json"))}
{CEN("--argjson com texto", "O valor do <code>--argjson</code> tem de ser JSON válido. Um texto sem aspas não é:", T("jqarg-erro2", "jq -n --argjson nome Ana '$nome'"))}
"""

def arg_ex():
    return (EX(1, "Texto de fora", "Qual opção cria uma variável de texto?", "jq ", "--arg", " s pago '.pedidos[] | select(.status == $s)' pedidos.json", rotulo="opção") +
            EX(2, "Número de fora", "Qual opção cria uma variável com valor JSON (número)?", "jq ", "--argjson", " min 30 '.[] | select(.idade > $min)' usuarios.json", rotulo="opção") +
            MC(3, "Por que <code>--arg min 30</code> com <code>.idade &gt; $min</code> não devolveu ninguém?", ["Porque $min é texto, e número é sempre menor que texto no jq", "Porque falta o -r", "Porque 30 é muito", "Porque o jq não compara"], 1) +
            MC(4, "O que o <code>-s</code> faz?", ["silencia erros", "junta todas as entradas numa lista", "ordena", "sai sem aspas"], 2))

def arg_miss():
    return (M("jqarg-m1", "com <code>--arg</code>, mostre (sem aspas) os nomes dos usuários que moram no <code>Rio de Janeiro</code>.", "jq -r --arg c 'Rio de Janeiro' '.[] | select(.cidade == $c) | .nome' usuarios.json", r"src:--arg;;outre:^Bruno Lima$") +
            M("jqarg-m2", "com <code>--argjson</code>, mostre os nomes dos usuários com idade maior ou igual a 35.", "jq -r --argjson min 35 '.[] | select(.idade >= $min) | .nome' usuarios.json", r"src:--argjson;;outre:^Bruno Lima\nDiego Rocha$"))

# ---------------------------------------------------------------- null
def null_corpo():
    return f"""
<h2>A ideia: dados reais têm buracos</h2>
<p>Em JSON de verdade, campos faltam, vêm <code>null</code> ou com tipo inesperado. A Carla, no <code>usuarios.json</code>, tem <code>"email": null</code>. Esta aula mostra como o jq lida com isso: o valor padrão <code>//</code>, o <code>?</code> que cala erros, o <code>if</code>, o <code>try</code> e o código de saída com <code>-e</code>.</p>
<hr>
<h2>1. Onde está o <code>null</code></h2>
{T("jqn-onde", "jq '.[].email' usuarios.json", "jq '.[] | select(.email == null) | .nome' usuarios.json")}
<hr>
<h2>2. Valor padrão: <code>//</code></h2>
<p><code>a // b</code> devolve <code>a</code>, a não ser que ele seja <code>null</code> ou <code>false</code>; aí devolve <code>b</code>:</p>
{T("jqn-padrao", "jq -r '.[] | .email // \"(sem e-mail)\"' usuarios.json", "jq '.peso // 0' produto.json")}
{ANAT((".email", "o valor normal."), ("//", "“ou, se for null/false”."), ('"(sem e-mail)"', "o valor padrão."))}
<hr>
<h2>3. <code>if</code> / <code>then</code> / <code>else</code></h2>
{T("jqn-if", "jq -r '.[] | if .ativo then \"\\(.nome): ativo\" else \"\\(.nome): inativo\" end' usuarios.json", "jq -r '.[] | \"\\(.nome): \\(if (.tags | length) == 0 then \"sem tags\" else (.tags | join(\",\")) end)\"' usuarios.json")}
<hr>
<h2>4. Calar erros: <code>?</code> e <code>try</code></h2>
<p>Um filtro com <code>?</code> no fim engole o erro e simplesmente não produz resultado. O <code>try … catch</code> permite trocar o erro por outra coisa:</p>
{T("jqn-try", "jq '.[] | .email | ascii_downcase' usuarios.json", "jq '.[] | (.email | ascii_downcase)?' usuarios.json", "jq -r '.[] | try (.email | ascii_downcase) catch \"falhou\"' usuarios.json")}
<p>No primeiro comando, o jq parou no erro da Carla e o Diego nem apareceu. A mensagem “explode input must be a string” quer dizer que o <code>ascii_downcase</code> recebeu algo que não é texto (o <code>null</code>); ela veio antes das outras linhas porque a saída de erro não espera na fila. Com <code>?</code>, a Carla foi pulada; com <code>try/catch</code>, virou “falhou”.</p>
<hr>
<h2>5. <code>-e</code>: o código de saída</h2>
<p>Com <code>-e</code>, o jq sai com código 1 se o último resultado for <code>null</code> ou <code>false</code>. Ótimo para <code>if</code> em scripts do Bash:</p>
{T("jqn-e", "jq -e '.preco' produto.json; echo \"código: $?\"", "jq -e '.peso' produto.json; echo \"código: $?\"")}
<hr>
<h2 id="errado">Quando dá errado</h2>
{CEN("Arquivo que não existe", "O jq avisa e sai com código 2:", T("jqn-erro", "jq . nada.json; echo \"código: $?\""))}
{CEN("Abrir null", "Abrir com <code>[]</code> um campo que não existe é erro (“Cannot iterate over null”: não dá para percorrer null). O <code>[]?</code> resolve:", T("jqn-erro2", "jq '.cores[]' pedidos.json", "jq '.cores[]?' pedidos.json; echo \"código: $?\""))}
"""

def null_ex():
    return (EX(1, "Valor padrão", "Qual operador dá um valor padrão para null?", "jq '.email ", "//", " \"nenhum\"' ", rotulo="operador") +
            EX(2, "Calar erro", "Qual símbolo, no fim do filtro, cala o erro?", "jq '.cores[]", "?", "' pedidos.json", rotulo="símbolo") +
            MC(3, "<code>null // \"x\"</code> dá:", ["null", "\"x\"", "erro", "false"], 2) +
            MC(4, "Com <code>-e</code>, quando o resultado é <code>null</code>, o código de saída é:", ["0", "1", "2", "5"], 2))

def null_miss():
    return (M("jqn-m1", "mostre o e-mail de cada usuário, sem aspas, trocando <code>null</code> por <code>sem-email</code>.", "jq -r '.[] | .email // \"sem-email\"' usuarios.json", r"src://;;outre:^sem-email$;;outre:^diego@exemplo\.com$") +
            M("jqn-m2", "mostre o nome dos usuários que têm e-mail (não nulo).", "jq -r '.[] | select(.email != null) | .nome' usuarios.json", r"src:!=\s*null;;outre:^Ana Souza\nBruno Lima\nDiego Rocha$"))

NIVEL = {"id": "n4", "nome": "Nível 4 · jq", "curto": "jq", "desc": "JSON no terminal: extrair, filtrar, montar e converter", "grupos": [
    {"grupo": "Navegando no JSON", "aulas": [
        aula(slug="jq-intro", menu="O que é o jq (. e -c)", title="O que é o jq: o filtro . e a opção -c", h1='O que é o <span class="hl">jq</span> (<span class="hl">.</span> e <span class="hl">-c</span>)',
             desc="Primeiros passos com o jq 1.7: o que é JSON, o filtro ., saída compacta com -c, ler do pipe e os erros de JSON quebrado.",
             intro="O <code>jq</code> entende JSON, o formato das APIs. Esta aula mostra o filtro mais simples, o <code>.</code>, que já deixa qualquer JSON legível.",
             aprender=["Objetos, listas e valores do JSON.", "O filtro <code>.</code> e a opção <code>-c</code>.", "Ler do pipe e entender os erros de JSON inválido."],
             corpo=intro_corpo, exercicios=intro_ex, missoes=intro_miss,
             ref=[("jq . arq.json", "formata o JSON."), ("jq -c . arq.json", "uma linha por resultado."), ("cmd | jq .", "formata a saída de outro comando."), ("jq --version", "a versão.")],
             resumo=["<code>.</code> é a entrada inteira.", "<code>-c</code> compacta.", "As mensagens do jq saem em inglês."]),
        aula(slug="jq-campos", menu="Campos (.campo, .a.b)", title="Campos no jq: .campo, aninhados e null", h1='Campos (<span class="hl">.campo</span>, <span class="hl">.a.b</span>)',
             desc="Pegar campos com jq: .campo, campos aninhados, vários com vírgula, null para chave inexistente e chaves com hífen.",
             intro="Num objeto JSON, <code>.chave</code> pega o valor. Esta aula mostra o caminho até qualquer dado, por mais fundo que esteja.",
             aprender=["<code>.campo</code> e <code>.a.b.c</code>.", "Vários campos com vírgula.", "Chave inexistente (<code>null</code>) e chaves com caracteres especiais."],
             corpo=campos_corpo, exercicios=campos_ex, missoes=campos_miss,
             ref=[(".nome", "o campo nome."), (".estoque.loja", "campo dentro de campo."), (".nome, .preco", "dois resultados."), ('."data-de-entrega"', "chave com hífen."), ('.["chave"]', "outra forma.")],
             resumo=["<code>.a.b</code> desce nos objetos.", "Chave que não existe dá <code>null</code>, não erro.", "Chaves com hífen vão entre aspas."]),
        aula(slug="jq-arrays", menu="Listas (.[0], .[], fatias)", title="Listas no jq: .[0], .[-1], fatias e .[]", h1='Listas (<span class="hl">.[0]</span>, <span class="hl">.[]</span>)',
             desc="Arrays no jq: índice .[0] e .[-1], fatias .[1:3], .[] para cada item, listas dentro de listas e .[] em objetos.",
             intro="Muito JSON é uma lista de coisas parecidas. Esta aula mostra como pegar um item, uma fatia ou cada item da lista.",
             aprender=["<code>.[0]</code>, <code>.[-1]</code> e fatias.", "<code>.[]</code>: um resultado por item.", "Listas dentro de listas."],
             corpo=arr_corpo, exercicios=arr_ex, missoes=arr_miss,
             ref=[(".[0]", "o primeiro item."), (".[-1]", "o último."), (".[1:3]", "itens 1 e 2."), (".[]", "cada item."), (".[].nome", "o nome de cada item."), (".a[].b[]", "duas camadas.")],
             resumo=["Posições começam em 0.", "<code>.[]</code> abre a lista.", "Num objeto, <code>.[]</code> dá os valores."]),
    ]},
    {"grupo": "Filtrando e transformando", "aulas": [
        aula(slug="jq-select", menu="O | do jq e select", title="O pipe do jq e o select", h1='O <span class="hl">|</span> do jq e <span class="hl">select</span>',
             desc="O pipe interno do jq e o select para filtrar: comparações, and, or, not, test com regex e any.",
             intro="Dentro do jq também existe pipe, e o <code>select</code> filtra itens por condição. Juntos, são o <code>grep</code> do JSON.",
             aprender=["O <code>|</code> dentro do programa jq.", "<code>select</code> com comparações, <code>and</code>, <code>or</code>, <code>not</code>.", "Regex com <code>test</code> e listas com <code>any</code>."],
             corpo=sel_corpo, exercicios=sel_ex, missoes=sel_miss,
             ref=[(".[] | .nome", "o nome de cada item."), ("select(.ativo)", "só os ativos."), ("select(.idade > 30)", "idade maior que 30."), ('select(.a == "x" or .b)', "ou."), ('select(.nome | test("^A"))', "regex."), ("select(.x | not)", "negação.")],
             resumo=["<code>|</code> no jq passa o resultado adiante.", "<code>select</code> deixa passar só o que é verdadeiro.", "Compare com <code>==</code>, nunca com <code>=</code>."]),
        aula(slug="jq-map", menu="map, length, keys e add", title="map, length, keys, has e add no jq", h1='<span class="hl">map</span>, <span class="hl">length</span>, <span class="hl">keys</span> e <span class="hl">add</span>',
             desc="Funções de lista no jq: map, length, keys, has, add, min, max, média e map com select.",
             intro="Transformar cada item e continuar com uma lista, contar, somar, listar chaves: as funções que olham a lista inteira.",
             aprender=["<code>map</code>.", "<code>length</code>, <code>keys</code> e <code>has</code>.", "<code>add</code>, <code>min</code>, <code>max</code> e a média."],
             corpo=map_corpo, exercicios=map_ex, missoes=map_miss,
             ref=[("map(.nome)", "lista de nomes."), ("length", "tamanho."), ("keys", "chaves do objeto."), ('has("x")', "a chave existe?"), ("add", "soma a lista."), ("add / length", "média.")],
             resumo=["<code>map(f)</code> = <code>[.[] | f]</code>.", "<code>length</code> mede listas, objetos e textos.", "<code>add / length</code> é a média."]),
        aula(slug="jq-texto", menu="Texto: -r, interpolação e join", title="Texto no jq: -r, interpolação \\( ), join e tostring", h1='Texto: <span class="hl">-r</span>, interpolação e <span class="hl">join</span>',
             desc="Saída crua com jq -r, interpolação de strings, join, split, ascii_upcase, + e tostring, com o erro de somar texto e número.",
             intro="Para passar o resultado do jq para o terminal, você quer texto, não JSON. Esta aula mostra o <code>-r</code> e as ferramentas de texto do jq.",
             aprender=["<code>-r</code> para tirar as aspas.", "Interpolação com <code>\\( )</code>.", "<code>join</code>, <code>split</code>, <code>+</code> e <code>tostring</code>."],
             corpo=str_corpo, exercicios=str_ex, missoes=str_miss,
             ref=[("jq -r '.[].nome'", "sem aspas."), ('"\\(.nome) tem \\(.idade)"', "interpolação."), ('join(", ")', "junta a lista."), ('split(" ")', "quebra o texto."), ("tostring", "número para texto."), ("ascii_upcase", "maiúsculas (sem acentos).")],
             resumo=["<code>-r</code> é o que liga o jq ao resto do terminal.", "<code>\\( )</code> monta textos com valores.", "Texto + número pede <code>tostring</code>."]),
        aula(slug="jq-objetos", menu="Montando objetos e listas", title="Montando objetos e listas com jq", h1='Montando <span class="hl">objetos</span> e listas',
             desc="Construir JSON com jq: {campo}, renomear e calcular campos, [ ] para listas, chaves calculadas, atualizar com = e +=, del.",
             intro="O jq também constrói JSON: só os campos que interessam, com nomes novos e campos calculados.",
             aprender=["<code>{nome, cidade}</code> e campos renomeados.", "Listas com <code>[ ]</code> e chaves calculadas.", "Mudar e apagar campos: <code>=</code>, <code>+=</code>, <code>del</code>."],
             corpo=obj_corpo, exercicios=obj_ex, missoes=obj_miss,
             ref=[("{nome, idade}", "objeto com dois campos."), ("{id: .codigo}", "renomeia."), ("[.[] | .id]", "lista de ids."), ("{(.nome): .idade}", "chave calculada."), (".preco = 10", "troca um campo."), ("del(.cores)", "apaga um campo.")],
             resumo=["<code>{ }</code> monta objetos; <code>[ ]</code>, listas.", "Campos calculados vão entre parênteses.", "<code>=</code> e <code>del</code> devolvem o objeto inteiro modificado."]),
    ]},
    {"grupo": "jq na prática", "aulas": [
        aula(slug="jq-ordenar", menu="Ordenar e agrupar (sort_by, group_by)", title="Ordenar e agrupar no jq: sort_by, group_by, unique", h1='Ordenar e agrupar (<span class="hl">sort_by</span>, <span class="hl">group_by</span>)',
             desc="Ordenar e agrupar JSON com jq: sort_by, reverse, min_by, max_by, group_by, unique e unique_by.",
             intro="Ordenar objetos por campo, agrupar por cidade, achar o mais velho: tudo sem sair do JSON.",
             aprender=["<code>sort_by</code> e <code>reverse</code>.", "<code>min_by</code> e <code>max_by</code>.", "<code>group_by</code>, <code>unique</code> e <code>unique_by</code>."],
             corpo=ord_corpo, exercicios=ord_ex, missoes=ord_miss,
             ref=[("sort_by(.idade)", "ordena por idade."), ("reverse", "inverte."), ("max_by(.idade)", "o de maior idade."), ("group_by(.cidade)", "agrupa."), ("unique", "sem repetidos."), ("unique_by(.cidade)", "um por cidade.")],
             resumo=["Essas funções trabalham sobre listas.", "<code>group_by</code> devolve lista de listas.", "Valores soltos? Junte com <code>[ ]</code> antes."]),
        aula(slug="jq-csv", menu="JSON para CSV (@csv e @tsv)", title="JSON para CSV com jq: @csv e @tsv", h1='JSON para CSV (<span class="hl">@csv</span> e <span class="hl">@tsv</span>)',
             desc="Converter JSON em CSV e TSV com jq: @csv, @tsv, cabeçalho, uma linha por item com as $p e gravar em arquivo.",
             intro="Transformar JSON em planilha é uma das tarefas mais pedidas. Os formatadores <code>@csv</code> e <code>@tsv</code> fazem isso.",
             aprender=["<code>@csv</code> e <code>@tsv</code> com <code>-r</code>.", "Cabeçalho e uma linha por item.", "Variáveis com <code>as $p</code> para listas dentro de listas."],
             corpo=csv_corpo, exercicios=csv_ex, missoes=csv_miss,
             ref=[("[.a, .b] | @csv", "linha CSV."), ("[.a, .b] | @tsv", "linha TSV."), ('["a","b"], (.[] | [.a,.b]) | @csv', "com cabeçalho."), (".x[] as $p | $p.y[]", "guarda o pai em $p.")],
             resumo=["<code>@csv</code> e <code>@tsv</code> recebem uma lista.", "Sempre com <code>-r</code>.", "Listas dentro da linha precisam de <code>join</code>."]),
        aula(slug="jq-arg", menu="Variáveis de fora (--arg, --argjson)", title="Variáveis no jq: --arg, --argjson, -n e -s", h1='Variáveis de fora (<span class="hl">--arg</span>, <span class="hl">--argjson</span>)',
             desc="Passar valores do shell para o jq com --arg e --argjson, -n para criar JSON, -s para juntar entradas, $ENV e o padrão curl | jq.",
             intro="Em scripts, o valor do filtro vem de uma variável do shell. O jq tem opções próprias para isso, sem brigar com aspas.",
             aprender=["<code>--arg</code> para textos e <code>--argjson</code> para números.", "<code>-n</code> e <code>-s</code>.", "<code>$ENV</code> e o padrão <code>curl … | jq</code>."],
             corpo=arg_corpo, exercicios=arg_ex, missoes=arg_miss,
             ref=[("--arg x valor", "$x é texto."), ("--argjson n 30", "$n é número."), ("jq -n '{a: 1}'", "sem entrada."), ("jq -s . a.json b.json", "junta as entradas numa lista."), ("$ENV.VAR", "variável de ambiente.")],
             resumo=["Nunca cole variáveis do shell dentro do filtro: use <code>--arg</code>.", "Números e booleanos vão com <code>--argjson</code>.", "<code>-s</code> engole tudo numa lista."]),
        aula(slug="jq-null", menu="null, //, ? e try", title="null, valor padrão (//), ? e try no jq", h1='<span class="hl">null</span>, <span class="hl">//</span>, <span class="hl">?</span> e try',
             desc="Tratar dados incompletos no jq: null, o operador //, if then else, o ? para calar erros, try catch e o código de saída com -e.",
             intro="Dados reais têm buracos. Esta aula mostra como o jq trata campos nulos e erros sem quebrar o script.",
             aprender=["Achar e tratar <code>null</code> com <code>//</code>.", "<code>if</code>/<code>then</code>/<code>else</code>.", "<code>?</code>, <code>try</code>/<code>catch</code> e <code>-e</code>."],
             corpo=null_corpo, exercicios=null_ex, missoes=null_miss,
             ref=[('.x // "padrão"', "valor padrão."), ("select(.x != null)", "só quem tem x."), ('if .a then "s" else "n" end', "decide."), ("(.x | f)?", "cala o erro."), ('try f catch "erro"', "troca o erro."), ("jq -e", "código 1 se null/false.")],
             resumo=["<code>//</code> dá um valor quando o campo é null.", "<code>?</code> e <code>try</code> evitam que um item ruim pare tudo.", "<code>-e</code> deixa o Bash saber se achou algo."]),
    ]},
]}
