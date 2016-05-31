# This is the driver file for COMSW4721 HW 02 authored by Patrick Rogan,
# UNI: psr2125, email: psr2125@columbia.edu
#
# This file reads in and processes data from the 'spam' data set which is 
# described in Elements of Statistical Learning (ESL), Friedman, Tibshirani 
# and Hastie, pages 300-301. Processing is as follows:
#
#   1. Read in data
#   2. Perform 10 fold CV on 6 different algorithms
#   3. Report the 10 fold CV error rates for each classifier
#   4. Select and report the classifier with the lowest 10 fold CV error rate
#   5. Calculate the training and test error rate of this classifier.
#
# Details on the individual learning algorithms will be given in their 
# individual sections. However, it is worth noting that the 10 fold CV for 
# each classifier is performed by COMSW4721_HW_02_CV.py, see script for 
# implementation details. 

# Load prerequsite packages and data
from scipy.io import loadmat
import numpy as np
import itertools
from COMSW4721_HW_02_CV import CV #10 fold cross validation module

spam = loadmat('spam_fixed.mat')

# spam['data] are 3065 emails with 57 features each
# spam['testdata] are 1536 emails with 57 features each

#convert to float32, this seems to speed up later calculations
spam['data'] = spam['data'].astype(np.float32, copy=False)
spam['testdata'] = spam['testdata'].astype(np.float32, copy=False)

# Create empty array of errors
allErrors = []

# Bank of Algorithms:
algorithms = []
# Classifier 1: Averaged Perceptron with 64 passes through the data. 
# This classifier is located in COMSW4721_HW_02_AvePercept.py
# See file for details.
import COMSW4721_HW_02_AvePercept 
algorithms.append(COMSW4721_HW_02_AvePercept.classifier())

# Classifier 2: Logistic regression with parameters estimated by MLE. 
# this classifier is from the Scikit Learn Library
from sklearn.linear_model import LogisticRegression
algorithms.append(LogisticRegression())

# Classifier 3: Generative model classifier where class conditional
# distributions are Gaussians sharing the same covariance matrix. MLE is used
# for parameter estimation. This is Linear Discriminant Analysis.
# this classifier is from the Scikit Learn Library
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
algorithms.append(LinearDiscriminantAnalysis(solver = 'lsqr'))

# Classifier 4: Generative model classifier where class conditional
# distributions are Gaussians with each class having its own covariance matrix.
# MLE is used  for parameter estimation. This is Quadratic Discriminant 
# Analysis.
# this classifier is from the Scikit Learn Library
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
algorithms.append(QuadraticDiscriminantAnalysis())

# Classifier 5: Averaged Perceptron with 64 passes through the data. 
# This classifier is located in COMSW4721_HW_02_AvePercept.py
# See file for details. Note, here the features have been mapped from 57 
# dimensions to 1710 dimensions by using all linear terms (57), all terms 
# squared (57) and all pairs of terms (57 choose 2) = 1596. 
algorithms.append(COMSW4721_HW_02_AvePercept.classifier())

# Classifier 6: Logistic regression with parameters estimated by MLE. 
# Here the features have been mapped from 57 dimensions to 1710 dimensions by
# using all linear terms (57), all terms squared (57) and all pairs of terms
# (57 choose 2) = 1596. 
# this classifier is from the Scikit Learn Library
algorithms.append(LogisticRegression())

# Calculate error rates for all algorithms

# Classifier 1
errors = CV(spam['data'], spam['labels'], algorithms[0])
allErrors.append(errors)
 
# Classifier 2
errors = CV(spam['data'],  np.ravel(spam['labels']), algorithms[1])
allErrors.append(errors)
# http://stackoverflow.com/questions/24935415/logistic-regression-function-on-sklearn

# Classifier 3
errors = CV(spam['data'], np.ravel(spam['labels']), algorithms[2])
allErrors.append(errors)

# Classifier 4
errors = CV(spam['data'], np.ravel(spam['labels']), algorithms[3])
allErrors.append(errors)

# Create new basis set to be used by final two algorithms
expandedBasis = [np.array([]) for i in range(0, np.shape(spam['data'])[0])]

combinations = [np.array([]),np.array([])]

