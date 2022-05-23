source("BaseFunctions/DataProcessing.R")
source("BaseFunctions/ModelFunctions_Modified_Tuning.R")
source('R/BasicFunctions.R')

#Animal Models, CTRL vs STZ mice, Balanced
#frequency <= 40 Hz and >= 0.1 Hz, time window for each observation (size.bin) = 60000 ms,
#Proportion 80/20, Maximum reading of files (size.of.register) = 120000 ms, with Tuning.

library(caret)
remove.columns <- c("patient","group", "obs")

mA.photo.60s.t <- read.csv("DataH_and_A/wavelet2022/AnimalsBalanced/dfmiceCTRLvsSTZ_0.1_40HzBalanceo.csv")
#mA.photo.60s.t <- read.csv("DataH_and_A/wavelet2022/dfmiceCTRLvsSTZ_0.1_40Hz.csv")
mA.photo.60s.t <- setDT(mA.photo.60s.t)

set.seed(1234567)

mA.trainIndex <- createDataPartition(mA.photo.60s.t$health.status, p = .8, 
                                     list = FALSE, 
                                     times = 1)

mA.setTrain <- mA.photo.60s.t[ mA.trainIndex,]
mA.setTest  <- mA.photo.60s.t[-mA.trainIndex,]
mA.setTrain$group <- "train"
mA.setTest$group <- "test"
mA.photo.60s.t.partitioning <- rbind(mA.setTrain, mA.setTest)

mA.model.control.animals <- TraingModelH2ODL(mA.photo.60s.t.partitioning, remove.columns, class.column = 'health.status', reproducible = T)
mA.model.control.animals.plot <- SingleModelROCPlot(mA.model.control.animals$performance, "Model Control vs DM  0.1Hz - 40Hz")
plot(mA.model.control.animals.plot, type="roc")

#Confutation matrix with caret
confusionMatrix(as.factor(as.data.frame(mA.model.control.animals$predictions)$predict), as.factor(mA.model.control.animals$testset$health.status), mode = "everything")

#Proportion of training
table(mA.setTrain$health.status)
#Proportion of validation
table(mA.setTest$health.status)
#Model metrics (validation)
mA.model.control.animals$performance

