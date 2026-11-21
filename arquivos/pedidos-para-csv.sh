#!/usr/bin/env bash
# pedidos-para-csv.sh: uma linha de CSV por item de pedido (projeto do Nível 5)
arq="${1:-pedidos.json}"
jq -r '
  ["pedido", "cliente", "status", "produto", "qtd", "preco", "subtotal"],
  (.pedidos[] as $p | $p.itens[] |
    [$p.id, $p.cliente, $p.status, .produto, .qtd, .preco, (.qtd * .preco)])
  | @csv' "$arq"
