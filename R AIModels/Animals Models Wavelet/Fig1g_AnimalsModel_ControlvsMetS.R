source("BaseFunctions/DataProcessing.R")
source("BaseFunctions/ModelFunctions_Modified_Tuning.R")
source('R/BasicFunctions.R')

#Animal Models, Neotomodon Alstoni Mice CH1and2 Group, Balanced
#frequency <= 40 Hz and >= 0.1 Hz, time window for each observation (size.bin) = 60000 ms,
#Proportion 80/20, Maximum reading of files (size.of.register) = 60000 ms, with Tuning.

library(caret)
remove.columns <- c("patient","group", "obs")

mA12.photo.60s.t <- read.csv("DataH_and_A/wavelet2022/AnimalsBalanced/dfGrupo Neotomodon Alstoni Mice CH1y2_0.1_40HzBalanceo.csv")
#mA12.photo.60s.t <- read.csv("DataH_and_A/wavelet2022/dfGrupo Neotomodon Alstoni Mice CH1y2_0.1_40Hz.csv")
mA12.photo.60s.t <- setDT(mA12.photo.60s.t)

set.seed(1234567)

mA12.trainIndex <- createDataPartition(mA12.photo.60s.t$health.status, p = .8, 
                                     list = FALSE, 
                                     times = 1)

mA12.setTrain <- mA12.photo.60s.t[ mA12.trainIndex,]
mA12.setTest  <- mA12.photo.60s.t[-mA12.trainIndex,]
mA12.setTrain$group <- "train"
mA12.setTest$group <- "test"
mA12.photo.60s.t.partitioning <- rbind(mA12.setTrain, mA12.setTest)

mA12.model.control.animals <- TraingModelH2ODL(mA12.photo.60s.t.partitioning, remove.columns, class.column = 'health.status', reproducible = T)
mA12.model.control.animals.plot <- SingleModelROCPlot(mA12.model.control.animals$performance, "Model Control vs MetS  0.1Hz - 40Hz")
plot(mA12.model.control.animals.plot, type="roc")

#Confutation matrix with caret
confusionMatrix(as.factor(as.data.frame(mA12.model.control.animals$predictions)$predict), as.factor(mA12.model.control.animals$testset$health.status), mode = "everything")

#Proportion of training
table(mA12.setTrain$health.status)
#Proportion of validation
table(mA12.setTest$health.status)
#Model metrics (validation)
mA12.model.control.animals$performance
