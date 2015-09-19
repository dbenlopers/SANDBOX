#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#define size 65536

float * Random() {

    unsigned int seed = 123;
    float *t = malloc(size*sizeof(float));
    int i;
    float num = 0.0;
    for(i=0; i<size; i++) {
        num = rand()/(RAND_MAX+1.0);
        t[i] = num;
    }

    return t;

}

float Scalar(float *s1, float *s2) {

    int i;
    float prod;

    for(i=0; i<size; i++) {
        prod += s1[i] * s2[i];
    }

    return prod;

}


int main(int argc, char * argv[]) {

    int i;
    time_t start, stop;
    double avg_time = 0;
    double cur_time;
    float *s1, *s2;

    for(i=0; i<100; i++) {
        s1 = Random();
        s2 = Random();
        start = clock();
        float scalar_product = Scalar(s1, s2);
        stop = clock();
        cur_time = ((double) stop-start) / CLOCKS_PER_SEC;
        avg_time += cur_time;
    }

    printf("Averagely used %f seconds.\n", avg_time / 100);

}
