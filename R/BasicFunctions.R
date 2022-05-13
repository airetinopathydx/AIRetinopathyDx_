.CreateConnection <- function(db.user = NULL, db.host = NULL, db.port = 3306, db.name = NULL, db.password = NULL) {
  if(is.null(db.user) & Sys.getenv("DB_USERNAME") != "") {
    db.user <- Sys.getenv("DB_USERNAME")
  }
  if(is.null(db.host) & Sys.getenv("DB_HOST") != "") {
    db.host <- Sys.getenv("DB_HOST")
  }
  if(is.null(db.password) & Sys.getenv("DB_PASSWORD") != "") {
    db.password <- Sys.getenv("DB_PASSWORD")
  }
  if(is.null(db.name) & Sys.getenv("DB_NAME") != "") {
    db.name <- Sys.getenv("DB_NAME")
  }
  db.con <- DBI::dbConnect(
    RMySQL::MySQL(), user = db.user, password = db.password, dbname = db.name, host = db.host, port = db.port
  )
  return(db.con)
}

.GetMode <- function(numeric.vector) {
  uniq.vector <- unique(numeric.vector)
  uniq.vector[which.max(tabulate(match(numeric.vector, uniq.vector)))]
}

#' Clean file names
#'
#'Allows to clean not valid characters from file names in order to
#'denominate each readed dataset. In most of the cases the files have
#'the patient name of the dataset.
#'
#' @param string.name.file file name to clean
#'
#' @return string with the name of the file without special characters
#' @export
#' @importFrom magrittr "%>%"
#' @examples
#' \dontrun{CleanNames('archivo de excel.xlsx')}
CleanNames <- function(string.name.file){
  string.name.file %>%
    stringr::str_replace("^.*/", "") %>%
    stringr::str_replace(".xlsx", "") %>%
    stringr::str_replace_all(" ","") %>%
    stringr::str_to_lower()
}

#' Normalize File names
#'
#' Some File names can have spaces and spetial character which could
#' generate some troubles in the readin process. This functions allow us to
#' quickly remove special character an errors
#'
#' Be carefull with the changes in local files.
#'
#' @param path.files Path to the files wich will be renaming
#' @param file.pattern Pattern to filter the files to be processed in the provided path
#'
#' @return Change the filenames of local files
#' @export
#'
#' @examples
#' \dontrun{NormalizeLocalFiles('Data/', ".csv")}
NormalizeLocalFiles <- function(path.files, file.pattern = ".csv") {
  files.name <- list.files(path.files, pattern = file.pattern)
  clean.names <- CleanNames(files.name)
  rename.result <- file.rename(file.path(path.files, files.name), file.path(path.files, clean.names))
  if(any(rename.result) == FALSE) {
    stop("Some files where no renamed")
  } else{
    message("Succesfully renaming")
  }
}

#' Read patients CSV data
#'
#' Read csv file with size defined by size.of.register argument and remove NA values.
#' The File needs to be in specific format, one column with the data.
#' The default size fo register is 300000 rows, it could be larger but
#' is the default size of the capture.
#' To avoid errors in the name field it's recommended to Nomalize the local file names.
#'
#' @seealso \code{\link{NormalizeLocalFiles}}
#'
#' @param path Path to the csv file
#' @param size.of.register Maximum number of rows to read from file
#'
#' @return DataFrame/Tibble with file information.
#' @export
#'
#' @examples
#' \dontrun{ReadPatientData("~/patientdata.csv", size.of.register = 300000)}
ReadPatientData <- function(path.files, size.of.register = 300000, file.pattern = "*.csv") {
  patient.registers <- list.files(path.files, pattern = file.pattern) %>%
    purrr::set_names(~stringr::str_replace(., ".csv", "")) %>%
    purrr::map(~data.table::fread(file.path(path.files, .), select = 1, na.strings = c(""))) %>%
    purrr::compact() %>%
    purrr::walk(~suppressWarnings(.[, V1 := as.numeric(V1)])) %>%
    purrr::map(na.omit) %>%
    purrr::map(~slice(., 1:size.of.register)) %>%
    purrr::map(~mutate(., index = row_number())) %>%
    dplyr::bind_rows(.id = "filename") %>%
    rename(register = V1)
}

