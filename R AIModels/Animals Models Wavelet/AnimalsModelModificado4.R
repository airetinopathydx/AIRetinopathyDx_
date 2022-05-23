source("BaseFunctions/DataProcessing.R")
source("BaseFunctions/ModelFunctions_Modified_Tuning.R")
source('R/BasicFunctions.R')

#Animal Models, Group LE vs. P23H rats, Balanced
#frequency <= 40 Hz and >= 0.1 Hz, time window for each observation (size.bin) = 60000 ms,
#Proportion 80/20, Maximum reading of files (size.of.register) = 240000 ms, with Tuning.

library(caret)
remove.columns <- c("patient","group", "obs")

mA4.photo.60s.t <- read.csv("DataH_and_A/wavelet2022/AnimalsBalanced/dfGrupo LE vs P23H rats_0.1_40HzBalanceo.csv")
#mA4.photo.60s.t <- read.csv("DataH_and_A/wavelet2022/dfGrupo LE vs P23H rats_0.1_40Hz.csv")
mA4.photo.60s.t <- setDT(mA4.photo.60s.t)

set.seed(1234567)

mA4.trainIndex <- createDataPartition(mA4.photo.60s.t$health.status, p = .8, 
                                     list = FALSE, 
                                     times = 1)

mA4.setTrain <- mA4.photo.60s.t[ mA4.trainIndex,]
mA4.setTest  <- mA4.photo.60s.t[-mA4.trainIndex,]
mA4.setTrain$group <- "train"
mA4.setTest$group <- "test"
mA4.photo.60s.t.partitioning <- rbind(mA4.setTrain, mA4.setTest)

mA4.model.control.animals <- TraingModelH2ODL(mA4.photo.60s.t.partitioning, remove.columns, class.column = 'health.status', reproducible = T)
mA4.model.control.animals.plot <- SingleModelROCPlot(mA4.model.control.animals$performance, "Model Control vs P23H  0.1Hz - 40Hz")
plot(mA4.model.control.animals.plot, type="roc")

#Confutation matrix with caret
confusionMatrix(as.factor(as.data.frame(mA4.model.control.animals$predictions)$predict), as.factor(mA4.model.control.animals$testset$health.status), mode = "everything")

#Proportion of training
table(mA4.setTrain$health.status)
#Proportion of validation
table(mA4.setTest$health.status)
#Model metrics (validation)
mA4.model.control.animals$performance

