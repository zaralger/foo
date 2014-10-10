#-*-coding:Utf-8 -*

import timeit
import random
import utl
REGISTRE_CIPHER = {}
REGISTRE_DECIPHER = {}

#permet de repérer une période dans un registre deja généré
def toirtoise_and_hare(initVect):
	#print "recherche de période"
	tic = timeit.default_timer()
	
	steps = 0
	tab = []
	
	while True:
		#try: 
			hare = next(REGISTRE_CIPHER[initVect])[1]
			tab += [hare]
			hare = next(REGISTRE_CIPHER[initVect])[1]
			tab += [hare]
			tortoise = tab[steps]
			steps +=1
		
			if hare == tortoise:
				toc = timeit.default_timer()
				spent_time = toc-tic
				#print "Temps de calcul de boucle:" + str(spent_time) +" sec."
				#print "boucle de " + str(steps)
				return steps
	
		#except:
		#	break 

	return 0

def lfsr(seed, taps):
	sr = seed
	nbits = seed.bit_length()
	while True:
		xor = 1
		for t in taps:
			if (sr & (1<<(t-1))) != 0:
				xor ^= 1
		sr = (xor << nbits-1) + (sr >> 1)
		yield xor, sr

#cyclique si masK > seed
def lfsr2(seed, mask):
	result = seed
	nbits = mask.bit_length()-1
    	while True:
		result = (result << 1)
		xor = result >> nbits
		if xor != 0:
			result ^= mask

		yield xor, result

# [0] => nb Bits
# [1] => nb Ones
# [2] => nb Zeros
def bitLenCount(int_type):
	length = 0
	ones = 0
	while (int_type):
		ones += (int_type & 1)
		length += 1
		int_type >>= 1
	zeros = length - ones
	return(length, ones, zeros)

#genere un LFSR (vecteur d'initialisation aléatoire et taps)
#genere un registre depuis ce LFSR
#renvoie le vecteur d'initialisation qui servira de clé pour indexer le registre

def startSenderSession(size,taps=[2,1],test=False):
	
	#genere un nouveau vecteur d'initialisation de la taille des briques à chiffrer
	initVect = 1<<(size-1) ^ random.randint(0, 2**(size-2))
	
	#genere le registre correspondant et le place en mémoire
	REGISTRE_CIPHER[initVect] = lfsr(initVect,taps)

	if test:
		return toirtoise_and_hare(initVect)	
		
	return initVect	

def startReceiverSession(initVect,taps=[2,1]):
	size = initVect.bit_length()
	
	REGISTRE_DECIPHER[initVect] = lfsr(initVect, taps)

#le sessionID correspond au vecteur d'initialisation utilisé pour générer le registre
def ciphering(msg, initVect):
	try:
		vect = next(REGISTRE_CIPHER[initVect])[1]
	except:
		list(REGISTRE_CIPHER[initVect])[1]

	msg=utl.xor(vect,msg)		
	return msg

def deciphering(msg,initVect):
	try:
		vect = next(REGISTRE_DECIPHER[initVect])[1]
	except:
		list(REGISTRE_CIPHER[initVect])[1]

        msg=utl.xor(vect,msg)
        return msg

def initiateurRegistre(size):
	initVect=startSenderSession(size)
	startReceiverSession(initVect)
	return initVect

def tester(msg,initVect):
	cipherMsg=ciphering(msg,initVect)
	
	msgClair=deciphering(cipherMsg,initVect)

	if (msg == msgClair):
		print "ok"
	else: 
		print "erreur: décodé en",
		print msgClair
	
	return msgClair
