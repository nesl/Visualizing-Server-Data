#include <stdio.h>
#include <string.h>

int main(int argc, const char *argv[])
{
    int i;
    if(argc > 1)
    {
        printf("Hello, here are the arguments: \n");
        for (i = 1; i < argc; i++) {
            printf("%s ", argv[i]);
        }
        printf("\n");
    }
    else
        printf("No arguments\n");
    return 0;
}
