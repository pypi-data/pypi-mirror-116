# package is called wday (Whirl Data is alternative to YAML)
import ast
from wday import *
from tkinter import ttk as QBSJFIWJFWOJWFJSONNWJLLGJEHGMICROSOFT
from tkinter import *
import os
import sys


class console:
	def put(args):
		return print(args)
	def get(args):
		return input(args)

class dictonary:
	def __init__(self,data):
		self.data = dict(data)
	def add(key,value):
		self.data[key] = value
	def remove(key):
		self.data[key] = ""
	def find(value):
		for xyz in self.data.keys():
			if self.data[xyz] == value:
				return xyz

class list:
	def __init__(self,data):
		self.data = list(data)
	def add(value):
		self.data.append(value)

def read(data):
	contents = {}
	for line in data.split(";"):
		line = line.replace("\n",'')
		if line == "":
			continue
		elif line.isspace():
			continue
		elif line.replace(" ","")[0] == "~" or line.replace(' ','')[0] == "@":
			continue
		else:
			try:
				linedata = ast.literal_eval(line[line.find('::')+len('::'):])
				contents[line[:line.find("::")]]=linedata
			except:
				return -1
			continue
	return contents

def script(file):
	try:
		QUBUFEZCHA = file[file.find("'''")+len("'''"):]
		BOLSHEVIEKSDEHS = file.find("'''")
		QEXNEKWMCNEOWJFNFNJWF = QUBUFEZCHA[:QUBUFEZCHA.find("'''")]
		init = read(file[:BOLSHEVIEKSDEHS])
		gui = QBSJFIWJFWOJWFJSONNWJLLGJEHGMICROSOFT
		exec(QEXNEKWMCNEOWJFNFNJWF)
	except:
		print('Script errored out.')
