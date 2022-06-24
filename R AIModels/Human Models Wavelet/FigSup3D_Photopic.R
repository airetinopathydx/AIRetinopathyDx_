source("BaseFunctions/DataProcessingDL.R")
source("BaseFunctions/ModelFunctions_ModifiedDL.R")
source('R/BasicFunctions.R')

# Human model Photopic DL
# time window for each observation (size.bin) = 60000 m, Proportion 80/20,
# Maximum reading of the files (size.of.register) = 60000 ms.

library(caret)
remove.columns <- c("patient", "patient.number","group", "obs")

m3.foto.60s <- read.csv("DataH_and_A/fourier2021/HumansPhotopicBalanced.csv")
m3.foto.60s <- setDT(m3.foto.60s)
m3.foto.60s.t <- TagTestTraining(m3.foto.60s[health.status %in% c('health', 'disorder')], factor.column = 'health.status', trainSet = 0.80, testSet = 0.20)

#Partitions the data
m3.trainIndex <- createDataPartition(m3.foto.60s.t$health.status, p = .8, 
                                  list = FALSE, 
                                  times = 1)

m3.setTrain <- m3.foto.60s.t[ m3.trainIndex,]
m3.setTest  <- m3.foto.60s.t[-m3.trainIndex,]
m3.setTrain$group <- "train"
m3.setTest$group <- "test"
m3.foto.60s.t.particionado <- rbind(m3.setTrain, m3.setTest)

#Trains the model
m3.model.sano.sindrome.met <- TraingModelH2ODL(m3.foto.60s.t.particionado, remove.columns, class.column = 'health.status', reproducible = T)
#Plots ROC
m3.model.sano.sindrome.met.plot <- SingleModelROCPlot(m3.model.sano.sindrome.met$performance, "Model Health vs Disorder - Photopic")
plot(m3.model.sano.sindrome.met.plot, type="roc")

#Additional metrics with caret
confusionMatrix(as.factor(as.data.frame(m3.model.sano.sindrome.met$predictions)$predict), as.factor(m3.model.sano.sindrome.met$testset$health.status), mode = "everything")

#Proportion of training
table(m3.setTrain$health.status)
#Proportion of validation
table(m3.setTest$health.status)
#Model metrics
m3.model.sano.sindrome.met$performance

