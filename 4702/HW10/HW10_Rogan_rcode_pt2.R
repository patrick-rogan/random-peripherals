# STAT4702 Homework 10
# Patrick Rogan
# UNI: psr2125

# Note that this code is derived from work presented by Robert V. Hogg, Joseph W. McKean and
# Allen T. Craig in Introduction to Mathematical Statistics, 7th edition on pages 651 and 
# 652. 

# 4.9.3 -------------------------------------------------------------------
percentciboot<-function(x,b,alpha){
  # x is a vector containing the original sample.
  # b is the desired number of bootstraps.
  # alpha: (1 - alpha) is the confidence coefficient.
  #
  # theta is the point estimate.
  # lower is the lower end of the percentile confidence interval.
  # upper is the upper end of the percentile confidence interval.
  # thetastar is the vector of bootstrapped theta^*s.
  #
  theta<-median(x)
  thetastar<-rep(0,b)
  n<-length(x)
  for(i in 1:b){xstar<-sample(x,n,replace=T)
    thetastar[i]<-median(xstar)
  }
  thetastar<-sort(thetastar)
  pick<-round((alpha/2)*(b+1))
  lower<-thetastar[pick]
  upper<-thetastar[b-pick+1]
  return(list(theta=theta,lower=lower,upper=upper))#,thetastar=thetastar))
  #list(theta=theta,lower=lower,upper=upper)
}
x = c(131.7, 4.3, 182.7, 265.6, 73.3, 61.9, 10.7, 10.8, 150.4, 
      48.8, 42.3, 22.5, 22.2, 8.8, 17.9, 150.6, 264.0, 103.0,
      154.4, 85.9)

percentciboot(x,3000,0.1)

# 4.9.5 -------------------------------------------------------------------
percentcibootstand<-function(x,b,alpha){
  # x is a vector containing the original sample.
  # b is the desired number of bootstraps.
  # alpha: (1 - alpha) is the confidence coefficient.
  #
  # theta is the point estimate.
  # lower is the lower end of the percentile confidence interval.
  # upper is the upper end of the percentile confidence interval.
  # thetastar is the vector of bootstrapped theta^*s.
  #
  theta<-mean(x)
  sdx = sd(x)
  thetastar<-rep(0,b)
  n<-length(x)
  for(i in 1:b){xstar<-sample(x,n,replace=T)
    bootMean = mean(xstar)  
    sdBoot = sd(xstar)
    thetastar[i]<-(bootMean - theta)/(sdBoot/sqrt(n))
  }
  thetastar<-sort(thetastar)
  pick<-round((alpha/2)*(b+1))
  lower<-thetastar[pick]
  upper<-thetastar[b-pick+1]
  lower2 = theta - upper*sdx/sqrt(n)
  upper2 = theta - lower*sdx/sqrt(n)
  return(list(theta=theta,lower=lower2,upper=upper2))#,thetastar=thetastar))
  #list(theta=theta,lower=lower,upper=upper)
}

x = c(119.7, 95.4, 104.1, 77.2, 92.8, 100.0, 85.4, 114.2, 108.6, 150.3, 93.4,
      102.3, 67.1, 105.8, 88.4, 107.5, 101.0, 0.9, 97.2, 94.1)

percentcibootstand(x, 3000, 0.1)

percentciboot<-function(x,b,alpha){
  # x is a vector containing the original sample.
  # b is the desired number of bootstraps.
  # alpha: (1 - alpha) is the confidence coefficient.
  #
  # theta is the point estimate.
  # lower is the lower end of the percentile confidence interval.
  # upper is the upper end of the percentile confidence interval.
  # thetastar is the vector of bootstrapped theta^*s.
  #
  theta<-mean(x)
  thetastar<-rep(0,b)
  n<-length(x)
  for(i in 1:b){xstar<-sample(x,n,replace=T)
  thetastar[i]<-mean(xstar)
  }
  thetastar<-sort(thetastar)
  pick<-round((alpha/2)*(b+1))
  lower<-thetastar[pick]
  upper<-thetastar[b-pick+1]
  return(list(theta=theta,lower=lower,upper=upper))#,thetastar=thetastar))
  #list(theta=theta,lower=lower,upper=upper)
}

percentciboot(x, 3000, 0.1)

# 4.9.13 ------------------------------------------------------------------
pairboot <- function(x,y,b){
  delta = x - mean(x) - y + mean(y)
  n = length(delta)
  ts = mean(x) - mean(y)
  tstar = rep(0,b)
  counter = 0
  for(i in 1:b){xstar<-sample(delta,n,replace=T)
    tstar[i]<-mean(xstar)
    if (tstar[i] >= ts){
      counter = counter + 1
    }
  }
  counter = counter/b  
  return(list(counter = counter))
}

# Cross
x = c(23.500, 12.000, 21.000, 22.000, 19.125, 21.500, 22.125, 20.375, 
      18.250, 21.625, 23.250, 21.000, 22.125, 23.000, 12.000)

# Self
y = c(17.375, 20.375, 20.000, 20.000, 18.375, 18.625, 18.625, 15.250,
      16.500, 18.000, 16.250, 18.000, 12.750, 15.500, 18.000)

pairboot(x,y,3000)

