#-*-coding:Utf-8 -*

from math import *
import binascii
import struct


#################################
##    UNIFIED TOOLS LIBRARY    ##
#################################

#-------------------------
### I/O Tools
#-------------------------

def stringCutter(string,MAXSIZE=10):
	if len(string) >= MAXSIZE:
		split = int(floor(MAXSIZE/3))
		str1 = string[:split]
		str2 = " ... "
		str3 = string[len(string)-(MAXSIZE-(split - len(str2))):]
		string = str1 + str2 + str3
	return string
	
#-------------------------
### File Managing
#-------------------------

#la dataList correspond aux éléments à écrire dans le fichier
#chaque case du tableau sera une nouvelle ligne du fichier
def writeArrayInFile(fileName, dataList):
	f = open(fileName, 'w')
	for line in dataList:
		f.write(str(line))
		f.write("\n")
	f.close()

#écris à la fin du fichier sans écraser le contenu précédent
def writeArrayInFileEnd(fileName, dataList):
	f = open(fileName, 'a')
	for line in dataList:
		f.write(str(line))
		f.write("\n")
	f.close()

def writeInFile(fileName, data):
	f = open(fileName, 'w')
	f.write(str(data))
	f.write("\n")
	f.close()

#de meme que la fonction d'écriture, cette fonction renvoie
#une liste avec une ligne du fichier par case
def readFile(fileName):
	f = open(fileName,'rb')
	dataList = f.readlines() 
	dataList = [word.strip() for word in dataList]
	return dataList

#-------------------------
### Hexa Tools
#-------------------------

# "EB 76 90 " => 0xEB7690 = 15431312
def dumpStringToHexInt(dumpString):
	dumpString = dumpString.replace(" ", "")
	dumpHex = int(dumpString, 16)
	return dumpHex

# "EB 76 90 " => ".v."
def dumpStringToText(dumpString):
	dumpString = dumpString.replace(" ", "")
	dumpText = dumpString.decode("hex")
	return dumpText
	
# "EB 76 90 " => "0xeb7690"
def dumpStringToHexString(dumpString):
	dumpString = dumpString.replace(" ", "")
	return "0x"+dumpString.lower()

# "0x90ab12cd" => "0xcd12ab90"
# nbBytes: 3
def littleEndian(hexaString):
	x = hexaString[2:].decode("hex")
	x = x[::-1]
	x = x.encode("hex")
	return "0x"+x
	
#-------------------------
### Binary Tools
#-------------------------

#transform string like "010001" or "0b1010103" to an integer 
def stringToBinary(string):
	binaryNb = int(string,2)
	return binaryNb

# 101 => 0b101 = 5
def intToBinary(integer):
	return int(str(integer),2)

# [1,0,1] => 101
def listToInteger(array):
	return int(''.join(map(str,array)))

# [1,0,1] => 0b101 = 5
def listToBinary(array):
	return intToBinary(listToInteger(array))

# 5 => [1,0,1]
# nbBit permet de paramétrer le nombre de Bits de poid fort à 0
def integerToBitList(integer, nbBit=0):
	nbBit = nbBit + 2
	bitList = [int(bit) for bit in format(integer,'#0'+str(nbBit) +"b")[2:]]
	return bitList

# 0xeb7690 => [0xeb, 0x76, 0x90]
def integerToBytesArray(integer, nbBytes):
	bytesArray = [int(hex(integer >> i & 0xff)[:-1],16) for i in range(8*nbBytes,0,-8)+[0]]	
	return bytesArray

def hexaStringToBinaryString(hexaString):
	binaryString = bin(int(hexaString, 16))[2:]
	return binaryString
