import os
import pathlib
import json
import shutil
from typing import ContextManager
from collections import defaultdict
class HashTable(object):
    def __init__(self, name):
        # Initiate our array with empty values.
        self.array = [None] * 11
        self.name = name
        self.size = 11
        self.reversed = 0
    #                               #if 0 pass else fail
    def add(self, instructionNumber, passOrFail):
      '''
      we will search the for instructionNumber 
      if it already exist we will add 1 on faillCounter if passOrFaill != 0 else add 1 to passCounter
      but we should note if the insrtuction dose not exixt before and it was a pass it will not be registred 

      '''
      # this function rerturn a key for the instruction number 
      if self.reversed > int(self.size/2):
        self.array = self.reHash()
      key = self.getKey(instructionNumber, self.size)
      # the follwing if statments will make sure to add one on whatever counter of it already exist before
      # and add new object if the instruction is 1st time and fail
      z = key
      j = 1
      h = z
      if self.array[key] == None and passOrFail != 0:
        newInstruction = Node(instructionNumber)
        self.array[key] = newInstruction
        self.reversed += 1
      elif self.array[key] == None and passOrFail == 0:
        pass
      elif passOrFail == 0 and self.array[key] != None and self.array[key].getInstructionNumber() == instructionNumber:
      	self.array[key].passCounter += 1
      elif passOrFail == 1 and self.array[key] != None and self.array[key].getInstructionNumber() == instructionNumber:
        self.array[key].failCounter += 1
      elif self.array[key] != None and self.array[key].getInstructionNumber() != instructionNumber:
        while self.array[h] != None:
          if self.array[h].getInstructionNumber() == instructionNumber and passOrFail == 1:
            self.array[h].failCounter += 1
          elif self.array[h].getInstructionNumber() == instructionNumber and passOrFail == 0:
            self.array[h].passCounter += 1
          h = self.quad(z, j, self.size)
          if j == self.size or (j == 1 and key == h):
            self.array = self.reHash()
          j += 1
        if passOrFail == 1:
          newInstruction = Node(instructionNumber)
          self.array[h] = newInstruction
          self.reversed += 1


    def quad(self, j, i ,size):
      return (j + (i * i)) % size
    def prime(self, n):
      while self.isPrime(n) == False:
        n += 1
      return n
    def isPrime(self, n):
      if n == 2 or n == 3:
        return True
      if n == 1 or n % 2 == 0:
        return False
      for i in range(3, int(n/2)):
        if n % i == 0:
          return False
      return True
    def getKey(self,instructionNumber, size):
      '''
      simple hash key will be the instuction number mode the size of the array
      '''
      key = instructionNumber % size
      return key
    def getName(self):
      return self.name
    def getArray(self):
      return self.array
    def reHash(self):
      newSize = self.prime(self.size*2)
      newArray = [None] * newSize
      for i in range(self.size):	
      	if self.array[i] != None:
      		key = self.getKey(self.array[i].getInstructionNumber(), newSize)
      		z = key
      		j = 1
      		h = z
      		if newArray[key] == None:
      			newInstruction = Node(self.array[i].instructionNumber)
      			newArray[key] = newInstruction
      			newArray[key].instructionNumber = self.array[i].instructionNumber
      			newArray[key].failCounter = self.array[i].failCounter
      			newArray[key].passCounter = self.array[i].getPassCounter()
      		else:
      			while newArray[h] != None:
      				h = quad(z, j, self.size)
      				if j == self.size or ( j == 1 and key == h):
      					return reHash()
      				j += 1
      		newInstruction = Node(self.array[i].instructionNumber)
      		newArray[h] = newInstruction
      		newArray[h].instructionNumber = self.array[i].instructionNumber
      		newArray[h].failCounter = self.array[i].failCounter
      		newArray[h].passCounter = self.array[i].getPassCounter()
      self.size = newSize
      return newArray

        
    def printHash(self):
      print(self.name, self.size)
      for i in self.array:
        if i != None:
          print(i.getInstructionNumber(), i.getFailCounter(), i.getPassCounter())
class Node():
  def __init__(self, instructionNumber):
    self.instructionNumber = instructionNumber
    self.failCounter = 1
    self.passCounter = 0
  def getInstructionNumber(self):
    return self.instructionNumber
  def getFailCounter(self):
    return self.failCounter
  def getPassCounter(self):
    return self.passCounter
