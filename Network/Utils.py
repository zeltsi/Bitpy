import hashlib

def command_padding(command):	# The message command should be padded to be 12 bytes long.
	command = command + (12-len(command)) * "\00"	
	return command

def checksum(payload):
	check = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
	return check

class Message():	# Takes two arguments, the payload of the message and the message command	

	def __init__(self, payload, command):
		self.payload 	= payload						#The message payload
		self.magic		=  "F9BEB4D9".decode("hex")		#The Magic number of the Main network -> This message will be accepted by the main network
		self.command	= command_padding(command)
		self.checksum	= checksum(payload)
		self.length 	= "to_uint32(payload)" #<===== module structure?

	def complete(self):
		return self.magic + self.command + self.length + self.checksum + self.payload
	

new = Message("ddd", "version")

print new.complete()










# magic = "F9BEB4D9".decode("hex")
# command = "version" + 5 * "\00"
# length = struct.pack("I", len(payload))