source("BaseFunctions/DataProcessingDL.R")
source("BaseFunctions/ModelFunctions_ModifiedDL.R")
source('R/BasicFunctions.R')

# Human model Mesotopic DL
# time window for each observation (size.bin) = 60000 m, Proportion 80/20,
# Maximum reading of the files (size.of.register) = 60000 ms.

library(caret)
remove.columns <- c("patient", "patient.number","group", "obs")

m4.foto.60s <- read.csv("DataH_and_A/fourier2021/HumansMesotopicBalanced.csv")
m4.foto.60s <- setDT(m4.foto.60s)
m4.foto.60s.t <- TagTestTraining(m4.foto.60s[health.status %in% c('health', 'disorder')], factor.column = 'health.status', trainSet = 0.80, testSet = 0.20)

#Partitions the data
m4.trainIndex <- createDataPartition(m4.foto.60s.t$health.status, p = .8, 
                                  list = FALSE, 
                                  times = 1)

m4.setTrain <- m4.foto.60s.t[ m4.trainIndex,]
m4.setTest  <- m4.foto.60s.t[-m4.trainIndex,]
m4.setTrain$group <- "train"
m4.setTest$group <- "test"
m4.foto.60s.t.particionado <- rbind(m4.setTrain, m4.setTest)

#Trains the model
m4.model.sano.sindrome.met <- TraingModelH2ODL(m4.foto.60s.t.particionado, remove.columns, class.column = 'health.status', reproducible = T)
#Plots ROC
m4.model.sano.sindrome.met.plot <- SingleModelROCPlot(m4.model.sano.sindrome.met$performance, "Model Health vs Disorder - Mesotopic")
plot(m4.model.sano.sindrome.met.plot, type="roc")

#Additional metrics with caret
confusionMatrix(as.factor(as.data.frame(m4.model.sano.sindrome.met$predictions)$predict), as.factor(m4.model.sano.sindrome.met$testset$health.status), mode = "everything")

#Proportion of training
table(m4.setTrain$health.status)
#Proportion of validation
table(m4.setTest$health.status)
#Model metrics
m4.model.sano.sindrome.met$performance

