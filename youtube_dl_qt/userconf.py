#!/usr/bin/env python3

import os	
from getpass import getuser

class UserDirs(object):
	"""
	Esta classe tem como atributos, diretórios comumente usados por programas nos sitemas Linux e Windows.
	"""

	def __init__(self, user=getuser()):
		from platform import system as kernel_type
		from pathlib import Path

		# Se uid for igual a 0, será usado as configurações do 'root' independênte do parâmetro 'user'.
		if (os.geteuid() == 0):
			self.user = 'root'
		else:
			self.user = user

		self.kernel_type = kernel_type()
		if (self.kernel_type == 'FreeBSD'):
			self.dir_home = os.path.abspath(os.path.join('/usr', Path.home()))
		else:
			self.dir_home = Path.home()

		del Path
		del kernel_type
		
		if os.name == 'nt': # Windows
			self.dir_bin = os.path.abspath(os.path.join(self.dir_home, 'AppData', 'Local', 'Programs'))
			self.dir_icons = None
			self.dir_desktop_links = self.dir_bin
			self.dir_optional = ''
			self.dir_gnupg = os.path.abspath(os.path.join(self.dir_home, '.gnupg'))
			self.dir_cache = os.path.abspath(os.path.join(self.dir_home, 'AppData', 'LocalLow'))
			self.dir_config = os.path.abspath(os.path.join(self.dir_home, 'AppData', 'Roaming'))
		elif os.name == 'posix':
			if (os.geteuid() == 0) or (self.user == 'root'): # Root
				self.dir_home = '/root'
				self.dir_bin = '/usr/local/bin'
				self.dir_icons = '/usr/share/icons/hicolor/128x128/apps'
				self.dir_desktop_links = '/usr/share/applications'
				self.dir_themes = '/usr/share/themes'
				self.dir_cache = '/var/cache'
				self.dir_gnupg = '/root/.gnupg'
				self.dir_config = '/etc'
				self.dir_optional = '/opt'
				self.file_bashrc = '/etc/bashrc'
			else: # User

				self.dir_bin = os.path.abspath(os.path.join(self.dir_home, '.local', 'bin'))
				self.dir_icons = os.path.abspath(os.path.join(self.dir_home, '.local', 'share', 'icons'))
				self.dir_desktop_links = os.path.abspath(os.path.join(self.dir_home, '.local', 'share', 'applications'))
				self.dir_cache = os.path.abspath(os.path.join(self.dir_home, '.cache'))
				self.dir_gnupg = os.path.abspath(os.path.join(self.dir_home, '.gnupg'))
				self.dir_config = os.path.abspath(os.path.join(self.dir_home, '.config'))
				self.dir_optional = os.path.abspath(os.path.join(self.dir_home, '.local', 'share'))
				self.file_bashrc = os.path.abspath(os.path.join(self.dir_home, '.bashrc'))

	def get_user_dirs(self):

		self.user_dirs = {
			'dir_home': self.dir_home,
			'dir_cache': self.dir_cache,
			'dir_config': self.dir_config,
			'dir_bin': self.dir_bin,
			'dir_icons': self.dir_icons,
			'dir_optional': self.dir_optional,
			'dir_gnupg': self.dir_gnupg,
			'dir_desktop_links': self.dir_desktop_links,
			}

		return self.user_dirs

	def create_dirs(self):

		_dirs = self.get_user_dirs()
		for key in _dirs:
			d = _dirs[key]
			try:
				os.makedirs(d)
			except(FileExistsError):
				pass
			except(PermissionError):
				#print(__class__.__name__, 'você não tem permissão para criar ...', d)
				pass
			except Exception as err:
				from time import sleep
				print(__class__.__name__, type(err), d)
				sleep(0.5)
				del sleep
			else:
				pass

class ConfigAppDirs(UserDirs):
	def __init__(self, appname, user=getuser()):
		super().__init__(user)
		self.appname = appname
		self.create_dirs()

		import tempfile
		self.temp_file = tempfile.NamedTemporaryFile(delete=True).name
		self.dir_temp = tempfile.TemporaryDirectory().name
		self.dir_unpack = os.path.abspath(os.path.join(self.dir_temp, 'unpack'))
		self.dir_gitclone = os.path.abspath(os.path.join(self.dir_temp, 'gitclone'))
		del tempfile

	def get_common_dirs(self):
		self.common_dirs = {
			'dir_cache_app': self.get_dir_cache(),
			'dir_config_app': self.get_dir_config(),
			'temp_file': self.temp_file,
			'dir_temp': self.dir_temp,
			'dir_unpack': self.dir_unpack,
			'dir_gitclone': self.dir_gitclone,
			'dir_download': self.get_dir_downloads(),
		}

		return self.common_dirs

	def create_common_dirs(self):
		_dirs = self.get_common_dirs()

		for k in _dirs:
			d = _dirs[k]

			try:
				os.makedirs(d)
			except(FileExistsError):
				pass
			except(PermissionError):
				print(__class__.__name__, 'você não tem permissão para criar ...', d)
			except Exception as err:
				from time import sleep
				print(__class__.__name__, type(err))
				sleep(0.5)
				del sleep
			else:
				pass

	def get_dir_cache(self):
		return os.path.join(self.dir_cache, self.appname)

	def get_dir_downloads(self):
		return os.path.abspath(os.path.join(self.get_dir_cache(), 'downloads'))

	def get_dir_config(self):
		return os.path.join(self.dir_config, self.appname)

	def get_file_config(self):
		return os.path.join(self.get_dir_config(), f'{self.appname}.json')

	def get_file_bashrc(self) -> str:
		"""Retornar o caminho do bashrc para o root ou usuário."""
		if os.name == 'posix':
			if (os.geteuid == 0) or (self.user == 'root'):
				return '/etc/bash.bashrc'
			else:
				return os.path.join(self.dir_home, '.bashrc')

	def config_bashrc(self) -> bool:
		'''
		Configurar o arquivo .bashrc do usuário para inserir o diretório ~/.local/bin
		na variável de ambiente $PATH. Essa configuração será abortada caso ~/.local/bin já 
		exista em ~/.bashrc ou exista na variável $PATH.
		'''
		if os.geteuid == 0:
			return True

		if self.kernel_type != 'Linux':
			return False

		# Verificar se ~/.local/bin já está no PATH do usuário atual.
		user_local_path = os.environ['PATH']
		if self.dir_bin in user_local_path:
			return True

		file_bashrc_backup = self.get_file_bashrc() + '.bak'
		if os.path.isfile(file_bashrc_backup) == False:
			import shutil
			shutil.copyfile(self.get_file_bashrc(), file_bashrc_backup)
			del shutil

		print(self.get_file_bashrc())
		with open(self.get_file_bashrc(), 'rt') as f:
			content = f.readlines()

		import re
		RegExp = re.compile(r'{}.*{}'.format('^export PATH=', self.dir_bin))
		for line in content:
			if (RegExp.findall(line) != []): # O arquivo já foi configurado anteriormente.
				return True
				break

		NewUserPath = f'export PATH={self.dir_bin}:{user_local_path}'
		content.append(NewUserPath)
		f = open(self.get_file_bashrc(), 'w')
		for line in  content:
			f.write(line)
		f.close()


