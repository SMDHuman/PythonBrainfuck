from graphics import *
from time import sleep

def isInside(mouse, box):
	mouseX = mouse.getX()
	mouseY = mouse.getY()
	p1X = box.p1.getX()
	p1Y = box.p1.getY()
	p2X = box.p2.getX()
	p2Y = box.p2.getY()
	if(p1X < mouseX and p1Y < mouseY and p2X > mouseX and p2Y > mouseY):
		return(1)
	else:
		return(0)

class BrainFuck():
	def __init__(self, name, size = 30000):
		programFile = open(f"{name}.txt", "r")
		programLines = programFile.readlines()
		self.program = [i for i in "".join(programLines)]
		while(" " in self.program):
			self.program.remove(" ")
		while("\n" in self.program):
			self.program.remove("\n")

		while("[" in self.program):
			openP = self.program.index("[")
			point = 1
			for i in range(openP+1, len(self.program)):
				if(self.program[i] == "]"):
					point -= 1
				elif(self.program[i] == "["):
					point += 1
				if(point == 0):
					self.program[i] = f"]{openP}"
					self.program[openP] = f"[{i}"
					break

		self.tape = [0] * size
		self.tapePointer = 0
		self.programPointer = 0

		self.output = 0
		self.input = 0
		self.enOut = 0
		self.enIn = self.program[0] == ","

	def run(self, mode = int):
		self.reset()
		while(self.isContinue()):
			self.next()
			io = self.ioAvailable()
			if(io == "out"):
				print( mode(self.getOutput()) , end = " ")
			elif(io == "in"):
				self.setInput(input("Give input : "))

	def next(self):
		cmd = self.program[self.programPointer]

		if(cmd == "+"):
			self.tape[self.tapePointer] += 1
			if(self.tape[self.tapePointer] == 256):
				self.tape[self.tapePointer] = 0
		elif(cmd == "-"):
			self.tape[self.tapePointer] -= 1
			if(self.tape[self.tapePointer] == -1):
				self.tape[self.tapePointer] = 255

		elif(cmd == ">"):
			self.tapePointer += 1
		elif(cmd == "<"):
			self.tapePointer -= 1

		elif(cmd == "."):
			self.output = self.tape[self.tapePointer]
			self.enOut = 1
		elif(cmd == ","):
			self.enIn = 1

		elif(cmd[0] == "["):
			if(self.tape[self.tapePointer] == 0):
				self.programPointer = int(cmd[1:])
		elif(cmd[0] == "]"):
			if(self.tape[self.tapePointer] != 0):
				self.programPointer = int(cmd[1:])

		self.programPointer += 1

	def ioAvailable(self):
		if(self.enIn):
			self.enIn = 0
			return("in")
		elif(self.enOut):
			self.enOut = 0
			return("out")
		else:
			return("")

	def getOutput(self):
		return(self.output)

	def setInput(self, x):
		if(x > 255):
			x = 255
		elif(x < 0):
			x = 0
		self.tape[self.tapePointer] = x

	def isContinue(self):
		return(self.programPointer != len(self.program))

	def reset(self):
		for i in range(len(self.tape)):
			self.tape[i] = 0
		self.programPointer = 0
		self.tapePointer = 0

