N, nombre = 1000000, 2 
liste, liste[1] = range(N+1), 0
 
while nombre**2 <= N:
	liste[nombre*2 :: nombre] = [0]*len( liste[nombre*2 :: nombre] )
	nombre += 1
print(filter(None, liste))
