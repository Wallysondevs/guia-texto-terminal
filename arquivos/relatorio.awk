# relatorio.awk: total vendido por vendedor (vendas.csv)
BEGIN { FS = "," }
NR > 1 { total[$2] += $4 * $5 }
END {
    for (v in total)
        printf "%-8s R$ %8.2f\n", v, total[v]
}
