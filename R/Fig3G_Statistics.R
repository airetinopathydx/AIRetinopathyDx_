library(MASS)

fit1<-lda(Categoria ~ Edad+Abdomen+Peso+sistolica+Glucosa+Colesterol+Trigliceridos+LDL+F1+F2+F3+`0.45` +`0.3`+`0.35`+`0.4`+`0.45`+`0.5`+`0.55` +`0.6`+`0.65`+ `0.7`+`0.8`, data=frecu,
          na.action="na.omit", CV=TRUE)

fit2<-lda(Categoria ~ Edad+Abdomen+Peso+sistolica+Glucosa+Colesterol+Trigliceridos+LDL+F1+F2+F3+`0.45` +`0.3`+`0.35`+`0.4`+`0.45`+`0.5`+`0.55` +`0.6`+`0.65`+`0.75`+`0.8`, data=frecu,
          na.action="na.omit" )

cbind(frecu$`Paciente`,frecu$Categoria, fit1$class)

ct2 <- table(frecu$CatBinaria, fit3$class)

ct <- table(frecu$Categoria, fit1$class)

ct

diag(prop.table(ct, 1))

sum(diag(prop.table(ct)))