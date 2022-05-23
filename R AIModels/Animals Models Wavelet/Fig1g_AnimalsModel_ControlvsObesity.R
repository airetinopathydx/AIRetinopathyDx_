source("BaseFunctions/DataProcessing.R")
source("BaseFunctions/ModelFunctions_Modified_Tuning.R")
source('R/BasicFunctions.R')

#Animal Models, Group CTL vs. HFD validation, Balanced
#frequency <= 40 Hz and >= 0.1 Hz, time window for each observation (size.bin) = 60000 ms,
#Proportion 80/20, Maximum reading of files (size.of.register) = 120000 ms, with Tuning.

library(caret)
remove.columns <- c("patient","group", "obs")

mA15.photo.60s.t <- read.csv("DataH_and_A/wavelet2022/AnimalsBalanced/dfGrupo CTL vs HFD validación_0.1_40HzBalanceo.csv")
#mA15.photo.60s.t <- read.csv("DataH_and_A/wavelet2022/dfGrupo CTL vs HFD validación_0.1_40Hz.csv")
mA15.photo.60s.t <- setDT(mA15.photo.60s.t)

set.seed(1234567)

mA15.trainIndex <- createDataPartition(mA15.photo.60s.t$health.status, p = .8, 
                                     list = FALSE, 
                                     times = 1)

mA15.setTrain <- mA15.photo.60s.t[ mA15.trainIndex,]
mA15.setTest  <- mA15.photo.60s.t[-mA15.trainIndex,]
mA15.setTrain$group <- "train"
mA15.setTest$group <- "test"
mA15.photo.60s.t.partitioning <- rbind(mA15.setTrain, mA15.setTest)

mA15.model.control.animals <- TraingModelH2ODL(mA15.photo.60s.t.partitioning, remove.columns, class.column = 'health.status', reproducible = T)
mA15.model.control.animals.plot <- SingleModelROCPlot(mA15.model.control.animals$performance, "Model Control vs Obesity  0.1Hz - 40Hz")
plot(mA15.model.control.animals.plot, type="roc")

#Confutation matrix with caret
confusionMatrix(as.factor(as.data.frame(mA15.model.control.animals$predictions)$predict), as.factor(mA15.model.control.animals$testset$health.status), mode = "everything")

#Proportion of training
table(mA15.setTrain$health.status)
#Proportion of validation
table(mA15.setTest$health.status)
#Model metrics (validation)
mA15.model.control.animals$performance
