#include <stdio.h>
#include <stdlib.h>

void file_read(){
    FILE * pFile;
    char buffer[100];
    int res;

    pFile = fopen("/home/arnaud/Desktop/TEMP/assoc.csv", "rb");
    if (pFile == NULL) {
        fputs("File Error", stderr);
        exit(1);
    }
    while (!feof(pFile)) {
        res = fread(buffer, 1, (sizeof buffer)-1, pFile);
        buffer[res] = 0;
        //printf("%s \n", buffer);
        //printf("res : %d \n", res);
    }
    fclose(pFile);
}

int main(int argc, char * argv[]) {
    file_read();
    return 0;
}
