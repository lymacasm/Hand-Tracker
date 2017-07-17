import serial

##TODO: Change reading individual fingers to one read command which recieves all three finger
##      Data at once. Parse the data using int(stuff.encode('hex')) or similar
##      Add read() and write() and readline() methods which simply call ser.XXX()
##      Store all fingers in a list/dictionary
##      

class SerialController:
	#This class provides functions for receiving data from the ADC
	debugMode = False #Sets the debug mode
	baudrate = 9600  #Sets the baudrate of the serial controller
	readCmd = 'r' #Sets the command to send to the ADC to read the values
	numChars = 10 #Sets the number of characters to be returned
	data = [0, 0, 0] #List containing the flex sensor data

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
	
	#readFingers()
	#Sends the command to read the fingers' value
	#Returns nothing, but stores the data received in the 'data' dictionary
	def  readFingers(self): 
		if(debugMode):
		print 'Sending command '+ self.readCmd + '.'
		self.ser.write(self.readCmd)
		vals = self.ser.read(numChars)
		for i in range(0,2):
			self.data[i] = int(vals[i].encode('hex'))
			
	
	#read()
	#Reads numChars amount of data from UART
	#Returns the data read
	def read(self):
		data = self.ser.read(numChars)
		if(debugMode):
			print 'Received data ' + data + '.'
		return data

	#Write()
	#Writes the string str to UART	
	def write(self, str):
		if(debugMode):
			print 'Writing string ' + str + '.'
		self.ser.write(str)

		
	
	
