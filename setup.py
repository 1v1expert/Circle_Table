#!/usr/bin/python3
# -*- coding: utf-8 -*-
from distutils.core import setup
import os, sys
import py2exe
from glob import glob
import PyQt5

NAME="Proga"

qt_platform_plugins = [("platforms", glob(PyQt5.__path__[0] + r'\plugins\platforms\*.*'))]
data_files.extend(qt_platform_plugins)
msvc_dlls = [('.', glob(r'C:\Windows\System32\msvc?100.dll'))]
data_files.extend(msvc_dlls)
# print(data_files)

sys.argv.append('py2exe')

setup(
	data_files=data_files,
	windows=[
		{
			"script": "form2.py",
		}
	],
	# zipfile=None,
	options={
		"py2exe": {
			"includes":["sip", "atexit",],
			# "packages": ['PyQt5'],
			"compressed": True,
			"dist_dir": "dist/" + NAME,
			# "bundle_files": 0, # не сработало ( с этой опцией на выходе прога не может найти msvc*.dll
			# "zipfile": None, # тоже лишнее
			"optimize": 2,
		}
	}
)