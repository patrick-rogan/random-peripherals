# Load prerequsite packages and data
from scipy.io import loadmat
import numpy as np
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

# dict of data with the following (relevant) fields:
#   data: 253 x 14 matrix of data, note the first column is all ones, which 
#         can be removed so long as the model explicitely calculates an 
#         an intercept
#   labels: 253 x 1 vector of Y values
#   testdata: 253 x 14 matrix of data, note the first column is all ones, which    
#         can be removed so long as the model explicitely calculates an 
#         an intercept
#   testlabels: 253 x 1 vector of Y values
#

housing = loadmat('housing.mat')

# throw out first column of 1s, the regression model used explicitly calculates
# the intercept
#housing['data'] = housing['data'][:,1:14]
#housing['testdata'] = housing['testdata'][:,1:14]

# Part A
lin = LinearRegression(fit_intercept=False)
#lin = LinearRegression()

lin.fit(housing['data'], housing['labels'])

print lin.coef_ 

lin2 = LinearRegression(fit_intercept=False)
lin2.fit(housing['data'], housing['labels']-np.mean(housing['labels']))

print lin2.coef_

model = sm.OLS(housing['labels'], housing['data'])

results = model.fit()

print results.summary()

# Part B
preds_train = lin.predict(housing['data'])
preds_test = lin.predict(housing['testdata'])

ave_sq_loss_train = ((housing['labels'] - preds_train) ** 2).sum()/len(housing['data'][:,1])

ave_sq_loss_test = ((housing['testlabels'] - preds_test) ** 2).sum()/len(housing['testdata'][:,1])

print ave_sq_loss_train
print ave_sq_loss_test

# Part C
housing['data'] = housing['data'][:,1:14]
housing['testdata'] = housing['testdata'][:,1:14]

from sklearn.linear_model import Lars

reduced = Lars(fit_intercept = True, n_nonzero_coefs = 3)

reduced.fit(housing['data'], housing['labels'])

print reduced.intercept_
print reduced.coef_
