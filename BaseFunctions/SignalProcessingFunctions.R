library(dplyr)
library(readxl)
library(stringr)
library(data.table)
library(purrr)


calcFFT <- function(signal.vector, normalize=TRUE, only.ps = FALSE) {
  n <- length(signal.vector)
  coeffs <- (fft(signal.vector) / n)[1:(n/2)]
  if(normalize){
    coeffs <- coeffs / n 
  }
  ps <- (Mod(coeffs)) ^ 2
  psMaxNorm <- ps / max(ps)
  frequencies <- (1:length(coeffs) / (n/1000))
  binfreq <- cut(frequencies, length(frequencies) %/% 1)
  ps <- tapply(psMaxNorm, binfreq, mean)
  freqbin <- strsplit(gsub("\\(|\\]", "", levels(binfreq)), ",")
  freqbin <- sapply(freqbin, function(x) mean(as.numeric(x)))
  if (only.ps) {
    return(ps)
  } else {
    return(data.table(frecuencia=freqbin, ps=ps))
  }
}

#Function that reads excel files. size.of.register is the maximum size of rows to read. Default 300,000 = 5 minutes
ReadExcelData <- function(path, size.of.register = 300000, max.lecture = 900) {
  list.files(path, pattern = "*.xlsx", full.names = T) %>%
    set_names(map_chr(., CleanNames)) %>%
    map(~ read_xlsx(path = .,sheet = 1,col_names = "signal", range = cell_cols(1), col_types = "numeric", progress = TRUE)) %>%
    map(na.omit) %>%
    
    #We filter the signal in the range of max.lecture  
    map(~ filter(., signal < max.lecture & signal > (max.lecture*-1))) %>%
    map(~ {if( length(as.matrix(.)) > size.of.register ) slice(.,1:size.of.register) else .})
    #map(~ slice(.,1:size.of.register))
}

BinningSignal <- function(signal.vector, max.lecture, size.bin) {
  if(max(abs(signal.vector)) < max.lecture) {
    if(length(signal.vector) %/% size.bin >= 2) {
      signal.splited <- split(signal.vector, cut(seq_along(signal.vector), length(signal.vector) %/% size.bin))
    }
    else {
      signal.splited <- split(signal.vector, 1)
    }
    signal.splited <- lapply(
      signal.splited, function(x) if (length(x) >= size.bin){
        x[1:size.bin]
      } else{
        NULL
      }
    )
    signal.splited <- compact(signal.splited)
    names(signal.splited) <- paste0("l",1:length(signal.splited))
    return(signal.splited)
  }
  #Filter eliminating values greater than 900 and less than -900 (max.lecture)
  signal.splited <- signal.vector[abs(signal.vector) < max.lecture]
  signal.splited <- split(signal.splited, 1)

  #Removes all null values from signal.splited
  signal.splited <- compact(signal.splited)
  signal.splited <- sapply(signal.splited, function(x) if(length(x)%/%size.bin > 1){
    split(x,1:length(x)%/%size.bin)
  } else{
    x
  })
  signal.splited <- split(signal.splited, 1)

  signal.splited.fixed <- list()
  for(i in 1:length(signal.splited)){
    if(is.list(signal.splited[[i]])){
      for(j in 1:length(signal.splited[[i]])){
        signal.splited.fixed[[paste0("l-",i,".",j)]] <- signal.splited[[i]][[j]]
      }
    } else {
      signal.splited.fixed[[paste0("l-",i)]] <- signal.splited[[i]]
    }
  }

  signal.splited <- lapply(signal.splited.fixed, function(x) if(length(x) >= size.bin){
    x[1:size.bin]
  } else {
    NULL
  })

  #Removes all null values from signal.splited
  signal.splited <- compact(signal.splited)
  names(signal.splited) <- paste0("l",1:length(signal.splited))
  return(signal.splited)
}