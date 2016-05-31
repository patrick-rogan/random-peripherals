# STAT4702 Homework 9
# Patrick Rogan
# UNI: psr2125

# 4.7.6 -------------------------------------------------------------------
beta0 = -6
beta1 = 0.05
beta2 = 1
x1=40
x2=3.5
exp(beta0+beta1*x1+beta2*x2)/(1+exp(beta0+beta1*x1+beta2*x2))

uniroot(function(x) exp(-6+0.05*x+1*3.5)/(1+exp(-6+0.05*x+1*3.5))-0.5, c(0,100))

# 4.7.7 -------------------------------------------------------------------
x = 4
mu1 = 10 #average %profit for dividend issuing companies
mu2 = 0.0 #average %profit for non-dividend issuing companies
var_hat = 36
pi1 = 0.8 # %companies issuing dividends
pi2 = 0.2

pi1*exp(-1/2*1/var_hat*(x-mu1)^2)/
  (pi1*exp(-1/2*1/var_hat*(x-mu1)^2) + pi2*exp(-1/2*1/var_hat*(x-mu2)^2))

# 4.7.10 ------------------------------------------------------------------
# Part a
setwd("~/Desktop/STAT4702/HW09")
library(ISLR)
attach(Weekly)

names(Weekly)
summary(Weekly)

png("Weekly1.png",width=832,height=574, units = "px") 
pairs(Weekly)
dev.off()
cor(Weekly[,-9])

# Part B
glm.fit = glm(Direction ~ Lag1+Lag2+Lag3+Lag4+Lag5+Volume,
              family = binomial, data = Weekly)
summary(glm.fit)

glm.probs = predict(glm.fit, type="response")
glm.pred = rep("Down",length(glm.probs))
glm.pred[glm.probs > 0.5] = "Up" #same up/down labeling convention used 
# in Smarket

# Part C
table(glm.pred,Direction)
mean(glm.pred == Direction)

# Part D
train = (Year<2009)
Weekly.2009 = Weekly[!train,]
Direction.2009 = Direction[!train]

glm.fit = glm(Direction ~ Lag2, family = binomial, data = Weekly, subset = train)
glm.probs = predict(glm.fit, Weekly.2009, type = "response")

glm.pred = rep("Down",length(Direction.2009))
glm.pred[glm.probs > 0.5] = "Up"

table(glm.pred, Direction.2009)
mean(glm.pred == Direction.2009)

# Part E
library(MASS)
lda.fit = lda(Direction ~ Lag2, data = Weekly, subset = train)
lda.pred = predict(lda.fit, Weekly.2009)
lda.class = lda.pred$class

table(lda.class, Direction.2009)
mean(lda.class == Direction.2009)

# Part F
qda.fit = qda(Direction ~ Lag2, data = Weekly, subset = train)
qda.class = predict(qda.fit, Weekly.2009)$class

table(qda.class, Direction.2009)
mean(qda.class == Direction.2009)

# Part G
library(class)
train.X = as.matrix(cbind(Lag2)[train,])
test.X = as.matrix(cbind(Lag2)[!train,])
train.Direction = Direction[train]

set.seed(1)
knn.pred = knn(train.X, test.X, train.Direction, k = 1)
table(knn.pred, Direction.2009)

(21+31)/(21+30+22+31)

# Part I
qda.fit = qda(Direction ~ Lag2+I(Lag2^2)+Lag2*Lag3, data = Weekly, subset = train)
qda.class = predict(qda.fit, Weekly.2009)$class

table(qda.class, Direction.2009)
mean(qda.class == Direction.2009)

# Revisit KNN
train.X = as.matrix(cbind(Lag2)[train,])
test.X = as.matrix(cbind(Lag2)[!train,])
train.Direction = Direction[train]

set.seed(1)
knn.pred = knn(train.X, test.X, train.Direction, k = 4)
table(knn.pred, Direction.2009)
(20+44)/(20+17+23+44)

# 4.7.11 ------------------------------------------------------------------
Auto = read.csv("/home/pat/Desktop/STAT4702/ISL_Datasets/Auto.csv", 
                header = T, na.strings = "?")
Auto = na.omit(Auto) 
attach(Auto)

# Part A
mpg01 = rep(0,length(mpg))
mpg01[(mpg > median(mpg))] = 1

Auto = data.frame(Auto,mpg01)

# Part B
png("Auto1.png",width=832,height=574, units = "px") 
pairs(Auto[,-9]) #Exclude name
dev.off()

png("Auto2.png",width=832,height=574, units = "px") 
par(mfrow = c(3,3))
for (i in 2:8){
  boxplot(Auto[mpg01==0,i],Auto[mpg01==1,i],ylab = colnames(Auto)[i],
          names=c("Below Median mpg","Above Median mpg"))
}
dev.off()

