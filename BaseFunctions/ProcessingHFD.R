library(readxl)
library(data.table)

datos <- sapply(groups.files$ctl.hfd, read_xlsx, simplify = F, USE.NAMES = T)
names(datos) <- gsub(".xlsx", "", sapply(strsplit(names(datos), "/"), '[[', 5))
datos.una.columna <- lapply(datos, function(x) x[,1])


# dos.columnas <- sapply(datos, length) > 1
# datos.una.columna <- lapply(datos[dos.columnas], function(x) rbindlist(list(x[,1], x[,2])))
# datos.fixed <- c(datos[!dos.columnas], datos.una.columna)


datos.fixed <- rbindlist(datos.una.columna, idcol = "file")
setnames(datos.fixed, "Var1", "signal")
datos.fixed[, group.factor := ifelse(grepl("CTL", file), "CTL", "HFD")]
datos.fixed[, id := gsub("CTL|HFD", "", subject)]
datos.fixed[, id :=  gsub("[[:digit:]]", "", id)]
datos.fixed[, group := "ctl.hdf"]
datos.fixed[, n.obs := .N, file]
