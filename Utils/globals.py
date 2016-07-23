from Utils.dataTypes import *
import queue

# Config variables
magic_number = to_hexa("F9BEB4D9")  # The Main network magic number
version_number = 70012
latest_known_block = 416419  # june 2016


type_id = { 1:"MSG_TX",
            2:"MSG_BLOCK",
            3:"MSG_FILTERED_BLOCK"
        }

UI = "CLI" # || "tkinter_gui" || "pyQt5_gui"


# We put there, every message we want to send to our connected node
sendingQueue = queue.Queue()

# We put there, every receiving messages from a bitcoin node
receivingQueue = queue.Queue()

messages = queue.Queue()

# Global structure of all messages received by bitcoin nodes
node_messages = [] # should only contains: [ {"timestamp":"", "command":"", "payload":""}, ... ]
