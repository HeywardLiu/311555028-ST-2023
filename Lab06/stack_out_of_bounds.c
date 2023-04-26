#include <stdlib.h>
#include <stdio.h>

int main(int argc, char **argv) {
  int stack_array[10]= {1};
  return stack_array[10];  // BOOM
}