#include <string.h>
#include "../utils.h"

/* Bubble Sort - O(N^2) */
void ordenar(char **vetor, int n) {
    char *temp;
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - 1 - i; j++) {
            if (strcmp(vetor[j], vetor[j + 1]) > 0) {
                temp = vetor[j]; vetor[j] = vetor[j + 1]; vetor[j + 1] = temp;
            }
        }
    }
}
