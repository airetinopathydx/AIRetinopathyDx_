source("BaseFunctions/SignalProcessingFunctions.R")

#Patients (second categorization)
#patients.vector <-  c( 1:40, 42:61, 68:110,
#  35, 38, 42, 43, 44, 45, 47, 49, 51,
#  111, 113, 115, 118, 119, 121, 123, 125, 128, 129,
#  131, 133, 135, 137, 139, 141, 143, 145, 147, 149,
#  151, 153, 155, 157, 159, 161, 163, 165, 167, 171,
#  173, 175, 177, 179, 181, 183, 185, 187, 189, 191,
#  193, 195, 197, 199, 201, 203, 205, 207, 209, 211,
#  213, 215, 217, 219, 221, 223, 225, 227, 229, 231,
#  232, 233, 235, 237, 239, 241, 243, 245, 247, 249,
#  251, 253, 255, 257, 259, 261, 263, 265, 267, 269,
#  271, 273, 275, 277, 279, 281, 283, 285, 287, 289,
#  291, 293, 295, 297, 299, 301, 303, 305, 307, 309,
#  311, 313, 315, 137, 319, 321, 323, 325, 327, 329,
#  331, 333, 335, 337, 339, 341, 343, 345, 347, 349,
#  351, 353, 355, 357, 359, 361, 363, 365, 367, 369,
#  371, 373, 375, 377, 379, 381, 383, 385, 387, 389,
#  391, 393, 395, 397, 399, 401, 403, 405, 407, 409,
#  411, 413, 415, 417, 419, 421, 423, 425, 427, 429,
#  431, 433, 435, 437, 439, 441, 443, 449, 451, 453,
#  457, 459, 461, 463, 467, 471, 473, 475
#)



#Patients (1st Categorization - balanced)
#patients.vector <-  c(1:40, 42:64, 68:77, 80:99, 102:105, 108:109,
#    111, 113, 115, 118, 119, 121, 123, 125, 128, 129, 131,
#    133, 135, 137, 139, 141, 143, 145, 147, 149, 151, 153,
#    155, 157, 159, 161, 163, 165, 167, 169, 171, 173, 175, 193, 197,
#    #177, 179, 181, 183, 185, 187, 189, 191, 193, 195, 197,#
#    199, 201, 203, 205, 207, 209, 211, 213, 215, 217, 219,
#    221, 223, 225, 227, 229, 231, 232, 233, 235, 237, 239, 243, 245, 247, 253, 261,
#    #241, 243, 245, 247, 249, 251, 253, 255, 257, 259, 261,#
#    263, 265, 267, 269, 271, 273, 275, 277, 279, 281, 283, 289, 301, 303,
#    #285, 287, 289, 291, 293, 295, 297, 299, 301, 303,#
#    305, 307, 309, 311, 313, 315, 317, 319, 321, 323, 325, 327,
#    329, 331, 333, 335, 337, 339, 341, 343, 345, 347, 349, 355,
#    #351, 353, 355, 357, 359, 361,
#    365, 367, 375, 377,
#    379, 393, 395, 397, 399, 401, 403, 405, 407, 409, 411, 431,
#    #413, 415, 417, 419, 421, 431, 433, 435, 437, 439, 441,
#    #443, 445, 447, 449, 451,
#    453, 455, 457, 459, 461)
#    #465, 467, 469, 473, 475)#


