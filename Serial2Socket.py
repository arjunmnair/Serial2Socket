#!/usr/bin/python3
######################################################################################################
# File    : Serial2Socket.py
# Author  : Arjun Nair
# License : See LICENSE file.
#
# To connect =>
#   $ stty -icanon -echo && nc <ip> <port>
######################################################################################################


######################################################################################################
# IMPORTS.
######################################################################################################

import sys
import time

from pynput.keyboard import KeyCode, Listener

from files import data_management, display_handler, serial_handler, socket_handler


######################################################################################################
# MAIN PROGRAM.
######################################################################################################

print_help = True
if(len(sys.argv) > 3):
	try:
		serial_port = sys.argv[1]
		serial_baudrate = int(sys.argv[2])
		socket_port = int(sys.argv[3])
		print_help = False
	except:
		pass
	
if(print_help):
	print('Usage :\r\npython3 Serial2Socket.py <serial_port> <serial_baudrate> <socket_port>')
	exit()


data_management_instance = data_management.DataManagement()

serial_handler_instance = serial_handler.SerialHandler(data_management_instance, serial_port, serial_baudrate)
serial_handler_instance.start()

socket_handler_instance = socket_handler.SocketHandler(data_management_instance, '0.0.0.0', socket_port)
socket_handler_instance.start()

display_handler_instance = display_handler.DisplayHandler(data_management_instance)
display_handler_instance.start()






#def key_on_release(key):
	#if(
		#(key == KeyCode.from_char('q'))
		#or (key == KeyCode.from_char('Q'))
	#):
		#data_management_instance.SIGNAL_EXIT()
		#print('Goodbye.')
		#return False
	#else:
		#return True
## Collect events until released
#listener = Listener(on_release=key_on_release)# as listener:
#listener.start()
#while(data_management_instance.EXIT_STATE() == False):
	#time.sleep(1)
#listener.stop()

print('q<Enter> to exit.')
while(data_management_instance.EXIT_STATE() == False):
	inp = input()
	if(
		(inp == 'q')
		or (inp == 'Q')
	):
		data_management_instance.SIGNAL_EXIT()
		print('Goodbye.')
		break
