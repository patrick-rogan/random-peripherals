# Load prerequsite packages and data
from scipy.io import loadmat
import numpy as np
import pickle
import csv

news = loadmat('news.mat') # load data

def train_NB(trainingFeatureMatrix, trainingLabels):
    # Naive Bayes classifier, a function that produces parameter estimations 
    # for mu_hat[y,i] and pi_hat[y]
    #
    # Function Inputs: 
    #
    # trainingFeatureMatrix: an N x 61188 matrix of training data 
    # trainingLabels: an N x 1 vector of training labels
    #
    # Function Outputs
    #
    # params: a dict of parameter estimates mu_hat and pi_hat

    numTrainingPoint = np.shape(trainingFeatureMatrix)[0]

    pi_hat = np.zeros(len(np.unique(trainingLabels))) # priors, one for each
                                                      # class
    
    mu_hat = np.zeros([len(np.unique(trainingLabels)),  
                      np.shape(trainingFeatureMatrix)[1]])
    # d x y matix of estimates for parameter mu_hat (for the hw this will be
    # 20 x 61188)

    denom = np.zeros(len(np.unique(trainingLabels))) #denominator portion of 
                                                     # mu_hat for each y
    # Calcultate Priors by MLE 
    for i in range(0,len(np.unique(trainingLabels))):
        sum_y = sum(trainingLabels == (i+1))[0]
        pi_hat[i] = 1.0*sum_y/numTrainingPoint
        denom[i] = 1.0*sum_y + 2 #denominator portion of mu_hat for each y

    # Calculate mu_hat by Laplace smoothing
    for i in range(0,len(np.unique(trainingLabels))):    
        relePts = \
        trainingFeatureMatrix[(np.transpose(trainingLabels==(i+1)))[0],:]       
        
        for j in range(0,np.shape(trainingFeatureMatrix)[1]):
            mu_hat[i,j] = (1 + relePts[:,j].sum())/denom[i] 
            
    params = {'mu_hat':mu_hat, 'pi_hat':pi_hat}
    
    return params

def classify_NB(params, testFeatureMatrix):
    # Naive Bayes classifier, a that takes parameter estimates from train_NB
    # and classified data.
    #
    # Function Inputs: 
    #
    # params:
    # testFeatureMatrix: an M x 61188 matrix of test data 
    #
    # Function Outputs
    #
    # preds: a M x 1 vector of labels produced by the classifier 

    # preallocate and densify for speed since sparse-nonsparse einsum 
    # operations don't seem to be supported 
    preds = np.zeros(np.shape(testFeatureMatrix)[0])
    testFeatureMatrix = testFeatureMatrix.todense()
    
    # create terms that do not change based on which test point is being 
    # scored
    m = np.log(1-params['mu_hat'])
    n = np.einsum('ij->i',m) + np.log(params['pi_hat'])
    lp = np.log(params['mu_hat'])    

    # predict class label    
    for s in range(0,np.shape(testFeatureMatrix)[0]):
        predict = np.einsum('ij,kj->k',testFeatureMatrix[s,:], lp) -\
        np.einsum('ij,kj->k', testFeatureMatrix[s,:], m)  + n
        preds[s] = np.argmax(predict)
    return preds

# if the classifier has already been fit load it, if not create and save
try:
    params = pickle.load(open("params.p","rb"))
except IOError:
    params = train_NB(news['data'], news['labels'])
    pickle.dump(params,open("params.p","wb"))

# Produce test and training points
trainLabeled = classify_NB(params, news['data'])
testLabeled = classify_NB(params, news['testdata'])

# Calculate training error rate
deltaTrain = trainLabeled - (np.transpose(news['labels'])-1) #change
#the class labels to 0 based instead of 1 to match 0 indexing
incorrectTrain = np.count_nonzero(deltaTrain)
trainErrorRate = 1.0*incorrectTrain/np.size(deltaTrain)   
print("Train Error Rate: " + str(trainErrorRate))

# Calculate test error rate
deltaTest = testLabeled - (np.transpose(news['testlabels'])-1)
incorrectTest = np.count_nonzero(deltaTest)
testErrorRate = 1.0*incorrectTest/np.size(deltaTest)   
print("Test Error Rate: " + str(testErrorRate))

# Part c: calculate alpha_{y,j} values
vocab = open('news.vocab') 
vocab = vocab.readlines()
vocab = [word.rstrip('\n') for word in vocab]
alphas = np.zeros(np.shape(params['mu_hat']))
wordsFinal = []

# since we would end up adding alpha_{y,0} to all terms, we don't need to 
# calculate it here, instead we just get the alpha{y,j} terms
for y in range(0,len(params['pi_hat'])):
    alphas[y,:] = np.log(params['mu_hat'][y,:]) - \
    np.log(1-params['mu_hat'][y,:])    
    args = np.argsort(alphas[y,:])    
    args = args[::-1][0:20]
    args = args[0:20]
    words = [vocab[arg] for arg in args]
    wordsFinal.append(words)

# save data to be included in writeup
with open("wordsFinal.csv","wb") as fileN:
    writeOut = csv.writer(fileN,delimiter='&')
    writeOut.writerows(wordsFinal)