#!/usr/bin/python3
######################################################################################################
# File    : display_handler.py
# Author  : Arjun Nair
# License : See LICENSE file.
#
######################################################################################################


######################################################################################################
# IMPORTS.
######################################################################################################

import threading
import time

from rich.live import Live
from rich.table import Table

from . import data_management


######################################################################################################
# CLASS.
######################################################################################################

class DisplayHandler(threading.Thread):
	__stop = False
	
	__data_management_instance = None

	def __init__(self, data_management_instance : data_management.DataManagement):
		threading.Thread.__init__(self)
		self.__data_management_instance = data_management_instance


	def run(self):
		
		
		with Live(self.__generate_table(), refresh_per_second=2) as live:
			while(self.__stop == False):
				time.sleep(0.4)
				live.update(self.__generate_table())
			
				if(self.__data_management_instance.EXIT_STATE()):
					self.STOP()

		
	def __generate_table(self) -> Table:
		"""Make a new table."""
		table = Table()
		table.add_column("Address")
		table.add_column("Port")

		for row in self.__data_management_instance.GET_SOCKET_LIST():
			value_address = row.GET_ADDRESS()[0]
			value_port = row.GET_ADDRESS()[1]
			table.add_row(
				f"{value_address}", f"{value_port}"
			)
		return table


	def STOP(self):
		self.__stop = True 
