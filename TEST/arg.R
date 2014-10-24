#!/usr/bin/env Rscript

suppressPackageStartupMessages(library("optparse"))


option_list <- list (
	make_option(c("-i", "--input"), type="character", help="Input Data Directory"),
	make_option(c("-o", "--output"), type="character", help="Output Directory"),
	make_option(c("-n", "--neg"), type="character", help="Negative Control"),
	make_option(c("-p", "--pos"), type="character", help="Positive Control"),
	make_option(c("-f", "--feat"), type="character", help="Feature to analyze"),
	make_option(c("-t", "--thres"), type="integer", help="Negative Control", default=NA),
	make_option(c("-m", "--median"), action="store_true",help="Median pooling of data"),
	make_option(c("-s", "--svm"), action="store_true", help="SVM processing of data")
	)


opt <- parse_args(OptionParser(option_list=option_list))
print(opt)