#Patients (1st Categorization)
patients.vector <-  c(1:40, 42:64, 68:77, 80:99)
    #111, 113, 115, 118, 119, 121, 123, 125, 128, 129, 131,
    #133, 135, 137, 139, 141, 143, 145, 147, 149, 151, 153,
    #155, 157, 159, 161, 163, 165, 167, 169, 171, 173, 175,
    #177, 179, 181, 183, 185, 187, 189, 191, 193, 195, 197,
    #199, 201, 203, 205, 207, 209, 211, 213, 215, 217, 219,
    #221, 223, 225, 227, 229, 231, 232, 233, 235, 237, 239,
    #241, 243, 245, 247, 249, 251, 253, 255, 257, 259, 261,
    #263, 265, 267, 269, 271, 273, 275, 277, 279, 281, 283,
    #285, 287, 289, 291, 293, 295, 297, 299, 301, 303,
    #305, 307, 309, 311, 313, 315, 317, 319, 321, 323, 325, 327,
    #329, 331, 333, 335, 337, 339, 341, 343, 345, 347, 349, 355,
    #351, 353, 355, 357, 359, 361,
    #365, 367, 375, 377,
    #379, 393, 395, 397, 399, 401, 403, 405, 407, 409, 411, 431,
    #413, 415, 417, 419, 421, 431, 433, 435, 437, 439, 441,
    #443, 445, 447, 449, 451,
    #453, 455, 457, 459, 461)
#    465, 467, 469, 473, 475)


#Healthy vs. sick (1st categorization)
health.patients <- list(health = c(3, 35, 38, 44, 45, 46, 49, 50, 51, 53,
 #54, 57, 58, 60, 72, 73, 76, 77, 80, 81,
 54, 57, 58, 60, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 80, 81,
 #84, 85, 104, 105, 110,
 82, 83, 84, 85, 104, 105, 110,
 
 113, 115, 118, 119, 121, 123, 125, 131, 133, 139,
 145, 149, 151, 155, 161, 165, 171, 175, 193, 197,
 199, 233, 235, 243, 245, 247, 253, 261, 263, 281,
 283, 289, 295, 301, 303, 311, 319, 335, 355, 367,
 369, 375, 393, 395, 397, 401, 403, 405, 411, 421,
 431, 453, 455, 457, 459, 461, 463, 463))

#For figure 4f 1st cat
#health.patients <- list(health = c(3, 35, 38, 44, 45, 46, 49, 50, 51, 53,
# 54, 57, 58, 60, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 80, 81, 82, 83,
# 84, 85, 104, 105), prediabetesysmeta = c(13, 14, 26, 29, 32, 33, 36, 39,
# 40, 42, 43, 47, 48, 52, 56, 61, 62), diabetessinrd = c(11, 12, 16, 19,
# 28, 37, 55, 59, 63, 86, 87, 88, 89, 90, 91, 102, 103))

#For figure 4g 1st cat
#health.patients <- list(health = c(3, 35, 38, 44, 45, 46, 49, 50, 51, 53, 54, 57, 58, 60, 68, 69, 70, 71,
# 72, 73, 74, 75, 76, 77, 80, 81, 82, 83, 84, 85, 104, 105), prediabetesysmeta = c(13, 14, 26, 29, 32, 33, 36, 39,
# 40, 42, 43, 47, 48, 52, 56, 61, 62), diabetessinrd = c(11, 12, 16, 19, 28, 37, 55, 59, 63, 86, 87, 88, 89, 90, 91, 102, 103),
# rdnpvariosyrdp = c(5, 6, 7, 8, 9, 10, 15, 17, 18, 20, 21, 22, 23, 24, 25, 27, 30, 31, 34, 92, 93, 96, 97, 98, 99, 106, 107, 108, 109))

SetupHealthStatus <- function(patients.vector, patients.status, alternative.status = NA) {
  try(if(!is.list(health.patients)) stop("To define status a list of patients.status with requeried"))
  #Generates a 1-column list named patient.number containing the numbers defined in patients.vector
  patient.index <- data.table(patient.number = patients.vector)
  if(length(patients.status) == 1){
    status.defined <- names(patients.status)
    patient.index[patient.number %in% patients.status[[status.defined]], health.status := status.defined]
    patient.index[is.na(health.status), health.status := alternative.status]
  } else {
    lapply(names(patients.status), function(x) patient.index[patient.number %in% patients.status[[x]], health.status := x ])
  }
  return(patient.index[])
}

