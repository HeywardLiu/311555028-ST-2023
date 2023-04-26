#include <stdlib.h>
#include <stdio.h>

int global_array[10] = {-1};

int main(int argc, char **argv) {
  return global_array[10];  // BOOM
}