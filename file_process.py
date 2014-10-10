#-*-coding:Utf-8 -*

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
	f = open(fileName,'r')
	dataList = f.readlines() 
	dataList = [word.strip() for word in dataList]
	return dataList
	
def readWholeFile(fileName):	
	f = open(fileName,'r')
	dataString = f.read() 
	return dataString
