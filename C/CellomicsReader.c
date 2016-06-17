#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <assert.h>
#include "zlib.h"
#include "tiffio.h"


#define CHUNK 16384

/* Decompress from file source to file dest until stream ends or EOF.
   inf() returns Z_OK on success, Z_MEM_ERROR if memory could not be
   allocated for processing, Z_DATA_ERROR if the deflate data is
   invalid or incomplete, Z_VERSION_ERROR if the version of zlib.h and
   the version of the library linked do not match, or Z_ERRNO if there
   is an error reading or writing the files. */

int inflateData(FILE* source, unsigned char **_dat, int *_datsize){
    int ret;
    unsigned have;
    z_stream strm;
    unsigned char in[CHUNK];
    unsigned char out[CHUNK];
    size_t datmaxsize;
    unsigned char *dat;
    int datsize;

    // allocate dat with a fixed size ; will be reallocated if necessary
    datmaxsize = CHUNK*2;
    datsize = 0;
    dat = (unsigned char *)malloc(datmaxsize);

    // allocate inflate state
    strm.zalloc = Z_NULL;
    strm.zfree = Z_NULL;
    strm.opaque = Z_NULL;
    strm.avail_in = 0;
    strm.next_in = Z_NULL;
    ret = inflateInit(&strm);
    if (ret != Z_OK) return ret;

    // decompress until deflate stream ends or end of file
    do {
        strm.avail_in = fread(in, 1, CHUNK, source);
        if (ferror(source)) {
            (void)inflateEnd(&strm);
            return Z_ERRNO;
        }
        if (strm.avail_in == 0) break;
        strm.next_in = in;
        // run inflate() on input until output buffer not full
        do {
            strm.avail_out = CHUNK;
            strm.next_out = out;
            ret = inflate(&strm, Z_NO_FLUSH);
            assert(ret != Z_STREAM_ERROR);  // state not clobbered
            switch (ret) {
            case Z_NEED_DICT:
                ret = Z_DATA_ERROR;     // and fall through
            case Z_DATA_ERROR:
            case Z_MEM_ERROR:
    	        (void)inflateEnd(&strm);
    	        return ret;
            }
            have = (CHUNK) - strm.avail_out;
            // reallocate dat if needed
            if (datsize + have >= datmaxsize) {
    	        datmaxsize = datmaxsize +  (CHUNK*2);
    	        dat = realloc(dat, datmaxsize);
          }
          memcpy(&dat[datsize], out, have);
          datsize += have;
        } while (strm.avail_out == 0);

        // done when inflate() says it's done
    } while (ret != Z_STREAM_END);

    // clean up and return
    (void)inflateEnd(&strm);
    *_datsize = datsize;
    *_dat = dat;
    return ret == Z_STREAM_END ? Z_OK : Z_DATA_ERROR;
}

// File based on http://dev.loci.wisc.edu/trac/software/browser/trunk/components/bio-formats/src/loci/formats/in/CellomicsReader.java


int main(){
    FILE *fin;
    int ret;
    unsigned char *dat, *pdat;
    int datsize;
    int width, height, nplanes, nbits, compression;

    fin = fopen("/home/akopp/Pictures/stack-sphero-collagen-9-steps-20 -mic-step-size-4x_E04f00d3.C01", "rb");
    if (!fin) perror("readCellomoics : cannot open file");

    //inflate zlib stream
    fseek(fin, 4, SEEK_SET);
    ret = inflateData(fin, &dat, &datsize);
    if (ret!=Z_OK) perror("readCellomics: cannot decompress stream");
    fclose(fin);

    //read header
    width = *(int *)(&dat[4]);
    height = *(int *)(&dat[8]);
    nplanes = *(short *)(&dat[12]);
    nbits = *(short *)(&dat[14]);
    compression = *(int *)(&dat[16]);
    if (width*height*nplanes*(nbits/8)+52 > datsize) {
        perror("readCellomics: compressed mode is not yed supported");
    }

    printf("%i %i %d %d %i \n", width, height, nplanes, nbits, compression);

    pdat = &dat[52];
    int16_t image[width * height * nplanes];
    int i ;
    for (i=0; i<width*height*nplanes; i++) {
        image[i] = (*((unsigned short *)pdat))/(int16_t)256;
        printf("%d \n", image[i]);
        pdat += sizeof(unsigned short);
    }

    return 0;
}

// int* readCellomics(const char* filename){
//     char *fin;
//     unsigned char *dat, *pdat;
//     int datsize;
//     int i, width, height, nplanes, nbits, compression;
//     int nprotect;
//     int ret;
//
//     // init
//     nprotect = 0;
//
//     // open file
//     fin = fopen(filename, "rb");
//     if (!fin) error("readCellomoics : cannot open file");
//
//     // inflate zlib stream
//     fseek(fin, 4, SEEK_SET);
//     ret = inflateData(fin, &dat, &datsize);
//     if (ret!=Z_OK) error("readCellomics: cannot decompress stream");
//     fclose(fin);
//
//     // read header
//     width = *(int *)(&dat[4]);
//     height = *(int *)(&dat[8]);
//     nplanes = *(short *)(&dat[12]);
//     nbits = *(short *)(&dat[14]);
//     compression = *(int *)(&dat[16]);
//     if (width*height*nplanes*(nbits/8)+52 > datsize) {
//         error("readCellomics: compressed mode is not yed supported");
//     }
//
//     // allocate new image
//
//     int image[width * height * nplanes];
//     nprotect++;
//     if (nplanes == 1) {
//         int dim[2];
//     } else
//         int dim[3];
//     nprotect++;
//
//     dim[0] = width;
//     dim[1] = height;
//     if (nplanes > 1) {
//         dim[1] = nplanes;
//     }
//
//     // copy planes
//     double *dimage[width * height * nplanes];
//     pdat = &dat[52];
//     if (nbits==8){
//         for (i=0; i<width*height*nplanes; i++) {
//             *dimage++ = (*((unsigned char *)pdat))/(double) 1 << 8;
//             pdat += sizeof(unsigned char);
//         }
//     }else if (nbits==16) {
//         for (i=0; i<width*height*nplanes; i++) {
//             *dimage++ = (*((unsigned short *)pdat))/(double) 1 << 16;
//             pdat += sizeof(unsigned short);
//         }
//     } else if (nbits==32) {
//         for (i=0; i<width*height*nplanes; i++) {
//             *dimage++ = (*((unsigned int *)pdat))/(double) 1 << 32;
//             pdat += sizeof(unsigned int);
//     }
//     } else {
//         free(dat);
//         error("readCellomics: unsupported nbits/pixel mode");
//     }
//
//     // free dat
//
//     free(dat);
//
//     return *image;
//
// }
