#!/usr/bin/python2.7 by kuronosuFear
import io
import zlib
import numpy as np
from sets import Set
import os

def dword2int(dword):
	#dword = int(dword.encode('hex'),16)
	return int(np.fromstring(dword, dtype=int))

# Load the file
ver='ver05'
path = 'Elder-Extracted-v5\\'

with open(ver + '.yke', 'rb') as f:
    rawData = f.read()

XORkeyOffset=96
XORkey=rawData[XORkeyOffset:XORkeyOffset+32]
index=0
watchData = bytearray()

for x in range(len(rawData)):
	watchData.append(ord(rawData[x])^ord(XORkey[index]))
	index=index+1
	if index>=32:
		index=0

with open(ver + '.ykd', 'wb') as fo:
	fo.write(watchData)

watchData=str(watchData)

if (dword2int(watchData[:4])==0x004b0059): #compare first 4-bytes to the marker
	print 'Correct File Found!'
else:
	print 'Incorrect File Found... Aborting'
	quit()

StartingOffset = 1048576

numberOfEntries = dword2int(watchData[StartingOffset:StartingOffset+4])
print str(numberOfEntries) + " entries found"

StartOfData = (numberOfEntries * 4) + 4 + StartingOffset

if not os.path.exists(os.path.dirname(path)):
	try:
		os.makedirs(os.path.dirname(path))
	except OSError as exc: # Guard against race condition
		if exc.errno != errno.EEXIST:
			raise

for entryNum in range(1,numberOfEntries+1):
	entryOffset = dword2int(watchData[StartingOffset+entryNum*4:StartingOffset+entryNum*4+4]) + StartingOffset
	sizeOfEntry = dword2int(watchData[entryOffset:entryOffset+4])
	#with open(path + "%08d"%(entryNum,)+"-%08d"%(sizeOfEntry,)+'.ykx', 'wb') as fo:
	with open(path + "%08d"%(entryNum,)+'.ykx', 'wb') as fo:
		fo.write(watchData[entryOffset+4:entryOffset+4+sizeOfEntry])