#' Insert Training Patient Data in Database
#'
#' This function will insert a dataframe in the database. If the table dosen't
#' exist it will create it. If the overwrite.info is set to TRUE it will replace the table.
#' With the append.info = TRUE it will add the info to the table.
#'
#' It's recomended to use ENVIROMENT variables set in the .Renviron file,
#' the variables accepted are DB_NAME as base name, DB_TABLE as table name,
#' DB_USERNAME, DB_HOST and DB_PASSWORD
#'
#' @param patient.registers Dataframe patients to insert in database
#' @param db.user Database user, if null will use DB_USERNAME enviroment variable
#' @param db.host Database address if null will use DB_HOST enviroment variable
#' @param db.port Database port
#' @param db.name Database name if null will use DB_NAME enviroment variable
#' @param db.table Database Table if null will use DB_TABLE enviroment variable
#' @param db.password Database Password if null will use DB_PASSWORD enviroment variable
#' @param overwrite.info Allows to overwrite previous table insertions
#' @param append.info Allows to append data to exist table
#'
#' @return TRUE invisibly if the insertion si succesfull and ERROR if it fails
#' @export
#'
#' @examples
#' \dontrun{InsertPatientsToDB(
#'   patient.registers,
#'   db.user = "user",
#'   db.host = "127.0.0.1",
#'   db.name = "erg_db",
#'   db.table = "patients",
#'   db.password = "secret"
#' )}
InsertPatientsToDB <- function(patient.registers, db.table = NULL, overwrite.info = FALSE, append.info = FALSE, ...) {
  if(is.null(db.table) & Sys.getenv("DB_TABLE") != "") {
    db.table <- Sys.getenv("DB_TABLE")
  }
  db.con <- .CreateConnection(...)
  DBI::dbWriteTable(
    conn = db.con, name = db.table, value = patient.registers, ovewrite = overwrite.info, append = append.info, row.names = FALSE
  )
  DBI::dbDisconnect(db.con)
}


#' Donwload raw patientes registers
#'
#' This function download the raw patients registers from MySQL database
#' This dataset will download raw dataset registers
#'
#' @param group.patients This argument is mandatory so it will determinate which experimental group will be downloaded
#' @param patient.select You can select the patient to download with the patient ID number
#' @param db.user Database user, if null will use DB_USERNAME enviroment variable
#' @param db.host Database address if null will use DB_HOST enviroment variable
#' @param db.port Database port
#' @param db.name Database name if null will use DB_NAME enviroment variable
#' @param db.table Database Table if null will use DB_TABLE enviroment variable
#' @param db.password Database Password if null will use DB_PASSWORD enviroment variable
#'
#' @return data.table patient data
#' @export
#' @examples
#' \dontrun{GetRawPatientsData(
#'   group.patients = "luz",
#'   db.user = "test_user",
#'   db.password = "test_password",
#'   db.host = "127.0.0.1",
#'   db.name = "erg"
#'   )}
#'
#' \dontrun{GetRawPatientsData(
#'   group.patients = "luz",
#'   patient.select = 51
#'   db.user = "test_user",
#'   db.password = "test_password",
#'   db.host = "127.0.0.1",
#'   db.name = "erg"
#'   )}
GetRawPatientsData <- function(group.patients, patient.select = NULL, ...) {
  if(length(group.patients) != 1 & !group.patients %in% c("luz", "obscuridad")){
    stop("No experimental group")
  }
  db.con <- .CreateConnection(...)
  patient.data <- dplyr::tbl(db.con, glue::glue("pacientes_{group.patients}"))
  if(is.null(patient.select)) {
    patient.data <- patient.data %>%
      dplyr::collect()
  } else {
    patient.data <- patient.data %>%
      dplyr::filter(patient_id = patient.select) %>%
      dplyr::collect()
  }
  DBI::dbDisconnect(db.con)
  data.table::setDT(patient.data)
  data.table::setkey(patient.data, filename)
  return(patient.data[])
}

