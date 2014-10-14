#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wave
import scipy.io.wavfile
import math
import struct
import re
import StringIO
import string

SAMPLEPERSYM = 25
SAMPLE_OFFSET = 10
FRAME_PREAMBLE = "0000000111110"
FRAME_END = "00000000000000000000000000000000000"
FILE =  "/home/jibey/Bureau/SDR/GRC/USRP_Down_FM0.wav"

def arrayToString(array):
	string = StringIO.StringIO()
	for element in array:
		string.write(str(element))
	string = string.getvalue()
	return string

def readSignalInWavFile(waveFile):
	waveHandle = wave.open(waveFile, "r")
	nframe = waveHandle.getnframes()
	signal = waveHandle.readframes(nframe)

	#récupère directement un tableau de INT - /!\ charge mémoire
	#sampleRate, signal = scipy.io.wavfile.read(waveFile)

	return signal

# calcul du seuil: 
#	- transformations des BYTES en INT 
#	- seuillage
#	- stockage dans une chaine de caractère
def threshold(signal,threshold):
	signal = [ 1 if struct.unpack("H", signal[i]+signal[i+1])[0] > threshold else 0 for i in range(0,len(signal),2)]
	return arrayToString(signal)

def clearZeros(signal_string):
	filtre = 32*2*SAMPLEPERSYM*"0"
	filtre_compiled = re.compile(filtre,re.S)
	signal_string = re.sub(filtre_compiled,"",signal_string)
	return signal_string

def clearOnes(signal_string):
	filtre = 32*2*SAMPLEPERSYM*"1"
	filtre_compiled = re.compile(filtre,re.S)
	signal_string = re.sub(filtre_compiled,"",signal_string)
	return signal_string

# on détermine le symbole grace à l'enchainement des échantillons, 
# la boucle FOR permet d'avoir une légère incertitude sur le nombre d'échantillons par symbole
def getBits_stringMatcher(signal_string):
	for nb in range(SAMPLEPERSYM,SAMPLEPERSYM-4,-1):
		filtre0 = nb*"0"
		filtre1 = nb*"1"
		filtre0_compiled = re.compile(filtre0)
		filtre1_compiled = re.compile(filtre1)
		signal_string = re.sub(filtre0_compiled,"0",signal_string)
		signal_string = re.sub(filtre1_compiled,"1",signal_string)
	return signal_string

# on détermine le symbole en prélevant un échantillon au milieu du plateau de chaque symbole
# ATTENTION, cette méthode est sensible au bruit !!!
def getBits_resampler(signal_string):
	sampledSignal = [signal_string[i] for i in range(len(signal_string)) if i%SAMPLEPERSYM == SAMPLEPERSYM/2+SAMPLE_OFFSET]
	return arrayToString(sampledSignal)

#une fois qu'on a récupéré la frame, il faut se souvenir qu'il peut y en avoir d'autres par la suite: penser à retirer la frame trouvée du tableau pour relancer une recherche
def getFrame(bitTrain):
	try:
		preamble = FRAME_PREAMBLE
		preamble_position = re.search(preamble,bitTrain).span()[0]
		end = FRAME_END
		end_position = re.search(end,bitTrain).span()[0]
		bitFrame = bitTrain[preamble_position+len(preamble):end_position]
		bitTrain = bitTrain [end_position:]

		if len(bitFrame) == 0:
			print "No more frame found !"
			return bitTrain, 0

		print "Frame Found !"
		return bitTrain,bitFrame

	except: 
		print "No more frame found !"
		return bitTrain, 0

# bitTrain : avant découpage par frame
# bitFrame : frame découpée
def FM0decode(bitTrain):
	decoDico = {}
	decoDico["01"]=0
	decoDico["10"]=0
	decoDico["11"]=1
	decoDico["00"]=1

	bitTrain, bitFrame = getFrame(bitTrain)

	if bitFrame != 0:
		decodedFrame = StringIO.StringIO()
		while len(bitFrame) > 1:
			# le str() permet que StringIO écrive le 0 
			decodedFrame.write(str(decoDico[bitFrame[:2]]))
			# pas d'overlap
			bitFrame = bitFrame[2:] 
		return decodedFrame.getvalue()
	else:
		return 0

def formatBinString(binString):
	binString += (8-len(binString)%8)*"0"
	binString = ' '.join(re.findall(".{8}",binString))
	return binString

# Importation du .wav dans une liste de BYTES
signal = readSignalInWavFile(FILE)	
signal = threshold(signal,8000)

# Suppression des parties vides du signal
signal = clearZeros(signal)
signal = clearOnes(signal)

# Récupération des bits bruts et décodage
#signal = getBits_stringMatcher(signal)
signal = getBits_resampler(signal)
print "Bits bruts: \n" + str(signal) 
signal = FM0decode(signal)
formattedSignal = formatBinString(signal)
print
print "Bits décodés: \n" + str(formattedSignal)
print 
print "Hexa: \n" +hex(int(str(signal) + (4-len(signal)%4)*"0",2))
print
