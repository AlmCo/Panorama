# -*- coding: utf-8 -*-

from datetime import datetime
from _winreg import OpenKey, QueryInfoKey, QueryValueEx, EnumKey, EnumValue, HKEY_LOCAL_MACHINE, KEY_READ, KEY_WOW64_64KEY

def readName(keyPath, name):
	# return the value of single path and name
	explorer = OpenKey(HKEY_LOCAL_MACHINE,keyPath, 0, KEY_READ | KEY_WOW64_64KEY)
	return str(QueryValueEx(explorer, name)[0])

def readValues(keyPath):
	# return Dict of name:value from key
	explorer = OpenKey(HKEY_LOCAL_MACHINE, keyPath, 0, KEY_READ | KEY_WOW64_64KEY)
	valuesDict = {}
	for i in range(QueryInfoKey(explorer)[1]):
		name, value, type = EnumValue(explorer, i)
		valuesDict[name] = value
	return valuesDict

def readKeys(keyPath):
	# return list of Keys
	explorer = OpenKey(HKEY_LOCAL_MACHINE, keyPath, 0, KEY_READ | KEY_WOW64_64KEY)
	KeysList = []
	for i in xrange(QueryInfoKey(explorer)[0]):
		name = EnumKey(explorer, i)
		KeysList.append(name)
	return KeysList
