#!/usr/bin/env bash
# relatorio-vendas.sh: relatório do vendas.csv (projeto do Nível 5)
arq="${1:-vendas.csv}"
awk -F, '
NR == 1 { next }
{
    total = $4 * $5
    por_vendedor[$2] += total
    por_dia[$1] += total
    geral += total
}
END {
    print "VENDAS POR VENDEDOR"
    PROCINFO["sorted_in"] = "@val_num_desc"
    for (v in por_vendedor) printf "  %-8s R$ %8.2f\n", v, por_vendedor[v]
    print "VENDAS POR DIA"
    PROCINFO["sorted_in"] = "@ind_str_asc"
    for (d in por_dia) printf "  %s R$ %8.2f\n", d, por_dia[d]
    printf "TOTAL GERAL      R$ %8.2f\n", geral
}' "$arq" | sed 's/\([0-9]\)\.\([0-9][0-9]\)$/\1,\2/'