png("Auto3.png",width=832,height=574, units = "px") 
par(mfrow = c(1,2))
perOri = rep(0,3)
for (j in 1:3){
  perOri[j] = sum(mpg01[origin == j])/sum(origin == j)*100
}
plot(c(1,2,3),perOri,xlab="Origin",ylab="% Vehicles Above Median MPG",
     main="% Vehicles Above Median MPG vs Origin")

perCyl = rep(0,5)
for (j in sort(unique(cylinders))){
  perCyl[j] = sum(mpg01[cylinders == j])/sum(cylinders == j)*100
}
plot(sort(unique(cylinders)),perCyl[c(-1,-2,-7)],xlab="Cylinders",ylab="% Vehicles Above Median MPG",
     main="% Vehicles Above Median MPG vs Cylinders")
dev.off()

# Part C
library(caret) #use createDataPartition from caret librart to create randomized 80:20 
# split so that year can be used as a predictor
set.seed(1)
train.ix = as.integer(createDataPartition(Auto$mpg01, p = .8, list = FALSE, times = 1))
train = rep(FALSE,length(mpg01))
train[train.ix] = TRUE
Auto.test = Auto[!train,] 
mpg01.test = mpg01[!train]

# Part D
lda.fit = lda(mpg01 ~ origin + displacement + horsepower + weight + year,
              data = Auto, subset = train)

lda.pred = predict(lda.fit, Auto.test)
lda.class = lda.pred$class

table(lda.class, mpg01.test)
mean(lda.class == mpg01.test)

# Part E
qda.fit = qda(mpg01 ~ origin + displacement + horsepower + weight + year,
              data = Auto, subset = train)
qda.class = predict(qda.fit, Auto.test)$class

table(qda.class, mpg01.test)
mean(qda.class == mpg01.test)

# Part F
glm.fit = glm(mpg01 ~ origin + displacement + horsepower + weight + year,
              family = binomial, data = Auto, subset = train)
glm.probs = predict(glm.fit, Auto.test, type = "response")

glm.pred = rep(0,length(mpg01.test))
glm.pred[glm.probs > 0.5] = 1

table(glm.pred, mpg01.test)
mean(glm.pred == mpg01.test)

# Part G
train.X = as.matrix(cbind(origin, displacement, horsepower, weight, year)[train,])
test.X = as.matrix(cbind(origin, displacement, horsepower, weight, year)[!train,])
train.mpg01 = mpg01[train]

set.seed(1)
knn.pred = knn(train.X, test.X, train.mpg01, k = 16)
table(knn.pred, mpg01.test)

# 4.7.13 ------------------------------------------------------------------
library(MASS)
attach(Boston)

crim01 = rep(0,length(crim))
crim01[crim > median(crim)] = 1
Boston = data.frame(Boston,crim01)

png("Boston1.png",width=832,height=574, units = "px") 
pairs(Boston) #Exclude name
dev.off()

png("Boston2.png",width=832,height=574, units = "px") 
par(mfrow = c(3,4))
for (i in 2:13){
  boxplot(Boston[crim01==0,i],Boston[crim01==1,i],ylab = colnames(Boston)[i],
          names=c("< Median Crime","> Median Crime"))
}
dev.off()

# Possible variables include indus, nox, age, dis, rad, tax, pratio, and lstat
# replot to weed out other variables
png("Boston3.png",width=832,height=574, units = "px") 
par(mfrow = c(3,3))
for (i in c(3,5,7,8,9,10,11,13)){
  boxplot(Boston[crim01==0,i],Boston[crim01==1,i],ylab = colnames(Boston)[i],
          names=c("< Median Crime","> Median Crime"))
}
dev.off()

# To further simplify, we'll rule out lstat and pratio leaving:
# indus, nox, age, dis, rad, tax

# So, we'll look at 4 subsets,
# i. All predictors
# ii. First subset of predictors
# iii. Second subset of predictors
# iv. Several subsets of iii in search of the best result

set.seed(1) #Looking at crim01 there are obvious streaks of 0s and 1s, we sample randomly
# to reduce any impact on our final results
train.ix = as.integer(createDataPartition(Boston$crim01, p = .8, list = FALSE, times = 1))
train = rep(FALSE,length(crim01))
train[train.ix] = TRUE
#train[320:406] = TRUE # second method, just look at last 86 points for test
Boston.test = Boston[!train,] 
crim01.test = crim01[!train]

# i. All predictors
glm.fit = glm(crim01 ~ zn + indus + chas + nox + rm + age + dis+
                rad + tax + ptratio + black +lstat + medv,
              family = binomial, data = Boston, subset = train)
