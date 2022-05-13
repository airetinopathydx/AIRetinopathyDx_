source("BaseFunctions/DataProcessing.R")
source("BaseFunctions/ModelFunctions_Modified_Tuning.R")
source('R/BasicFunctions.R')

#Animal Models, CTRL vs STZ mice, Balanced
#frequency <= 2.1 Hz and >= 0.9 Hz, time window for each observation (size.bin) = 60000 ms,
#Proportion 80/20, Maximum reading of files (size.of.register) = 120000 ms, with Tuning.

library(caret)
remove.columns <- c("patient","group", "obs")

mA2.photo.60s.t <- read.csv("DataH_and_A/wavelet2022/AnimalsBalanced/dfmiceCTRLvsSTZ_0.9_2.1HzBalanceo.csv")
#mA2.photo.60s.t <- read.csv("DataH_and_A/wavelet2022/dfmiceCTRLvsSTZ_0.9_2.1Hz.csv")
mA2.photo.60s.t <- setDT(mA2.photo.60s.t)

set.seed(1234567)

mA2.trainIndex <- createDataPartition(mA2.photo.60s.t$health.status, p = .8, 
                                     list = FALSE, 
                                     times = 1)

mA2.setTrain <- mA2.photo.60s.t[ mA2.trainIndex,]
mA2.setTest  <- mA2.photo.60s.t[-mA2.trainIndex,]
mA2.setTrain$group <- "train"
mA2.setTest$group <- "test"
mA2.photo.60s.t.partitioning <- rbind(mA2.setTrain, mA2.setTest)

mA2.model.control.animals <- TraingModelH2ODL(mA2.photo.60s.t.partitioning, remove.columns, class.column = 'health.status', reproducible = T)
mA2.model.control.animals.plot <- SingleModelROCPlot(mA2.model.control.animals$performance, "Modelo CTRL vs STZ 0.9Hz - 2.1Hz")
plot(mA2.model.control.animals.plot, type="roc")

#Confutation matrix with caret
confusionMatrix(as.factor(as.data.frame(mA2.model.control.animals$predictions)$predict), as.factor(mA2.model.control.animals$testset$health.status), mode = "everything")

#Proportion of training
table(mA2.setTrain$health.status)
#Proportion of validation
table(mA2.setTest$health.status)
#Model metrics (validation)
mA2.model.control.animals$performance

