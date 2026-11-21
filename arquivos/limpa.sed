# limpa.sed: tira comentários e linhas vazias do config.txt
/^#/d
/^$/d
s/=/ = /
