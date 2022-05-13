source("BaseFunctions/DataProcessing.R")
source("BaseFunctions/ModelFunctions_Modified_Tuning.R")
source('R/BasicFunctions.R')

#Human Models, Control vs. Overweight + Obesity + Metabolic Syndrome - 2nd categorization (Balanced),
#Frequency <= 40 Hz and >= 0.3 Hz, time window for each observation (size.bin) = 60000 ms,
#Proportion 80/20, Maximum reading of the files (size.of.register) = 360000 ms, with Tuning.

library(caret)
remove.columns <- c("patient", "patient.number","group", "obs")

m2.photo.60s.t <- read.csv("DataH_and_A/wavelet2022/dfControlvsSobrepeso_ObesidadySM2daCat_0.3_40HzBalanceado.csv")
m2.photo.60s.t <- setDT(m2.photo.60s.t)

set.seed(1234567)

#Partitions the data
m2.trainIndex <- createDataPartition(m2.photo.60s.t$health.status, p = .8, 
                                     list = FALSE, 
                                     times = 1)

m2.setTrain <- m2.photo.60s.t[ m2.trainIndex,]
m2.setTest  <- m2.photo.60s.t[-m2.trainIndex,]
m2.setTrain$group <- "train"
m2.setTest$group <- "test"
m2.photo.60s.t.partitioning <- rbind(m2.setTrain, m2.setTest)

#Trains the model.
m2.model.control.humans <- TraingModelH2ODL(m2.photo.60s.t.partitioning, remove.columns, class.column = 'health.status', reproducible = T)
m2.model.control.humans.plot <- SingleModelROCPlot(m2.model.control.humans$performance, "Modelo Sano vs Sobrepeso + Obesidad + MetS  0.3 - 40Hz")
plot(m2.model.control.humans.plot, type="roc")

#Proportion of training
table(m2.setTrain$health.status)
#Proportion of validation
table(m2.setTest$health.status)
#Model metrics
m2.model.control.humans$performance

#Additional metrics
dfPredictions <- as.data.frame(m2.model.control.humans$predictions)
confusionMatrix(as.factor(dfPredictions$predict), as.factor(m2.model.control.humans$testset$health.status), mode = "everything")

#Save the model
#modelfile <- h2o.download_mojo(m2.model.control.humans$model, path=".", get_genmodel_jar=TRUE)

#############################################################################################
