# STAT4702 Homework 8
# Patrick Rogan
# UNI: psr2125
# 3.7.8 -------------------------------------------------------------------
Auto = read.csv("/home/pat/Desktop/STAT4702/ISL_Datasets/Auto.csv", 
                header = T, na.strings = "?")
Auto = na.omit(Auto) #looking at the data, this does not have an impact on
#this exercise
attach(Auto)

mpgVSHP = lm(mpg ~ horsepower, data = Auto)

summary(mpgVSHP)

summary(mpgVSHP)$sigma/mean(mpg) # part ii
summary(mpgVSHP)$r.squared

predict(mpgVSHP, data.frame(horsepower = (c(98))), interval = "confidence")

plot(horsepower, mpg,main="MPG vs Horsepower",xlab = "Horsepower", ylab = "MPG")
abline(mpgVSHP)
par(mfrow = c(2,2))

plot(mpgVSHP)

# 3.7.9 -------------------------------------------------------------------
pairs(Auto)
options(digits = 4)
cor(Auto[,-9])

multiMPG = lm(mpg ~ cylinders + displacement + horsepower + weight +
                acceleration + year + origin, data = Auto)

summary(multiMPG)

multiMPG2 = lm(mpg ~ cylinders + displacement + horsepower + weight +
                acceleration + origin, data = Auto)

summary(multiMPG2)

plot(multiMPG)

mMPGwIntAll = lm(mpg ~ cylinders*displacement*horsepower*weight*
                acceleration*year*origin, data = Auto)

summary(mMPGwInt)

cor(data.frame(Auto$cylinders,Auto$displacement,Auto$horsepower,Auto$weight,
               Auto$acceleration,Auto$year,Auto$origin))

mMPGwInt2 = lm(mpg ~ cylinders+displacement+horsepower*weight+
                 displacement:acceleration+acceleration+year+origin, data = Auto)

summary(mMPGwInt2)

plot(mMPGwInt2)

#Non-linear effects
nlMPG = lm(mpg ~ cylinders + displacement + log(displacement) + horsepower +log(horsepower)  +
              weight + log(weight) + acceleration + year +I(year^2) + origin,data = Auto)

summary(nlMPG)
plot(nlMPG)

# 3.7.10 ------------------------------------------------------------------
rm(list = ls())
library(ISLR)
attach(Carseats)

mLMC = lm(Sales ~ Price + Urban + US, data = Carseats)
summary(mLMC)

mLMC2 = lm(Sales ~ Price + US, data = Carseats)
summary(mLMC2)

contrasts(US)

confint(mLMC2)

par(mfrow = c(2,2))
plot(mLMC2)
(2 + 1)/length(US)

# 3.7.11 ------------------------------------------------------------------
set.seed(1)
x = rnorm(100)
y = 2*x + rnorm(100)
noI = lm(y~x+0)
summary(noI)

noII = lm(x~y+0)
summary(noII)

tstat = sqrt(length(x)-1)*x%*%y/
  sqrt(x%*%x*y%*%y-(x%*%y)^2)

IM = lm(x~y)
IMI = lm(y~x)
summary(IM)$coefficients[6] - summary(IMI)$coefficients[6] #the two are

#equivalent down to the available precision
# 3.7.13 ------------------------------------------------------------------
set.seed(1)
X = rnorm(100) # N(0,1) default
eps = rnorm(100, mean = 0, sd = 0.25)

Y = -1 + 0.5*X + eps
length(Y)

plot(X,Y,main="Y vs X")

regYX = lm(Y ~ X)
summary(regYX)

abline(regYX,col="black",lwd=c(2.5,2.5)) 
abline(-1,0.5,col = "cyan",lwd=c(2.5,2.5))
leg.txt = c("Least Squares Line","Population Line")
legend(-2,y=0,leg.txt,
  lty=c(1,1),
  lwd=c(2.5,2.5),
  col=c("black","cyan"))

quadXY = lm(Y ~ X + I(X^2))

summary(quadXY)

confint(regYX)