ERGBatchProcess <- function(files.path, max.lecture = 900, size.bin = 30000, remove.registers = 1:5, filtrar.altas = T, keep.raw = F, size.of.register = 300000) {
  #files.data is a list containing the data read by the .xlsx files.
  files.data <- ReadExcelData(files.path, size.of.register, max.lecture)
  if(size.bin >= 300000) {
    files.data.raw <- files.data
  } else {
    #The data are preprocessed with the BinningSignal function.
    files.data.raw <- files.data %>%
      map(function(x) BinningSignal(x$signal, max.lecture, size.bin))
  }
  #Stores in files.data.processed the data preprocessed with the fast Fourier transform.
  files.data.processed <- files.data.raw %>%
    map_df(., ~ map_df(., calcFFT, .id = 'obs'), .id = 'patient')
  #If true filtrar.altas (frequencies >= 40)
  if(filtrar.altas) {
    #Deletes rows containing a column with a frequency greater than or equal to 40.
    files.data.processed <- files.data.processed %>%
    filter(frecuencia < 40)
    #https://www.rdocumentation.org/packages/data.table/versions/1.13.6/topics/setDT
    setDT(files.data.processed)
  }
  #Creates a new column named patient.number and assigns the patient number according to the file name
  files.data.processed[, patient.number := as.numeric(str_extract(patient,"[:digit:]{2,4}"))]
  #Generates a list of patient status (health/disorder) -> patient.number and health.status
  patients.index <- SetupHealthStatus(patients.vector, health.patients, alternative.status = 'disorder')
  #Add the health.status tag to patients according to their patient.number.
  files.data.processed <- merge(files.data.processed, patients.index, by = "patient.number", all.x = T)
  #Removes unlabeled patients and records contained in remove.registers
  files.data.processed <- files.data.processed[!is.na(health.status), .SD[-remove.registers], .(patient, obs)]
  #Create a new column named id and assign a number starting from 1 to infinity with format f_######
  files.data.processed[, id := sprintf("f_%06d", rowid(obs)), patient]
  if(keep.raw) {
    return(list(
      files.data.raw = files.data.raw[],
      files.data.preprocessed = files.data.processed[]
    ))
  }
  #Returns preprocessed data
  return(files.data.processed[])
}

