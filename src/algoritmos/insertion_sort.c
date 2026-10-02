#include <string.h>
#include "../utils.h"

/* Insertion Sort - O(N^2) */
void ordenar(char **vetor, int n) {
    for (int i = 1; i < n; i++) {
        char *chave = vetor[i];
        int j = i - 1;
        while (j >= 0 && strcmp(vetor[j], chave) > 0) {
            vetor[j + 1] = vetor[j];
            j = j - 1;
        }
        vetor[j + 1] = chave;
    }
}
