library(h2o)
library(tibble)
library(ggplot2)
library(data.table)


TraingModelH2ODL <- function(dataset.t, remove.columns, class.column, reproducible = T) {
  h2o.init(nthreads = 2)
  predictor.names <- names(dataset.t[, .SD, .SDcols = -remove.columns])
  predictor.names <- predictor.names[!predictor.names %in% class.column]
  dataset.t.train.h2o <- as.h2o(dataset.t[group == "train", .SD, .SDcols = -remove.columns])
  dataset.t.test.h2o <- as.h2o(dataset.t[group == "test", .SD, .SDcols = -remove.columns])
  dataset.t.train.h2o[, class.column] <- as.factor(dataset.t.train.h2o[, class.column])
  dataset.t.test.h2o[, class.column] <- as.factor(dataset.t.test.h2o[, class.column])
  
  #dataset.model.dl <- h2o.deeplearning(
  #  x = predictor.names, y = class.column, training_frame = dataset.t.train.h2o, 
  #  validation_frame = dataset.t.test.h2o,
  #  seed = 123456, reproducible = reproducible#, nfolds = 10
  #)
  
  #dataset.model.dl <- h2o.naiveBayes(
  #  x = predictor.names, y = class.column, training_frame = dataset.t.train.h2o, 
  #  validation_frame = dataset.t.test.h2o,
  #  seed = 123456
  #)
  
  dataset.model.dl <- h2o.randomForest(
    x = predictor.names, y = class.column, training_frame = dataset.t.train.h2o, 
    validation_frame = dataset.t.test.h2o, binomial_double_trees = TRUE,
    seed = 123456, ntrees = 150, min_rows = 2, max_depth = 15
  )
  
  # DRF hyperparameters
  #drf_params1 <- list(ntrees = c(50, 70, 90, 100, 150, 200, 250, 300, 350, 400, 450, 500),
  #                    max_depth = c(9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20),
  #                    min_rows = c(1,2,3,4))
  
  # Train and validate a cartesian grid of GBMs
  #drf_grid1 <- h2o.grid("randomForest", x = predictor.names, y = class.column,
  #                      grid_id = "drf_grid2",
  #                      training_frame = dataset.t.train.h2o,
  #                      validation_frame = dataset.t.test.h2o,
  #                      seed = 123456,
  #                      hyper_params = drf_params1)
  
  # Get the grid results, sorted by validation AUC
  #drf_gridperf1 <- h2o.getGrid(grid_id = "drf_grid2",
  #                             sort_by = "auc",
  #                             decreasing = TRUE)
  
  #No
  #dataset.model.dl <- h2o.psvm(
  #  x = predictor.names, y = class.column, training_frame = dataset.t.train.h2o, 
  #  validation_frame = dataset.t.test.h2o,
  #  seed = 123456
  #)
  
  dataset.predict <- h2o.predict(dataset.model.dl, dataset.t.test.h2o)
  dataset.perf <- h2o.performance(dataset.model.dl, dataset.t.test.h2o)
  return(list(
    model = dataset.model.dl,
    predictions = dataset.predict,
    performance = dataset.perf,
    trainset = dataset.t[group == "train", .SD, .SDcols = -remove.columns],
    trainset_tag = dataset.t[group == "train"],
    trainseth2o = dataset.t.train.h2o,
    testset = dataset.t[group == "test", .SD, .SDcols = -remove.columns],
    testset_tag = dataset.t[group == "test"],
    testseth2o = dataset.t.test.h2o,
    predictornames = predictor.names,
    classcolumn = class.column
    #,drf_gridperf1 = drf_gridperf1
  ))
}

MultipleModelROCPlot <- function(list.performance.models, main.title, vector.names) {
  list.performance.models %>%
    map(., 'performance') %>%
    map(function(x) x %>%
          .@metrics %>%
          .$thresholds_and_metric_scores %>%
          .[c('tpr','fpr')] %>%
          add_row(tpr = 0, fpr = 0, .before = T) %>%
          add_row(tpr = 0,fpr = 0, .before = F)
    ) %>% 
    map2(vector.names, function(x, y) x %>% add_column(model = y)) %>%
    reduce(rbind) %>% 
    ggplot(aes(fpr, tpr, col = model)) +
    geom_line() +
    geom_segment(aes(x = 0, y = 0, xend = 1, yend = 1), linetype = 2, col = 'grey') +
    xlab('False Positive Rate') +
    ylab('True Positive Rate') +
    ggtitle(main.title) +
    theme_minimal()
}