glm.probs = predict(glm.fit, Boston.test, type = "response")

glm.pred = rep(0,length(crim01.test))
glm.pred[glm.probs > 0.5] = 1

table(glm.pred, crim01.test)
mean(glm.pred == crim01.test)

lda.fit = lda(crim01 ~ zn + indus + chas + nox + rm + age + dis+
                rad + tax + ptratio + black +lstat + medv,
              data = Boston, subset = train)

lda.pred = predict(lda.fit, Boston.test)
lda.class = lda.pred$class

table(lda.class, crim01.test)
mean(lda.class == crim01.test)

train.X = as.matrix(cbind(zn, indus, chas, nox, rm, age, dis,
                            rad, tax, ptratio, black, lstat, medv)[train,])
test.X = as.matrix(cbind(zn, indus, chas, nox, rm, age, dis,
                         rad, tax, ptratio, black, lstat, medv)[!train,])
train.crim01 = crim01[train]

set.seed(1)
knn.pred = knn(train.X, test.X, train.crim01, k = 1)
table(knn.pred, crim01.test)

# ii. First subset of predictors: indus, nox, age, dis, rad, tax, ptratio, and lstat
glm.fit = glm(crim01 ~ indus + nox + age + dis+
                rad + tax + ptratio +lstat,
              family = binomial, data = Boston, subset = train)
glm.probs = predict(glm.fit, Boston.test, type = "response")

glm.pred = rep(0,length(crim01.test))
glm.pred[glm.probs > 0.5] = 1

table(glm.pred, crim01.test)
mean(glm.pred == crim01.test)

lda.fit = lda(crim01 ~ indus + nox + age + dis+
                rad + tax + ptratio +lstat,
              data = Boston, subset = train)

lda.pred = predict(lda.fit, Boston.test)
lda.class = lda.pred$class

table(lda.class, crim01.test)
mean(lda.class == crim01.test)

train.X = as.matrix(cbind(indus, nox, age, dis,
                            rad, tax, ptratio, lstat)[train,])
test.X = as.matrix(cbind(indus, nox, age, dis,
                         rad, tax, ptratio, lstat)[!train,])
train.crim01 = crim01[train]

set.seed(1)
knn.pred = knn(train.X, test.X, train.crim01, k = 1)
table(knn.pred, crim01.test)

# iii. Second subset of predictors: indus, nox, age, dis, rad, tax
glm.fit = glm(crim01 ~ indus + nox + age + dis+
                rad + tax,
              family = binomial, data = Boston, subset = train)
glm.probs = predict(glm.fit, Boston.test, type = "response")

glm.pred = rep(0,length(crim01.test))
glm.pred[glm.probs > 0.5] = 1

table(glm.pred, crim01.test)
mean(glm.pred == crim01.test)

lda.fit = lda(crim01 ~ indus + nox + age + dis+
                rad + tax,
              data = Boston, subset = train)

lda.pred = predict(lda.fit, Boston.test)
lda.class = lda.pred$class

table(lda.class, crim01.test)
mean(lda.class == crim01.test)

train.X = as.matrix(cbind(indus, nox, age, dis,
                          rad, tax)[train,])
test.X = as.matrix(cbind(indus, nox, age, dis,
                         rad, tax)[!train,])
train.crim01 = crim01[train]

set.seed(1)
knn.pred = knn(train.X, test.X, train.crim01, k = 1)
table(knn.pred, crim01.test)

# iv. Several subsets of iii in search of the best result, use greedy approach
# remove predictors that improve the model starting from tax working up to indus
# note this was done with the randomized train indices. Turns out the removal of
# any one of these parameters does not improve all of the models.
glm.fit = glm(crim01 ~ indus + nox + age + dis+
                rad + tax,
              family = binomial, data = Boston, subset = train)
glm.probs = predict(glm.fit, Boston.test, type = "response")

glm.pred = rep(0,length(crim01.test))
glm.pred[glm.probs > 0.5] = 1

table(glm.pred, crim01.test)
mean(glm.pred == crim01.test)

lda.fit = lda(crim01 ~ indus + nox + age + dis+
                rad + tax,
              data = Boston, subset = train)

lda.pred = predict(lda.fit, Boston.test)
lda.class = lda.pred$class

table(lda.class, crim01.test)
mean(lda.class == crim01.test)

train.X = as.matrix(cbind(indus, nox, age, dis,
                          rad, tax)[train,])
test.X = as.matrix(cbind(indus, nox, age, dis,
                         rad, tax)[!train,])
train.crim01 = crim01[train]

set.seed(1)
knn.pred = knn(train.X, test.X, train.crim01, k = 1)
table(knn.pred, crim01.test)