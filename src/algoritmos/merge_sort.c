#include <string.h>
#include <stdlib.h>
#include "../utils.h"

/* Merge Sort - O(N log N) */
static void merge(char **vetor, int l, int m, int r) {
    int n1 = m - l + 1;
    int n2 = r - m;
    char **L = (char **)malloc(n1 * sizeof(char *));
    char **R = (char **)malloc(n2 * sizeof(char *));
    for (int i = 0; i < n1; i++) L[i] = vetor[l + i];
    for (int j = 0; j < n2; j++) R[j] = vetor[m + 1 + j];
    int i = 0, j = 0, k = l;
    while (i < n1 && j < n2) {
        if (strcmp(L[i], R[j]) <= 0) { vetor[k] = L[i]; i++; }
        else { vetor[k] = R[j]; j++; }
        k++;
    }
    while (i < n1) { vetor[k] = L[i]; i++; k++; }
    while (j < n2) { vetor[k] = R[j]; j++; k++; }
    free(L); free(R);
}

static void mergeSort_internal(char **vetor, int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;
        mergeSort_internal(vetor, l, m);
        mergeSort_internal(vetor, m + 1, r);
        merge(vetor, l, m, r);
    }
}

void ordenar(char **vetor, int n) {
    mergeSort_internal(vetor, 0, n - 1);
}