SingleModelROCPlot <- function(model.performance, main.title) {
  model.performance.data <- model.performance %>%
    .@metrics %>%
    .$thresholds_and_metric_scores %>%
    .[c('tpr','fpr')] %>%
    add_row(tpr = 0, fpr = 0, .before = T) %>%
    add_row(tpr = 0,fpr = 0, .before = F) %>%
    ggplot(aes(fpr, tpr)) +
    geom_line(size= 1.3, col = "#E31B23") +
    geom_segment(aes(x = 0, y = 0, xend = 1, yend = 1), linetype = 2, col = 'grey', size= 1.1) +
    xlab('False Positive Rate') +
    ylab('True Positive Rate') +
    ggtitle(main.title) +
    theme_minimal()
}

TrainCaretModel <- function(dataset.complete, control.structure, selected.model, discard.variables) {
  dataset.complete[, health.status := as.factor(health.status)]
  dataset.complete[, "health.status"] <- as.factor(dataset.complete[, "health.status"])
  set.seed(825)
  hiperparametros <- data.frame(usekernel = FALSE, fL = 0 , adjust = 0)
  training.model <- train(
    health.status ~ .,
    data = dataset.complete[group == "train", .SD, .SDcols = -discard.variables],
    method = selected.model,
    tuneGrid = hiperparametros,
    trControl = control.structure,
    verbose = T
  )
  model.prediction <- predict(
    training.model, 
    dataset.complete[group == "test", .SD, .SDcols = -discard.variables]
  )
  model.prediction.prob <- predict(
    training.model, 
    dataset.complete[group == "test", .SD, .SDcols = -discard.variables], type = "prob"
  )
  return(list(
    model = training.model,
    prediction = model.prediction,
    prediction.prob = model.prediction.prob
  ))
}

ModelROCPlotCaret <- function(caret.models) {
  probabilites.roc <-  rbindlist(sapply(caret.models, '[[', "prediction.prob", simplify = F), idcol = "models")
  setnames(probabilites.roc, c("disorder", "health"), c('tpr','fpr'))
  ggplot(probabilites.roc, aes(tpr, fpr, col = "red")) +
    geom_line() +
    geom_segment(aes(x = 0, y = 0, xend = 1, yend = 1), linetype = 2, col = 'grey', size= 1.1) +
    xlab('False Positive Rate') +
    ylab('True Positive Rate') +
    ggtitle(main.title) +
    theme_minimal()
}

GetROCData <- function(model.prediction, test.data.class){
  roc.data <- roc(test.data.class, model.prediction$prediction.prob$disorder, auc = T)
  fpr <- as.vector(apply(data.frame(roc.data$specificities), 2, function (x) 1-x))
  roc.data.dt <- data.table(tpr = rev(roc.data$sensitivities), fpr = rev(fpr))
  roc.ggplot.curve <- roc.data.dt %>%
    ggplot(aes(y=tpr, x=fpr, col = "red")) +
    geom_line() +
    geom_segment(aes(x = 0, y = 0, xend = 1, yend = 1), linetype = 2, col = 'grey', size= 1.1) +
    xlab('False Positive Rate') +
    ylab('True Positive Rate') +
    theme_minimal()
  extra.measures <- confusionMatrix(model.prediction$prediction, test.data.class, mode = "prec_recall")
  return(list(auc = roc.data$auc, plot = roc.ggplot.curve, curve.data = roc.data.dt, extra.measures = extra.measures))
}


ROCMultiPlotFromCaret <- function(roc.data.list, main.title){
  roc.data <- sapply(roc.data.list, '[[', 'curve.data', simplify = F, USE.NAMES = T)
  roc.data <- rbindlist(roc.data, idcol = 'model') %>%
    ggplot(aes(y=tpr, x=fpr, col = model)) +
    geom_line(size= 1.3) +
    geom_segment(aes(x = 0, y = 0, xend = 1, yend = 1), linetype = 2, col = 'grey', size= 1.1) +
    xlab('False Positive Rate') +
    ylab('True Positive Rate') +
    ggtitle(main.title) +
    theme_minimal()
}
