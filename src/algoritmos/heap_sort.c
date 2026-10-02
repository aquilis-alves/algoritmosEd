#include <string.h>
#include "../utils.h"

/* Heap Sort - O(N log N) */
static void heapify(char **vetor, int n, int i) {
    int largest = i;
    int l = 2 * i + 1;
    int r = 2 * i + 2;
    char *temp;
    if (l < n && strcmp(vetor[l], vetor[largest]) > 0) largest = l;
    if (r < n && strcmp(vetor[r], vetor[largest]) > 0) largest = r;
    if (largest != i) {
        temp = vetor[i]; vetor[i] = vetor[largest]; vetor[largest] = temp;
        heapify(vetor, n, largest);
    }
}

void ordenar(char **vetor, int n) {
    char *temp;
    for (int i = n / 2 - 1; i >= 0; i--) heapify(vetor, n, i);
    for (int i = n - 1; i > 0; i--) {
        temp = vetor[0]; vetor[0] = vetor[i]; vetor[i] = temp;
        heapify(vetor, i, 0);
    }
}
