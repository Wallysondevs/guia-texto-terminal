#!/usr/bin/env bash
# criar-arquivos.sh — cria os arquivos de exemplo do Guia Texto no Terminal
# na pasta atual. Uso: mkdir -p ~/guia-texto-teste && cd ~/guia-texto-teste && bash criar-arquivos.sh
# Rode de novo sempre que quiser voltar os arquivos ao original.
set -e
cat > acesso.log <<'FIM_DO_ARQUIVO'
192.168.0.12 - - [02/Mar/2026:08:15:02 -0300] "GET /index.html HTTP/1.1" 200 5120
192.168.0.15 - - [02/Mar/2026:08:15:09 -0300] "GET /produtos.html HTTP/1.1" 200 8340
192.168.0.12 - - [02/Mar/2026:08:16:30 -0300] "GET /carrinho.html HTTP/1.1" 200 2210
192.168.0.20 - - [02/Mar/2026:08:17:45 -0300] "POST /pagar HTTP/1.1" 500 310
192.168.0.15 - - [02/Mar/2026:08:18:02 -0300] "GET /logo.png HTTP/1.1" 304 0
192.168.0.33 - - [02/Mar/2026:08:20:11 -0300] "GET /admin HTTP/1.1" 403 150
192.168.0.12 - - [02/Mar/2026:08:21:40 -0300] "POST /pagar HTTP/1.1" 200 420
192.168.0.20 - - [02/Mar/2026:08:22:05 -0300] "GET /sobre.html HTTP/1.1" 404 180
192.168.0.15 - - [02/Mar/2026:08:25:17 -0300] "GET /index.html HTTP/1.1" 200 5120
192.168.0.33 - - [02/Mar/2026:08:26:00 -0300] "GET /admin HTTP/1.1" 403 150
192.168.0.12 - - [02/Mar/2026:08:30:12 -0300] "GET /produtos.html HTTP/1.1" 200 8340
192.168.0.20 - - [02/Mar/2026:08:31:48 -0300] "POST /pagar HTTP/1.1" 500 310
FIM_DO_ARQUIVO
cat > config.txt <<'FIM_DO_ARQUIVO'
# Configuração do site da loja
nome=Loja da Ana
porta=8080
debug=sim
# e-mail de contato
email=contato@lojadaana.example

