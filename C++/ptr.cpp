#include <iostream>
using namespace std;

void prout()
{
    //int* pointeur(0);
    //pointeur = new int;
    //cout << "Quel est votre age ? ";
    //cin >> *pointeur;
    // On écrit dans la case mémoire pointée par le pointeur 'pointeur'
    //cout << "Vous avez " << *pointeur << " ans." << endl;
    //cout << "adresse pointeur" << pointeur << endl;
    // Test sur les pointeurs
    //*pointeur = 42;
    //cout << "Vous avez " << *pointeur << " ans." << endl;
    //cout << "adresse pointeur" << pointeur << endl;
    //On utilise à nouveau *pointeur
    //delete pointeur;   //Ne pas oublier de libérer la mémoire
    
    int ageUser(24);
    int *ptr = NULL;

    ptr = &ageUser;
    cout << "Adresse de ageUser : " << &ageUser << endl;
    cout << "Val adresse ptr : " << ptr << endl;
    cout << "Val adresse ptr : " << *ptr << endl;
    

    // init ptr test
    int number = 88;    // Declare an int variable and assign an initial value
    int * pNumber;      // Declare a pointer variable pointing to an int (or int pointer)
    pNumber = &number;  // assign the address of the variable number to pointer pNumber
 
    cout << pNumber << endl;  // Print content of pNumber (0x22ccf0)
    cout << &number << endl;  // Print address of number (0x22ccf0)
    cout << *pNumber << endl; // Print value pointed to by pNumber (88)
    cout << number << endl;   // Print value of number (88)
 
    *pNumber = 99;            // Re-assign value pointed to by pNumber
    cout << pNumber << endl;  // Print content of pNumber (0x22ccf0)
    cout << &number << endl;  // Print address of number (0x22ccf0)
    cout << *pNumber << endl; // Print value pointed to by pNumber (99)
    cout << number << endl;   // Print value of number (99)
                             // The value of number changes via pointer 
    cout << &pNumber << endl; // Print the address of pointer variable pNumber (0x22ccec)

    // reference test
    //int number = 88;          // Declare an int variable called number
    int & refNumber = number; // Declare a reference (alias) to the variable number
                             // Both refNumber and number refer to the same value
     
    cout << number << endl;    // Print value of variable number (88)
    cout << refNumber << endl; // Print value of reference (88)
            
    refNumber = 99;            // Re-assign a new value to refNumber
    cout << refNumber << endl;
    cout << number << endl;    // Value of number also changes (99)
                      
    number = 55;               // Re-assign a new value to number
    cout << number << endl;
    cout << refNumber << endl; // Value of refNumber also changes (55)
}

void ref_vs_ptr() {
   int number1 = 88, number2 = 22;
 
   // Create a pointer pointing to number1
   int * pNumber1 = &number1;  // Explicit referencing
   *pNumber1 = 99;             // Explicit dereferencing
   cout << *pNumber1 << endl;  // 99
   cout << &number1 << endl;   // 0x22ff18
   cout << pNumber1 << endl;   // 0x22ff18 (content of the pointer variable - same as above)
   cout << &pNumber1 << endl;  // 0x22ff10 (address of the pointer variable)
   pNumber1 = &number2;        // Pointer can be reassigned to store another address
                          
    // Create a reference (alias) to number1
   int & refNumber1 = number1;  // Implicit referencing (NOT &number1)
   refNumber1 = 11;             // Implicit dereferencing (NOT *refNumber1)
   cout << refNumber1 << endl;  // 11
   cout << &number1 << endl;    // 0x22ff18
   cout << &refNumber1 << endl; // 0x22ff18
   //refNumber1 = &number2;     // Error! Reference cannot be re-assigned
                             // error: invalid conversion from 'int*' to 'int'
   refNumber1 = number2;        // refNumber1 is still an alias to number1.
   // Assign value of number2 (22) to refNumber1 (and number1).
   number2++;   
   cout << refNumber1 << endl;  // 22
   cout << number1 << endl;     // 22
   cout << number2 << endl;     // 23
}

int main()
{
    prout();
    ref_vs_ptr();
    return 0;
}


