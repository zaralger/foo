#! /usr/bin/python
# -*- coding: cp1252 -*-

import fractions
import random
import utl
import base64

GFIELD = 67 # notre premier
SECRET = 19 # secret par defaut
N = 6 # N shares
K = 3 # K elements

## PAS ENCORE GERE : FAIT QUE PRIME=61
## DONC PERTE DE 3 CHAR, A CHOISIR
## ET FAIRE UN TABLEAU DE TRAD
## OU PAS

## 6 BITS

def ascii26bits(char):
	val = 32
	if int(hex(ord(char))[2:],16) > 32:
		if int(hex(ord(char))[2:],16) < 96:
			val = int(hex(ord(char))[2:],16)
	val -= 32
	return val

def sixbits2ascii(val):
	val = int(val)+32
	return chr(val)

def convert_string_6bits(string):
	array = []
	for i in string:
		array += [ascii26bits(i)]
	return array

def convert_6bits_string(array):
	string = ""
	for i in array:
		string += sixbits2ascii(i)
	return string

## MATHS

def euclideEtendu(a, b):
	x,y,u,v =0,1,1,0
	while a!= 0:
		q = b//a
		r = b%a
		m = x-u*q
		n = y-v*q
		b,a,x,y,u,v = a,r,u,v,m,n
	return b,x,y

def get_invA(a, m):
	invA = 0
	if (fractions.gcd(a,m) == 1):
		g, x, y = euclideEtendu(a,m)
		invA = x%m
	return invA

def simple_fractions(num,den):
	k = fractions.gcd(num,den)
	num = num/k
	den = den/k
	return (num,den)

def modulo_fractions(num,den,modulo):
	den = get_invA(den,modulo)
	return (num*den)%modulo

def hardcore_fractions(tfracts):
	tA = []
	tB = []
	for k in tfracts:
		tA += [k[0]]
		tB += [k[1]]

	num = 0
	den = 1
	for i in range(len(tfracts)):
		tnum = tA[i]
		for y in range(len(tfracts)):
			if y != i:
				tnum *= tB[y]
				tnum = tnum
		num += tnum
		den *= tB[i]
	return (num,den)

## CRYPTOFUNCTIONS

def gen_random_values():
	values = []
	for i in range(K-1):
		values += [random.randint(1,GFIELD-1)]
	return values

def poly_calc(X,rvalues):
	Y = SECRET
	for i in range(len(rvalues)):
		Y += (rvalues[i]*pow(X,(i+1)))
	return Y%GFIELD

def create_shares(rvalues):
	shares = {}
	for i in range(N):
		y = i+1
		shares[y] = poly_calc(y,rvalues)
	return shares

def LSF_calc(shares,nb):
	num = 1
	den = 1
	for i in shares:
		if i != nb:
			num *= (-i)
			den *= (nb-i)
	num = (num)
	den = (den)
	return (num,den)

def reconstruction(shares):
	snum = 0
	sden = 1
	secret = 0
	tfracts = []
	for i in shares:

		num,den = LSF_calc(shares,i)		
		num,den = simple_fractions(num,den)
		
		num = (num*shares[i])
		num,den = simple_fractions(num,den)

		tfracts += [[num,den],]

	hfract = hardcore_fractions(tfracts)
	return hfract

def K_shares(shares,nb):
	# mazel tov !
	return dict(random.sample(shares.items(),nb))

def pretreat_string(string):
	#string = str(string).upper()
	#array6 = convert_string_6bits(string)
	string = base64.b64encode(string)
	msgB64_array = []
	for i in string:
		#retrait du padding pour la base64
		if i != '=':
			msgB64_array += [utl.base64ToInt(i)]
	
	return msgB64_array

def posttreat_string(msg):
	msg = msg + "=" * (4 - len(msg) % 4)
	msg = base64.b64decode(msg)
	return msg

def sending_routine(array, conf):
	global SECRET
	K = conf["shamir_k"]
	N = conf["shamir_n"]
	
	karray = []
	
	for i in array:
		SECRET = i
		rvalues = gen_random_values()

		shares = create_shares(rvalues)
	
		#ici on envoie le maximum de redondance possible, on peut réduire à des fins de test
		kshares = K_shares(shares,N)
		karray += [kshares]
		

	return karray

def receiving_routine(karray, conf):
	K = conf["shamir_k"]
	N = conf["shamir_n"]
	
	farray = []
	newstring = []
	for kshares in karray:
		hfract = reconstruction(kshares)
		farray += [modulo_fractions(hfract[0],hfract[1],GFIELD)]
		#newstring = convert_6bits_string(farray)
	for i in farray:
		#print i
		newstring += [utl.intToBase64(i)]
	newstring = ''.join(newstring)
	return newstring

#string = "AZErtyUIOP123('?-!*&²_"
#print string
#array6 = pretreat_string(string)
#karray = sending_routine(array6)
#newstring = receiving_routine(karray)
#print newstring
