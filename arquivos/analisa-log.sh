#!/usr/bin/env bash
# analisa-log.sh: resumo do acesso.log (projeto do Nível 5)
arq="${1:-acesso.log}"
if [ ! -r "$arq" ]; then
    echo "analisa-log.sh: não consigo ler o arquivo $arq" >&2
    exit 1
fi
echo "== Relatório de $arq =="
echo "Pedidos: $(wc -l < "$arq")"
echo
echo "-- Por status --"
awk '{n[$9]++} END {for (s in n) print s, n[s]}' "$arq" | sort
echo
echo "-- IPs que mais acessaram --"
awk '{n[$1]++} END {for (ip in n) print n[ip], ip}' "$arq" | sort -rn | head -3
echo
echo "-- Erros (4xx e 5xx) --"
awk '$9 >= 400 {print $9, $6, $7}' "$arq" | tr -d '"' | sort | uniq -c | sort -rn
echo
awk '{b += $10} END {printf "Total enviado: %.1f KB\n", b / 1024}' "$arq"
