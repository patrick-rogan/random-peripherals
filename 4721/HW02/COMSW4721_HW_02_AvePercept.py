# 64 Pass Averaged-Perceptron  
# Uses the Online Perceptron algorithm 64 times and averages the resulting 
# weight vectors and scalar biases to form one weight vector and bias. 
class classifier:
    
    @staticmethod
    def fit(trainingFeatureMatrix, trainingLabels):
    # Averaged Perceptron classifier, a function that produces weight vector
    # and bias values by running the Online Perceptron algorithm 64 times and
    # averaging the results
    # 
    # Function Inputs: 
    #
    # trainingFeatureMatrix: an N x M matrix of samples, features
    # trainingLabels: an N x 1 vector of labels
    #
    # Function Outputs
    #
    # params: a dict of parameter estimates weight_v and bias
        import numpy as np
        import random 

        w = np.zeros(np.shape(trainingFeatureMatrix)[1])
        b = 0

        params = {'weight_v':w, 'bias':b, 'cached_wt':w, 'cached_bias':b,
                    'counter': 1}        

        for i in range(0,64):
            indices = random.sample(range(0,np.shape(trainingFeatureMatrix)[0]),
            np.shape(trainingFeatureMatrix)[0])            
            
            tempFeatureMatrix = trainingFeatureMatrix[indices]            
            tempLabels = trainingLabels[indices]
           
            for i in range(0,np.shape(tempFeatureMatrix)[0]):
                if tempLabels[i]*(np.dot(params['weight_v'],
                    tempFeatureMatrix[i]) + params['bias']) <= 0:
                    
                    params['weight_v'] = params['weight_v']  +\
                    tempLabels[i]*tempFeatureMatrix[i]
                    
                    params['bias'] = params['bias'] + tempLabels[i]
                
                    params['cached_wt'] = params['cached_wt'] + \
                    tempLabels[i]*tempFeatureMatrix[i]*params['counter'] 
                
                    params['cached_bias'] = params['cached_bias'] + \
                    tempLabels[i]*params['counter'] 
                    
                params['counter'] += 1

        w = params['weight_v'] - 1/params['counter']*params['cached_wt']
        b = params['bias'] - 1/params['counter']*params['cached_bias']

        final_params = {'weight_v':w, 'bias':b}
        return final_params
    
    @staticmethod
    def test(testFeatureMatrix,params):
    # Averaged Perceptron classifier, takes test data and produces class labels
    #
    # Function Inputs: 
    #
    # testFeatureMatrix: an N x M matrix of samples, features
    # params: a dict of a weight vector and bias
    #    
    # Function Outputs
    #
    # preds: a M x 1 vector of labels produced by the classifier 
        import numpy as np    
        preds = np.einsum('ij,j->i',testFeatureMatrix,params['weight_v']) +\
        params['bias']
    
        return np.sign(preds)