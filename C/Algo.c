#include <stdio.h>
#include <stdlib.h>

long long int fibb(int n) {
	long long int fnow = 0, fnext = 1, tempf;
	while(--n>0){
		tempf = fnow + fnext;
		fnow = fnext;
		fnext = tempf;
		}
		return fnext;
}

void Fibo(int *n, long long int *arr){
    *(arr) = 0;
    *(arr+1) = 1;

    for (int i=2; i <= *n; i++){
        *(arr+i) = *(arr+i-1) + *(arr+i-2);
    }

}

int main(int argc, char **argv) {
    int n = 20;
    long long int x = fibb(n);
    printf("%i->%lli\n",n,x);

    long long int arr[n];
    long long int *arrpt;
    arrpt = &arr[0];
    Fibo(&n, arrpt);
    for (int i=0; i <= sizeof(arr)/sizeof(long long int); i++){
        printf("%i -> %lli \n", i, arr[i]);
        printf("%i -> %lli \n", i, *(arrpt+i));
    }
    // for (int i=0; i <= sizeof(arr)/sizeof(long long int); i++){
    //     printf("%i -> %lli <-> %lli \n", i, *(arrpt+i), arr[i]);
    // }
    return 1;
}
