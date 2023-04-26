#include <stdlib.h>
#include <stdio.h>

int main(int argc, char* argv[]){
    int a[3] = {0, 0, 0};
    int b[3] = {1, 1, 1};

    printf("Before:\n");
    for(int i=0; i<3; i++) {
        printf("  b[%d] = %d\n", i, b[i]);
    }
    printf("\n&a[8] = %p, &b[0]:%p\n\n", &a[8], &b[0]);
    
    a[8] = 0;  // Modifify array of b by crossing redzone

    printf("After modification:\n");
    for(int i=0; i<3; i++) {
        printf("  b[%d] = %d\n", i, b[i]);
    }
    return 0;
}