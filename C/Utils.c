#include <string.h>
#include <stdlib.h>
#include "utils.h"


/************************************************************************************/
/*  Safe memory allocation                                                          */
/************************************************************************************/
void* _safeMalloc(const char* file, int line, size_t size)
{
    void* p = malloc(size);
    if (p == NULL)
        fprintf(stderr, "Failed memory allocation in %s at line %d\n", file, line);
    return p;
}

void* _safeCalloc(const char* file, int line, size_t number, size_t size)
{
    void* p = calloc(number, size);
    if (p == NULL)
        fprintf(stderr, "Failed memory allocation in %s at line %d\n", file, line);
    return p;
}

void* _safeRealloc(const char* file, int line, void* ptr, size_t size)
{
    void* p = realloc(ptr, size);
    if (p == NULL)
        fprintf(stderr, "Failed memory allocation in %s at line %d\n", file, line);
    return p;
}

char* _safeStrdup(const char* file, int line, char* s)
{
    char* str = strdup(s);
    if (str == NULL)
        fprintf(stderr, "Failed memory allocation in %s at line %d\n", file, line);
    return str;
}

char* _safeStrAppend(const char* file, int line, char* x, const char* y)
{
    size_t len1 = strlen(x);
    size_t len2 = strlen(y);
    x = (char*) safeRealloc(x, (len1 + len2 + 1) * sizeof(char));
    return (char*) memcpy((void*) &x[len1], (void*) y, (len2 + 1));
}


/************************************************************************************/
/*  Safe file open functions                                                        */
/************************************************************************************/
gzFile _safeGzOpen(const char* file, int line, char* filename, char* mode)
{
    gzFile fp = gzopen(filename, mode);
    if (fp == NULL)
        fprintf(stderr, "Unable to open the GZ file. Error in %s at line %d\n", file, line);
    return fp;
}

FILE* _safeFOpen(const char* file, int line, char* filename, char* mode)
{
    FILE* fp = fopen(filename, mode);
    if (fp == NULL)
        fprintf(stderr, "Unable to open the file. Error in %s at line %d\n", file, line);
    return fp;
}

/************************************************************************************/
/*  String shortener                                                                */
/************************************************************************************/
char* shortName(char* name)
{
    char* p = strpbrk(name," \t");
    if (p != 0)
        *p = 0;
    return name;
}
