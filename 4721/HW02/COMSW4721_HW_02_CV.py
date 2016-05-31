# This function performs 10 fold cross validation and was bult for COMSW4721 
# HW 02 authored by Patrick Rogan, UNI: psr2125, email: psr2125@columbia.edu

# Algorithm for performing 10 fold CV. Takes in a matrix of training data where
# the rows are the data points and the columns the features, a vector of labels
# for the training data, and a learning algorithm.
    # Function Inputs: 
    #
    # trainingData: an N x M matrix of samples, features
    # trainingLabels: an N x 1 vector of labels
    # learningAlgorithm: a function that corresponds to a machine learning
    #                    algorithm
    #
    # Function Outputs
    #
    # score: a tuple containing the cross validation error rate and the 
    #        associated estimated standard error.

def CV(trainingData, trainingLabels, learningAlgorithm):
    import numpy as np
    import random 
    
    errors = np.zeros(10) #initialize errors to 0
    
    # We have no idea if our data is ordered in any way, so we select the 10
    # folds at random (using a set seed so the algorithm appears deterministic)
    # and then apply CV.
    
    # Determine the number of points to put into each fold
    N = np.repeat(len(trainingLabels)/10,10) 
    random.seed(100)
    N[random.sample(range(0,10),len(trainingLabels)%10)] += 1    
    
    points = set(range(0,len(trainingLabels)))
    folds = []
    for i in range(0,10):
        random.seed(100)
        foldIndices = random.sample(points, N[i])
        folds.append(foldIndices)
        points = set.difference(points, set(foldIndices))
    
    # Run cross validation on the partitions as determined above    
    for i in range(0,10):
        # Get training and test indices for this fold
        trainingIndices = list(set.difference(set(range(0,len(trainingLabels))),
                                         folds[i]))
        testIndices = list(folds[i])
        
        # Train and test algorithm; save error rate for fold. Note the slightly
        # different ways of testing the sklearn algorithms and the home made
        # algorithm.
        params = learningAlgorithm.fit(trainingData[trainingIndices], 
                                       trainingLabels[trainingIndices])        

        if "sklearn" in str(type(learningAlgorithm)):
            errors[i] = 1 - learningAlgorithm.score(trainingData[testIndices], 
                        trainingLabels[testIndices])
        else:
            labels = learningAlgorithm.test(trainingData[testIndices], params)    
            delta = labels - np.transpose(trainingLabels[testIndices])
            incorrect = np.count_nonzero(delta)
            errors[i] = 1.0*incorrect/np.size(delta)  

    score = (np.mean(errors) ,np.sqrt(np.var(errors)))
    return score

    
    