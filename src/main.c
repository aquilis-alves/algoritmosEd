/*
 * Programa genérico de ordenação: é compilado junto com UM arquivo de src/algoritmos/,
 * que fornece a função ordenar().
 *
 * Uso: programa <arquivo_entrada> <arquivo_ordenado> <arquivo_tempos>
 *   - lê as palavras (uma por linha) de <arquivo_entrada>
 *   - ordena e mede apenas o tempo do algoritmo
 *   - grava as palavras ordenadas em <arquivo_ordenado> (sobrescreve)
 *   - acrescenta o tempo em segundos ao final de <arquivo_tempos>
 */
#include <stdio.h>
#include "utils.h"

int main(int argc, char **argv) {
    if (argc != 4) {
        fprintf(stderr, "Uso: %s <entrada> <ordenado> <tempos>\n", argv[0]);
        return 1;
    }

    int n = 0;
    char **vetor = ler_palavras(argv[1], &n);
    if (!vetor) {
        fprintf(stderr, "Erro ao abrir '%s'\n", argv[1]);
        return 1;
    }

    double inicio = agora();
    ordenar(vetor, n);
    double tempo = agora() - inicio;

    if (salvar_palavras(argv[2], vetor, n) != 0 || salvar_tempo(argv[3], tempo) != 0) {
        fprintf(stderr, "Erro ao gravar arquivos de saida\n");
        liberar_palavras(vetor, n);
        return 1;
    }

    printf("%d palavras ordenadas em %.6f s\n", n, tempo);
    liberar_palavras(vetor, n);
    return 0;
}
