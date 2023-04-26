#include <stdlib.h>
#include <stdio.h>

int main(int argc, char **argv) {
  int *array = malloc(sizeof(int)*10);
  free(array);
  return array[10];  // BOOM
}