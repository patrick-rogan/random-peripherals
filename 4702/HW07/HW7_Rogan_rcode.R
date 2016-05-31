# STAT4702 Homework 7, Problems 2.4.8, 2.4.9, 2.4.10
# Patrick Rogan
# UNI: psr2125

# 2.4.8 -------------------------------------------------------------------
# a
college = read.csv('/home/pat/Desktop/STAT4702/ISL_Datasets/College.csv')

# b
fix(college)
rownames(college) = college[,1]
fix(college)
college = college[,-1]
fix(college)

# c
# i
summary(college)
# ii
pairs(college[,1:10])

# iii
boxplot(college[college$Private == "Yes",9], 
        college[college$Private =="No",9], 
        names = c("Private","Public"),ylab="Outstate",
        main="Outstate Tuition Public and Private")
# iv
Elite = rep("No", nrow(college))
Elite[college$Top10perc >50] = " Yes "
Elite = as.factor(Elite)
college = data.frame(college, Elite)
boxplot(college$Outstate ~ college$Elite,
        names = c("Non-Elite","Elite"),
        ylab="Outstate",
        main="Outstate Tuition Non-Elite and Elite")

# v
par(mfrow = c(2,2))
hist(college$Room.Board, breaks = 30)
hist(college$Outstate, breaks = 5)
hist(college$Outstate, breaks = 18)
hist(college$PhD, breaks = 20)

# 2.4.9 -------------------------------------------------------------------
# a
Auto = read.csv("/home/pat/Desktop/STAT4702/ISL_Datasets/Auto.csv", 
                header = T, na.strings = "?")
Auto = na.omit(Auto)

# d 
Auto2 = Auto[-(10:85),]
for(i in 1:(length(Auto2[1,])-2)){
  print(c(diff(range(Auto2[,i])),"&", mean(Auto2[,i]),"&",sqrt(var(Auto2[,i]))))
  }
# e
pairs(Auto)

# e
par(mfrow = c(2,2))
boxplot(Auto$mpg ~ Auto$cylinders,
        ylab="MPG", xlab = "# Cylinders",
        main="MPG vs Cylinders")

boxplot(Auto$mpg ~ Auto$year, 
        ylab="MPG", xlab = "Year",
        main="MPG vs Year")

boxplot(Auto$mpg ~ Auto$origin, 
        ylab="MPG", xlab = "Origin",
        main="MPG vs Origin")

plot(Auto$acceleration, Auto$mpg, 
     main = "MPG vs Acceleration",
     ylab = "MPG", xlab = "Acceleration")

# 2.4.10 ------------------------------------------------------------------
library(MASS)
Boston
dim(Boston)
?Boston

par(mfrow = c(2,2))
pairs(Boston$crim ~ Boston$age)

library(corrplot)
corrplot(cor(Boston),method = "shade")

print(
  c(
    diff(range(Boston$crim)), "&", min(Boston$crim), "&", max(Boston$crim), "&", median(Boston$crim)
    )
  )

print(
  c(
    diff(range(Boston$tax)), "&", min(Boston$tax), "&", max(Boston$tax), "&", median(Boston$tax)
  )
)

print(
  c(
    diff(range(Boston$ptratio)), "&", min(Boston$ptratio), "&", max(Boston$ptratio), "&", median(Boston$ptratio)
  )
)

Boston[which(Boston$crim > 0.97*max(Boston$crim)),]
Boston[which(Boston$tax > 0.97*max(Boston$tax)),]
Boston[which(Boston$ptratio > 0.97*max(Boston$ptratio)),]

for (i in 1:ncol(Boston)){
  print(
    c(
      colnames(Boston[i]),diff(range(Boston[,i])), "&", min(Boston[,i]), "&", max(Boston[,i]),
      "&", median(Boston[,i])
    )
  )
}




