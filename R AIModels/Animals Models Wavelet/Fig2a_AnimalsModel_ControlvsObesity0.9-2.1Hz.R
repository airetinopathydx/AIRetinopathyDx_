source("BaseFunctions/DataProcessing.R")
source("BaseFunctions/ModelFunctions_Modified_Tuning.R")
source('R/BasicFunctions.R')

#Animal Models, Group CTL vs. Obesity (HFD), Balanced
#frequency <= 2.1 Hz and >= 0.9 Hz, time window for each observation (size.bin) = 60000 ms,
#Proportion 80/20, Maximum reading of files (size.of.register) = 120000 ms, with Tuning.

library(caret)
remove.columns <- c("patient","group", "obs")

mA16.photo.60s.t <- read.csv("DataH_and_A/wavelet2022/AnimalsBalanced/dfControlvsObesity_HFDv_0.9_2.1Hz.csv")
mA16.photo.60s.t <- setDT(mA16.photo.60s.t)

set.seed(1234567)

mA16.trainIndex <- createDataPartition(mA16.photo.60s.t$health.status, p = .8, 
                                     list = FALSE, 
                                     times = 1)

mA16.setTrain <- mA16.photo.60s.t[ mA16.trainIndex,]
mA16.setTest  <- mA16.photo.60s.t[-mA16.trainIndex,]
mA16.setTrain$group <- "train"
mA16.setTest$group <- "test"
mA16.photo.60s.t.partitioning <- rbind(mA16.setTrain, mA16.setTest)

mA16.model.control.animals <- TraingModelH2ODL(mA16.photo.60s.t.partitioning, remove.columns, class.column = 'health.status', reproducible = T)
mA16.model.control.animals.plot <- SingleModelROCPlot(mA16.model.control.animals$performance, "Model Control vs Obesity  0.9Hz - 2.1Hz")
plot(mA16.model.control.animals.plot, type="roc")

#Confusion matrix with caret
confusionMatrix(as.factor(as.data.frame(mA16.model.control.animals$predictions)$predict), as.factor(mA16.model.control.animals$testset$health.status), mode = "everything")

#Proportion of training
table(mA16.setTrain$health.status)
#Proportion of validation
table(mA16.setTest$health.status)
#Model metrics (validation)
mA16.model.control.animals$performance
