import coverage
import pytest as py
import optparse 
import os
import json
import logging
import pathlib
import Hash

def covreageData(src_file, file):
	data = []
	readTest(src_file,data)
	if not data:
		print('no file test_ files has been found in ', file, ' directory')
		return
	f = open("test_1c.py", "w")
	func = ("""
import coverage
import pytest as py
""" + data[0] + """
def test_add():
	cov = coverage.Coverage()
	flag = 0 
	""")


	#---------------------------------
	test = ("""
	cov.start()
	try:""")
	i = '0'
	j=0

	#------------------------------------
	test2 = ("""
	except Exception:
		flag = 0
	cov.stop()
	if flag == 1:
		out = passs+"/testPassed" +'""")
	test3 = ("""'+ ".json"
		cov.json_report(outfile=out)
	else:
		out = faill+"/testFailed" +'""")
	test4 =  ("""'+ ".json"
		cov.json_report(outfile=out)
	cov.erase()
		""")
	os.system("mkdir pass")
	os.system("mkdir faill")
	f.write(func)
	data.pop(0)
	for line in data:
			
		f.write(test + line +"\n		flag=1" + test2 + i + test3 + i + test4)
		j+=1
		i = str(j)
	os.system("cd pass; mkdir " + file)
	os.system("cd faill; mkdir " + file)
	f.write('\npasss= "pass/'+file + '"')
	f.write('\nfaill="faill/'+file + '"')
	f.write("\ntest_add()")
	f.close()
	os.system("python3 test_1c.py")
	os.system("rm test_1c.py")

def covreageDataDir(src_file, file):
	data = []
	readDirTest(file,data)
	if not data:
		print('no file test_ files has been found in ', file, ' directory')
		return
	dirs=""
	for r, d, f in os.walk(src_file):
		for dir in d:
			dirs+="sys.path.insert(1,'"+src_file+"/"+str(dir)+"')\n"
	dirs+="sys.path.insert(1,'"+src_file+"')\n"
	f = open("test_1c.py", "w")
	dir = str(src_file)
	
	

	func = ("""
import coverage
import pytest as py
import sys
""" + dirs +"""
""" + data[0] + """
def test_add():
	cov = coverage.Coverage()
	flag = 0
""")


	#---------------------------------
	test = ("""
	cov.start()
	try:""")
	i = '0'
	j=0

	#------------------------------------
	test2 = ("""
	except Exception:
		flag = 0
	cov.stop()
	if flag == 1:
		out = passs+"/testPassed" +'""")
	test3 = ("""'+ ".json"
		cov.json_report(outfile=out)
	else:
		out = faill+"/testFailed" +'""")
	test4 =  ("""'+ ".json"
		cov.json_report(outfile=out)
	cov.erase()
		""")
	os.system("mkdir pass")
	os.system("mkdir faill")
	f.write(func)
	data.pop(0)
	for line in data:
		if 'test_' in line:
			name = line.strip()
			os.system("cd pass; mkdir " + name)
			os.system("cd faill; mkdir " + name)
			f.write('\npasss= "pass/'+line + '"')
			f.write('\nfaill="faill/'+line + '"')
			f.write("\ntest_add()")
			f.close()
			os.system("python3 test_1c.py")
			f = open("test_1c.py", "w")
			f.write(func)
			continue
			
		f.write(test + line +"\n		flag=1" + test2 + i + test3 + i + test4)
		j+=1
		i = str(j)
	os.system("rm test_1c.py")

 
def readTest(src_file,data):
	file1 = open(src_file, 'r')
	Lines = file1.readlines()
	count = 0
	x = ''
	for line in Lines:
		line = line.strip()
		if 'import' in line:
			if not data:
				data.append(line)
				continue
			data[0] = data[0] + '\n' + line
		elif 'assert' in line:
			if x == '':
				x = '\n		' + line + '\n'
				data.append(x)
				continue
			x += '\n		' + line + '\n'
			data.append(x)
			x = ''
		elif 'def' in line or line == '' or '#' in line:
			continue
		else:
			x += '\n		' + line + '\n'
	
			
def readDirTest(dir_test, data):
	x = ''
	for r, d, f in os.walk(dir_test):
		for file in f:
			if file.endswith(".py"):
				if 'test_' in file:
					d = open(os.path.join(r, file)).readlines()
					for line in d:
						line = line.strip()
						if 'import' in line:
							if not data:
								data.append(line)
								continue
							data[0] = data[0] + '\n' + line
						elif 'def' in line or line == '' or '#' in line:
							continue
						elif 'assert' in line:
							if x == '':
								x = '\n		' + line + '\n'

								data.append(x)
								x=''
								continue

							x += '\n		' + line + '\n'
							
							data.append(x)
							x = ''
						else:
							x += '\n		' + line + '\n'
							
							
					dirName = file.replace('.py', '')
					data.append(dirName)
	
	

		
class driver():
    def __init__(self):
        pass
    def mainFunction(self):
        # with open('/home/mohanad/config.json') as f:
        #     data = json.load(f)
        # threshold = data[' Threshold_size ']
        # maxCommands = data[' Max_commands ']
        # maxLogFiles = data[' Max_log_files ']
        # sameDir = data[' Same_dir ']
        # output = data[' output ']
        parser = optparse.OptionParser(" usage %prog -s < script path > -o < output path >")
        
        #                       src = test cases file
        parser.add_option("-t", dest='srcPath', type='string', help=' testing file path')

        #
        parser.add_option("-o", dest='output', type='string', help=' the output file')
       
        #                       main file
        parser.add_option("-f", dest='file', type='string', help=' file path of the main project')

        parser.add_option("--dt", dest='dir_test', type='string', help=' directory path of the main project test cases')
        parser.add_option("--df", dest='dir_srcPath', type='string', help=' directory path of the main project')
        (options, args) = parser.parse_args()
        
        #--- Text implanting
        

        if(options.srcPath != None and options.file != None):
            covreageData(options.srcPath, options.file)
            Hash.readDir(options.srcPath)
            os.system("rm -rf pass")
            os.system("rm -rf faill")
        elif (options.dir_test != None and options.dir_srcPath != None):
        	files = []
        	covreageDataDir(options.dir_srcPath, options.dir_test)
        	for r, d, f in os.walk(options.dir_srcPath):
        		for file in f:
        			if file.endswith(".py") and not file.endswith(".pyc"):
        				files.append(file)
        	Hash.readDir(files, options.dir_srcPath)
        	os.system("rm -rf pass")
        	os.system("rm -rf faill")
        else:
        	print('enter -dt for the directory test cases file and df for the directory of the main project files or\n -f for the file you want to test and -t for it test cases')
    """ we will find the test cases lines number in this function"""


if __name__ == '__main__':
    obj = driver()
    obj.mainFunction()
