#!/usr/bin/env python3

import os
import re
import sys
#get everything in a directory
from os import listdir

#get current working directory
cwd = os.getcwd()

#check if it is a file and not a directory
from os.path import isfile, join
onlyfiles = [f for f in listdir(cwd) if isfile(join(cwd,f))]

#hold cpp and h files
cppHolder = []
hHolder = []

#patterns for cpp and h
patternCpp = re.compile(".*.cpp$")
patternH = re.compile(".*.h$")

#loop through and segregate .h and .cpp files
for i in range(len(onlyfiles)):
	if re.match(patternCpp,onlyfiles[i]):
	 	cppHolder.append(onlyfiles[i])
	 	
	if re.match(patternH,onlyfiles[i]):
	 	hHolder.append(onlyfiles[i])

#To count number of entry points in source files	 	
count = 0

foundSource = True

#check for no source files
if not cppHolder:
	print("No source files found.It is unlikely that the executable will build and run correctly")
	foundSource = False

entryPoint = " "
#Loop and check for entry points in files
for i in range(len(cppHolder)):
	with open(cppHolder[i],'r') as f:
		for line in f.readlines():
		 if 'int main()' in line:
		 	entryPoint = cppHolder[i]
		 	count += 1
		 	

#check for no and multiple entry points
if(count > 1 and foundSource):
	print("Multiple files were found with a 'main' entry point.It is unlikely that the executable will build and run correctly")
	
elif(count < 1 and foundSource):
	print("No files were found with a 'main' entry point.It is unlikely that the executable will build and run correctly")
	 	

# sort them alphabetically 
cppHolder = sorted(cppHolder)
hHolder = sorted(hHolder)


#create a file called Makefile	 	
f = open('Makefile','w')
sys.stdout = f

#Loop through it and print SOURCE files
with open('Makefile','w') as f:
	print('SOURCE =', end=' ')
	for i in range(len(cppHolder)):
		if(i == 0):
			print(cppHolder[i], end=' ')
			
		if(i != 0):
			print('\t\t',cppHolder[i], end=' ')
			
		if(i != len(cppHolder)-1):
			print('\\')

#remove .cpp from file name
entryPoint = entryPoint[:-4]			
print('\n\nOBJS = $(SOURCE:.cpp=.o)')

print("\n#GNU C/C++ Compiler\nGCC = g++\n\n# GNU C/C++ Linker\nLINK = g++\n\n# Compiler flags\nINC =\nCFLAGS = -Wall -O3 -std=c++11 $(INC)\nCXXFLAGS = $(CFLAGS)\n\n# Fill in special libraries needed here\nLIBS =\n\n.PHONY: clean\n\n# Targets include all, clean, debug, tar")

print("\nall : ",entryPoint,"\n\n",entryPoint,": $(OBJS)\n\t$(LINK) -o $@ $^ $(LIBS)\n\nclean:\n\trm -rf *.o *.d core",entryPoint,"\n\ndebug: CXXFLAGS = -DDEBUG -g -std=c++11\ndebug:",entryPoint,"\n\ntar: clean\n\ttar zcvf",entryPoint,".tgz $(SOURCE) *.h Makefile\n\nhelp:\n\t@echo \"	make",entryPoint,"- same as make all\"\n\t@echo \"\tmake all   - builds the main target\"\n\t@echo \"\tmake       - same as make all\"\n\t@echo \"\tmake clean - remove .o .d core gas\"\n\t@echo \"	make debug - make all with -g and -DDEBUG\"\n\t@echo \"	make tar   - make a tarball of .cpp and .h files\"\n\t@echo \"	make help  - this message\"\n\n-include $(SOURCE:.cpp=.d)\n\n%.d: %.cpp\n\t@set -e; /usr/bin/rm -rf $@;$(GCC) -MM $< $(CXXFLAGS) > $@\n")