ERGBatchProcessAnimals <- function(files.path, max.lecture = 900, size.bin = 30000, remove.registers = 1:5, filtrar.altas = T, keep.raw = F, size.of.register = 300000) {
  #files.data is a list containing the data read by the .xlsx files.
  files.data <- ReadExcelData(files.path, size.of.register)
  if(size.bin >= 300000) {
    files.data.raw <- files.data
  } else {
    #The data are preprocessed with the BinningSignal function.
    files.data.raw <- files.data %>%
      map(function(x) BinningSignal(x$signal, max.lecture, size.bin))
  }
  #Stores in files.data.processed the data preprocessed with the fast Fourier transform.
  files.data.processed <- files.data.raw %>%
    map_df(., ~ map_df(., calcFFT, .id = 'obs'), .id = 'patient')
  #If true filtrar.altas (frequencies >= 40)
  if(filtrar.altas) {
    #Deletes rows containing a column with a frequency greater than or equal to 40.
    files.data.processed <- files.data.processed %>%
    filter(frecuencia < 40)
    #https://www.rdocumentation.org/packages/data.table/versions/1.13.6/topics/setDT
    setDT(files.data.processed)
  }
  
  #Creates a new column named health.status and assigns the health status according to the file name
  #Only for multiclass CTRL mice vs STZ mice evolution and STZ mice evo
  files.data.processed[, health.status := str_extract(str_extract(patient,"[a-z]{4,6}[0-9]+"),"[a-z]{4,6}")]
  files.data.processed$health.status[which(files.data.processed$health.status == "stzi")] <- "semana4"
  files.data.processed$health.status[which(files.data.processed$health.status == "ctli")] <- "semana4"
  files.data.processed$health.status[which(files.data.processed$health.status == "stzii")] <- "semana6"
  files.data.processed$health.status[which(files.data.processed$health.status == "ctlii")] <- "semana6"
  files.data.processed$health.status[which(files.data.processed$health.status == "stziii")] <- "semana8"
  files.data.processed$health.status[which(files.data.processed$health.status == "ctliii")] <- "semana8"
  files.data.processed$health.status[which(files.data.processed$health.status == "stziv")] <- "semana12"
  files.data.processed$health.status[which(files.data.processed$health.status == "ctliv")] <- "semana12"

  #files.data.processed[, health.status := str_extract(str_extract(patient,"[a-z]{3,4}"),"[a-z]{3,4}")]
  #files.data.processed$health.status[which(files.data.processed$health.status == "stzi")] <- "disorder"
  #files.data.processed$health.status[which(files.data.processed$health.status == "jstz")] <- "disorder"
  #files.data.processed$health.status[which(files.data.processed$health.status == "rpp")] <- "disorder"
  #files.data.processed$health.status[which(files.data.processed$health.status == "enve")] <- "disorder"
  #files.data.processed$health.status[which(files.data.processed$health.status == "obb")] <- "disorder"
  #files.data.processed$health.status[which(files.data.processed$health.status == "hfdx")] <- "disorder"
  #files.data.processed$health.status[which(files.data.processed$health.status == "hfdi")] <- "disorder"
  #files.data.processed$health.status[which(files.data.processed$health.status == "hfdv")] <- "disorder"
  #files.data.processed$health.status[which(files.data.processed$health.status == "ctrl")] <- "health"
  #files.data.processed$health.status[which(files.data.processed$health.status == "jctr")] <- "health"
  #files.data.processed$health.status[which(files.data.processed$health.status == "ctlv")] <- "health"
  #files.data.processed$health.status[which(files.data.processed$health.status == "ctlx")] <- "health"
  #files.data.processed$health.status[which(files.data.processed$health.status == "ctli")] <- "health"
  #files.data.processed$health.status[which(files.data.processed$health.status == "cont")] <- "health"
  #files.data.processed$health.status[which(files.data.processed$health.status == "lean")] <- "health"
  
  #Removes unlabeled patients and records contained in remove.registers
  files.data.processed <- files.data.processed[, .SD[-remove.registers], .(patient, obs)]
  #Create a new column named id and assign a number starting from 1 to infinity with format f_######
  files.data.processed[, id := sprintf("f_%06d", rowid(obs)), patient]
  if(keep.raw) {
    return(list(
      files.data.raw = files.data.raw[],
      files.data.preprocessed = files.data.processed[]
    ))
  }
  #Returns preprocessed data
  return(files.data.processed[])
}

TagTestTrainingAnimals <- function(dataset.input, factor.column = "health.status", trainSet = 0.8, testSet = 0.2, seed = 13) {
  rearrange.formula <-  paste("patient + obs +", factor.column, "+ group ~ id")
  set.seed(seed)
  dataset.input.tagged <- dataset.input[!is.na(patient) & !is.na(get(factor.column))] %>%
    select(patient) %>%
    distinct(patient) %>%
    rowwise() %>%
    mutate(group = sample(
      c("train", "test"),
      1,
      replace = TRUE,
      prob = c(trainSet, testSet)
    ))
  #The row "id" is converted into columns with the value of "ps".
  dataset.input <- merge(dataset.input, dataset.input.tagged)
  dataset.input.t <- data.table::dcast(
    dataset.input[!is.na(get(factor.column))], rearrange.formula, value.var = 'ps'
  )
  return(dataset.input.t)
}

TagTestTraining <- function(dataset.input, factor.column = "health.status", trainSet = 0.8, testSet = 0.2, seed = 13) {
  rearrange.formula <-  paste("patient + patient.number + obs +", factor.column, "+ group ~ id")
  set.seed(seed)
  dataset.input.tagged <- dataset.input[!is.na(patient.number) & !is.na(get(factor.column))] %>%
    select(patient.number) %>%
    distinct(patient.number) %>%
    rowwise() %>%
    mutate(group = sample(
      c("train", "test"),
      1,
      replace = TRUE,
      prob = c(trainSet, testSet)
    ))
  #The row "id" is converted into columns with the value of "ps".
  dataset.input <- merge(dataset.input, dataset.input.tagged)
  dataset.input.t <- data.table::dcast(
    dataset.input[!is.na(get(factor.column))], rearrange.formula, value.var = 'ps'
  )
  return(dataset.input.t)
}

