import os,sys

#indiquer le dossier cible en argument
folder = sys.argv[1]

extension_source=".cbr"
extension_dest=".rar"

for filename in os.listdir(folder):
	infilename = os.path.join(folder,filename)
	if not os.path.isfile(infilename): continue
	oldbase = os.path.splitext(filename)
	newname = infilename.replace(extension_source, extension_dest)
	output = os.rename(infilename, newname)
	print filename
