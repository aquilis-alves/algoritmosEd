#include <string.h>
#include "../utils.h"

/* Quick Sort (particionamento de Lomuto, pivo = ultimo elemento) */
static void quickSort_internal(char **vetor, int low, int high) {
    if (low < high) {
        char *pivo = vetor[high];
        int i = (low - 1);
        char *temp;
        for (int j = low; j <= high - 1; j++) {
            if (strcmp(vetor[j], pivo) < 0) {
                i++;
                temp = vetor[i]; vetor[i] = vetor[j]; vetor[j] = temp;
            }
        }
        temp = vetor[i + 1]; vetor[i + 1] = vetor[high]; vetor[high] = temp;
        int pi = i + 1;
        quickSort_internal(vetor, low, pi - 1);
        quickSort_internal(vetor, pi + 1, high);
    }
}

void ordenar(char **vetor, int n) {
    quickSort_internal(vetor, 0, n - 1);
}
