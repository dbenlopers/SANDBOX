#!/bin/bash

pdflatex CV_short.tex
pdflatex CV_Long.tex

rm *.aux
rm *.out
rm *.log
