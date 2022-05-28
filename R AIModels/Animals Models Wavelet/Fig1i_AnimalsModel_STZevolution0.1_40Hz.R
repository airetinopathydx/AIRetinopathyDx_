source("BaseFunctions/DataProcessing.R")
source("BaseFunctions/ModelFunctions_Modified_Tuning.R")
source('R/BasicFunctions.R')

#Animal Models, Group STZ mice evolution (weeks), Balanced
#frequency <= 40 Hz and >= 0.1 Hz, time window for each observation (size.bin) = 60000 ms,
#Proportion 80/20, Maximum reading of files (size.of.register) = 60000 ms, with Tuning.

library(caret)
remove.columns <- c("patient","group", "obs")

mA18.photo.60s.t <- read.csv("DataH_and_A/wavelet2022/AnimalsBalanced/dfSTZmiceEvolution0.1_40Hz.csv")

mA18.photo.60s.t <- setDT(mA18.photo.60s.t)

set.seed(1234567)

mA18.trainIndex <- createDataPartition(mA18.photo.60s.t$health.status, p = .8, 
                                     list = FALSE, 
                                     times = 1)

mA18.setTrain <- mA18.photo.60s.t[ mA18.trainIndex,]
mA18.setTest  <- mA18.photo.60s.t[-mA18.trainIndex,]
mA18.setTrain$group <- "train"
mA18.setTest$group <- "test"
mA18.photo.60s.t.partitioning <- rbind(mA18.setTrain, mA18.setTest)

#Train the model
mA18.model.control.animals <- TraingModelH2ODL(mA18.photo.60s.t.partitioning, remove.columns, class.column = 'health.status', reproducible = T)

#Get Confusion matrix with caret
confusionMatrix(as.factor(as.data.frame(mA18.model.control.animals$predictions)$predict), as.factor(mA18.model.control.animals$testset$health.status), mode = "everything")

#Proportion of training
table(mA18.setTrain$health.status)
#Proportion of validation
table(mA18.setTest$health.status)
#Model metrics H2O (validation)
mA18.model.control.animals$performance

