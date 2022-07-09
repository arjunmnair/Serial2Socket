#!/usr/bin/python3
######################################################################################################
# File    : data_management.py
# Author  : Arjun Nair
# License : See LICENSE file.
#
######################################################################################################


######################################################################################################
# IMPORTS.
######################################################################################################

import queue


######################################################################################################
# CLASS.
######################################################################################################

class DataManagement(object):
	__receive_queue = None
	__socket_objects = None
	__exit_signal    = None
	
	def __init__(self):
		self.__receive_queue = queue.Queue()
		self.__socket_objects = []
		self.__exit_signal = False
	
	def REGISTER_SOCKET_OBJECT(self, t):
		self.__socket_objects.append(t)
	def UNREGISTER_SOCKET_OBJECT(self, t):
		self.__socket_objects.remove(t)
	def GET_SOCKET_LIST(self):
		return self.__socket_objects
	def PUT_SEND_TEXT(self, t):
		for obj in self.__socket_objects:
			obj.PUT_SEND_TEXT(t)
	
	def PUT_RECEIVED_TEXT(self, t):
		self.__receive_queue.put(t)
	def GET_RECEIVED_TEXT(self):
		t = None
		try:
			t = self.__receive_queue.get(block=False)
		except:
			t = None
		return t
	
	def SIGNAL_EXIT(self):
		self.__exit_signal = True
	def EXIT_STATE(self):
		return self.__exit_signal
