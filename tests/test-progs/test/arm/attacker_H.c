#include <stdio.h>
#include <stdlib.h>

int main() {
	int i, j;
	int * buffer;
	buffer = (int *) malloc(sizeof(int)*1000);
	
	for (i = 0; i < 1000; i++) buffer[i] = i;

	printf ("Finish initialization\n");
	
	return 0;
}