CsvDir = '/home/arnaud/Desktop/Anne/valerieschreiber/'
filelist <- dir(pattern = ".csv", path = CsvDir, ignore.case = TRUE)

for (file in filelist) {
  file.path <- paste(CsvDir,file, sep = "/")
  df <- read.csv(file.path)
  
#   res <- t(sapply(by(df$SpotMeanArea, list(df$Well), cut, breaks = c(0,2,4,6,8,10,12,14,16,18,20,25,30,35,40,45,50,55,60,100,200)), table))
#   file.path <- paste(CsvDir,paste('SpotMeanArea_repartition', file, sep = ''), sep = "/")
#   print(file.path)
#   write.csv(x = res, file = file.path) 
  
#   res <- t(sapply(by(df$SpotMeanAreaCh2, list(df$Well), cut, breaks = c(0,2,4,6,8,10,12,14,16,18,20,25,30,35,40,45,50,55,60,100,200)), table))
#   file.path <- paste(CsvDir,paste('SpotMeanArea_Repartition_Ch2', file, sep = ''), sep = "/")
#   print(file.path)
#   write.csv(x = res, file = file.path) 
#   
#   res <- t(sapply(by(df$SpotCountCh2, list(df$Well), cut, breaks = c(0,2,4,6,8,10,12,14,16,18,20,25,30,35,40,45,50,55,60,100,200)), table))
#   file.path <- paste(CsvDir,paste('SpotCount_Repartition_Ch2', file, sep = ''), sep = "/")
#   print(file.path)
#   write.csv(x = res, file = file.path)
  
  res <- t(sapply(by(df$CellNucCountCh1, list(df$Well), cut, breaks = c(0,1,2,100)), table))
  file.path <- paste(CsvDir,paste('CellNucCountCh1_Repartition', file, sep = '_'), sep = "/")
  print(file.path)
  write.csv(x = res, file = file.path)
  
  res <- t(sapply(by(df$CellMicroNucCountCh1, list(df$Well), cut, breaks = c(-1,0,1,2,100)), table))
  file.path <- paste(CsvDir,paste('CellMicroNucCountCh1_Repartition', file, sep = '_'), sep = "/")
  print(file.path)
  write.csv(x = res, file = file.path)
  
}
