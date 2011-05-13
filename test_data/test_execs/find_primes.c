#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

int is_prime (int p) 
{
    int i;
    if (p < 2) return 0; 
    i = 2; 
    while (i*i <= p) {
        if (p % i == 0) return 0; 
        i++;
    } 
    return 1;
}

int main(int argc, const char *argv[])
{
    int i, first_time;

    if(argc != 3)
        return -1;

    int N = atoi(argv[1]);
    
    int num_threads = atoi(argv[2]);

    if(N < 2 || num_threads < 1)
        return -1;

    int *output = malloc(N*sizeof(int));

    omp_set_num_threads(num_threads);

    #pragma omp parallel for schedule(dynamic, 1) shared(output)
    for (i = 2; i <= N; i++) 
        output[i] = is_prime(i);

    first_time = 0;
    for (i = 2; i <= N; i++) 
    {
        if(output[i])
        {
            if(first_time == 0)
            {
                printf("%d", i);
                first_time = 1;
            }
            else
                printf(", %d", i);
        }
    }

    printf("\n");
    return 0;
}
