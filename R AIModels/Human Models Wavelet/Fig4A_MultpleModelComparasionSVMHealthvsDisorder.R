source("BaseFunctions/DataProcessing.R")
source("BaseFunctions/ModelFunctions_Modified.R")
source('R/BasicFunctions.R')

#Human multimodel, 1st and 2nd balanced training data - 2nd categorization,
#frequency <= 40 Hz and >= 0.3 Hz, time window for each observation (size.bin) = 60000 ms,
#Proportion 80/20, Maximum reading of the files (size.of.register) = 360000 ms.
#SVM Linear and SVM Radial

library(doParallel)
library(caret)
library(pROC)

cl <- makeCluster(detectCores())
registerDoParallel(cl)

#Loading of preprocessed data
photo.60s.t <- read.csv("DataH_and_A/wavelet2022/HumansBalanced/dfHealthvsDisorder_0.3_40Hz_2ndCat.csv")
photo.60s.t <- setDT(photo.60s.t)

#Set the seed.
set.seed(1234567)

#Split the data in 80/20
m2.trainIndex <- createDataPartition(photo.60s.t$health.status, p = .8, 
                                     list = FALSE, 
                                     times = 1)

setTrain <- photo.60s.t[ m2.trainIndex,]
setTest  <- photo.60s.t[-m2.trainIndex,]
setTrain$group <- "train"
setTest$group <- "test"
photo.60s.t.partitioning <- rbind(setTrain, setTest)

#Setup variables to train the model
tc <- trainControl(
  method = "repeatedcv",
  number = 10,
  repeats = 10,
  classProbs =  TRUE,
  savePredictions = TRUE,
  verboseIter = TRUE
)

#Start the training of the model
discard.variables <-  c("patient", "patient.number", "obs", "group")
#models.list <- c("nb") #, "nnet")
models.list <- c("svmLinear", "svmRadial")
caret.models <- sapply(
  models.list, function(x) try(TrainCaretModel(photo.60s.t.partitioning, tc, x, discard.variables)), simplify = F, USE.NAMES = T
)

photo.60s.t.partitioning$health.status <- as.factor(photo.60s.t.partitioning$"health.status")

#Generate ROC data
generate.roc.data <- sapply(
  caret.models,
  function(x) try(GetROCData(x, photo.60s.t.partitioning[group == "test", health.status])),
  simplify = F,
  USE.NAMES = T
)

#Plot ROC in one plot
caret.models.plot <- ROCMultiPlotFromCaret(generate.roc.data, "Multiple-Model SVM - Health vs Disorder")
plot(caret.models.plot)


#smvLinearROC <- plot.roc(as.factor(photo.60s.t.partitioning[group == "test", health.status]),
#         caret.models$svmLinear$prediction.prob$disorder)
#smvLinearROC

#Linear SVM confusion matrix
confusionMatrix(as.factor(caret.models$svmLinear$prediction), as.factor(photo.60s.t.partitioning[group == "test", health.status]), mode = "everything")

#smvRadialROC <- plot.roc(as.factor(photo.60s.t.partitioning[group == "test", health.status]),
#         caret.models$svmRadial$prediction.prob$disorder)
#smvRadialROC

#Radial SVM confusion matrix
confusionMatrix(as.factor(caret.models$svmRadial$prediction), as.factor(photo.60s.t.partitioning[group == "test", health.status]), mode = "everything")

#caret.nb <- TrainCaretModel(photo.60s.t.partitioning, tc, "nb", discard.variables)
#caret.nnet<- TrainCaretModel(photo.60s.t.partitioning, tc, "nnet", discard.variables)
#caret.knn<- TrainCaretModel(photo.60s.t.partitioning, tc, "knn", discard.variables)

#Stops the current cluster
stopCluster(cl)
