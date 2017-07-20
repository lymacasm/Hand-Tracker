import serial, struct

class SerialController:
	#This class provides functions for receiving data from the ADC
	debugMode = False #Sets the debug mode
	baudrate = 9600  #Sets the baudrate of the serial controller
	readCmd = 'r'  #Sets the command to send to the ADC to read the values
	numChars = 6 #Sets the number of characters to be returned
	data = [0, 0, 0] #List containing the unparsed flex sensor data
	fings = [0, 0, 0] #List containing the parsed data

	#default constructor
	def __init__(self):
		pass
	
	
	#destructor which closes the serial port
	def __del__(self): 
		self.ser.close()
	
	
	#initialize()
	#Initializes the serial port on the RPi.
	#NOTE: MUST BE CALLED BEFORE READ COMMANDS WILL WORK
	def initialize(self): #initializes the serial port on the RPi
		self.ser = serial.Serial ("/dev/ttyS0")
		self.ser.baudrate = self.baudrate
	
	#readFingers
	#Sends the command to read the fingers' value
	#Stores the data in the 'data' list and the parsed data
	#	in the fings list
	def  readFingers(self): 
		if(self.debugMode):
			print 'Sending command ' + self.readCmd + '.'
		self.ser.write(self.readCmd)
		for i in range(3):
			self.data[i] = self.read(self.numChars/3)
			self.fings[i] = struct.unpack('<H',self.data[i])[0]
		if(self.debugMode):
			print 'Received data ' + self.data + '.'
			print 'Parsed data as ' + self.fings + '.'
		

	#read(num)
	#Reads num amount of data from UART
	#Returns the data read
	def read(self,num):
		data = self.ser.read(num)
		if(self.debugMode):
			print 'Receieved data ' + data + '.'
		return data

	#readline()
	#Reads a line from UART
	def readline(self):
		if(self.debugMode):
			print 'Reading a line'
		data = self.ser.readline()
		if(self.debugMode):
			print 'Received data = ' + data + '.'
		return data

	#flush()
	#Flushes the buffer 
	def flush(self):
		self.ser.flush()

