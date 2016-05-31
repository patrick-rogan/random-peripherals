# Load prerequsite packages and data
from scipy.io import loadmat
import matplotlib.pyplot as plt
import numpy as np
import random 

ocr = loadmat('ocr.mat')

#convert to float32, this seems to speed up later calculations
ocr['data'] = ocr['data'].astype(np.float32, copy=False)
ocr['testdata'] = ocr['testdata'].astype(np.float32, copy=False)

def one_NN(trainingFeatureMatrix, trainingLabels, testFeatureMatrix):
    # oneNN, a function that performs 1-Nearest Neighbor classification on a 
    # matrix that corresponds to handwritten digits and returns a vector of 
    # predicted labels.
    #
    # Function Inputs: 
    #
    # trainingFeatureMatrix: an N x M matrix of images, features
    # trainingLabels: an N x 1 vector of image labels
    # testFeatureMatrix: a K * M matrix of unlabeled images
    #
    # Function Outputs
    #
    # testLabels: a K x 1 vector of image labels

    # Calculate the magnitude^2 of each vector in the training set        
    mag2 =np.einsum('ij,ij->i',trainingFeatureMatrix,trainingFeatureMatrix) 
    
    # Determine loop range and preallocate array of test labels    
    indices = range(0,np.shape(testFeatureMatrix)[0])
    testLabels = np.zeros(np.shape(testFeatureMatrix)[0])
    
    for i in indices:
        # Subtract twice the dot product of all points in the training feature
        # matrix and the current test point from the magnitude squared of the
        # each vector in the training feature matrix. 
        distances = mag2 - \
        2.0*np.einsum('ij,j', trainingFeatureMatrix,testFeatureMatrix[i])

        # Classify the point as the class of the closest point from the 
        # training set.
        testLabels[i] = trainingLabels[np.argmin(distances)]

    return testLabels

# Begin evaluation of 1NN classifier
    
N = [1000,2000,4000,8000]

errors = np.zeros((4,10))

# Classify points and determine test error rate for each sample
for n in range(0,4):
    print("Evaluating Training Sample Size: " + str(N[n]))
    for i in range(0,10):
        sel = random.sample(xrange(60000),N[n]) 
        labels = one_NN(ocr['data'][sel], ocr['labels'][sel],ocr['testdata'])
        delta = labels - np.transpose(ocr['testlabels'])
        incorrect = np.count_nonzero(delta)
        errors[n,i] = 1.0*incorrect/np.size(delta)        
 
means = np.mean(errors,1)
stdev = np.sqrt(np.var(errors,1))

plt.errorbar(N, means, yerr=stdev, fmt='o')
plt.axis([500, 8500, 0.04, 0.13])
plt.grid()
plt.xlabel("Number of Training Images") 
plt.ylabel("Test Error Rate")      
plt.title("Test Error Rate for 1-NN Classifier of Handwritten Digits")
plt.savefig('Problem_1.eps', format='eps', dpi=1000)
