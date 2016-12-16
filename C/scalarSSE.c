#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <xmmintrin.h>
#include <x86intrin.h>
#include <time.h>
#define size 65536

float * Random() {

    unsigned int seed = 123;
    float *t __attribute__((aligned(size))) = malloc(size*sizeof(float));
    int i;
    float num = 0.0;
    for(i=0; i<size; i++) {
        num = rand()/(RAND_MAX+1.0);
        t[i] = num;
    }

    return t;

}

float ScalarSSE(float *m1, float *m2) {

    float prod;
    int i;
    __m128 X, Y, Z;

    for(i=0; i<size; i+=4) {
        X = _mm_load_ps(&m1[i]);
        Y = _mm_load_ps(&m2[i]);
        X = _mm_mul_ps(X, Y);
        Z = _mm_add_ps(X, Z);
    }

    for(i=0; i<4; i++) {
        prod += Z[i];
    }

    return prod;

}

int16_t find_max(int16_t* buff, int size)
{
    int16_t maxmax[8];
    int i;
    int16_t max = buff[0];

    __m128i *f8 = (__m128i*)buff;
    __m128i maxval = _mm_setzero_si128();
    __m128i maxval2 = _mm_setzero_si128();
    for (i = 0; i < size / 16; i++) {
        maxval = _mm_max_epi16(maxval, f8[i]);
    }
    maxval2 = maxval;
    for (i = 0; i < 3; i++) {
        maxval = _mm_max_epi16(maxval, _mm_shufflehi_epi16(maxval, 0x3));
        _mm_store_si128(&maxmax, maxval);
        maxval2 = _mm_max_epi16(maxval2, _mm_shufflelo_epi16(maxval2, 0x3));
        _mm_store_si128(&maxmax, maxval2);
    }
    _mm_store_si128(&maxmax, maxval);
    for(i = 0; i < 8; i++)
        if(max < maxmax[i])
            max = maxmax[i];
    return max;
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
        float scalar_product_sse = ScalarSSE(s1, s2);
        stop = clock();
        cur_time = ((double) stop-start) / CLOCKS_PER_SEC;
        avg_time += cur_time;
    }

    printf("Averagely used %f seconds.\n", avg_time / 100);

}