GetMode <- function(v) {
  uniqv <- unique(v)
  uniqv[which.max(tabulate(match(v, uniqv)))]
}

ERGBatchProcessPrediction <- function(files.path, max.lecture = 900, size.bin = 30000, remove.registers = 1:5, filtrar.altas = T, keep.raw = F, size.of.register = 300000) {
  rearrange.formula <-  "patient + patient.number + obs  ~ id"
  #files.data is a list containing the data read by the .xlsx files.
  files.data <- ReadExcelData(files.path, size.of.register, max.lecture)
  if(size.bin >= 300000) {
    files.data.raw <- files.data
  } else {
    #The data are preprocessed with the BinningSignal function.
    files.data.raw <- files.data %>%
      map(function(x) BinningSignal(x$signal, max.lecture, size.bin))
  }
  #Stores in files.data.processed the data preprocessed with the fast Fourier transform.
  files.data.processed <- files.data.raw %>%
    map_df(., ~ map_df(., calcFFT, .id = 'obs'), .id = 'patient')
  #If true filtrar.altas (frequencies >= 40)
  if(filtrar.altas) {
    #Deletes rows containing a column with a frequency greater than or equal to 40.
    files.data.processed <- files.data.processed %>%
      filter(frecuencia < 40)
    #https://www.rdocumentation.org/packages/data.table/versions/1.13.6/topics/setDT
    setDT(files.data.processed)
  }
  #Creates a new column named patient.number and assigns the patient number according to the file name.
  files.data.processed[, patient.number := as.numeric(str_extract(patient,"[:digit:]{2,4}"))]

  #Removes patients with no records contained in remove.registers
  files.data.processed <- files.data.processed[, .SD[-remove.registers], .(patient, obs)]
  #Create a new column named id and assign a number starting from 1 to infinity with format f_######
  files.data.processed[, id := sprintf("f_%06d", rowid(obs)), patient]
  files.data.processed.t <- data.table::dcast(
    files.data.processed, rearrange.formula, value.var = 'ps'
  )
  #Returns preprocessed data
  return(files.data.processed.t[])
}

PrepareDataForPrediction <- function(files.path, max.lecture = 900, size.bin = 30000, remove.registers = 1:5, filtrar.altas = T) {
  rearrange.formula <-  "patient + patient.number + obs  ~ id"
  files.data <- ReadExcelData(files.path)
  if(size.bin >= 300000) {
    files.data.raw <- files.data
  } else {
    files.data.raw <- files.data %>%
      map(function(x) BinningSignal(x$signal, max.lecture, size.bin))
  }
  files.data.processed <- files.data.raw %>%
    map_df(., ~ map_df(., calcFFT, .id = 'obs'), .id = 'patient')
  if(filtrar.altas) {
    files.data.processed <- files.data.processed %>%
    filter(frecuencia < 40)
    setDT(files.data.processed)
  }
  #Creates a new column named patient.number and assigns the patient number according to the file name
  files.data.processed[, patient.number := as.numeric(str_extract(patient,"[:digit:]{2,3}"))]

  #Removes records contained in remove.registers
  files.data.processed.smite <- files.data.processed[, .SD[-remove.registers], .(patient, obs)]

  #Create a new column named id and assign a number starting from 1 to infinity with format f_######
  files.data.processed.smite[, id := sprintf("f_%06d", rowid(obs)), patient]
  files.data.processed.t <- data.table::dcast(
    files.data.processed.smite, rearrange.formula, value.var = 'ps'
  )
  return(files.data.processed.t[])
}