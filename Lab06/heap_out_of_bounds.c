#include <stdlib.h>
#include <stdio.h>

int main(int argc, char **argv) {
  int *array =  malloc(sizeof(int)*100);
  array[0] = 1;
  int res = array[100];  // BOOM
  free(array);
  return res;
}