# h
set.seed(1)
X = rnorm(100) # N(0,1) default
eps = rnorm(100, mean = 0, sd = 0.05)

Y = -1 + 0.5*X + eps
length(Y)

plot(X,Y,main="Y vs X")

regYX = lm(Y ~ X)
summary(regYX)

abline(regYX,col="black",lwd=c(2.5,2.5)) 
abline(-1,0.5,col = "cyan",lwd=c(2.5,2.5))
leg.txt = c("Least Squares Line","Population Line")
legend(-2,y=0,leg.txt,
       lty=c(1,1),
       lwd=c(2.5,2.5),
       col=c("black","cyan"))

confint(regYX)

# i
set.seed(1)
X = rnorm(100) # N(0,1) default
eps = rnorm(100, mean = 0, sd = 2)

Y = -1 + 0.5*X + eps
length(Y)

plot(X,Y,main="Y vs X")

regYX = lm(Y ~ X)
summary(regYX)

abline(regYX,col="black",lwd=c(2.5,2.5)) 
abline(-1,0.5,col = "cyan",lwd=c(2.5,2.5))
leg.txt = c("Least Squares Line","Population Line")
legend(-2,y=4,leg.txt,
       lty=c(1,1),
       lwd=c(2.5,2.5),
       col=c("black","cyan"))
confint(regYX)

# 3.7.14 ------------------------------------------------------------------
set.seed(1)
x1 = runif(100)
x2 =0.5*x1 + rnorm(100)/10
y = 2 + 2*x1 + 0.3*x2 + rnorm(100)

plot(x1,x2, main="x2 vs x1")

regYX1X2 = lm(y~x1+x2)

summary(regYX1X2)

regYX1 = lm(y~x1)

summary(regYX1)

regYX2 = lm(y~x2)
summary(regYX2)

x1 = c(x1, 0.1)
x2 = c(x2, 0.8)
y = c(y, 6)

regYX1X2 = lm(y~x1+x2)
summary(regYX1X2)
par(mfrow = c(2,2))
plot(regYX1X2)

regYX1 = lm(y~x1)
summary(regYX1)
par(mfrow = c(2,2))
plot(regYX1)

regYX2 = lm(y~x2)
summary(regYX2)
par(mfrow = c(2,2))
plot(regYX2)

# 3.7.15 ------------------------------------------------------------------
library(MASS)
dim(Boston)
par(mfrow = c(4,4))

linearPredictors = c(1:(length(colnames(Boston))-1))

for (x in 2:length(colnames(Boston))){
  cm = lm(Boston$crim ~ Boston[,x]) 
  sm = summary(cm)
  print(summary(cm))
  linearPredictors[(x-1)] = sm$coefficients[2]
  if (sm$coefficients[8] < 0.05){
    cat(colnames(Boston[x]),"p-value", sm$coefficients[8],"\n")
    plot(Boston[,x], Boston[,1], xlab=colnames(Boston[x]), 
         ylab = "crim",main=c("crim vs",colnames(Boston[x])))
  }
}

multiPredictors = c(1:(length(colnames(Boston))-1))

attach(Boston)
multiB = lm(crim ~. , data = Boston)
smM = summary(multiB)
multiPredictors = smM$coefficients[2:14]
par(mfrow=c(2,1))
plot(linearPredictors,multiPredictors,xlab = "Univariate Regression Coefficient",
     ylab = "Multivariate Regression Coefficient", 
     main="Multivariate vs Univariate Regression Coefficient")

plot(linearPredictors[-4],multiPredictors[-4],xlab = "Univariate Regression Coefficient",
     ylab = "Multivariate Regression Coefficient", 
     main="Multivariate vs Univariate Regression Coefficient: Nox Removed")


for (x in 2:length(colnames(Boston))){
  cm = lm(Boston$crim ~ Boston[,x] + I(Boston[,x]^2) + I(Boston[,x]^3)) 
  sm = summary(cm)
  print(colnames(Boston)[x])
  print(summary(cm))
}
