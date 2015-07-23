CsvDir = '/home/arnaud/Desktop/Schneider/Plaque du 02072015/'
filelist <- dir(pattern = "ratio_cleaned.csv", path = CsvDir, ignore.case = TRUE)

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
  
  res <- t(sapply(by(df$ratio_taget_I, list(df$Well), cut, breaks = seq(0,3, by = 0.1)), table))
  file.path <- paste(CsvDir,paste('ratio_target_I_Repartition', file, sep = '_'), sep = "/")
  print(file.path)
  write.csv(x = res, file = file.path)
  
  res <- t(sapply(by(df$ratio_taget_II, list(df$Well), cut, breaks = seq(0,3, by = 0.1)), table))
  file.path <- paste(CsvDir,paste('ratio_target_II_Repartition', file, sep = '_'), sep = "/")
  print(file.path)
  write.csv(x = res, file = file.path)
  
}
