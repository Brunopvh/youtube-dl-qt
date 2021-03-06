#!/usr/bin/env python3

import os

__version__ = '2021-03-05'

class UserDirs(object):
	"""
	Esta classe retorna os diretórios comumente usado por programas instalados manualmente no sistema.
	ou seja, retorna o diretório a ser usado por binários, destiono de arquivos '.desktop' etc.
	  Os valore mudam para o usuário é o root. Se receber create_dirs=True irá criar os diretórios
	se necessário, se receber False apenas atribui os valores sem criar nada.
	"""

	def __init__(self, create_dirs=False):
		import tempfile
		from platform import system as kernel_type
		from pathlib import Path

		self.kernel_type = kernel_type()
		if (self.kernel_type == 'FreeBSD'):
			self.dir_home = os.path.abspath(os.path.join('/usr', Path.home()))
		else:
			self.dir_home = Path.home()

		self.file_temp = tempfile.NamedTemporaryFile(delete=True).name
		self.dir_temp = tempfile.TemporaryDirectory().name
		self.dir_unpack = os.path.abspath(os.path.join(self.dir_temp, 'unpack'))
		self.dir_gitclone = os.path.abspath(os.path.join(self.dir_temp, 'gitclone'))
		self.appname = ''

		del tempfile
		del Path
		del kernel_type
		
		if os.name == 'nt': # Windows
			self.dir_bin = os.path.abspath(os.path.join(self.dir_home, 'AppData', 'Local', 'Programs'))
			self.dir_icons = None
			self.dir_desktop_links = ''
			self.dir_gnupg = os.path.abspath(os.path.join(self.dir_home, '.gnupg'))
			self.dir_cache = os.path.abspath(os.path.join(self.dir_home, 'AppData', 'LocalLow'))
			self.dir_config = os.path.abspath(os.path.join(self.dir_home, 'AppData', 'Roaming'))
		elif os.name == 'posix':
			if (os.geteuid() == 0): # Root
				self.dir_bin = '/usr/local/bin'
				self.dir_icons = '/usr/share/icons/hicolor'
				self.dir_desktop_links = '/usr/share/applications'
				self.dir_themes = '/usr/share/themes'
				self.dir_cache = '/var/cache'
				self.dir_gnupg = '/root/.gnupg'
				self.dir_config = '/etc'
				self.file_bashrc = '/etc/bashrc'
			else: # User

				self.dir_bin = os.path.abspath(os.path.join(self.dir_home, '.local', 'bin'))
				self.dir_icons = os.path.abspath(os.path.join(self.dir_home, '.local', 'share', 'icons'))
				self.dir_desktop_links = os.path.abspath(os.path.join(self.dir_home, '.local', 'share', 'applications'))
				self.dir_cache = os.path.abspath(os.path.join(self.dir_home, '.cache'))
				self.dir_gnupg = os.path.abspath(os.path.join(self.dir_home, '.gnupg'))
				self.dir_config = os.path.abspath(os.path.join(self.dir_home, '.config'))
				self.file_bashrc = os.path.abspath(os.path.join(self.dir_home, '.bashrc'))

		self.user_dirs = {
			'dir_home': self.dir_home,
			'dir_cache': self.dir_cache,
			'dir_config': self.dir_config,
			'dir_bin': self.dir_bin,
			'dir_icons': self.dir_icons,
			'dir_gnupg': self.dir_gnupg,
			'dir_temp': self.dir_temp,
			'dir_unpack': self.dir_unpack,
			'dir_gitclone': self.dir_gitclone,
			'dir_desktop_links': self.dir_desktop_links,
			}

		# Criar os diretórios se receber True
		if create_dirs == True:
			for key in self.user_dirs:
				d = self.user_dirs[key]
				try:
					os.makedirs(d)
				except(FileExistsError):
					pass
				except Exception as err:
					from time import sleep
					print(type(err))
					sleep(0.25)
					del sleep
				else:
					pass

	# Getter
	@property
	def appname(self):
		return self._appname
	
	# Setter
	@appname.setter
	def appname(self, name):
		self._appname = name

	def get_dir_cache(self):
		'''Diretório cache deste programa baseado no appnamme
			EX: cfg = UserDirs(True)
			    cfg.appname = "MyAppName"
			    print(cfg.get_dir_cache())
		'''
		return os.path.abspath(os.path.join(self.dir_cache, self.appname))

	def get_dir_config(self):
		'''
		Diretório de configuração deste programa baseado em appname
			EX: cfg = UserDirs(True)
			    cfg.appname = "MyAppName"
			    print(cfg.get_dir_config())
		'''
		return os.path.abspath(os.path.join(self.dir_config, self.appname))

	def get_file_config(self):
		'''Arquivo de configuração exclusivo do programa baseado em appname
			EX: cfg = UserDirs(True)
			    cfg.appname = "MyAppName"
			    print(cfg.get_file_config())
		'''
		dir_appname_config = self.get_dir_config()
		file_name_config = '{}.conf'.format(self.appname)
		return os.path.abspath(os.path.join(dir_appname_config, file_name_config))
		
	