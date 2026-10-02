#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "utils.h"

#ifdef _WIN32
#include <windows.h>
double agora(void) {
    LARGE_INTEGER freq, cnt;
    QueryPerformanceFrequency(&freq);
    QueryPerformanceCounter(&cnt);
    return (double)cnt.QuadPart / (double)freq.QuadPart;
}
#else
#include <time.h>
double agora(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9;
}
#endif

char **ler_palavras(const char *caminho, int *n) {
    FILE *f = fopen(caminho, "r");
    if (!f) return NULL;

    int capacidade = 1024, total = 0;
    char **vetor = malloc(capacidade * sizeof(char *));
    char linha[4096];

    while (fgets(linha, sizeof(linha), f)) {
        linha[strcspn(linha, "\r\n")] = '\0';
        if (linha[0] == '\0') continue;
        if (total == capacidade) {
            capacidade *= 2;
            vetor = realloc(vetor, capacidade * sizeof(char *));
        }
        vetor[total++] = strdup(linha);
    }
    fclose(f);
    *n = total;
    return vetor;
}

int salvar_palavras(const char *caminho, char **vetor, int n) {
    FILE *f = fopen(caminho, "w");
    if (!f) return 1;
    for (int i = 0; i < n; i++) {
        fputs(vetor[i], f);
        fputc('\n', f);
    }
    fclose(f);
    return 0;
}

int salvar_tempo(const char *caminho, double segundos) {
    FILE *f = fopen(caminho, "a");
    if (!f) return 1;
    fprintf(f, "%.9f\n", segundos);
    fclose(f);
    return 0;
}

void liberar_palavras(char **vetor, int n) {
    for (int i = 0; i < n; i++) free(vetor[i]);
    free(vetor);
}
