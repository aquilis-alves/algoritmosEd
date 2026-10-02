#ifndef UTILS_H
#define UTILS_H

/* Implementada em cada arquivo de src/algoritmos/ (um algoritmo por arquivo). */
void ordenar(char **vetor, int n);

/* Lê um arquivo com uma palavra por linha. Retorna o vetor e grava a quantidade em *n. */
char **ler_palavras(const char *caminho, int *n);

/* Grava o vetor em um arquivo, uma palavra por linha. Retorna 0 em caso de sucesso. */
int salvar_palavras(const char *caminho, char **vetor, int n);

/* Acrescenta uma linha com o tempo (em segundos) ao arquivo. Retorna 0 em caso de sucesso. */
int salvar_tempo(const char *caminho, double segundos);

/* Relógio de alta resolução, em segundos. */
double agora(void);

void liberar_palavras(char **vetor, int n);

#endif
