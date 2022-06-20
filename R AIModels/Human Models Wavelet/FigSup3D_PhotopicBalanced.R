source("BaseFunctions/DataProcessingDL.R")
source("BaseFunctions/ModelFunctions_ModifiedDL.R")
source('R/BasicFunctions.R')

# Human model Photopic DL, frecuency <= 40 Hz and >= 0.3 Hz,
# time window for each observation (size.bin) = 60000 m, Proportion 80/20,
# Maximum reading of the files (size.of.register) = 60000 ms.

library(caret)
remove.columns <- c("patient", "patient.number","group", "obs")

#m2.foto.60s <- ERGBatchProcess("DataH_and_A/espcondluzyValidaciónBalanceados/",
#                               max.lecture = 900, size.bin = 60000,
#                               remove.registers = 1:5, filtrar.altas = T,
#                               size.of.register = 60000)
m2.foto.60s <- read.csv("DataH_and_A/fourier2021/HumansPhotopicBalanced.csv")
m2.foto.60s <- setDT(m2.foto.60s)
m2.foto.60s.t <- TagTestTraining(m2.foto.60s[health.status %in% c('health', 'disorder')], factor.column = 'health.status', trainSet = 0.80, testSet = 0.20)

#Partitions the data
m2.trainIndex <- createDataPartition(m2.foto.60s.t$health.status, p = .8, 
                                  list = FALSE, 
                                  times = 1)

m2.setTrain <- m2.foto.60s.t[ m2.trainIndex,]
m2.setTest  <- m2.foto.60s.t[-m2.trainIndex,]
m2.setTrain$group <- "train"
m2.setTest$group <- "test"
m2.foto.60s.t.particionado <- rbind(m2.setTrain, m2.setTest)

#Trains the model
m2.model.sano.sindrome.met <- TraingModelH2ODL(m2.foto.60s.t.particionado, remove.columns, class.column = 'health.status', reproducible = T)
#Plots ROC
m2.model.sano.sindrome.met.plot <- SingleModelROCPlot(m2.model.sano.sindrome.met$performance, "Model Health vs Disorder Photopic")
plot(m2.model.sano.sindrome.met.plot, type="roc")

#Matriz de confución con caret
confusionMatrix(as.factor(as.data.frame(m2.model.sano.sindrome.met$predictions)$predict), as.factor(m2.model.sano.sindrome.met$testset$health.status))

#Proportion of training
table(m2.setTrain$health.status)
#Proportion of validation
table(m2.setTest$health.status)
#Model metrics
m2.model.sano.sindrome.met$performance

