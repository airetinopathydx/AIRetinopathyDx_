source("BaseFunctions/DataProcessingDL.R")
source("BaseFunctions/ModelFunctions_ModifiedDL.R")
source('R/BasicFunctions.R')

# Human model Photopic and Mesotopic DL,
# time window for each observation (size.bin) = 60000 m, Proportion 80/20,
# Maximum reading of the files (size.of.register) = 300000 ms.

library(caret)
remove.columns <- c("patient", "patient.number","group", "obs")

m5.foto.60s <- read.csv("DataH_and_A/fourier2021/HumansPhotopic_and_MesotopicBalanced.csv")
m5.foto.60s <- setDT(m5.foto.60s)
m5.foto.60s.t <- TagTestTraining(m5.foto.60s[health.status %in% c('health', 'disorder')], factor.column = 'health.status', trainSet = 0.80, testSet = 0.20)

#Partitions the data
m5.trainIndex <- createDataPartition(m5.foto.60s.t$health.status, p = .8, 
                                  list = FALSE, 
                                  times = 1)

m5.setTrain <- m5.foto.60s.t[ m5.trainIndex,]
m5.setTest  <- m5.foto.60s.t[-m5.trainIndex,]
m5.setTrain$group <- "train"
m5.setTest$group <- "test"
m5.foto.60s.t.particionado <- rbind(m5.setTrain, m5.setTest)

#Trains the model
m5.model.sano.sindrome.met <- TraingModelH2ODL(m5.foto.60s.t.particionado, remove.columns, class.column = 'health.status', reproducible = T)
#Plots ROC
m5.model.sano.sindrome.met.plot <- SingleModelROCPlot(m5.model.sano.sindrome.met$performance, "Model Health vs Disorder - Photopic and Mesotopic")
plot(m5.model.sano.sindrome.met.plot, type="roc")

#Additional metrics with caret
confusionMatrix(as.factor(as.data.frame(m5.model.sano.sindrome.met$predictions)$predict), as.factor(m5.model.sano.sindrome.met$testset$health.status), mode = "everything")

#Proportion of training
table(m5.setTrain$health.status)
#Proportion of validation
table(m5.setTest$health.status)
#Model metrics
m5.model.sano.sindrome.met$performance

