source("BaseFunctions/DataProcessing.R")


DefineFilteType <- function(file.processed) {
  name.columns <- names(file.processed)
  number.columns <- length(name.columns)
  is.tab.separated <- gsub("^(Contents).*", "\\1", name.columns[1])
  if(is.tab.separated == 'Contents'){
    file.identifier <- is.tab.separated
  } else{
    file.identifier <- paste0(paste(name.columns, collapse = ""), "-", number.columns)
  }
  type.file <- switch (
    file.identifier,
    "V1V2-2" = list(skip = 5, header = F, select = c("V1")),
    "TIEMPOCH1-2" = list(select = c("CH1")),
    "TIEMPOCH1V3-3" = list(select = c("CH1")),
    "TIEMPOCH1CH2-3" = list(select = c("CH1")),
    "V1V2V3-3" = list(skip = 5, header = F, select = c("V1")),
    "V1V2V3V4V5V6V7V8V9V10V11V12V13V14V15V16V17V18V19V20V21V22V23-23" = list(skip = 3, select = c("V21")),
    "V1V2V3V4V5V6V7V8V9V10V11V12V13V14V15V16V17V18V19V20V21V22V23V24V25-25" = list(skip = 3, select = 21),
    'Contents' = list( select = 8, sep = "\t", quote = "")
  )
  return(type.file)
}

AnimalDataSetProcess <- function(main.dataset, group.selected, keep.raw = FALSE, determine.obs = NA, multiple.sample = F) {
  group.dataset <- main.dataset[group == group.selected, .(group.factor, signal, file, n.obs)]
  if(multiple.sample) {
    group.dataset.seg <- map(
      group.dataset[n.obs >= determine.obs, unique(file)],
      function(x) BinningSignal(group.dataset[file == x, signal], max.lecture = 900, size.bin = determine.obs)
    )
    names(group.dataset.seg) <- group.dataset[n.obs >= determine.obs, unique(file)]
    group.dataset.seg <- group.dataset.seg %>%
      map(bind_rows) %>%
      bind_rows(., .id = 'file')
      setDT(group.dataset.seg)
      group.dataset.seg <- melt(group.dataset.seg, id.vars = "file")
      group.dataset.seg.fft <- group.dataset.seg[, calcFFT(value), .(file, variable)]
      group.dataset.seg.fft <- merge(group.dataset.seg.fft, unique(group.dataset[, .(file, group.factor)]))
      group.dataset.seg.fft[, id := sprintf("f%06d", seq_len(.N)), .(file, variable)]
      #group.dataset.seg.fft <- dcast(group.dataset.seg.fft, file + group.factor + variable ~ id, value.var = "ps")
      group.dataset.fft <- group.dataset.seg.fft[frecuencia < 40]
  } else {
    if(is.na(determine.obs)) {
      determine.obs <- GetMode(group.dataset$n.obs)
      group.dataset <- group.dataset[n.obs >= determine.obs]
      group.dataset <- group.dataset[, .SD[1:determine.obs], file]
      group.dataset[, n.obs := NULL]
      group.dataset.fft <- group.dataset[, calcFFT(signal), .(file, group.factor)]
      group.dataset.fft <- group.dataset.fft[frecuencia < 40]
      group.dataset.fft[, id := sprintf("f_%06d", rowid(group.factor)), file]
    }
  }
  if(keep.raw) {
    return(list(
      group.dataset.raw = group.dataset[],
      group.dataset.fft = group.dataset.fft[]
    ))
  }
  return(group.dataset.fft[])
}

AnimalTagTestTraining <- function(dataset.input, factor.column = "group.factor", multiple.sample = F) {
  if(multiple.sample) {
    rearrange.formula <-  paste("file + group + variable +", factor.column, "~ id")
  } else {
    rearrange.formula <-  paste("file + group +", factor.column, "~ id")
  }
  set.seed(13)
  dataset.input.tagged <- dataset.input[!is.na(get(factor.column))] %>%
    select(file) %>%
    distinct(file) %>%
    rowwise() %>%
    mutate(group = sample(
      c("train", "test"),
      1,
      replace = TRUE,
      prob = c(0.8, 0.2)
    ))
  dataset.input <- merge(dataset.input, dataset.input.tagged)
  dataset.input.t <- data.table::dcast(
    dataset.input[!is.na(get(factor.column))], rearrange.formula, value.var = 'ps'
  )
  return(dataset.input.t[])
}
