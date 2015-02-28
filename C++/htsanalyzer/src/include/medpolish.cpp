#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <vector>
#include "medpolish.h"
#include "stat.h"

/*
    Function to perform median polish on matrix data
*/


/*******************************************************************************
 **
 ** double sum_abs(std::vector<std::vector<double> > &z, int rows, int cols)
 **
 ** std::vector<std::vector<double> > &z - matrix of doubles
 ** int rows - dimension of matrix
 ** int cols - dimension of matrix
 **
 ** returns the sum of the absolute values of elements of the matrix *z
 **
 ******************************************************************************/
static double sum_abs(std::vector<std::vector<double> > &z, int rows, int cols){
 
  int i, j;
  double sum = 0.0;

  for (i=0; i < rows; i++)
    for (j=0; j < cols; j++)
      sum+=fabs(z[i][j]);

  return sum;
}

/********************************************************************************
 **
 ** void get_row_median(std::vector<std::vector<double> > &z, std::vector<double> &rdelta, int rows, int cols)
 **
 ** std::vector<std::vector<double> > &z - matrix of dimension  rows*cols
 ** std::vector<double> &rdelta - on output will contain row medians (vector of length rows)
 ** int rows, cols - dimesion of matrix
 **
 ** get the row medians of a matrix 
 **
 ********************************************************************************/

static void get_row_median(std::vector<std::vector<double> > &z, std::vector<double> &rdelta, int rows, int cols){
   
  int i,j;
  std::vector<double> buffer;

  for (i = 0; i < rows; i++){ 
    for (j = 0; j < cols; j++){
      buffer[j] = z[i][j];
    }
    rdelta[i] = stat::median(buffer);
  }
}

/********************************************************************************
 **
 ** void get_col_median(std::vector<std::vector<double> > &z, std::vector<double> &cdelta, int rows, int cols)
 **
 ** std::vector<std::vector<double> > &z - matrix of dimension  rows*cols
 ** std::vector<double> &cdelta - on output will contain col medians (vector of length cols)
 ** int rows, cols - dimesion of matrix
 **
 ** get the col medians of a matrix 
 **
 ********************************************************************************/

static void get_col_median(std::vector<std::vector<double> > &z, std::vector<double> &cdelta, int rows, int cols){
  
  int i,j;
  std::vector<double> buffer;
  for (j = 0; j < cols; j++){
    for (i = 0; i < rows; i++){  
      buffer[i] = z[i][j];
    }
    cdelta[i] = stat::median(buffer);
  }
}

/***********************************************************************************
 **
 ** void subtract_by_row(std::vector<std::vector<double> > &z, std::vector<double> &rdelta, int rows, int cols)
 ** 
 ** std::vector<std::vector<double> > &z - matrix of dimension rows by cols
 ** std::vector<double> &rdelta - vector of length rows
 ** int rows, cols dimensions of matrix
 **
 ** subtract the elements of &rdelta off each row of &z
 **
 ***********************************************************************************/

static void subtract_by_row(std::vector<std::vector<double> > &z, std::vector<double> &rdelta, int rows, int cols){
  
  int i,j;

  for (i = 0; i < rows; i++){
    for (j = 0; j < cols; j++){
      z[i][j]-= rdelta[i];
    }
  }
}


/***********************************************************************************
 **
 ** void subtract_by_col(std::vector<std::vector<double> > &z, std::vector<double> &cdelta, int rows, int cols)
 ** 
 ** std::vector<std::vector<double> > &z - matrix of dimension rows by cols
 ** std::vector<double> &cdelta - vector of length rows
 ** int rows, cols dimensions of matrix
 **
 ** subtract the elements of &cdelta off each col of &z
 **
 ***********************************************************************************/

static void subtract_by_col(std::vector<std::vector<double> > &z, std::vector<double> &cdelta, int rows, int cols){
  
  int i,j;
  for (j = 0; j < cols; j++){
    for (i = 0; i < rows; i++){
      z[i][j]-= cdelta[j];
    }
  }

}

/***********************************************************************************
 **
 ** void rmod(std::vector<double> &r, std::vector<double> &rdelta, int rows)
 ** 
 ** std::vector<double> &r - vector of length rows
 ** std::vector<double> &rdelta - vector of length rows
 ** int rows, cols dimensions of matrix
 **
 ** add elementwise *rdelta to *r
 **
 ***********************************************************************************/


static void rmod(std::vector<double> &r, std::vector<double> &rdelta, int rows){
  int i;

  for (i = 0; i < rows; i++){
    r[i]= r[i] + rdelta[i];
  }
}

/***********************************************************************************
 **
 ** void cmod(double *c, double *cdelta, int cols)
 ** 
 ** double *c - vector of length rows
 ** double *cdelta - vector of length rows
 ** int cols length of vector
 **
 ** add elementwise *cdelta to *c
 **
 ***********************************************************************************/

static void cmod(std::vector<double> &c, std::vector<double> &cdelta, int cols){
  int j;

  for (j = 0; j < cols; j++){
    c[j]= c[j] + cdelta[j];
  }
}





void median_polish_fit(std::vector<std::vector<double> > &z, int rows, int cols, std::vector<double> &r, std::vector<double> &c, double &t){
 

  int i,j,iter;
  int maxiter = 10;
  double eps=0.01;
  double oldsum = 0.0,newsum = 0.0;
  double delta;
  std::vector<double> rdelta ;
  std::vector<double> cdelta ;


  t = 0.0;

  for (iter = 1; iter <= maxiter; iter++){
    get_row_median(z,rdelta,rows,cols);
    subtract_by_row(z,rdelta,rows,cols);
    rmod(r,rdelta,rows);
    delta = stat::median(c);
    for (j = 0; j < cols; j++){
      c[j] = c[j] - delta;
    }
    t = t + delta;
    get_col_median(z,cdelta,rows,cols);
    subtract_by_col(z,cdelta,rows,cols);
    cmod(c,cdelta,cols);
    delta = stat::median(r);
    for (i =0; i < rows; i ++){
      r[i] = r[i] - delta;
    }
    t = t+delta;
    newsum = sum_abs(z,rows,cols);
    if (newsum == 0.0 || fabs(1.0 - oldsum/newsum) < eps)
      break;
    oldsum = newsum;
  }

}


/*! \brief Compute medianpolish  
 * @param data a matrix containing data stored column-wise stored in rows*cols length of memory
 * @param rows the number of rows in the matrix 
 * @param cols the number of columns in the matrix
 * @param results pre-allocated space to store output log2 averages. Should be of length cols
 * @param resultsSE pre-allocated space to store SE of log2 averages. Should be of length cols. Note that this is just NA values
 */
 
void MedianPolish(std::vector<std::vector<double> > &data, int rows, int cols, std::vector<double> &results){

  int j;
  double t;
  std::vector<double> r ;
  std::vector<double> c ;
  
  median_polish_fit(data, rows, cols, r, c, t);
  
  for (j=0; j < cols; j++){
    results[j] =  t + c[j]; 
  }

}


