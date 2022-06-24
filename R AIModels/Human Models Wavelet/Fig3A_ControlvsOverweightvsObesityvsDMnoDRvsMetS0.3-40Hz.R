source("BaseFunctions/DataProcessing.R")
source("BaseFunctions/ModelFunctions_Modified_Tuning.R")
source('R/BasicFunctions.R')

#Human models, 1st and 2nd training data - 2nd categorization, Balanced
#(Multiclass) Control vs Overweight vs Obesity vs DM no DR vs MetS
#frequency <= 40 Hz and >= 0.3 Hz, time window for each observation (size.bin) = 60000 ms,
#Proportion 80/20, Maximum reading of the files (size.of.register) = 360000 ms, with Tuning.

library(caret)
remove.columns <- c("patient", "patient.number","group", "obs")

mm1.photo.60s.t <- read.csv("DataH_and_A/wavelet2022/HumansBalanced/Multiclass/dfControlvsOverweightvsObesityvsDMnoDRvsMetS_0.3_40Hz_2ndCat.csv")
mm1.photo.60s.t <- setDT(mm1.photo.60s.t)

set.seed(1234567)

#Partitions the data
mm1.trainIndex <- createDataPartition(mm1.photo.60s.t$health.status, p = .8, 
                                     list = FALSE, 
                                     times = 1)

mm1.setTrain <- mm1.photo.60s.t[ mm1.trainIndex,]
mm1.setTest  <- mm1.photo.60s.t[-mm1.trainIndex,]
mm1.setTrain$group <- "train"
mm1.setTest$group <- "test"
mm1.photo.60s.t.partitioning <- rbind(mm1.setTrain, mm1.setTest)

#Model training
mm1.model.control.humans <- TraingModelH2ODL(mm1.photo.60s.t.partitioning, remove.columns, class.column = 'health.status', reproducible = T)

#Proportion of training
table(mm1.setTrain$health.status)
#Proportion of validation
table(mm1.setTest$health.status)
#Model metrics
mm1.model.control.humans$performance

#Additional metrics
dfPredictions <- as.data.frame(mm1.model.control.humans$predictions)
confusionMatrix(as.factor(dfPredictions$predict), as.factor(mm1.model.control.humans$testset$health.status), mode = "everything")

#Saving the model
#modelfile <- h2o.download_mojo(mm1.model.control.humans$model, path=".", get_genmodel_jar=TRUE)

#############################################################################################