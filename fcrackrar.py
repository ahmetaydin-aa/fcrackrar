from unrar import rarfile
from unrar.rarfile import BadRarFile

import sys, getopt
import os

def main(argv):
	inputfile = ''
	wordfile = ''
	try:
		opts, args = getopt.getopt(argv,"hi:w:",["ifile=","wfile="])
	except getopt.GetoptError:
		print('fcrackrar.py -i <inputfile> -w <wordlistfile>')
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print('fcrackrar.py -i <inputfile> -w <wordlistfile>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-w", "--wfile"):
			wordfile = arg

	if inputfile == '' or wordfile == '':
		print('fcrackrar.py -i <inputfile> -w <wordlistfile>')
		sys.exit(2)


	rar = rarfile.RarFile(inputfile)
	names = rar.namelist()
	filename = ".".join(rar.filename.split(".")[0:-1])

	wordlist = open(wordfile, "r")
	password = find_pass(rar, names[0], wordlist)

	if password == "":
		print("!!! KEY CANNOT BE FOUND IN WORDLIST !!!")
	else:
		extract_files(rar, password, names, filename)

def find_pass(rar, name, wordlist):
	password = ""

	for	line in wordlist:
		line = line[:-1]
		print("{}".format(line))
		try:
			data = rar.read(name, line)
			if data != b'':
				password = line
				print("KEY FOUND [ {} ]".format(password))
				break
		except BadRarFile:
			pass
		except Exception as e:
			print("Error!\n{}".format(e))
			wordlist.close()
			sys.exit(1)

	wordlist.close()
	return password

def extract_files(rar, password, names, filename):
	for name in names:
		ext_file_path = "./" + filename + "/" + name
		os.makedirs(os.path.dirname(ext_file_path), exist_ok=True)
		
		ext_file = open(ext_file_path, "wb")
		ext_file.write(rar.read(name, password))
		ext_file.close()


if __name__ == "__main__":
	main(sys.argv[1:])