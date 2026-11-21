#!/usr/bin/env bash
# coleta.sh — roda de verdade os comandos de todas as aulas e guarda as saídas.
#
#   bash tools/coleta.sh            (todas as caixas de tools/comandos.txt)
#   bash tools/coleta.sh sed-p-1    (só as caixas cujo id começa com o prefixo)
#
# Para cada caixa ("### id" em tools/comandos.txt):
#   1. recria do zero a pasta de teste /tmp/guia-texto-teste rodando o
#      arquivos/criar-arquivos.sh (assim um sed -i de uma caixa não suja a outra);
#   2. roda cada linha como um comando do Bash, nessa pasta, em pt_BR.UTF-8,
#      juntando a saída normal e a de erro (2>&1), como aparece no terminal;
#   3. grava o bruto em _saidas/<id>.json (fora do git) e a cópia anonimizada
#      em _saidas-anon/<id>.json (também fora do git). As aulas são geradas
#      só a partir da cópia anonimizada.
# Nada de rede, nada fora da pasta de teste.
set -u
cd "$(dirname "$0")/.."
RAIZ=$(pwd)
TESTE=/tmp/guia-texto-teste
LISTA=tools/comandos.txt
FILTRO="${1:-}"
mkdir -p _saidas _saidas-anon
ANON_HOST=$(hostname)
ANON_USER=$(id -un)

anonimiza() {
  sed -e "s#$TESTE#/home/ana/guia-texto-teste#g" \
      -e "s#$RAIZ#/home/ana/guia-texto-terminal#g" \
      -e "s#$HOME#/home/ana#g" \
      -e "s#/home/$ANON_USER#/home/ana#g" \
      -e "s#$ANON_HOST#notebook#g" \
      -e "s#\b$ANON_USER\b#ana#g"
}

roda_caixa() {
  local id="$1"; shift
  [ -n "$FILTRO" ] && [[ "$id" != "$FILTRO"* ]] && return 0
  rm -rf "$TESTE"; mkdir -p "$TESTE"; cp "$RAIZ/arquivos/criar-arquivos.sh" "$TESTE/"
  ( cd "$TESTE" && bash criar-arquivos.sh >/dev/null ) || { echo "falhou criar-arquivos.sh"; exit 1; }
  local bruto="[]" anon="[]" tmp; tmp=$(mktemp)
  for cmd in "$@"; do
    ( cd "$TESTE" && env -i PATH=/usr/local/bin:/usr/bin:/bin HOME="$TESTE" \
        LANG=pt_BR.UTF-8 LC_ALL=pt_BR.UTF-8 TERM=dumb \
        timeout 10 bash -c "$cmd" </dev/null >"$tmp" 2>&1 )
    local cod=$?
    bruto=$(jq -c --arg c "$cmd" --rawfile o "$tmp" --argjson s "$cod" '. + [{cmd: $c, out: $o, status: $s}]' <<<"$bruto")
    local ca oa; ca=$(printf '%s' "$cmd" | anonimiza); anonimiza <"$tmp" >"$tmp.a"
    anon=$(jq -c --arg c "$ca" --rawfile o "$tmp.a" --argjson s "$cod" '. + [{cmd: $c, out: $o, status: $s}]' <<<"$anon")
  done
  printf '%s\n' "$bruto" | jq . >"_saidas/$id.json"
  printf '%s\n' "$anon" | jq . >"_saidas-anon/$id.json"
  rm -f "$tmp" "$tmp.a"
  echo "coletada: $id ($# comando(s))"
}

id=""; cmds=()
while IFS= read -r linha || [ -n "$linha" ]; do
  if [[ "$linha" == "### "* ]]; then
    [ -n "$id" ] && roda_caixa "$id" "${cmds[@]}"
    id="${linha#\#\#\# }"; cmds=()
  elif [ -n "$linha" ]; then
    cmds+=("$linha")
  fi
done <"$LISTA"
[ -n "$id" ] && roda_caixa "$id" "${cmds[@]}"
rm -rf "$TESTE"
