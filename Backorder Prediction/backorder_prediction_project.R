# Company         : Stevens
# Team            : CS-513
# Assigningment   : final project
# ID              : 10422338
# Email ID        : athadani@stevens.edu

rm(list = ls())
# ---------------------reading and cleaning the file-------------------------------------
initial <- read.csv("new_dataset_51_49.csv") # with NA and -99 values to be removed
# filling in NA values of lead_time using mean as kNN is not 
library('VIM')
library(class)
library(kknn)
initial <- kNN(initial, variable = 'lead_time', 
               dist_var = colnames(initial)[colnames(initial)!="lead_time"])
initial <- initial[,-23] # removing an extra column generated
# replacing -99 values in perf_6_months and perf_12_months cols with NA and filling those values
initial$perf_6_month_avg[initial$perf_6_month_avg==-99] <- NA
initial$perf_12_month_avg[initial$perf_12_month_avg==-99] <- NA
initial <- kNN(initial, variable = c('perf_6_month_avg','perf_12_month_avg'), 
               dist_var = colnames(initial)[c(1:13,16:22)])
initial <- initial[,-c(23,24)] # removing extra cols generated

# converting Yes and no to 0 and 1
for (i in 1: length(initial)){
  if(is.factor(initial[,i])){
    initial[,i] <- ifelse(initial[,i]=="Yes",1,0)
  }
}

write.csv(initial1, "new_without_NA_dataset_51_49.csv") # without NA but de-normalized
# ------------------------------------normalizing the data and save in a file-----------------
initial <- read.csv("new_without_NA_dataset_51_49.csv")
initial <- initial[,-1]
mmnorm <-function(x,minx,maxx) {z<-((x-minx)/(maxx-minx))
return(z)
}

for(i in 1:16){
  if(i==12){next}
  temp.vect <- as.vector(initial[,i])
  initial[,i] <- as.data.frame(mmnorm(temp.vect, min(temp.vect), max(temp.vect)))
}

write.csv(initial, "new_norm_without_NA_dataset_51_49.csv")
# ------------------------- applying feature selection models----------------------------
initial <- read.csv("new_norm_without_NA_dataset_51_49.csv")
initial <- initial[,-1]
# 1. finding linear correlation among each pair of variables
library(corrplot)
corrplot(cor(initial))

# 2. applying C5.0 to find important variables
library(C50)
initial$went_on_backorder <- factor(initial$went_on_backorder)
mytree <- C5.0(went_on_backorder~., data = initial)
summary(mytree)
plot(mytree)

# 3. applying random forest to find important variables
library(randomForest)
fit <- randomForest(went_on_backorder~., data = initial, 
                    importance= TRUE, ntree= 200)
importance(fit, type = 1)
varImpPlot(fit, type = 1)

# 4. Using stepwise (forward and backward) methods to find important variables
library(olsrr)
initial$went_on_backorder <- as.integer(initial$went_on_backorder)
model <- lm(went_on_backorder ~ ., data = initial)
ols_stepwise(model)
ols_step_forward(model)
# -------------------------------------creating a training and testing data set----------------------------
index <- sample(nrow(initial), round(nrow(initial)*0.7))
train <- initial[index,]
test <- initial[-index,]
# ---------------------------------------applying models on different variable combinations----------------
train1 <- train[,c('national_inv', 'in_transit_qty', 'lead_time', 'forecast_3_month',
                   'sales_1_month', 'min_bank', 
                   'perf_6_month_avg',
                   'deck_risk','stop_auto_buy',
                   'local_bo_qty','went_on_backorder')]
test1 <- test[,c('national_inv', 'in_transit_qty', 'lead_time', 'forecast_3_month',
                 'sales_1_month', 'min_bank', 
                 'perf_6_month_avg',
                 'deck_risk','stop_auto_buy',
                 'local_bo_qty','went_on_backorder')]
