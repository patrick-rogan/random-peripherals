# STAT4702 Homework 10
# Patrick Rogan
# UNI: psr2125

# 5.4.2 -------------------------------------------------------------------
n = 10000
1-(1-1/n)^n

# G
n = 1:100000
pNinBS = 1-(1-1/n)^n

plot(n,pNinBS, xlab = 'n', ylab = "P(jth observation in Bootstrap)",
     main = "P(jth observation in Bootstrap) vs Sample Size")

# H
store = rep(NA, 10000)
for (i in 1:10000){
  store [i]= sum (sample(1:100, rep = TRUE)==4) > 0
}
mean(store)

# 5.4.6 -------------------------------------------------------------------
library(ISLR)
library(boot)
attach(Default)

# Part A
glm.fit = glm(default ~ income + balance, family = binomial, data = Default)
summary(glm.fit)

# Part B
boot.fn <- function(Default,index){
  glm.fit = glm(default ~ income + balance, family = binomial, 
                data = Default, subset = index)
  return(coefficients(glm.fit))  
}

# Part C
set.seed(1)
boot(Default,boot.fn,1000)

# 5.4.9 -------------------------------------------------------------------
library(MASS)
attach(Boston)

# Part A
mu_hat = mean(medv)

# Part B
SE_mu_hat = sqrt(var(medv))/sqrt(length(medv))

# Part C
boot.fn <- function(Boston,index){
  meanMedv = mean(medv[index])
  return(meanMedv)
}

set.seed(1)
result = boot(Boston,boot.fn,1000)

# Part D
ci = cat(boot.ci(result, type="bca")[[4]][4], boot.ci(result, type="bca")[[4]][5])

# Part E
median(medv)

# Part F
boot.fn <- function(Boston,index){
  seMed = median(medv[index])
  return(seMed)
}
  
set.seed(1)
result = boot(Boston, boot.fn,1000)

# Part G
unname(quantile(medv,0.1))

# Part H
boot.fn <- function(Boston,index){
  seMed = unname(quantile(medv[index],0.1))
  return(seMed)
}

set.seed(1)
result = boot(Boston, boot.fn,1000)
