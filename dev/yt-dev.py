#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
import platform

__version__ = '2020-12-25'

dir_of_executable = os.path.dirname(os.path.realpath(__file__))
__appname = 'ytdl-qt'

class SetUserConfiguration:

	def __init__(self, kernel_type=platform.system()):
		self.kernel_type = kernel_type
		self.dir_home = ''
		self.dir_cache = ''
		self.dir_config = ''
		self.dir_bin = ''
		self.dir_desktop_links = ''
		self.dir_temp = ''
		self.file_temp = ''
		self.user_info = {
			'home': '',
			'cache': '',
			'config': '',
			'bin': '',
			'desktop_links': '',
			'dir_temp': '',
			'file_temp': '',
		}

	# Getter para kernel_type
	@property
	def kernel_type(self):
		return self._kernel_type

	# Setter para kernel_type
	@kernel_type.setter
	def kernel_type(self, kernel):
		if isinstance(kernel, str):
			if (kernel == 'Windows') or (kernel == 'Linux'):
				self._kernel_type = kernel
			else:
				sefl._kernel_type = None
		else:
			self._kernel_type = None

	def _set_all(self):
		"""
        Setar e retornar arquivos e diretórios respeitando as particularidades do Linux e Windows.
		  É necessário definir a variável __appname para ser usada como subdiretório do diretório
		de configuração em cada sistema.
		"""
		import tempfile
	    from pathlib import Path
        
		self.dir_home = Path().home
		if self.kernel_type == 'Linux':
			self.dir_bin = os.path.abspath(os.path.join(self.dir_home, '.local', 'bin'))
			self.dir_desktop_links = os.path.abspath(os.path.join(self.dir_home, '.local', 'share', 'applications'))
			self.dir_cache = os.path.abspath(os.path.join(self.dir_home, '.cache', __appname))
			self.dir_config = os.path.abspath(os.path.join(self.dir_home, '.config', __appname))
	    elif self.kernel_type == 'Windows':
			pass
		
		
		self.file_temp = tempfile.NamedTemporaryFile(delete=False).name
		self.dir_temp = tempfile.TemporaryDirectory().name
		if os.path.isdir(self.dir_temp) == False:
			os.makedirs(self.dir_temp)

        def get_all(self):
			self.user_info[]
		