for c in itertools.combinations(range(0,np.shape(spam['data'])[1]),2):
    combinations[0] = np.append(combinations[0],c[0])
    combinations[1] = np.append(combinations[1],c[1])        

combinations[0] = combinations[0].tolist()
combinations[1] = combinations[1].tolist()
    
for i in range(0,np.shape(spam['data'])[0]):
    expandedBasis[i] = np.append(expandedBasis[i],
                             np.einsum('i,i->i',
                                       spam['data'][i,combinations[0]],
                                       spam['data'][i,combinations[1]]))

for i in range(0,np.shape(spam['data'])[0]):
    expandedBasis[i] = np.append(expandedBasis[i],spam['data'][i])
    expandedBasis[i] = np.append(expandedBasis[i],spam['data'][i]**2)

expandedBasis = np.array(expandedBasis)

# Classifier 5
errors = CV(expandedBasis, spam['labels'], algorithms[4])
allErrors.append(errors)

# Classifier 6
errors = CV(expandedBasis,  np.ravel(spam['labels']), algorithms[5])
allErrors.append(errors)

print allErrors

errors = []
# Select the classifier with the lowest CV error rate:
for i in allErrors:
    errors.append(i[0])

errors = np.array(errors)
classifierIX = np.argmin(errors)

print("Algorithm Selected: " + str(classifierIX+1))

if classifierIX > 3: # if a classifier using an expanded basis was better, 
# calculate the expanded basis for the test data
    expandedBasisT = [np.array([]) for i in range(0,
                      np.shape(spam['testdata'])[0])]

    combinations = [np.array([]),np.array([])]

    for c in itertools.combinations(range(0,np.shape(spam['testdata'])[1]),2):
        combinations[0] = np.append(combinations[0],c[0])
        combinations[1] = np.append(combinations[1],c[1])        

    combinations[0] = combinations[0].tolist()
    combinations[1] = combinations[1].tolist()
    
    for i in range(0,np.shape(spam['testdata'])[0]):
        expandedBasisT[i] = np.append(expandedBasisT[i],
                                 np.einsum('i,i->i',
                                           spam['testdata'][i,combinations[0]],
                                           spam['testdata'][i,combinations[1]])
                                           )
                                       
    for i in range(0,np.shape(spam['testdata'])[0]):
        expandedBasisT[i] = np.append(expandedBasisT[i],spam['testdata'][i])
        expandedBasisT[i] = np.append(expandedBasisT[i],spam['testdata'][i]**2)

    expandedBasisT = np.array(expandedBasisT)

algorithm = algorithms[classifierIX]

# Of the classifier selected, calculate the training and test error rates.
if "sklearn" in str(type(algorithm)):
    if classifierIX < 4:
        algorithm.fit(spam['data'], np.ravel(spam['labels'])) 
        print (1 - algorithm.score(spam['data'], np.ravel(spam['labels'])))    
        print (1 - algorithm.score(spam['testdata'],
                                   np.ravel(spam['testlabels'])))
    else:
        algorithm.fit(expandedBasis, np.ravel(spam['labels'])) 
        print (1 - algorithm.score(expandedBasis, np.ravel(spam['labels'])))    
        print (1 - algorithm.score(expandedBasisT, 
                                   np.ravel(spam['testlabels'])))
                                   
else:
    if classifierIX < 4:    
        params = algorithm.fit(spam['data'], spam['labels'])      
        labels = algorithm.test(spam['data'], params)
        delta = labels - np.transpose(spam['labels'])
        incorrect = np.count_nonzero(delta)
        print 1.0*incorrect/np.size(delta) #print train error
        labels = algorithm.test(spam['testdata'], params)
        delta = labels - np.transpose(spam['testlabels'])
        incorrect = np.count_nonzero(delta)    
        print 1.0*incorrect/np.size(delta) #print test error    
    else:
        params = algorithm.fit(expandedBasis, spam['labels'])      
        labels = algorithm.test(expandedBasis, params)
        delta = labels - np.transpose(spam['labels'])
        incorrect = np.count_nonzero(delta)
        print 1.0*incorrect/np.size(delta) #print train error
        labels = algorithm.test(expandedBasisT, params)
        delta = labels - np.transpose(spam['testlabels'])
        incorrect = np.count_nonzero(delta)    
        print 1.0*incorrect/np.size(delta) #print test error  