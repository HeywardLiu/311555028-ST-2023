#include <stdlib.h>
#include <stdio.h>

int* ptr;

void foo() {
    int local[10] = {-1};
    ptr = &local[0];
}

int main(int argc, char* argv[]){
    foo();
    *ptr = 0;
}