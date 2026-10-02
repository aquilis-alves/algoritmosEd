"""
Executa automaticamente todos os algoritmos de ordenação (programas em C) N vezes
para cada arquivo de entrada, sem menus nem perguntas.

Estrutura gerada:
    bin/                               executáveis compilados a partir de src/
    output/<entrada>/palavras_filtradas.txt   palavras após o pré-processamento
    output/<entrada>/<algoritmo>/tempos.txt   um tempo (s) por linha, gravado pelo programa em C
    output/<entrada>/<algoritmo>/ordenado.txt palavras ordenadas, gravadas pelo programa em C

Uso:
    python teste_ordenacao.py                      # todos os arquivos de inputs/, todos os algoritmos, 5 execuções
    python teste_ordenacao.py -a mergeSort quickSort -f nomes250k.txt
    python teste_ordenacao.py -n 10
"""
import argparse
import glob
import os
import re
import subprocess
import sys

DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
DIR_INPUTS = os.path.join(DIRETORIO_ATUAL, "inputs")
DIR_SRC = os.path.join(DIRETORIO_ATUAL, "src")
DIR_ALGORITMOS = os.path.join(DIR_SRC, "algoritmos")
DIR_BIN = os.path.join(DIRETORIO_ATUAL, "bin")
DIR_OUTPUT = os.path.join(DIRETORIO_ATUAL, "output")

EXECUCOES_PADRAO = 5
FLAGS_GCC = ["-O2", "-std=gnu11"]

# nome do algoritmo -> arquivo em src/algoritmos/
ALGORITMOS = {
    "bubbleSort": "bubble_sort.c",
    "selectionSort": "selection_sort.c",
    "insertionSort": "insertion_sort.c",
    "shellSort": "shell_sort.c",
    "mergeSort": "merge_sort.c",
    "quickSort": "quick_sort.c",
    "heapSort": "heap_sort.c",
}


# 1. PRÉ-PROCESSAMENTO
def pre_processar_texto(texto_bruto):
    """Converte para minúsculas e remove números, símbolos e caracteres especiais."""
    texto_limpo = texto_bruto.lower()
    texto_limpo = re.sub(r"[^a-z\s]", "", texto_limpo)
    return texto_limpo.split()


def carregar_e_filtrar_arquivo(caminho):
    """Lê o arquivo, limpa o texto e devolve (palavras, qtd_antes, qtd_depois)."""
    palavras_antes = 0
    palavras_depois = []
    with open(caminho, "r", encoding="utf-8") as f:
        for linha in f:
            palavras_antes += len(linha.split())
            palavras_depois.extend(t for t in pre_processar_texto(linha) if t)
    return palavras_depois, palavras_antes, len(palavras_depois)


# 2. COMPILAÇÃO
def executavel_de(nome_algoritmo):
    sufixo = ".exe" if os.name == "nt" else ""
    return os.path.join(DIR_BIN, nome_algoritmo + sufixo)


def compilar(nome_algoritmo):
    """Compila main.c + utils.c + o arquivo do algoritmo em bin/<algoritmo>."""
    os.makedirs(DIR_BIN, exist_ok=True)
    fontes = [
        os.path.join(DIR_SRC, "main.c"),
        os.path.join(DIR_SRC, "utils.c"),
        os.path.join(DIR_ALGORITMOS, ALGORITMOS[nome_algoritmo]),
    ]
    saida = executavel_de(nome_algoritmo)
    cmd = ["gcc", *FLAGS_GCC, *fontes, "-o", saida]
    resultado = subprocess.run(cmd, capture_output=True, text=True)
    if resultado.returncode != 0:
        print(f"[ERRO] Falha ao compilar {nome_algoritmo}:\n{resultado.stderr}")
        sys.exit(1)
    return saida


# 3. EXECUÇÃO
def executar_experimento(nome_algoritmo, exe, arquivo_filtrado, pasta_saida, execucoes, esperado):
    os.makedirs(pasta_saida, exist_ok=True)
    caminho_ordenado = os.path.join(pasta_saida, "ordenado.txt")
    caminho_tempos = os.path.join(pasta_saida, "tempos.txt")

    # Recomeça o arquivo de tempos (o programa em C apenas acrescenta uma linha por execução)
    open(caminho_tempos, "w").close()

    print(f"\n  {nome_algoritmo}: {execucoes} execuções")
    for i in range(1, execucoes + 1):
        r = subprocess.run([exe, arquivo_filtrado, caminho_ordenado, caminho_tempos],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print(f"    [ERRO] Execução {i} falhou: {r.stderr.strip()}")
            sys.exit(1)
        print(f"    -> Execução {i}: {r.stdout.strip()}")

    with open(caminho_tempos) as f:
        tempos = [float(l) for l in f if l.strip()]
    print(f"    [RESULTADO] Média: {sum(tempos) / len(tempos):.6f} s")

    # Conferência: a saída do C precisa ser igual à ordenação de referência
    with open(caminho_ordenado, encoding="utf-8") as f:
        obtido = f.read().split("\n")[:-1]
    if obtido != esperado:
        print(f"    {nome_algoritmo} NÃO está corretamente ordenado!")


def main():
    parser = argparse.ArgumentParser(description="Executar os algoritmos de ordenação em C automaticamente.")
    parser.add_argument("-f", "--arquivos", nargs="+",
                        help="arquivos dentro de inputs/ (padrão: todos os nomes*.txt)")
    parser.add_argument("-a", "--algoritmos", nargs="+", choices=list(ALGORITMOS),
                        help="algoritmos a executar (padrão: todos)")
    parser.add_argument("-n", "--execucoes", type=int, default=EXECUCOES_PADRAO,
                        help=f"execuções por algoritmo (padrão: {EXECUCOES_PADRAO})")
    args = parser.parse_args()

    if args.arquivos:
        arquivos = [os.path.join(DIR_INPUTS, a) for a in args.arquivos]
    else:
        arquivos = sorted(glob.glob(os.path.join(DIR_INPUTS, "nomes*.txt")))
    for a in arquivos:
        if not os.path.exists(a):
            sys.exit(f"Arquivo não encontrado: {a}")
    if not arquivos:
        sys.exit(f"Nenhum arquivo nomes*.txt em {DIR_INPUTS}")

    algoritmos = args.algoritmos or list(ALGORITMOS)

    print("Compilando os programas")
    executaveis = {nome: compilar(nome) for nome in algoritmos}

    for caminho in arquivos:
        nome_entrada = os.path.splitext(os.path.basename(caminho))[0]
        pasta_entrada = os.path.join(DIR_OUTPUT, nome_entrada)
        os.makedirs(pasta_entrada, exist_ok=True)

        palavras, antes, depois = carregar_e_filtrar_arquivo(caminho)
        arquivo_filtrado = os.path.join(pasta_entrada, "palavras_filtradas.txt")
        with open(arquivo_filtrado, "w", encoding="utf-8") as f:
            f.writelines(p + "\n" for p in palavras)

        print(f"\n=== {os.path.basename(caminho)} ===")
        print(f"ANTES:  {antes}")
        print(f"DEPOIS: {depois}")

        esperado = sorted(palavras)
        for nome in algoritmos:
            executar_experimento(nome, executaveis[nome], arquivo_filtrado,
                                 os.path.join(pasta_entrada, nome), args.execucoes, esperado)

    print("\nConcluído")


if __name__ == "__main__":
    main()