# ----------------------------------applying random forest-----------------------------------
library(randomForest) # 88.68%
train1$went_on_backorder <- factor(train1$went_on_backorder)
test1$went_on_backorder <- factor(test1$went_on_backorder)
fit <- randomForest(went_on_backorder~., data = train1, importance= TRUE, ntree= 200)
prediction <- predict(fit, test1)
table(actual = test1[,11], prediction)
accuracy <- sum(prediction == test1[,11])/nrow(test1)
# ----------------------------applying knn-------------------------------------------
library(class)
library(kknn)
error_rate <- c()
for(i in seq(1,13,2)){
  predict <- knn(train = train1[,-11], test = test1[,-11],
                 cl = train1[,11], k = i)
  error_rate <- append(error_rate,sum(predict!=test1[,11])/nrow(test1))
  print(table(Predicted = predict, Actual = test1[,11]))
}
k <- seq(1,13,2)
plot(x = k,y = error_rate, type = 'l', main = "Un-weighted kNN")
# shows k = 15 is most appropriate
# --------------------------------------------applying neural net---------------------------
library(neuralnet) # 2 gives 87%, 3 gives 85.34%
train1$went_on_backorder <- fac(train1$went_on_backorder)
test1$went_on_backorder <- as.integer(test1$went_on_backorder)
y <- colnames(train1)
f <- as.formula(paste("went_on_backorder ~", paste(y[!y %in% "went_on_backorder"], collapse = " + ")))
accurate <- c()
for(i in c(2:5)){
  mymodel <- neuralnet(f, data = train1, hidden = i, linear.output = FALSE)
  myoutput <- compute(mymodel, test1[,1:10])
  myoutput <- as.vector(unlist(myoutput$net.result))
  myoutput <- ifelse(myoutput>=0.5, 1, 0)
  accuracy <- sum(myoutput == test1[,11])/nrow(test1)*100 
  accurate <- append(accurate, accuracy)
}
plot(x = c(2:5),y = accurate, type = 'l')
# summary(mymodel)
# plot(mymodel)

# predicting the outputs for test data set using the model created above
mymodel <- neuralnet(f, data = train1, hidden = c(2,2), linear.output = FALSE)
myoutput <- compute(mymodel, test1[,1:10])
myoutput <- as.vector(unlist(myoutput$net.result))
myoutput1 <- myoutput
myoutput <- ifelse(myoutput>=0.5, 1, 0)
accuracy <- sum(myoutput == test1[,11])/nrow(test1)*100
plot(mymodel)
# ------------------------------------applying clustering------------------------------
train_dist <- dist(train1[,-11])
hclust_results <- hclust(train_dist)
hclust_3 <- cutree(hclust_results,2)
table(hclust_3, train1[,11])

kmeans_3 <- kmeans(train1[,-11], 2, nstart = 10)

prop.table(table(train1[,11],kmeans_3$cluster))
plot(train1[,c(6,7)], col = train1$went_on_backorder)

# --------------------------------applying C5.0--------------------------
library(rpart) #for recursive partisioning of data (87.5%)
library(rpart.plot)
library(rattle)
library(C50)
# creating C5.0 model using train data set and observing their summary
mytree <- C5.0(factor(went_on_backorder)~., data = train1)
summary(mytree)
# predicting the outputs for test data set using the model created above
myoutput <- predict(mytree, test1[,-11], type = "class")
table(predicted = myoutput, actual = test1[,11])
plot(mytree)
accuracy <- sum(myoutput == test1[,11])/nrow(test1) * 100 # getting an accuracy of 92.85%
# --------------------------------applying Naive Bayes-----------------------------
library(e1071)
NB_model<-naiveBayes(factor(went_on_backorder)~.,data=train1)
prediction<-predict(NB_model,test1[,-11])

table(prediction,test1[,11])
accuracy <- sum(prediction == test1[,11])/nrow(test1) * 100
#  -----------------------------applying weighted knn----------------------------
train1$went_on_backorder <- factor(train1$went_on_backorder)
test1$went_on_backorder <- factor(test1$went_on_backorder)
error_rate <- c()
for(i in seq(1,13,2)){
  predict <- kknn(formula = went_on_backorder~., train = train1,
                  test = test1[,-11], kernel = "rectangular", k = i)
  fit <- fitted(predict)

  error_rate <- append(error_rate,sum(fit!=test1[,11])/nrow(test1))
  print(table(Predicted = fit, Actual = test1[,11]))
}
k <- seq(1,13,2)
plot(x = k,y = error_rate, type = 'l', main = "Weighted kNN")
# shows k = 15 as the optimum value of k
#  -------------------------applying SVM ------------------------------------------
library(e1071)
library(rpart)
train1$went_on_backorder <- factor(train1$went_on_backorder)
test1$went_on_backorder <- factor(test1$went_on_backorder)
svm.model <- svm(went_on_backorder ~ ., data = train1)
prediction <- predict(svm.model, test1[,-11])

table(prediction,test1[,11])
accuracy <- sum(prediction == test1[,11])/nrow(test1) * 100