class bfVisualiser():
	def __init__(self):
		self.size = 400
		self.win = GraphWin("BrainFuck Visualiser", self.size, self.size / 2, autoflush = False)
		self.win.setBackground("#576366")

		self.programSize = 5
		self.tapeSize = 5
		self.automatic = 1
		self.speed = 0.5

		self.programTexts = [Text(Point(self.size / 2 + (x * 36), 36), "") for x in range(-self.programSize, self.programSize + 1)]
		for text in self.programTexts:
			text.setSize(36)
			text.draw(self.win)

		self.tapeTexts = [Text(Point(self.size / 2 + (x * 48), self.size / 2 - 36), "") for x in range(-self.tapeSize, self.tapeSize + 1)]
		for text in self.tapeTexts:
			text.setSize(18)
			text.draw(self.win)

		self.programPointerText = Text(Point(self.size / 2, 36*2.5), "^")
		self.programPointerText.setSize(36)
		self.programPointerText.setFill("red")
		self.programPointerText.draw(self.win)

		self.tapePointerText = Text(Point(self.size / 2, 36*3.25), "v")
		self.tapePointerText.setSize(30)
		self.tapePointerText.setFill("red")
		self.tapePointerText.draw(self.win)

		self.programAdressText = Text(Point(36*4.5, 36*2.25), "0 :")
		self.programAdressText.setSize(18)
		self.programAdressText.draw(self.win)

		self.tapeAdressText = Text(Point(36*4.5, 36*3.25), "0 :")
		self.tapeAdressText.setSize(18)
		self.tapeAdressText.draw(self.win)

		self.inputEntry = Entry(Point(300, 100), 3)
		#self.inputEntry.draw(self.win)

		self.outputText = Entry(Point(self.size/2, self.size/2 - 12), 44)
		self.outputText.setFill("Black")
		self.outputText.setTextColor("white")
		self.outputText.draw(self.win)

		self.runBox = Rectangle(Point(0, 70), Point(60, 100))
		self.runBox.setFill("red")
		self.runBox.setWidth(3)
		self.runBox.draw(self.win)

		self.runText = Text(Point(30, 85), "Stop")
		self.runText.setSize(18)
		self.runText.draw(self.win)

		self.fastBox = Rectangle(Point(60, 70), Point(90, 100))
		self.fastBox.setFill("yellow")
		self.fastBox.setWidth(3)
		self.fastBox.draw(self.win)

		self.fastText = Text(Point(75, 85), ">>")
		self.fastText.setSize(15)
		self.fastText.draw(self.win)

		self.nextBox = Rectangle(Point(0, 100), Point(60, 130))
		self.nextBox.setFill("blue")
		self.nextBox.setWidth(3)
		self.nextBox.draw(self.win)

		self.nextText = Text(Point(30, 115), "Step")
		self.nextText.setSize(18)
		self.nextText.draw(self.win)

		self.programPointer = 0
		self.program = []

		self.tapePointer = 0
		self.tape = []

	def isOpen(self):
		return(self.win.isOpen())

	def setProgram(self, p):
		for cmd in p:
			if(cmd[0] == "[" or cmd[0] == "]"):
				self.program.append(cmd[0])
			else:
				self.program.append(cmd)
		self.program = [" "] * self.programSize + self.program + [" "] * self.programSize

	def setTape(self, tape):
		self.tape = [" "] * self.tapeSize + tape + [" "] * self.tapeSize

	def addOutput(self, text):
		self.outputText.setText(self.outputText.getText() + str(text))

	def getInput(self):
		self.inputEntry.draw(self.win)
		while(self.win.checkKey() != "Return"):
			pass
		self.inputEntry.undraw()
		out = int(self.inputEntry.getText())
		self.inputEntry.setText("")
		return(out)

	def getNextAction(self):
		if(self.win.isOpen()):
			mouse = self.win.checkMouse()
			if(mouse):
				if(isInside(mouse, self.nextBox)):
					return(1)
				if(isInside(mouse, self.runBox)):
					self.automatic = 1
					self.runBox.setFill("red")
					self.runText.setText("Stop")
					return(1)

			if(self.win.checkKey() == "Return"):
				return(1)
			return(0)
		else:
			exit()

	def update(self):
		mouse = self.win.checkMouse()
		if(mouse):
			if(isInside(mouse, self.runBox)):
				if(self.automatic):
					self.speed = 0.5
					self.automatic = 0
				else:
					self.automatic = 1
			if(isInside(mouse, self.fastBox)):
				self.speed = 0

		if(self.automatic == 0):
			self.runBox.setFill("green")
			self.runText.setText("Run")
			while(self.getNextAction() == 0):
				pass
		else:
			self.runBox.setFill("red")
			self.runText.setText("Stop")

		self.programAdressText.setText(f"{self.programPointer} :")
		self.tapeAdressText.setText(f"{self.tapePointer} :")
		for text, i in zip(self.programTexts, range(len(self.programTexts))):
			text.setText(self.program[self.programPointer + i])

		for text, i in zip(self.tapeTexts, range(len(self.tapeTexts))):
			text.setText(self.tape[self.tapePointer + i])
		self.win.update()

		if(self.automatic):
			sleep(self.speed)

	def waitClick(self):
		self.win.getMouse()

bf = BrainFuck("test", 20)

vs = bfVisualiser()

vs.setProgram(bf.program)

while(vs.isOpen() and bf.isContinue()):
	vs.programPointer = bf.programPointer
	vs.tapePointer = bf.tapePointer
	vs.setTape(bf.tape)

	vs.update()

	bf.next()

	io = bf.ioAvailable()
	if(io == "out"):
		vs.addOutput(int(bf.getOutput()))
	elif(io == "in"):
		bf.setInput(vs.getInput())

if(vs.isOpen()):
	vs.waitClick()
	