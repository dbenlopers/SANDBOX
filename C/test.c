#include <stdio.h>
#include <stdlib.h>
//#include <math.h>

/*int main () {
        int age ;
        char nom[] = "Arnaud KOPP" ;
        age = 24;
	printf("Bonjour\n");
	printf("Tu est %s et tu as %d ans\n",nom,age);
	//getchar(); //permet d'attendre la frappe d'une touche pour la fin de l'execution
	return 0;
}*/

int main () {
        int a;
        int b;
        int somme;
        printf("Enter Calculatrice \n\n");
        printf("a Value ? \n");
        scanf("%d", &a); // saisie de la valeur a
        printf("b Value ? \n");
        scanf("%d", &b); // saisie de la valeur b
        somme=(a+b);
        printf("Valeur de a + b : %d \n",somme);
        printf("Valeur absolue de a + b : %d \n", abs(somme));
        return 0;
}

