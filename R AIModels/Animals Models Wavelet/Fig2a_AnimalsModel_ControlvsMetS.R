source("BaseFunctions/DataProcessing.R")
source("BaseFunctions/ModelFunctions_Modified_Tuning.R")
source('R/BasicFunctions.R')

#Animal Models, Neotomodon Alstoni Mice CH1and2 Group, Balanced
#frequency <= 2.1 Hz and >= 0.9 Hz, time window for each observation (size.bin) = 60000 ms,
#Proportion 80/20, Maximum reading of files (size.of.register) = 60000 ms, with Tuning.

library(caret)
remove.columns <- c("patient","group", "obs")

mA13.photo.60s.t <- read.csv("DataH_and_A/wavelet2022/AnimalsBalanced/dfGrupo Neotomodon Alstoni Mice CH1y2_0.9_2.1HzBalanceo.csv")
#mA13.photo.60s.t <- read.csv("DataH_and_A/wavelet2022/dfGrupo Neotomodon Alstoni Mice CH1y2_0.9_2.1Hz.csv")
mA13.photo.60s.t <- setDT(mA13.photo.60s.t)

set.seed(1234567)

mA13.trainIndex <- createDataPartition(mA13.photo.60s.t$health.status, p = .8, 
                                     list = FALSE, 
                                     times = 1)

mA13.setTrain <- mA13.photo.60s.t[ mA13.trainIndex,]
mA13.setTest  <- mA13.photo.60s.t[-mA13.trainIndex,]
mA13.setTrain$group <- "train"
mA13.setTest$group <- "test"
mA13.photo.60s.t.partitioning <- rbind(mA13.setTrain, mA13.setTest)

mA13.model.control.animals <- TraingModelH2ODL(mA13.photo.60s.t.partitioning, remove.columns, class.column = 'health.status', reproducible = T)
mA13.model.control.animals.plot <- SingleModelROCPlot(mA13.model.control.animals$performance, "Model Control vs MetS  0.9Hz - 2.1Hz")
plot(mA13.model.control.animals.plot, type="roc")

#Confutation matrix with caret
confusionMatrix(as.factor(as.data.frame(mA13.model.control.animals$predictions)$predict), as.factor(mA13.model.control.animals$testset$health.status), mode = "everything")

#Proportion of training
table(mA13.setTrain$health.status)
#Proportion of validation
table(mA13.setTest$health.status)
#Model metrics (validation)
mA13.model.control.animals$performance
