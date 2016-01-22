#include <stdio.h>
#include <stdlib.h>

void file_read(){
    FILE * pFile;
    char buffer[200];
    int res;

    pFile = fopen("/home/akopp/Desktop/TEST.csv", "r");
    if (pFile == NULL) {
        fputs("File Error", stderr);
        exit(1);
    }
    while (!feof(pFile)) {
        res = fread(buffer, 1, (sizeof buffer)-1, pFile);
        buffer[res] = 0;
        printf("%s", buffer);
    }
    fclose(pFile);
}

int main(int argc, char * argv[]) {
    file_read();
    return 0;
}
