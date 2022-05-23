source("BaseFunctions/DataProcessing.R")
source("BaseFunctions/ModelFunctions_Modified_Tuning.R")
source('R/BasicFunctions.R')

#Animal Models, Group STZ mice evolution CH1and2, Balanced
#frequency <= 2.1 Hz and >= 0.9 Hz, time window for each observation (size.bin) = 60000 ms,
#Ratio 80/20, Maximum reading of files (size.of.register) = 60000 ms, with Tuning.

library(caret)
remove.columns <- c("patient","group", "obs")

mA19.photo.60s.t <- read.csv("DataH_and_A/wavelet2022/AnimalsBalanced/dfGrupo STZ mice evolution CH1y2_0.9_2.1HzBalanceo.csv")
#mA19.photo.60s.t <- read.csv("DataH_and_A/wavelet2022/dfGrupo STZ mice evolution CH1y2_0.9_2.1Hz.csv")
mA19.photo.60s.t <- setDT(mA19.photo.60s.t)

set.seed(1234567)

mA19.trainIndex <- createDataPartition(mA19.photo.60s.t$health.status, p = .8, 
                                     list = FALSE, 
                                     times = 1)

mA19.setTrain <- mA19.photo.60s.t[ mA19.trainIndex,]
mA19.setTest  <- mA19.photo.60s.t[-mA19.trainIndex,]
mA19.setTrain$group <- "train"
mA19.setTest$group <- "test"
mA19.photo.60s.t.partitioning <- rbind(mA19.setTrain, mA19.setTest)

mA19.model.partitioning.animals <- TraingModelH2ODL(mA19.photo.60s.t.partitioning, remove.columns, class.column = 'health.status', reproducible = T)
mA19.model.partitioning.animals.plot <- SingleModelROCPlot(mA19.model.partitioning.animals$performance, "Model STZ EVO  0.9Hz - 2.1Hz")
plot(mA19.model.partitioning.animals.plot, type="roc")

#Confutation matrix with caret
confusionMatrix(as.factor(as.data.frame(mA19.model.partitioning.animals$predictions)$predict), as.factor(mA19.model.partitioning.animals$testset$health.status), mode = "everything")

#Proportion of training
table(mA19.setTrain$health.status)
#Proportion of validation
table(mA19.setTest$health.status)
#Model metrics (validation)
mA19.model.partitioning.animals$performance
