import sys
from copy import deepcopy
import os
import time

#converter that converts numbers to chars and vice versa
class converter:
	allNums = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]
	allChars = ['-','#','A','B','C','D','E','F','G','H','I','J','K','L']
	@staticmethod
	def convertToChar(num):
		index = converter.allNums.index(num)
		return converter.allChars[index]
	
	@staticmethod
	def convertToNum(char):
		index = converter.allChars.index(char)
		return converter.allNums[index]

#position
class pos:
	def __init__(self, posX, posY):
		self.posX = posX
		self.posY = posY

#direction of a part that contains the positions the part will fill in this direction
class way:
	def __init__(self, poss):
		self.poss = poss

#part that contains directions
class part:
	def __init__(self, name, ways):
		self.name = name
		self.ways = ways
		
	#this method is returning all parts with all directions graphic
	@staticmethod
	def getPartsGraphic():
		result = 'parts:\n\n'
		
		#for every part in the part list
		for part in allParts:
			#add the name of the part to the result
			result += '{0}:\n\n'.format(part.name)		
			#for every direction of the current part
			for way in part.ways:
				#create a matrix with 0 as placeholders
				a = [[0 for i in range(4)] for i in range(4)]
				#for every position of the current direction of the current part
				for pos in way.poss:
					#mark the position with a 1
					a[pos.posX][pos.posY] = 1
				
				#add the matrix that contains the current direction graphic of the current part to the result
				for y in range(4):
					for x in range(4):
						result += converter.convertToChar(a[x][y])
					result += '\n'
				#add a new line to the result between every direction
				result += '\n'
			
			#add a double new line to the result between every part
			result += '\n\n'
		
		#return the result
		return result
		
#gameboard
class board:
	#board dimensions
	width = 11
	height = 5
	
	def __init__(self, settings):
		#create the board
		self.fields = {}
		
		#for every line of the settings
		for lineIndex in range(0, board.height):
			#for every char in the line
			for charIndex in range(0, board.width):
				if settings[lineIndex][charIndex] == '-':
					self.fields[(charIndex, lineIndex)] = converter.convertToNum('-')
				else:
					self.fields[(charIndex, lineIndex)] = converter.convertToNum('#')
	
	#this method return true if the direction of a part is fitting with the offset in the board
	def wayFitsIn(self, way, offsetX, offsetY):
		#the default is that the part fits
		fits = True
		#for every position of the direction
		for pos in way.poss:
			#check if the current position of the direction is on the board, so it is not over the border
			if not (pos.posX + offsetX >= 0 and pos.posX + offsetX < board.width and pos.posY + offsetY >= 0 and pos.posY + offsetY < board.height):
				fits = False
				break
			
			#check if the current position of the direction is free on the board
			if self.fields[(pos.posX + offsetX, pos.posY + offsetY)] != 0:
				fits = False
				break
			
		#return the result
		return fits
	
	#this method returns a board graphic
	def getBoardGraphic(self):
		result = ''
		
		#for every line of the board
		for y in range(0, board.height):
			#for every column of the current line
			for x in range(0, board.width):
				#add the content of the current field to the result
				result += converter.convertToChar(self.fields[(x, y)])
			result += '\n'
		
		#return the result
		return result
		
