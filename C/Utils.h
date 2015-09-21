#ifndef UTILS_H_INCLUDED
#define UTILS_H_INCLUDED

#include <stdio.h>
#include <zlib.h>


/************************************************************************************/
/*  Error macros                                                                    */
/************************************************************************************/
#define DEBUG(FORMAT, ARGS...) \
    do { \
    fprintf(stderr, "[%s:%d]:", __FILE__, __LINE__); \
    fprintf(stderr, FORMAT, ARGS); \
    fputc('\n', stderr); \
    } while(0)

#define ERROR(MESSAGE, ENDING) \
    do { \
    DEBUG("%s", MESSAGE); \
    return ENDING; \
    } while(0)


/************************************************************************************/
/*  Safe memory allocation macros                                                   */
/************************************************************************************/
#define safeMalloc(size) _safeMalloc(__FILE__, __LINE__, size)
#define safeCalloc(number, size) _safeCalloc(__FILE__, __LINE__, number, size)
#define safeRealloc(ptr, size) _safeRealloc(__FILE__,__LINE__, ptr, size)
#define safeStrdup(s) _safeStrdup(__FILE__, __LINE__, s)
#define safeStrAppend(x,y) _safeStrAppend(__FILE__, __LINE__, x, y)
#define safeGzOpen(filename, mode) _safeGzOpen(__FILE__, __LINE__, filename, mode)
#define safeFOpen(filename, mode) _safeFOpen(__FILE__, __LINE__, filename, mode)



/************************************************************************************/
/*  Prototypes                                                                      */
/************************************************************************************/
void* _safeMalloc(const char* file, int line, size_t size);
void* _safeCalloc(const char* file, int line, size_t number, size_t size);
void* _safeRealloc(const char* file, int line, void* ptr, size_t size);
char* _safeStrdup(const char* file, int line, char* s);
char* _safeStrAppend(const char* file, int line, char* x, const char* y);
gzFile _safeGzOpen(const char* file, int line, char* filename, char* mode);
FILE* _safeFOpen(const char* file, int line, char* filename, char* mode);
char* shortName(char* name);

#endif // UTILS_H_INCLUDED
