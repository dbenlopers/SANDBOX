#CellTCA R script PROJECT

R script for HTS data analyzis in single cell resolution (MAIN.R). Contain a R package like directory named Core

##Dependancies

* limma
* prada
* bioDist
* e1071
* ggplot2
* reshape2
* foreach
* doMC
* data.table
* optparse
* methods.

##OPTIONS 

	-i INPUT, --input=INPUT		Input Directory with data files

	-o OUTPUT, --output=OUTPUT	Output Directory where results will be saved

	-n NEG, --neg=NEG		Negative Control in plate

	-p POS, --pos=POS		Positive Control in plate

	-v TOX,  --tox=TOX		Toxicity Control in plate

	-f FEAT, --feat=FEAT		Feature to analyze (column in data file

	-t THRES, --thres=THRES		Threshold for considering cell as positive : [default NA] 

	-m, --median			Median pooling of data replicats 

	-s, --svm			SVM processing of data replicats

	-j MC, --mc=MC			Number of core to used : [default 1]

	-h, --help			Show this help message and exit

##EXAMPLE 

/CellTCA/MAIN.R -i /inputDir/ -o /outputDir/ -p "positiveSample" -n "negativeSample" -v "toxicSample" -f "Component" -t 80 -m -j 3 


This program use "cheat" for basics multiprocessing, work only on linux

##INPUT

Need data file and plate format file in csv format


##CONTACT

kopp@igbmc.fr


