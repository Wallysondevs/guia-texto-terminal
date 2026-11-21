# Guia Texto no Terminal — sed, awk e jq do zero

**Site:** https://wallysondevs.github.io/guia-texto-terminal/

Curso estático, em português do Brasil, para aprender a editar, filtrar, somar e transformar texto e JSON no terminal do Linux com **sed**, **awk** e **jq**. Complementa o [Guia Bash](https://wallysondevs.github.io/guia-bash/).

- Uma aula por assunto, em cinco níveis: Base (pipes, filtros, grep e regex), sed, awk, jq e Projetos.
- Toda saída mostrada nas aulas foi **colhida de verdade** (GNU sed 4.9, GNU awk 5.2, jq 1.7, Bash 5.2, `pt_BR.UTF-8`) na pasta de teste `~/guia-texto-teste`, com os arquivos inventados de [`arquivos/`](arquivos/).
- Missões no modo “cole a saída”: o leitor roda o comando no próprio terminal, cola a resposta e a página confere.

## Usar

Abra `index.html` no navegador, ou publique a pasta no GitHub Pages (é tudo estático, com links relativos; o `.nojekyll` desliga o Jekyll).

Para praticar, crie a pasta de teste com os arquivos de exemplo:

```bash
cd ~ && git clone https://github.com/Wallysondevs/guia-texto-terminal.git
mkdir -p ~/guia-texto-teste && cd ~/guia-texto-teste
bash ~/guia-texto-terminal/arquivos/criar-arquivos.sh
```

(Se você clonou em outra pasta, troque `~/guia-texto-terminal` pelo caminho dela. O `git clone` acima, rodado na sua pasta pessoal, cria exatamente `~/guia-texto-terminal`.)

## Manutenção

| Arquivo | Para quê |
| --- | --- |
| `tools/aulas_n1.py` … `aulas_n5.py` | O texto das aulas, os comandos de cada caixa e as missões. |
| `tools/gerar.py comandos` | Escreve `tools/comandos.txt` (o que a coleta roda) e `arquivos/criar-arquivos.sh`. |
| `tools/coleta.sh` | Roda de verdade cada caixa numa pasta de teste recriada do zero; grava `_saidas/` (bruto) e `_saidas-anon/` (anonimizado). Nenhuma das duas pastas vai para o git. |
| `tools/gerar.py paginas` | Gera as páginas `.html` e o `NIVEIS` do `assets/site.js` só a partir de `_saidas-anon/`. Se faltar coleta, para com erro. |
| `tools/checar-privacidade.sh` | Procura dados da máquina de coleta nas páginas e no histórico (lista real fora do repo, `PROIBIDO=...`). |
| `tools/testar-missoes.js` | Confere a estrutura das missões e as metas `src`. |
| `tools/testar-navegador.js --todas` | Abre cada página num Chrome headless e testa as missões (positivos e negativos). |

Fluxo completo:

```bash
python3 tools/gerar.py comandos && bash tools/coleta.sh && python3 tools/gerar.py paginas
PROIBIDO=lista.txt bash tools/checar-privacidade.sh
node tools/testar-missoes.js
PUPPETEER_DIR=/caminho/puppeteer-core node tools/testar-navegador.js --todas
```

A coleta precisa de `gawk`, `jq` e do locale `pt_BR.UTF-8` (com as traduções do sed, do gawk, do coreutils e da libc) para reproduzir as mensagens em português.
