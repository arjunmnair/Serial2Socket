#!/usr/bin/python3
######################################################################################################
# File    : socket_handler.py
# Author  : Arjun Nair
# License : See LICENSE file.
#
######################################################################################################


######################################################################################################
# IMPORTS.
######################################################################################################

import errno
import gc
import os
import queue
import select
import socket
import threading
import time

from . import data_management


######################################################################################################
# CLASS.
######################################################################################################


class _socket_thread(threading.Thread):
	__stop = False
	
	__connection = None
	__address = None
	__send_queue = None

	__data_management_instance = None
	
	def __init__(self, data_management_instance : data_management.DataManagement, connection, address):
		threading.Thread.__init__(self)
		self.__data_management_instance = data_management_instance
		self.__connection = connection
		self.__address = address
		self.__send_queue = queue.Queue()


	def run(self):
		self.__data_management_instance.REGISTER_SOCKET_OBJECT(self)
		self.__connection.setblocking(False)
		tttt = 0
		with self.__connection:
			#print('[%d] Connected.' % self.__address[1])
			while(self.__stop == False):
				## Receive stuff.
				try:
					data = self.__connection.recv(4096)
					if(len(data)):
						self.__data_management_instance.PUT_RECEIVED_TEXT(data)
					else:
						break
				except socket.error as e:
					err = e.args[0]
					if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
						pass
					else:
						break
				
				## Send stuff.
				try:
					snd = self.__send_queue.get(block=False)
				except:
					snd = None
				if(snd != None):
					try:
						self.__connection.sendall(snd)
					except:
						break
					
				if(self.__data_management_instance.EXIT_STATE()):
					self.STOP()
					
				
		#print('[%d] Disconnected.' % self.__address[1])
		self.__data_management_instance.UNREGISTER_SOCKET_OBJECT(self)
		gc.collect()
	
	def PUT_SEND_TEXT(self, t):
		self.__send_queue.put(t)
	
	def GET_ADDRESS(self):
		return self.__address

	def STOP(self):
		self.__stop = True 
	
	
class SocketHandler(threading.Thread):
	__stop = False
	
	__host = ''
	__port = 0

	__data_management_instance = None
	
	def __init__(self, data_management_instance : data_management.DataManagement, host, port):
		threading.Thread.__init__(self)
		self.__data_management_instance = data_management_instance
		self.__host = host
		self.__port = port


	def run(self):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.setblocking(False)
			s.bind((self.__host, self.__port))
			print('Listening on \'%s : %d\'.' % (self.__host, self.__port))
			s.listen()
			
			while(self.__stop == False):
				try:
					conn, addr = s.accept()
					socket_th = _socket_thread(self.__data_management_instance, conn, addr)
					socket_th.start()
				except:
					pass
					
				if(self.__data_management_instance.EXIT_STATE()):
					self.STOP()
			
			print('Stopping socket.')

	def STOP(self):
		self.__stop = True 
