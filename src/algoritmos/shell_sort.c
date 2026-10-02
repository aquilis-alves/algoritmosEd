#include <string.h>
#include "../utils.h"

/* Shell Sort - sequencia de gaps n/2, n/4, ..., 1 */
void ordenar(char **vetor, int n) {
    for (int gap = n / 2; gap > 0; gap /= 2) {
        for (int i = gap; i < n; i++) {
            char *temp = vetor[i];
            int j;
            for (j = i; j >= gap && strcmp(vetor[j - gap], temp) > 0; j -= gap) {
                vetor[j] = vetor[j - gap];
            }
            vetor[j] = temp;
        }
    }
}
