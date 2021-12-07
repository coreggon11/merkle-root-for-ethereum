'''
Merkle Root Implementation in Python, the script assumes data is contained in csv file and each line in the file
represents a new transaction,
Currently supports calculating the merkle root of a large data set contained inside the csv file,
next feature, how to validate a single data point without traversing the whole file
SOURCE CODE FROM https://github.com/anudishjain/Merkle-Tree/blob/master/MerkleScript.py
original source code updated because hashlib uses different hashing than ethereum's keccak256
ALSO THE ORIGINAL CODE NOT WORKING LOL
'''

import json
from csv import *
from web3 import Web3
import time

filePath = "./docs/airdrop2.csv"
# absolute or relative path to the csv file containing the transactions or data '''

fileOpen = open(filePath, 'rU')
# opening the file for reading in Universal NewLine (rU) 

fileReader = reader(fileOpen)
# initializing the CSV Reader for traversing data inside the csv file

storeHash = []
# list to store the hashes as they are calculated

parents = {}
siblings = {}

i = 0

for row in fileReader :

	for tnx in row :
	
		end = str(tnx).__len__() - 1
		hash = Web3.keccak(hexstr = str(tnx)[:end])
		storeHash.append(hash)
		i += 1
		print('{} hashes added'.format(i))

		# calculate hash row wise and save them in the storeHash

if (len(storeHash) % 2 != 0) :
	storeHash.append(storeHash[-1])

	'''
	Merkle Tree is a complete binary tree, 
	so if the number of inputs from CSV are odd, we duplicate the last record's hash in the list
	'''

operations = 0
total = 0

startTotal = time.time()

while (len(storeHash)> 1) : 
	# we run the loop till we don't get a single hash

	start = time.time() * 1000

	for i in range(0, len(storeHash) - 1, 2) : 

		hash = Web3.keccak(storeHash[i] + storeHash[i+1])
		parents[storeHash[i].hex()] = hash.hex()
		parents[storeHash[i+1].hex()] = hash.hex()
		siblings[storeHash[i].hex()] = storeHash[i+1].hex()
		siblings[storeHash[i+1].hex()] = storeHash[i].hex()
		storeHash[i // 2] = hash
		# hash of the i th leaf and i + 1 th leaf are concatenated
		# to find the hash parent to the both

	del storeHash[-len(storeHash)//2:]

	operations += 1
	elapsed = (time.time() * 1000) - start
	total += elapsed
	average = total / operations
	reamining = len(storeHash)
	secs = (average * reamining) / 1000
	print('Hash eliminated in {} millis. {} hashes remaining. Average {} millis per hash. Estimated {} seconds ({} minutes) remaining'.format(elapsed, reamining, average, secs, secs / 60))
	# as we now have the hash to the upper level of the tree, we delete the extra space in the array.
	# in each iteration of this loop the size of the storeHash list is halved.

merkleFile = open('merkle.csv', 'w')
# create the file for saving the merkle root

jsonString = json.dumps(parents)
jsonFile = open("./parents.json", "w")
jsonFile.write(jsonString)
jsonFile.close()

jsonString = json.dumps(siblings)
jsonFile = open("./siblings.json", "w")
jsonFile.write(jsonString)
jsonFile.close()

print('Finished in {} seconds.'.format(time.time() - startTotal))

write = writer(merkleFile)

write.writerow(storeHash)

print('merkle root: {}'.format(storeHash))
# write to the file in simple text mode
