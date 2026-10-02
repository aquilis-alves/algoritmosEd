#include <string.h>
#include "../utils.h"

/* Selection Sort - O(N^2) */
void ordenar(char **vetor, int n) {
    char *temp;
    for (int i = 0; i < n - 1; i++) {
        int min_idx = i;
        for (int j = i + 1; j < n; j++) {
            if (strcmp(vetor[j], vetor[min_idx]) < 0) {
                min_idx = j;
            }
        }
        temp = vetor[min_idx]; vetor[min_idx] = vetor[i]; vetor[i] = temp;
    }
}
