#include <iostream>
using namespace std;

void prout()
{
    int* pointeur(0);
    pointeur = new int;
    cout << "Quel est votre age ? ";
    cin >> *pointeur;
    //On écrit dans la case mémoire pointée par le pointeur 'pointeur'
    cout << "Vous avez " << *pointeur << " ans." << endl;
    cout << "adresse pointeur" << pointeur << endl;
    // Test sur les pointeurs
    *pointeur = 42;
    cout << "Vous avez " << *pointeur << " ans." << endl;
    cout << "adresse pointeur" << pointeur << endl;
    //On utilise à nouveau *pointeur
    delete pointeur;   //Ne pas oublier de libérer la mémoire
    pointeur = 0;       //Et de faire pointer le pointeur vers rien
    
    int ageUser(24);
    int *ptr = NULL;

    ptr = &ageUser;
    cout << "Adresse de ageUser : " << &ageUser << endl;
    cout << "Val adresse ptr : " << ptr << endl;
    cout << "Val adresse ptr : " << *ptr << endl;

}

int main()
{
    prout();
    return 0;
}


