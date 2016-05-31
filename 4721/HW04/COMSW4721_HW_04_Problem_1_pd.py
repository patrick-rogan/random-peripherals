# This is a supporting file for COMSW4721 HW 04 authored by Patrick Rogan,
# UNI: psr2125, email: psr2125@columbia.edu
#
# This file reads in two three column matrices of movie reviews (one 
# training data and the other test data) and executes several iterations
# of the regularized version of the Alternating Least Squares (ALS) algorithm.
#
# Script was run using Python 3.4.3

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def clip(z):
	"""Return clipped input parameter
	"""
	if z < 1:
		return 1
	elif z > 5:
		return 5
	else:
		return z

# Read in train movie ratings file, change indices from 1 to 0 base
ratings = pd.read_csv('ratings_train.csv',header=None)
ratings.iloc[:,0] = [r-1 for r in ratings.iloc[:,0]]
ratings.iloc[:,1] = [r-1 for r in ratings.iloc[:,1]]

pairsTr = list(zip(ratings.iloc[:,0],ratings.iloc[:,1]))

# Set up parameter definitions
mu = ratings.iloc[:,2].mean()
m = 943
n = 1682
lambd = 10

# Create a matrix A[i,j] populated by movie reviews
A = np.zeros([m,n])
for l in range(0,len(ratings)):
	A[ratings.iloc[l,0],ratings.iloc[l,1]] = ratings.iloc[l,2]

# Read in test movie ratings file, change indices from 1 to 0 base
ratingsTe = pd.read_csv('ratings_test.csv',header=None)
ratingsTe.iloc[:,0] = [r-1 for r in ratingsTe.iloc[:,0]]
ratingsTe.iloc[:,1] = [r-1 for r in ratingsTe.iloc[:,1]]

pairsTe = list(zip(ratingsTe.iloc[:,0],ratingsTe.iloc[:,1]))

# Create a matrix ATE[i*,j*] populated by movie reviews. The dimensionality is
# larger than needed, but this doesn't have a meaningful impact on performance
# or any impact on the result.
ATE = np.zeros([m,n])
for l in range(0,len(ratingsTe)):
	ATE[ratingsTe.iloc[l,0],ratingsTe.iloc[l,1]] = ratingsTe.iloc[l,2]

# Draw u and v from a N(0,(1/k)I) distribution
k = 10
mean = 0
var = 1/k 

u = np.empty([m,k])
v = np.empty([n,k])

# Note these are larger than required this was done so delberately to make 
# subsequent indexing easier
for i in range(0,m):
	u[i,:] = np.random.normal(mean, var, k)

for j in range(0,n):
	v[j,:] = np.random.normal(mean, var, k)

# Define the number of ALS iterations and initialize some additional 
# parameters to 0
T = 40
b = np.zeros(m)
c = np.zeros(n)
L = np.zeros(T)
test_RMSE = np.zeros(T)

# Execute the ALS algorithm for T iterations, note that if a row in A[i,j] is empty 
# (all values are zero) an update for b and u or c and v will not be performed.
for t in range(0,T):

	# Update b
	for i in range(0,m):
		if sum(A[i,:]) != 0:
			moviesR = list(ratings.iloc[:,1][ratings.iloc[:,0] == i])
			b[i] = -1*(sum(np.dot(u[i,:],np.transpose(v[moviesR,:]))) + \
				len(moviesR)*mu - sum(A[i,:]) + \
				c[moviesR].sum())/len(moviesR)
	# Update u
	for i in range(0,m):
		if sum(A[i,:]) != 0:
			moviesR = list(ratings.iloc[:,1][ratings.iloc[:,0] == i])
			mult = [(mu - A[i,j] + c[j] +b[i]) for j in range(0,n)]
			uSum = [v[j,:]*mult[j] for j in moviesR]
			mx = np.zeros([k,k]) 
			for j in moviesR:
				mx += np.outer(v[j,:],v[j,:])
			mx += 2*lambd*np.identity(k) 
			mxi = np.linalg.inv(mx)
			u[i,:] = -1*np.dot(mxi,np.einsum('mk->k',uSum))

	# Update c
	for j in range(0,n):
		if sum(A[:,j]) != 0:
			viewerR = list(ratings.iloc[:,0][ratings.iloc[:,1] == j])
			c[j] = -1*(sum(np.dot(u[viewerR,:],np.transpose(v[j,:]))) + \
				len(viewerR)*mu - sum(A[:,j]) + \
				b[viewerR].sum())/len(viewerR)

	# Update v
	for j in range(0,n):
		if sum(A[:,j]) != 0:
			viewerR = list(ratings.iloc[:,0][ratings.iloc[:,1] == j])
			mult = [(mu - A[i,j] + c[j] +b[i]) for i in range(0,m)]
			vSum = [u[i,:]*mult[i] for i in viewerR]
			mx = np.zeros([k,k])
			for i in viewerR:
				mx += np.outer(u[i,:],u[i,:]) 
			mx += 2*lambd*np.identity(k) 
			mxi = np.linalg.inv(mx)	
			v[j,:] = -1*np.dot(mxi,np.einsum('mk->k',vSum))

	# Calculate regularized log likelihood
	for pair in pairsTr:
		L[t] += -1/2*(np.dot(u[pair[0],:],np.transpose(v[pair[1],:])) + \
			b[pair[0]] + c[pair[1]] + mu - A[pair[0],pair[1]])**2

	l2_u = np.sum([np.dot(u[i,:],u[i,:]) for i in range(0,m)])
	l2_v = np.sum([np.dot(v[j,:],v[j,:]) for j in range(0,n)])
	L[t] = L[t] - lambd*(l2_u + l2_v)

	# Calculate test RMSE
	sum_clipped_squared = 0
	for pair in pairsTe:
		sum_clipped_squared += (clip(np.dot(u[pair[0],:],np.transpose(v[pair[1],:])) + \
		b[pair[0]] + c[pair[1]] + mu) - ATE[pair[0],pair[1]])**2

	test_RMSE[t] = (1/(len(pairsTe))*sum_clipped_squared)**(0.5)

# Plot figures
plt.scatter(list(range(1,T+1)), L)
plt.axis([0,T+1,L.min()*1.1,L.max()*0.9])
plt.grid()
plt.xlabel("ALS Iteration #") 
plt.ylabel("Regularized Log Likelihood")      
plt.title("Regularized Log Likelihood vs ALS Iteration")
plt.savefig('Problem_1d1.eps', format='eps', dpi=1000)
plt.close()

plt.scatter(list(range(1,T+1)), test_RMSE)
plt.axis([0,T+1,test_RMSE.min()*0.9,test_RMSE.max()*1.1])
plt.grid()
plt.xlabel("ALS Iteration #") 
plt.ylabel("Test RMSE")      
plt.title("Test RMSE vs ALS Iteration")
plt.savefig('Problem_1d2.eps', format='eps', dpi=1000)
plt.close()
