# STAT4702 Homework 11
# Patrick Rogan
# UNI: psr2125

#  6.8.6 ------------------------------------------------------------------
beta = seq(-5,8.66,0.1)
lambda = 5
y_i = 10

# Part A
par(mar=c(5.1,4.7,4.1,2.1))
plot(beta, (y_i - beta)^2 + lambda*beta^2, xlab = expression(beta), 
     ylab = expression((y[i]-beta[j])^2-lambda*beta[j]^2),
     text(0.1,250,expression(paste(hat(beta[j]^R) ,"=", y[i]/(1+lambda),"=", 5/3))), 
     main = expression(paste("Ridge Regression Minimization vs ", beta)))
text(7,150,expression(paste(lambda,"=",5)))
text(7.1,135,expression(paste(y[i],"=",10)))
abline(v = y_i/(1 + lambda))

# Part B
beta = seq(2,15,0.1)
par(mar=c(5.1,4.7,4.1,2.1))
plot(beta, (y_i - beta)^2 + lambda*abs(beta), xlab = expression(beta), 
     ylab = expression((y[i]-beta[j])^2-lambda*abs(beta[j])),
     text(6,90,expression(paste(hat(beta[j]^L) ,"=", y[i]-lambda/2,"=", 15/2))), 
     main = expression(paste("Lasso Minimization vs ", beta)))
text(6,86,expression(paste("as ",y[i], ">",lambda/2)))
text(14,60,expression(paste(lambda,"=",5)))
text(14.1,57,expression(paste(y[i],"=",10)))
abline(v = y_i - lambda/2)

# 6.8.10 ------------------------------------------------------------------
set.seed(1)
X = matrix(0,nrow = 1000, ncol = 20)
meanVec = c(0,120,2,0.25,100,14,1,0,10,99,2,100,2000,3,180,18,0,0,0,0)
sdVec = c(1,.7,1,5,.5,.2,.8,.1,.2,3,2,5,1,9,3,1.1,2.4,2.1,3,0.2)

eps = rnorm(1000, mean = 0, sd = 2.0)
betaVect = c(0,1,4,0,100,1,6,170,1,70,0,100,4,2,200,1,7,0,0,0)
beta0 = 3
Y = beta0 + eps
for (i in 1:20){
  X[,i] = rnorm(1000, mean = meanVec[i], sd = sdVec[i]) 
  Y = Y + betaVect[i]*X[,i]
}

simDat = data.frame(Y,X)
colnames(simDat) = c("Y","X1","X2","X3","X4","X5","X6","X7","X8","X9","X10","X11","X12",
                     "X13","X14","X15","X16","X17","X18","X19","X20")

# Part B
library(caret)

train.ix = as.integer(createDataPartition(simDat[,1], p = .9, list = FALSE, times = 1))
train = rep(FALSE,length(simDat[,1]))
train[train.ix] = TRUE
simDat.test = simDat[!train,]

# Part C
library(leaps)
attach(simDat)
regfit.full = regsubsets(Y~., simDat, subset = train,nvmax = 20)
summary(regfit.full)
trainMSE = rep(0,20)
testMSE = rep(0,20)
delBeta = rep(0,20)

for (i in c(1:20)){
  tempFrame = simDat[colnames(simDat[,-1])[summary(regfit.full)$which[i,c(2:21)]]]
  tfz = data.frame(tempFrame[train,])
  tfz2 = data.frame(tempFrame[!train,])  
  tempFrame = data.frame(simDat[,1],tempFrame)
  tempFrame = tempFrame[train,]
  colnames(tempFrame)[1] = "Y" 
  attach(tempFrame)
  lm.fit = lm(Y ~., tempFrame, subset = train)
  
  betav= unname(lm.fit$coefficients[-1]) - betaVect[summary(regfit.full)$which[i,c(2:21)]]
  delBeta[i] = sqrt(betav%*%betav)
  
  lm.p = unname(predict(lm.fit, tfz))
  lm.p2 = unname(predict(lm.fit,tfz2))
  
  trainMSE[i] =  mean((simDat$Y[train]-lm.p)^2)
  testMSE[i] =  mean((simDat$Y[!train]-lm.p2)^2)
}

plot(c(1:20),trainMSE, xlab = "Number of Predictors", ylab = "Training MSE",
     main = "Training MSE vs Number of Predictors")
plot(c(4:20),testMSE[4:20], xlab = "Number of Predictors", ylab = "Test MSE",
     main = "Test MSE vs Number of Predictors",
     sub = "Models with < 7 Predictors Excluded due to Scale")
par(mar=c(5.1,5.1,4.1,2.1))
plot(c(1:20),delBeta[1:20], xlab = "Number of Predictors", 
     ylab = expression(sqrt(sum((beta[j]-hat(beta[j]^r)))^2)),
     main = expression(paste(sqrt(sum((beta[j]-hat(beta[j]^r)))^2), " vs Number of Predictors")))