#all parts with all ways
allParts = [
	part('L', [way([pos(1,0), pos(0,1), pos(1,1), pos(2,1), pos(1,2)])]),
	part('K', [way([pos(0,0), pos(1,0), pos(0,1), pos(1,1)])]),
	part('J', [way([pos(0,0), pos(1,0), pos(2,0), pos(3,0)]), way([pos(0,0), pos(0,1), pos(0,2), pos(0,3)])]),
	part('G', [way([pos(0,0), pos(1,0), pos(2,0), pos(2,1), pos(2,2)]), way([pos(2,0), pos(2,1), pos(0,2), pos(1,2), pos(2,2)]), way([pos(0,0), pos(0,1), pos(0,2), pos(1,2), pos(2,2)]), way([pos(0,0), pos(1,0), pos(2,0), pos(0,1), pos(0,2)])]),
	part('F', [way([pos(0,0), pos(0,1), pos(1,1)]), way([pos(0,0), pos(1,0), pos(0,1)]), way([pos(0,0), pos(1,0), pos(1,1)]), way([pos(1,0), pos(0,1), pos(1,1)])]),
	part('I', [way([pos(0,0), pos(1,0), pos(1,1), pos(0,2), pos(1,2)]), way([pos(0,0), pos(2,0), pos(0,1), pos(1,1), pos(2,1)]), way([pos(0,0), pos(1,0), pos(0,1), pos(0,2), pos(1,2)]), way([pos(0,0), pos(1,0), pos(2,0), pos(0,1), pos(2,1)])]),
	part('H', [way([pos(0,0), pos(1,0), pos(1,1), pos(2,1), pos(2,2)]), way([pos(2,0), pos(1,1), pos(2,1), pos(0,2), pos(1,2)]), way([pos(0,0), pos(0,1), pos(1,1), pos(1,2), pos(2,2)]), way([pos(1,0), pos(2,0), pos(0,1), pos(1,1), pos(0,2)])]),
	part('D', [way([pos(0,0), pos(1,0), pos(2,0), pos(3,0), pos(2,1)]), way([pos(1,0), pos(1,1), pos(0,2), pos(1,2), pos(1,3)]), way([pos(1,0), pos(0,1), pos(1,1), pos(2,1), pos(3,1)]), way([pos(0,0), pos(0,1), pos(1,1), pos(0,2), pos(0,3)]), way([pos(2,0), pos(0,1), pos(1,1), pos(2,1), pos(3,1)]), way([pos(0,0), pos(0,1), pos(0,2), pos(1,2), pos(0,3)]), way([pos(0,0), pos(1,0), pos(2,0), pos(3,0), pos(1,1)]), way([pos(1,0), pos(0,1), pos(1,1), pos(1,2), pos(1,3)])]),
	part('E', [way([pos(0,0), pos(1,0), pos(1,1), pos(2,1), pos(3,1)]), way([pos(1,0), pos(0,1), pos(1,1), pos(0,2), pos(0,3)]), way([pos(0,0), pos(1,0), pos(2,0), pos(2,1), pos(3,1)]), way([pos(1,0), pos(1,1), pos(0,2), pos(1,2), pos(0,3)]), way([pos(2,0), pos(3,0), pos(0,1), pos(1,1), pos(2,1)]), way([pos(0,0), pos(0,1), pos(0,2), pos(1,2), pos(1,3)]), way([pos(1,0), pos(2,0), pos(3,0), pos(0,1), pos(1,1)]), way([pos(0,0), pos(0,1), pos(1,1), pos(1,2), pos(1,3)])]),
	part('C', [way([pos(0,3), pos(1,0), pos(1,1), pos(1,2), pos(1,3)]), way([pos(0,0), pos(0,1), pos(1,1), pos(2,1), pos(3,1)]), way([pos(0,0), pos(1,0), pos(0,1), pos(0,2), pos(0,3)]), way([pos(0,0), pos(1,0), pos(2,0), pos(3,0), pos(3,1)]), way([pos(0,0), pos(0,1), pos(0,2), pos(0,3), pos(1,3)]), way([pos(0,0), pos(1,0), pos(2,0), pos(3,0), pos(0,1)]), way([pos(0,0), pos(1,0), pos(1,1), pos(1,2), pos(1,3)]), way([pos(3,0), pos(0,1), pos(1,1), pos(2,1), pos(3,1)])]),
	part('B', [way([pos(0,0), pos(1,0), pos(0,1), pos(1,1), pos(2,1)]), way([pos(0,0), pos(1,0), pos(0,1), pos(1,1), pos(0,2)]), way([pos(0,0), pos(1,0), pos(2,0), pos(1,1), pos(2,1)]), way([pos(1,0), pos(0,1), pos(1,1), pos(0,2), pos(1,2)]), way([pos(1,0), pos(2,0), pos(0,1), pos(1,1), pos(2,1)]), way([pos(0,0), pos(0,1), pos(1,1), pos(0,2), pos(1,2)]), way([pos(0,0), pos(1,0), pos(2,0), pos(0,1), pos(1,1)]), way([pos(0,0), pos(1,0), pos(0,1), pos(1,1), pos(1,2)])]),
	part('A', [way([pos(0,0), pos(0,1), pos(1,1), pos(2,1)]), way([pos(0,0), pos(1,0), pos(0,1), pos(0,2)]), way([pos(0,0), pos(1,0), pos(2,0), pos(2,1)]), way([pos(1,0), pos(1,1), pos(0,2), pos(1,2)]), way([pos(2,0), pos(0,1), pos(1,1), pos(2,1)]), way([pos(0,0), pos(0,1), pos(0,2), pos(1,2)]), way([pos(0,0), pos(1,0), pos(2,0), pos(0,1)]), way([pos(0,0), pos(1,0), pos(1,1), pos(1,2)])])
]

