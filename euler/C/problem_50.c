#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

const int M = 1000000;
bool P[M];

void make_prime_table(bool *p, int N)
{
	p[0] = false;
	p[1] = false;
	for(int i = 2; i < N; i++)
		p[i] = true;
	for(int i = 2; i < N; i++)
		for(int j = i+i; j < N; j+=i)
			p[j] = false;
}

bool is_prime(int n)
{
	return P[n];
}

long next_prime(long n, long N)
{
	for(long i=n+1; (i<N); i++ )
		if(is_prime(i))
			return(i);
    
	return 0;
}

int main(int argc, char *argv[])
{
    make_prime_table(P,M);
    int N = 1000000;
	long S = 0;
	long K = 0;
	for(long n = 2; n ; n=next_prime(n, N))
	{
		long s = n;
		for(long m = next_prime(n, M), k=0; m ; m = next_prime(m, N), k++)
		{
			s += m;
			if((s < N) && is_prime(s) && (k > K))
				K = k, S = s;
		}
	}
	printf("Done\n");
}