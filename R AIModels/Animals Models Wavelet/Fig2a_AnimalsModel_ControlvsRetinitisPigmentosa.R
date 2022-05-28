source("BaseFunctions/DataProcessing.R")
source("BaseFunctions/ModelFunctions_Modified_Tuning.R")
source('R/BasicFunctions.R')

#Animal Models, Control vs ReitinitisPigmentosa, Balanced
#frequency <= 2.1 Hz and >= 0.9 Hz, time window for each observation (size.bin) = 60000 ms,
#Proportion 80/20, Maximum reading of files (size.of.register) = 240000 ms, with Tuning.

library(caret)
remove.columns <- c("patient","group", "obs")

mA5.photo.60s.t <- read.csv("DataH_and_A/wavelet2022/AnimalsBalanced/dfControlvsRetinitisPigmentosa_P23Hrats0.9_2.1Hz.csv")
mA5.photo.60s.t <- setDT(mA5.photo.60s.t)

set.seed(1234567)

mA5.trainIndex <- createDataPartition(mA5.photo.60s.t$health.status, p = .8, 
                                     list = FALSE, 
                                     times = 1)

mA5.setTrain <- mA5.photo.60s.t[ mA5.trainIndex,]
mA5.setTest  <- mA5.photo.60s.t[-mA5.trainIndex,]
mA5.setTrain$group <- "train"
mA5.setTest$group <- "test"
mA5.photo.60s.t.partitioning <- rbind(mA5.setTrain, mA5.setTest)

mA5.model.control.animals <- TraingModelH2ODL(mA5.photo.60s.t.partitioning, remove.columns, class.column = 'health.status', reproducible = T)
mA5.model.control.animals.plot <- SingleModelROCPlot(mA5.model.control.animals$performance, "Model Control vs RetinitisPigmentosa  0.9Hz - 2.1Hz")
plot(mA5.model.control.animals.plot, type="roc")

#Confusion matrix with caret
confusionMatrix(as.factor(as.data.frame(mA5.model.control.animals$predictions)$predict), as.factor(mA5.model.control.animals$testset$health.status), mode = "everything")

#Proportion of training
table(mA5.setTrain$health.status)
#Proportion of validation
table(mA5.setTest$health.status)
#Model metrics (validation)
mA5.model.control.animals$performance