totalSolutionsFound = 0
#this method is recursiv and solves the lvl
def solve(curPartIndex, curBoard, curParts):	
	#increase the current part index so that the next part is placed and not the same
	curPartIndex += 1
	
	#Check if all parts are placed
	if curPartIndex == len(curParts):
		print('\nsolution found:\n{0}\nsearching for other solutions...'.format(curBoard.getBoardGraphic()))
		#continue searching for solutions
		global totalSolutionsFound
		totalSolutionsFound += 1
		return
		
	#get the current part
	part = curParts[curPartIndex]
	
	#for every direction of the part
	for way in part.ways:
		#for every position that is possible on the board
		for posX in range(0, board.width):
			for posY in range(0, board.height):
				#check if the direction fits in this position on the board
				if curBoard.wayFitsIn(way, posX, posY):
					#when the part fits, draw it on a copy of the current board
					curBoardCopy = deepcopy(curBoard)
					for pos in way.poss:
						curBoardCopy.fields[(pos.posX + posX, pos.posY + posY)] = part.name
					#and place the next part
					solve(curPartIndex, curBoardCopy, curParts)
					
#this method gets the startsettings, creates the board and starts solving				
def startSolving():	
	#get the filepath to the settingsfile of the lvl the user wants to solve 	
	filename = raw_input('settings filepath:')
	
	#check if the file exists
	if not os.path.isfile(filename):
		print("file '{0}' does not exist.\ndone.".format(filename))
		return
		
	#get the startsettings from the settings file
	with open(filename, 'r') as settingsFile:
		settings = settingsFile.read().splitlines()
	
	#get the name of the lvl from the first line of the file	
	lvlName = settings[0]
	print('\nlvlname:{0}'.format(lvlName))
	
	#create the board for the lvl
	b = board(settings[1:board.height + 1])
	
	#create a new list that will contain all parts that are not placed. read them from the last line of the file
	notPlacedParts = []
	placedParts = settings[board.height + 1].split(',')
	#therefor go through all parts that are available
	for part in allParts:
		#and check if the part is not in the placed parts list
		if not part.name in placedParts:
			#add the part to the parts that are not placed list
			notPlacedParts.append(part)
			
	#print the startboard
	print('board:\n{0}'.format(b.getBoardGraphic()))

	#print out the parts that are not placed
	notPlacedPartsChars = ''
	for part in notPlacedParts:
		notPlacedPartsChars += '{0}, '.format(part.name)
		
	notPlacedPartsChars = notPlacedPartsChars[0:-2]
	print('parts that are not placed:{0}\n'.format(notPlacedPartsChars))
	
	#change the names of all parts to numbers
	for part in notPlacedParts:
		part.name = converter.convertToNum(part.name)
	
	cmd = raw_input('Start? [y, n]')
	
	if cmd.lower() == 'y':
		print('searching for solutions...')
		#solve the lvl
		startTime = time.time()
		solve(-1, b, notPlacedParts)
		elapsedTime = round((startTime - time.time()) * (-1), 2)
		global totalSolutionsFound
		if totalSolutionsFound == 1:
			print('1 solution was found in {0}s.'.format(elapsedTime))
		else:
			print('{0} solutions were found in {1}s.'.format(totalSolutionsFound, elapsedTime))
		print('done.')
	else:
		print('done.')

def main(args):
	#show all directions if the user wants it
	cmd = raw_input('show all parts? [y, n]:')

	if cmd.lower() == 'y':
		#show all parts
		print(part.getPartsGraphic())
		#start solving a lvl
		startSolving()
	elif cmd.lower() == 'n':
		#start solving a lvl
		startSolving()
	else:
		print('done.')
		
	return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
