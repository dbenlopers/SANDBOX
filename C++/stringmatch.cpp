#include <iostream>
#include <string.h>

using namespace std;

void KMP_Prefix(string pattern, int* pre_table,int m){
    pre_table[1] = 0;
    int i=0;
    for(int j = 1; j < m; j++){
        while (i > 0 && pattern[i] != pattern[j]) {
            i = pre_table[i];
        }
        if(pattern[i] == pattern[j]){
            i++;
        }
        pre_table[j] = i;
    }
}

int KMPMatching(string pattern, string long_string ,int* table){
    int n = long_string.length();
    int m = pattern.length();
    int i = 0, j = 0, k = 0;
    while(n - k >= m){
        while(j < m && long_string[i] == pattern[j]){
            i++;
            j++;
        }
        if(j >= m){
            cout << "pattern found at: " << k << endl;
        }
        if(j > 0 && table[j-1] > 0)
            k = i - table[j-1];
        else{
            if(i == k) i++;
            k = i;
        }
        if(j >= 1) j = table[j-1];
    }
}

void KMP(){
    string pattern;
    string long_string;
	cout << "Enter the string that we look for some patterns.\n>> ";
	cin >> long_string;
	cout << "Enter the pattern that we look for.\n>> ";
	cin >> pattern;

    int m = pattern.length();
    int pre_table[m];
    for (int i = 0; i < m; i++) {
        pre_table[i] = 0;
    }

    KMP_Prefix(pattern,pre_table,m);
    KMPMatching(pattern, long_string, pre_table) ;
}

void FSAutomata(int table[][3], string pattern, int m, int a){

    for (int i = 0; i <= m; i++) {
        for (int j = 0; j < a; j++) {
            if(pattern[i] == (j+'a')){
                table[i][j] = i+1;
            }
            else{
                string sub = pattern.substr(0,i);
                sub += (j+'a');
                int sublen = sub.length();
                int k = 0;
                for (k = 0; k < sublen; k++){
                    string subsub = sub.substr(k);
                    if( !strncmp( pattern.c_str(), subsub.c_str(), sublen - k) ){
                        break;
                    }
                }
                table[i][j] = sublen - k;
            }
        }
    }
}

void FSARun(int table[][3], string long_string, int m , int a){
    int state = 0;
    int lsize = long_string.length();
    int i = 0;
    cout << lsize << " is the size of string\n";
    for(i = 0; i < lsize; i++){
        state = table[state][long_string[i] - 'a'];
        if(state == m)
            cout << "match found at: " << i - m + 1 << endl;
    }
}

void FSM(){
    string pattern;
    string long_string;
	cout << "Enter the string that we look for some patterns.\n>> ";
	cin >> long_string;
	cout << "Enter the pattern that we look for.\n>> ";
	cin >> pattern;

    int m = pattern.length();
    int n = long_string.length();
    int table[m+1][3];
    for(int i = 0; i <= m; i++)
        for (int j = 0; j < 3; j++)
            table[i][j] = 0;

    FSAutomata(table, pattern, m , 3);
    FSARun(table, long_string, m, 3);

}

int main(){
	char kf = 0;
	cout << "Press K or F to make choice between KMP and FSM accordingly.\n";
	cout << "Press X for exit.";
	while(kf != 'x' || kf != 'X') {
		cin >> kf >> ws;
		if(kf != 'f' || kf != 'F') {
			FSM();
		}
		else if(kf != 'k' || kf != 'K') {
			KMP();
		}
		 else if(kf != 'x' || kf != 'X') {
			cout << "Choose a valid key among F,M,X.";
		 }
	}
    return 0;
}