def readFiles(dir, passOrFail, array, textCounter, acceptedFiles):
  '''
  in this function i enter three variables dir = the current execuation path + pass or faill 
  paassOrFaill = 0 for passed test case and 1 for failed test case 
  array = it will be an array of hash objects each object will be defined by the name of the function 
  array need to be imprved to become a hash array
  '''
  count = 0
  index = 0
  for filename in os.listdir(dir):
    
    # here we start reading the directory which better to be a function test cases 
    for file in os.listdir(dir + "/" + str(filename)):
      j = 0
      
      
      #read the json file and add the executed instruction 
      with open(dir + "/" + filename + "/" + file) as json_file:
        data = json.load(json_file)
        executed = data["files"].items()
        for z in executed:
          
          t = True
          flagValied = 0 # this flag will help us know if the current reading file is in the test case dir
          for key in range(len(z)):

            if t == True:
              t = False
              #--------- here we chck if the file is one of the file that need to be tested
              for i in acceptedFiles:
                if i in z[key]:
                  flagValied = 1
              #==========
              if flagValied == 0:
                continue
                
              if z[key] in textCounter:# this here will help us count the test cases
                if passOrFail == 0:
                  j = textCounter[str(z[key])]["pass"]
                else:
                  j = textCounter[str(z[key])]["fail"]
              flag = 0
              #this for loop finds if we already defined the object!
              for i in range(len(array)):
                if array[i].getName() == z[key]:
                  flag = 1
                  index = i
                  break
                
              if flag == 0:
                array.append(HashTable(z[key]))
                index = count
                count += 1
              
            else:
              t = True
              if flagValied == 0:
                continue
              flagValied = 0
              
              d = z[key]["executed_lines"]
              for i in d:
                array[index].add(i, passOrFail)
              continue
            j += 1
            if passOrFail == 0:# this set of code to count how many test cases are there and if they are passed or failed
              textCounter[str(z[key])]["pass"] = j
            else:
              textCounter[str(z[key])]["fail"] = j
              textCounter[str(z[key])]["pass"] = 0 # we set pass to 0 becuase we always start counting the failed test casses and becase we dont want it raise error in line 98
      
  

  
def readDir(acceptedFiles, dirFiles):
  # ob = HashTable("name1")
  # ob.add(3,1)
  # ob.add(4,0)
  # print(ob.array[4], "1")
  array = []
  testCasesCounter = defaultdict(dict)
  
  readFiles(str(pathlib.Path(__file__).parent.absolute())+"/faill", 1, array, testCasesCounter, acceptedFiles)
  readFiles(str(pathlib.Path(__file__).parent.absolute())+"/pass", 0, array, testCasesCounter, acceptedFiles)
  firstInstruction = {}
  dir = str(pathlib.Path(__file__).parent.absolute())+"/faill"
  find_lines_dictionary(dirFiles, firstInstruction)
  trantoula(array, firstInstruction, testCasesCounter)


def trantoula(testData, firstInstruction, testCasesCounter):	
  #testCasesCounter = number of test cases, firstInstruction = should be an array of 1st lines in each function
  # testData = the has
  susup = defaultdict(dict)
  for i in range(len(testData)):
    if testData[i].getName() in testCasesCounter: # check if there is any failed text cases 
      if "fail" not in testCasesCounter[testData[i].getName()]:
        print(testData[i].getName() + " passed the test successfully")
      # here tarntoula start !
      else:
        for z in testData[i].getArray():
            if z == None:
              continue
            else:
              faildedS = z.getFailCounter()
              passS = z.getPassCounter()
              totalFailed = testCasesCounter[testData[i].getName()]["pass"] + testCasesCounter[testData[i].getName()]["fail"]
              sus = faildedS / (totalFailed * (faildedS + passS))
              susup[testData[i].getName()][z.getInstructionNumber()] = sus

  for i in susup:
    instructionList = sort(susup[i])
    sts = firstInstruction[i]
    array = sts
    for instruction in instructionList:
      for functionIndex in range(len(array)):
        if array[functionIndex] < instruction and (functionIndex+1 >= len(array) or array[functionIndex+1] > instruction):
          if instructionList[array[functionIndex]] < instructionList[instruction]:
          	print(i, instruction, instructionList[instruction])
    
    
  
# 
def sort(s):
  return({k: v for k, v in sorted(s.items(), key=lambda item: item[1], reverse=True)})

def find_lines_dictionary(directory, lines_dictionary):
	counter = 0
	place = 1000
	for r, d, f in os.walk(directory):
		for file in f:
			if file.endswith(".py"):
				infilename = os.path.join(r, file)
				if not os.path.isfile(infilename):
					continue
				oldbase = os.path.splitext(infilename)
				if infilename.endswith(".py"):
					counter = 0
					# list of all files names
					# lines_dictionary.update({filename: counter})
					with open(infilename) as openfile:
						array = []
						for line in openfile:
							counter += 1
							for part in line.split():
								if "def" in part:
									place = counter
									continue
								elif line == "\n":
									continue
								elif counter > place and place != 0:
									if infilename not in lines_dictionary:
										array.append(counter)
										place = 0
										continue
									elif type(lines_dictionary[infilename]) == list:
										array.append(counter)
										place = 0
										continue
									else:
										lines_dictionary[infilename] = [
										lines_dictionary[infilename], counter]
										array.append(counter)
										place = 0
										continue
						lines_dictionary[infilename] = (array)
				else:
					continue
if __name__ == "__main__":
  readDir(["nrm.py"], "")
