#include <iostream>
#include <string>
#include <ctime>
#include <cstdlib>

using namespace std;

string randomizer(string word)
{
    string random;
    int position (0);
    
    while (word.size() != 0)
    {
        position = rand() % word.size();
        random += word[position];
        word.erase(position, 1);
    }
    return random;
}

int main()
{
    string mysteryWord, randomWord, userWord;
    
    srand(time(0));
    
    cout << "Word please ?? :" << endl;
    cin >> mysteryWord;
    
    randomWord = randomizer(mysteryWord);
    
    do
    {
        cout << endl << "find the Word !! " << randomWord << endl;
        cin >> userWord;
        if (userWord == mysteryWord )
        {
            cout << "Congrat !!" << endl;
        }
        else
        {
            cout << "isn't that !!" << endl;
        }
    }while (userWord != mysteryWord);
        
        return 0;
}
