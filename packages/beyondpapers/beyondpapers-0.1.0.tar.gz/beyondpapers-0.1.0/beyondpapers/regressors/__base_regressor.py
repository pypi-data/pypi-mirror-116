import numpy as np


##### Base Gratient Descent ####
class GradientDescentRegressor:
    
    
    def __init__(self,iterations=100,learning_rate=0.01,weights=np.nan,verbose=False,random_state=100):
        ''' 
            """ Vanilla Gradient Descent Algorithm 

            Read more in the :ref: https://github.com/beyond-papers/beyondpapers

            Parameters
            ----------
            iterations : int , default 100
                Set number of iterations to run.
            learning_rate : float , classifier function, default=0.01
                Set learning rate  of the model.    
            weights : array , default np.nan
                weights make gradient descent learn incrementally. Calling fit on the model will reuse the weights.
            random_state : int , default 100
                random state can be change for different random weight initialisation.
            
            """
        '''
        self.iterations,self.learning_rate,self.weights,self.verbose,self.random_state =\
        iterations,learning_rate,weights,verbose , random_state
     
    def fit(self,X,y):
        np.random.seed(self.random_state) 
        num_features = X.shape[1]
        #Initialisations
        iterations,learning_rate,weights=self.iterations,self.learning_rate,self.weights
        
        ### Intialise Weights if not exist
        if weights is np.nan:
            bias=np.array(0.0)
            feature_weights=np.random.rand(num_features)
            weights = np.hstack([bias,feature_weights]).T
        ### Transfer Weights    
        else:
            weights = self.weights
            
        ### Add bias col for bias
        bias_col = np.ones(X.shape[0]).reshape(X.shape[0],1)
        X = np.hstack([bias_col,X]).T    
       
        for i in range(iterations):
            ypred=np.dot(weights,X)

            error = ypred - y

            sum_of_squared_error = sum(error**2)
            delta_gradient = learning_rate*np.dot(X,error)/X.shape[1] 

            weights =weights-delta_gradient
        
            self.weights = weights
            
            if self.verbose == True:
                print('Iterarion error {}: {} '.format(i,sum_of_squared_error))
            
    def predict(self,X):
        bias_col = np.ones(X.shape[0]).reshape(X.shape[0],1)
        X = np.hstack([bias_col,X]).T 
        ypred=np.dot(self.weights,X)
        return ypred
    


    