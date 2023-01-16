#!/usr/bin/python3
######################################################################################################
# File    : serial_handler.py
# Author  : Arjun Nair
# License : See LICENSE file.
#
######################################################################################################


######################################################################################################
# IMPORTS.
######################################################################################################

import gc
import serial
import threading

from . import data_management

######################################################################################################
# CLASS.
######################################################################################################

class SerialHandler(threading.Thread):
	__stop = False
	
	__connection = None
	__port = ''
	__baudrate = 0
	
	__data_management_instance = None

	def __init__(self, data_management_instance : data_management.DataManagement, port, baudrate):
		threading.Thread.__init__(self)
		self.__data_management_instance = data_management_instance
		self.__port = port
		self.__baudrate = baudrate
		try:
			self.__connection = serial.Serial(self.__port, baudrate=self.__baudrate, timeout=0.001)
			print('Serial port \'%s : %s\'.' % (self.__port, self.__baudrate))
		except Exception as e:
			self.__connection = None
			print('Unknown serial port (%s : %s).' % (port, e))
			self.__data_management_instance.SIGNAL_EXIT()


	def run(self):
		while ( (self.__stop == False) and (self.__connection) ):
			try:
				rcv = self.__connection.read(1000)
			except:
				self.__data_management_instance.SIGNAL_EXIT()
				break
			if(len(rcv)):
				self.__data_management_instance.PUT_SEND_TEXT(rcv)
			
			snd = self.__data_management_instance.GET_RECEIVED_TEXT()
			if(snd != None):
				try:
					self.__connection.write(snd)
				except:
					self.__data_management_instance.SIGNAL_EXIT()
					break
			gc.collect()
			
			if(self.__data_management_instance.EXIT_STATE()):
				self.STOP()

	def STOP(self):
		self.__stop = True 
