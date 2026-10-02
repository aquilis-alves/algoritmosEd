"""
Gera DOIS gráficos comparativos a partir de output/, separados por complexidade:

    1) O(N log N): shellSort, mergeSort, quickSort, heapSort
    2) O(N²):      bubbleSort, selectionSort, insertionSort

Lê:   output/<entrada>/<algoritmo>/tempos.txt   (um tempo em segundos por linha)
Gera: output/graficos/grafico_n_log_n.png
      output/graficos/grafico_n_quadrado.png
      output/resumo_estatistico.csv             (média, desvio padrão, mín., máx. por algoritmo)

Cada gráfico mostra, para cada algoritmo do grupo, o tempo médio (± desvio padrão)
em cada tamanho de entrada (nomes250k, nomes500k, nomes1m).

Uso:
    python grafico_comparativo.py            # salva os PNGs
    python grafico_comparativo.py --mostrar  # também abre as janelas dos gráficos
"""
import argparse
import csv
import os
import statistics

import matplotlib.pyplot as plt

DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
DIR_OUTPUT = os.path.join(DIRETORIO_ATUAL, "output")
DIR_GRAFICOS = os.path.join(DIR_OUTPUT, "graficos")

ORDEM = ["bubbleSort", "selectionSort", "insertionSort",
         "shellSort", "mergeSort", "quickSort", "heapSort"]

# Observação: o Shell Sort (gaps N/2, N/4, ..., 1) tem pior caso O(N²), mas na prática
# tem desempenho comparável aos O(N log N), por isso fica nesse grupo.
GRUPO_N_LOG_N = ["shellSort", "mergeSort", "quickSort", "heapSort"]
GRUPO_N_QUADRADO = ["bubbleSort", "selectionSort", "insertionSort"]

CORES_ENTRADA = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3"]


def ordem_natural(entrada):
    """nomes250k < nomes500k < nomes1m (ordena pelo tamanho, não pelo alfabeto)."""
    n = entrada.lower().replace("nomes", "")
    mult = 1_000_000 if n.endswith("m") else 1_000 if n.endswith("k") else 1
    digitos = "".join(c for c in n if c.isdigit())
    return (int(digitos) * mult if digitos else 0, entrada)


def carregar_resultados():
    """Retorna {entrada: {algoritmo: [tempos]}}."""
    resultados = {}
    if not os.path.isdir(DIR_OUTPUT):
        return resultados
    for entrada in sorted(os.listdir(DIR_OUTPUT), key=ordem_natural):
        pasta = os.path.join(DIR_OUTPUT, entrada)
        if not os.path.isdir(pasta) or entrada == "graficos":
            continue
        dados = {}
        for alg in ORDEM:
            caminho = os.path.join(pasta, alg, "tempos.txt")
            if os.path.exists(caminho):
                with open(caminho) as f:
                    tempos = [float(l) for l in f if l.strip()]
                if tempos:
                    dados[alg] = tempos
        if dados:
            resultados[entrada] = dados
    return resultados


def formatar(t):
    if t < 1:
        return f"{t * 1000:.0f} ms"
    if t < 100:
        return f"{t:.2f} s"
    return f"{t:.0f} s"


def grafico_grupo(resultados, algoritmos, titulo, nome_arquivo, mostrar):
    """Barras agrupadas: um grupo por algoritmo, uma barra por tamanho de entrada."""
    entradas = list(resultados)
    algs = [a for a in algoritmos if any(a in d for d in resultados.values())]
    if not algs:
        print(f"[AVISO] Nenhum dado para: {titulo}")
        return

    largura = 0.8 / len(entradas)
    fig, ax = plt.subplots(figsize=(11, 6))
    maior = 0

    for j, entrada in enumerate(entradas):
        posicoes, medias, desvios = [], [], []
        for i, a in enumerate(algs):
            tempos = resultados[entrada].get(a)
            if not tempos:
                continue
            posicoes.append(i + (j - (len(entradas) - 1) / 2) * largura)
            medias.append(statistics.mean(tempos))
            desvios.append(statistics.stdev(tempos) if len(tempos) > 1 else 0)

        barras = ax.bar(posicoes, medias, width=largura, yerr=desvios, capsize=3,
                        label=entrada, color=CORES_ENTRADA[j % len(CORES_ENTRADA)],
                        edgecolor="black", linewidth=0.5, zorder=3)
        for barra, media, desvio in zip(barras, medias, desvios):
            ax.annotate(formatar(media),
                        xy=(barra.get_x() + barra.get_width() / 2, media + desvio),
                        xytext=(0, 3), textcoords="offset points",
                        ha="center", va="bottom", fontsize=8, fontweight="bold")
        if medias:
            maior = max(maior, max(m + d for m, d in zip(medias, desvios)))

    ax.set_ylim(0, maior * 1.12)  # folga para os rótulos
    ax.set_xticks(range(len(algs)))
    ax.set_xticklabels(algs, fontsize=11)
    ax.set_ylabel("Tempo médio de execução (segundos) ± desvio padrão")
    ax.set_title(titulo, fontsize=13, fontweight="bold")
    ax.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)
    ax.legend(title="Arquivo de entrada", loc="upper left")
    fig.tight_layout()

    caminho = os.path.join(DIR_GRAFICOS, nome_arquivo)
    fig.savefig(caminho, dpi=150)
    print(f"[GRÁFICO] {caminho}")
    if not mostrar:
        plt.close(fig)


def salvar_resumo(resultados):
    caminho = os.path.join(DIR_OUTPUT, "resumo_estatistico.csv")
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["entrada", "algoritmo", "execucoes", "media_s", "desvio_padrao_s", "minimo_s", "maximo_s"])
        for entrada, dados in resultados.items():
            for alg in ORDEM:
                if alg in dados:
                    t = dados[alg]
                    w.writerow([entrada, alg, len(t), f"{statistics.mean(t):.9f}",
                                f"{statistics.stdev(t) if len(t) > 1 else 0:.9f}",
                                f"{min(t):.9f}", f"{max(t):.9f}"])
    print(f"[CSV] {caminho}")


def main():
    parser = argparse.ArgumentParser(description="Gera os gráficos O(N log N) e O(N²) a partir de output/.")
    parser.add_argument("--mostrar", action="store_true", help="exibe os gráficos além de salvá-los")
    args = parser.parse_args()

    if not args.mostrar:
        plt.switch_backend("Agg")

    resultados = carregar_resultados()
    if not resultados:
        raise SystemExit("[ERRO] Nenhum tempos.txt encontrado em output/. Rode teste_ordenacao.py primeiro.")

    os.makedirs(DIR_GRAFICOS, exist_ok=True)
    grafico_grupo(resultados, GRUPO_N_LOG_N,
                  "Algoritmos O(N log N) — tempo médio por tamanho de entrada",
                  "grafico_n_log_n.png", args.mostrar)
    grafico_grupo(resultados, GRUPO_N_QUADRADO,
                  "Algoritmos O(N²) — tempo médio por tamanho de entrada",
                  "grafico_n_quadrado.png", args.mostrar)
    salvar_resumo(resultados)

    if args.mostrar:
        plt.show()


if __name__ == "__main__":
    main()