#' Calculate Fourier Transformation
#'
#' Get the fourier transformation for a signal vector. The functions allows to normalize the signal dividing by
#' the number of values. It can return only the seed power or also the position vector
#'
#' @param signal.vector Vector with signal data
#' @param normalize Allows to normalize the coefficients
#' @param only.ps Define if the function returns only the seed power or a dataset with poer and frecuencies
#'
#' @return A seed power vector or a frequency/power dataframe
#' @export
#'
#' @examples \dontrun{calcFFT(signal.vector, normalize = TRUE, only.ps = FALSE)}
calcFFT <- function(signal.vector, normalize = TRUE, only.ps = FALSE) {
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
    return(data.table::data.table(frecuencia=freqbin, ps=ps))
  }
}

#' BinningSignal Signal segmentation
#'
#' Segmentation of signal by bin. It allows to split and group same segments of the signals to compare segments
#'
#' @param signal.vector Vector with the fourier trasnform signal to segmentate
#' @param max.lecture Maximum value of the signal
#' @param size.bin Size of he bin to be segmented
#'
#' @return Signal with splitted values
#' @export
#'
#' @examples \dontrun{BinningSignal(signal.vector, max.lecture = 90, size.bin = 2)}
BinningSignal <- function(signal.vector, max.lecture, size.bin) {
  if(max(abs(signal.vector)) < max.lecture) {
    signal.splited <- split(signal.vector, cut(seq_along(signal.vector), length(signal.vector) %/% size.bin))
    signal.splited <- lapply(
      signal.splited, function(x) if (length(x) >= size.bin){
        x[1:size.bin]
      }else{
        NULL
      }
    )
    signal.splited <- purrr::compact(signal.splited)
    names(signal.splited) <- paste0("l",1:length(signal.splited))
    return(signal.splited)
  }
  signal.splited <- split(signal.vector, rleid(abs(signal.vector) > max.lecture))
  signal.splited <- sapply(
    signal.splited,
    function(x) if(length(x) > size.bin & abs(x[1]) < max.lecture){
      x
    } else {
      NULL
    })
  signal.splited <- purrr::compact(signal.splited)
  signal.splited <- sapply(signal.splited, function(x) if(length(x)%/%size.bin > 1){
    split(x,1:length(x)%/%size.bin)
  } else{
    x
  })
  signal.splited.fixed <- list()
  for(i in 1:length(signal.splited)){
    if(is.list(signal.splited[[i]])){
      for(j in 1:length(signal.splited[[i]])){
        signal.splited.fixed[[paste0("l-",i,".",j)]] <- signal.splited[[i]][[j]]
      }
    }else{
      signal.splited.fixed[[paste0("l-",i)]] <- signal.splited[[i]]
    }
  }
  signal.splited <- lapply(signal.splited.fixed, function(x) if(length(x) >= size.bin){
    x[1:size.bin]
  }else{
    NULL
  })
  signal.splited <- purrr::compact(signal.splited)
  names(signal.splited) <- paste0("l",1:length(signal.splited))
  return(signal.splited)
}
