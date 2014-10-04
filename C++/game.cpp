#include <iostream>
using namespace std;
void guessing_game();

int main() {
        guessing_game();
}

void guessing_game() {
        int guess, counter = 0 , number = 5;
        bool found = false;
        do {
                cout << "Trouve le bon chiffre :\t";
                cin >> guess;
                if (guess >100 or guess <=0)
                {
                        cout << "Chiffre entre 1 et 100 \n\n";
                        counter++;
                }
                else if (guess < number)
                {
                        cout << "trop bas, retente ta chance !! \n\n";
                        counter++;
                }
                else if (guess > number)
                {
                        cout << "trop haut, retente ta chance !! \n\n";
                        counter++;
                }
                else //ont trouve dans ce cas
                {
                        cout << "Tu a trouver !!\n";
                        found = true;
                        counter++;
                }
         } while (!found);
         cout << "ca ta pris " << counter << " essaie ! \n";
         cout << "merci d'avoir jouer !! \n\n";
}