#' Animal Dataset Process
#'
#' This function process data applying fourirer transformation, filter sample and in case of necesity apply binning to
#' the signal. it requires a dataset with multiple signals.
#' Uses file column, hich have filename, to process the different signals.
#'
#' @param patient.registers Dataset whit multiple files read. The dataset must have the group.factor column, group column,
#' signal, file and n.obs to be processed
#' @param minimal.obs Minimal númber of observations for a sample, use to be 60000 miliseconds to use one minute of register
#' @param multi.sample Use binning to repeat sample from register
#' @param high.frec.filter filter frecuencies over this value, default value 40
#'
#' @return Lis with one or multiple dataset processed
#' @export
#'
#' @examples
#' \dontrun{AnimalDataSetProcess(archvodeexceldata, 'neotomodon', keep.raw = FALSE)}
AnimalDataSetProcess <- function(patient.registers, minimal.obs = NULL, multi.sample = F, high.frec.filter = 40) {
  if(is.null(minimal.obs) & multi.sample) {
    stop("Can NOT create multisample without minimal observation")
  }
  patient.summary <- patient.registers[, .N, filename]
  if(is.null(minimal.obs)) {
    minimal.obs <- .GetMode(patient.summary$N)
  }

  if(sum(minimal.obs >= patient.summary$N) >= nrow(patient.summary)) {
    stop(glue::glue(
      "Minimal observation must be bigger than {min(patient.summary$N)}
      Which corresponds to {patient.summary[order(N)][1, filename]}")
    )
  }
  patient.registers <- patient.registers[patient.summary[N >= minimal.obs, .(filename)],  nomatch = 0]

  if(multi.sample) {
    group.dataset.seg <- purrr::map(
      patient.registers[, unique(filename)],
     ~ BinningSignal(patient.registers[filename == .x, register], max.lecture = 900, size.bin = minimal.obs)
    ) %>%
      purrr::set_names(patient.registers[, unique(filename)])%>%
      purrr::map(bind_rows) %>%
      dplyr::bind_rows(.id = 'filename') %>%
      tidyr::pivot_longer(-filename, names_to = "sample", values_to = "register")
  } else {
    group.dataset.seg <- patient.registers[, .SD[1:minimal.obs], filename] %>%
      dplyr::group_by(filename) %>%
      dplyr::mutate(sample = "l1")
  }
  group.dataset.seg <- group.dataset.seg %>%
    dplyr::group_by(filename, sample) %>%
    dplyr::group_modify(~ calcFFT(.x$register)) %>%
    dplyr::group_by(filename, sample) %>%
    dplyr::mutate(id = sprintf("f%06d", dplyr::row_number()))
  if(!is.null(high.frec.filter)) {
    group.dataset.seg <- group.dataset.seg %>%
      dplyr::filter(frecuencia < high.frec.filter)
  }
  return(group.dataset.seg[])
}


#' Classificate patients
#'
#' This function allow you tu identify the experimental group for each patient filename
#'
#' @param group.dataset.seg dataset with al patient register
#' @param patient.column Column with file identificator
#' @param db.user Database user, if null will use DB_USERNAME enviroment variable
#' @param db.host Database address if null will use DB_HOST enviroment variable
#' @param db.port Database port
#' @param db.name Database name if null will use DB_NAME enviroment variable
#' @param db.table Database Table if null will use DB_TABLE enviroment variable
#' @param db.password Database Password if null will use DB_PASSWORD enviroment variable
#'
#' @return dataset with an extra column with group identificatio
#' @export
#'
#' @examples
#' \dontrun{ClassifyExperimentalGroup(pacientes.luz.fft, "filename")}
ClassifyExperimentalGroup <- function(group.dataset.seg, patient.column = "filename", ...) {
  patients.dataset <- data.table::data.table(filename = unique(group.dataset.seg$filename))
  patients.dataset[, patients.vector := gsub("paciente", "", filename)]
  patients.dataset[, lateralidad := ifelse(grepl("od", patients.vector), "derecho", "izquierdo")]
  patients.dataset[, patients.vector := gsub("o[d|i].*", "", patients.vector)]
  db.con <- .CreateConnection(...)
  patient.data <- dplyr::tbl(db.con, "grupo_experimental") %>%
    filter(paciente %in% !!patients.dataset$patients.vector) %>%
    inner_join(patients.dataset, by = c("paciente" = "patients.vector"), copy = T) %>%
    select(filename, grupo) %>%
    inner_join(group.dataset.seg, by = "filename", copy = T) %>%
    collect()
  DBI::dbDisconnect(db.con)
  return(patient.data)
}

#' Animal Tag Test training
#'
#' This function allows you to tag randomly the test and training groups need for algorithm training phase
#'
#' @param dataset.input Input with processed dataset which will be partitionated in training and test groups
#' @param factor.column Dataset Column to use it for partitioning
#' @param multiple.sample Allos to process segmented files
#'
#' @return
#' @export
#'
#' @examples
#' \dontrun{AnimalTagTestTraining(archvodeexceldata, factor.column = "filename", multiple.sample = FALSE)}
AnimalTagTestTraining <- function(dataset.input, factor.column = "filename", multiple.sample = F) {
  if(multiple.sample) {
    rearrange.formula <-  paste("filename + group + variable +", factor.column, "~ id")
  } else {
    rearrange.formula <-  paste("filename + group +", factor.column, "~ id")
  }
  set.seed(13)
  dataset.input.tagged <- dataset.input[!is.na(get(factor.column))] %>%
    dplyr::select(filename) %>%
    dplyr::distinct(filename) %>%
    dplyr::rowwise() %>%
    dplyr::mutate(group = sample(
      c("train", "test"),
      1,
      replace = TRUE,
      prob = c(0.8, 0.2)
    ))
  dataset.input <- data.table::merge(dataset.input, dataset.input.tagged)
  dataset.input.t <- data.table::dcast(
    dataset.input[!is.na(get(factor.column))], rearrange.formula, value.var = 'ps'
  )
  return(dataset.input.t[])
}