tema=claro
idioma=pt-BR
FIM_DO_ARQUIVO
cat > contatos.txt <<'FIM_DO_ARQUIVO'
Ana Souza;(11) 91234-5678;ana@exemplo.com
Bruno Lima;(21) 99876-5432;bruno@exemplo.com
Carla Dias;(31) 98765-1234;carla@exemplo.com
Diego Rocha;(41) 97654-3210;diego@exemplo.com
FIM_DO_ARQUIVO
cat > frutas.txt <<'FIM_DO_ARQUIVO'
banana
maçã
laranja
banana
uva
maçã
banana
FIM_DO_ARQUIVO
cat > limpa.sed <<'FIM_DO_ARQUIVO'
# limpa.sed: tira comentários e linhas vazias do config.txt
/^#/d
/^$/d
s/=/ = /
FIM_DO_ARQUIVO
cat > log.txt <<'FIM_DO_ARQUIVO'
2026-03-02 08:15:02 INFO  login usuario=ana
2026-03-02 08:17:45 ERRO  falha no pagamento pedido=1042
2026-03-02 08:20:11 INFO  pedido criado pedido=1043
2026-03-02 09:01:37 AVISO estoque baixo produto=caderno
2026-03-02 09:05:59 INFO  login usuario=bruno
2026-03-02 09:12:03 ERRO  tempo esgotado no servidor de e-mail
2026-03-02 10:30:44 INFO  logout usuario=ana
2026-03-02 10:45:20 ERRO  falha no pagamento pedido=1047
2026-03-02 11:02:15 AVISO disco 85% cheio
2026-03-02 11:15:00 INFO  login usuario=carla
FIM_DO_ARQUIVO
cat > nomes.txt <<'FIM_DO_ARQUIVO'
Ana
bruno
Carla
Diego
ana paula
Bruno
Eduarda
Carla
Fábio
FIM_DO_ARQUIVO
cat > notas.txt <<'FIM_DO_ARQUIVO'
Ana 8.5 9.0 7.5
Bruno 6.0 5.5 7.0
Carla 9.5 10.0 9.0
Diego 4.0 6.5 5.0
Eduarda 7.0 8.0 8.5
FIM_DO_ARQUIVO
cat > pedidos.json <<'FIM_DO_ARQUIVO'
{
  "loja": "Papelaria da Ana",
  "atualizado": "2026-03-05",
  "pedidos": [
    {"id": 1042, "cliente": "Bruno", "status": "pago", "itens": [{"produto": "caderno", "qtd": 2, "preco": 12.5}, {"produto": "caneta", "qtd": 5, "preco": 2.0}]},
    {"id": 1043, "cliente": "Carla", "status": "pendente", "itens": [{"produto": "mochila", "qtd": 1, "preco": 89.9}]},
    {"id": 1044, "cliente": "Diego", "status": "pago", "itens": [{"produto": "estojo", "qtd": 1, "preco": 15.0}, {"produto": "caneta", "qtd": 3, "preco": 2.0}]},
    {"id": 1045, "cliente": "Ana", "status": "cancelado", "itens": [{"produto": "caderno", "qtd": 4, "preco": 12.5}]}
  ]
}
FIM_DO_ARQUIVO
cat > produto.json <<'FIM_DO_ARQUIVO'
{"nome": "caderno", "preco": 12.5, "estoque": {"loja": 40, "deposito": 120}, "cores": ["azul", "verde", "preto"]}
FIM_DO_ARQUIVO
cat > quebrado.json <<'FIM_DO_ARQUIVO'
{"nome": "caderno", "preco": 12.5,
FIM_DO_ARQUIVO
cat > relatorio.awk <<'FIM_DO_ARQUIVO'
# relatorio.awk: total vendido por vendedor (vendas.csv)
BEGIN { FS = "," }
NR > 1 { total[$2] += $4 * $5 }
END {
    for (v in total)
        printf "%-8s R$ %8.2f\n", v, total[v]
}
FIM_DO_ARQUIVO
cat > texto.txt <<'FIM_DO_ARQUIVO'
O rato roeu a roupa do rei de Roma.
A rainha, com raiva, rasgou o resto.
O rato fugiu para o mato.
Rato que é rato não volta.
FIM_DO_ARQUIVO
cat > usuarios.json <<'FIM_DO_ARQUIVO'
[
  {"id": 1, "nome": "Ana Souza", "email": "ana@exemplo.com", "idade": 28, "cidade": "São Paulo", "ativo": true, "tags": ["admin", "vendas"]},
  {"id": 2, "nome": "Bruno Lima", "email": "bruno@exemplo.com", "idade": 35, "cidade": "Rio de Janeiro", "ativo": false, "tags": ["vendas"]},
  {"id": 3, "nome": "Carla Dias", "email": null, "idade": 22, "cidade": "Belo Horizonte", "ativo": true, "tags": []},
  {"id": 4, "nome": "Diego Rocha", "email": "diego@exemplo.com", "idade": 41, "cidade": "São Paulo", "ativo": true, "tags": ["suporte"]}
]
FIM_DO_ARQUIVO
cat > vendas.csv <<'FIM_DO_ARQUIVO'
data,vendedor,produto,quantidade,preco
2026-03-02,Ana,caderno,3,12.50
2026-03-02,Bruno,caneta,10,2.00
2026-03-02,Carla,mochila,1,89.90
2026-03-03,Ana,caneta,5,2.00
2026-03-03,Diego,caderno,2,12.50
2026-03-03,Bruno,estojo,4,15.00
2026-03-04,Carla,caderno,6,12.50
2026-03-04,Ana,mochila,2,89.90
2026-03-04,Diego,caneta,20,2.00
2026-03-05,Bruno,mochila,1,89.90
2026-03-05,Carla,estojo,3,15.00
2026-03-05,Ana,caderno,4,12.50
FIM_DO_ARQUIVO
echo "Arquivos de exemplo criados em $(pwd)"
