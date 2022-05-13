source("BaseFunctions/DataProcessing.R")
source("BaseFunctions/ModelFunctions_Modified_Tuning.R")
source('R/BasicFunctions.R')

#Human models, 1st and 2nd balanced training data - 2nd categorization,
#frequency <= 40 Hz and >= 0.3 Hz, time window for each observation (size.bin) = 60000 ms,
#Proportion 80/20, Maximum reading of the files (size.of.register) = 360000 ms, with Tuning.

library(caret)
library(pROC)
remove.columns <- c("patient", "patient.number","group", "obs")

m2.photo.60s.t <- read.csv("DataH_and_A/wavelet2022/dfBalanceWaveletSegundaCat28022022A_0.3_40Hz.csv")
m2.photo.60s.t <- setDT(m2.photo.60s.t)

set.seed(1234567)

#Partitions the data
m2.trainIndex <- createDataPartition(m2.photo.60s.t$health.status, p = .8, 
                                     list = FALSE, 
                                     times = 1)

m2.setTrain <- m2.photo.60s.t[ m2.trainIndex,]
m2.setTest  <- m2.photo.60s.t[-m2.trainIndex,]
m2.setTrain$group <- "train"
m2.setTest$group <- "test"
m2.photo.60s.t.partitioning <- rbind(m2.setTrain, m2.setTest)

#Trains the model
m2.model.control.humans <- TraingModelH2ODL(m2.photo.60s.t.partitioning, remove.columns, class.column = 'health.status', reproducible = T)
m2.model.control.humans.plot <- SingleModelROCPlot(m2.model.control.humans$performance, "Modelo SANO vs ENFERMO")
plot(m2.model.control.humans.plot, type="roc")

#Proportion of training
table(m2.setTrain$health.status)
#Proportion of validation
table(m2.setTest$health.status)
#Model metrics
m2.model.control.humans$performance

#Additional metrics
dfPredictions <- as.data.frame(m2.model.control.humans$predictions)
confusionMatrix(as.factor(dfPredictions$predict), as.factor(m2.model.control.humans$testset$health.status), mode = "everything")

#Save the model (optional)
#modelfile <- h2o.download_mojo(m2.model.control.humans$model, path=".", get_genmodel_jar=TRUE)


#############################################################################################

#----------- External validation process ----------------
#Reads the external validation data pre-processed

dataval.60s <- read.csv("DataH_and_A/wavelet2022/dfValidacionExternaEtiquetadoListo_0.3_40Hz_Balanceado.csv")
dataval.60s <- setDT(dataval.60s)

#Validation set patient count.
table(dataval.60s$health.status)

#Performs the prediction with the loaded model
dataval.60s.t.h2o <- as.h2o(dataval.60s)
dataval.60s.t.h2o[, 'health.status'] <- as.factor(dataval.60s.t.h2o[, 'health.status'])
prediccion.val.model1 <- h2o.predict(m2.model.control.humans$model, dataval.60s.t.h2o)
dfPredictions.val <- as.data.frame(prediccion.val.model1)
confusionMatrix(as.factor(dfPredictions.val$predict), as.factor(dataval.60s$health.status), mode = "everything")
write.csv(dfPredictions.val,"./prediccion.dtValExterna_Fig4aBalanceado.csv")


#Calculate validation metrics based on the trained model (Note: only if labels are known).
dataset.perf <- h2o.performance(m2.model.control.humans$model, dataval.60s.t.h2o)
#dataset.perf
model.control.syndrome.val.plot <- SingleModelROCPlot(dataset.perf,
                                                   "ROC - External Validation")
plot(model.control.syndrome.val.plot, type="roc")

# Plot ROC Caret
rocCaret <- plot.roc(dataval.60s$health.status,
         dfPredictions.val$disorder)

rocCaret

dataset.perf

#Performs prediction with a pre-trained model (optional)
#prediccion.val <- h2o.mojo_predict_df(
#  dataval.60s,
#  '../../MOJO/DRF_model_R_1647047572848_2945.zip'
#)
#Convert prediction.val to dataframe for display in R
#prediccion.dt <- as.data.frame(prediccion.val)
#setDT(prediccion.dt)
#Saves the prediction in a csv file
#write.csv(prediccion.dt,"./prediccionValidaciónExterna_WaveletFig4a.csv")

rocCaret <- plot.roc(dataval.60s$health.status,
                     prediccion.dt$disorder)

rocCaret


#h2o.shutdown()

#----------- End of validation process --------------


#write.csv(as.data.frame(m2.model.control.humans$drf_gridperf1@summary_table),"./Tunning 02152022.csv")
