# Python3 implementation of the approach 

# import random module
import random

# Function to return the next 
# random number 
def getNum(v) :

	# Size of the vector 
	n = len(v)

	# Generate a random number within
	# the index range
	index = random.randint(0, n - 1)

	# Get random number from the vector 
	num = v[index] 

	# Remove the number from the vector 
	v[index], v[n - 1] = v[n - 1], v[index]
	v.pop() 

	# Return the removed number 
	return num-1

# Function to generate n non-repeating 
# random numbers 
def generateRandom(n) :
	
	v = [0] * n

	# Fill the vector with the values 
	# 1, 2, 3, ..., n 
	for i in range(n) : 
		v[i] = i + 1

	# While vector has elements get a 
	# random number from the vector 
	# and print it 
	while (len(v)) :
		print(getNum(v), end = " ") 

# Driver code 
if __name__ == "__main__" :
	
	n = 25
	generateRandom(n)
	
# This code is contributed by Ryuga
