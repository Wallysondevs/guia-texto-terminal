#!/usr/bin/env bash
# painel.sh: resumo dos arquivos da loja (projeto final do Nível 5)
echo "== Painel da Papelaria =="
echo "Erros no log do sistema: $(grep -c ERRO log.txt)"
echo "Respostas 5xx no site:   $(awk '$9 >= 500' acesso.log | wc -l)"
total=$(awk -F, 'NR > 1 {t += $4 * $5} END {printf "%.2f", t}' vendas.csv | tr . ,)
echo "Vendas no CSV:           R\$ $total"
echo "Pedidos pagos no JSON:   $(jq '[.pedidos[] | select(.status == "pago")] | length' pedidos.json)"
echo "Pagamentos que falharam:"
grep 'falha no pagamento' log.txt | sed -E 's/^([0-9-]+) ([0-9:]+).*pedido=([0-9]+)$/  \1 \2  pedido \3/'
