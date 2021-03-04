#!/usr/bin/env python3

import os
import tempfile

class UserDirs(object):
	"""
	Esta classe retorna os diretórios comumente usado por programas instalados manualmente no sistema.
	ou seja, retorna o diretório a ser usado por binários, destiono de arquivos '.desktop' etc.
	  Os valore mudam para o usuário é o root. Se receber create_dirs=True irá criar os diretórios
	se necessário, se receber False apenas atribui os valores sem criar nada.
	"""

	def __init__(self, create_dirs=False):
		from platform import system as kernel_type
		from pathlib import Path

		self.kernel_type = kernel_type()
		if (self.kernel_type == 'FreeBSD'):
			self.dir_home = os.path.abspath(os.path.join('/usr', Path.home()))
		else:
			self.dir_home = Path.home()

		del Path
		del kernel_type
		
		if os.name == 'nt': # Windows
			self.dir_bin = os.path.abspath(os.path.join(self.dir_home, 'AppData', 'Local', 'Programs', self.appname))
			self.dir_icons = ''
			self.dir_desktop_links = ''
			self.dir_gnupg = os.path.abspath(os.path.join(self.dir_home, '.gnupg'))
			self.dir_cache = os.path.abspath(os.path.join(self.dir_home, 'AppData', 'LocalLow', self.appname))
			self.dir_config = os.path.abspath(os.path.join(self.dir_home, 'AppData', 'Roaming', self.appname))
			self.file_config = os.path.abspath(os.path.join(self.dir_config, f'{self.appname}.conf'))
		elif os.name == 'posix':
			if (os.geteuid() == 0): # Root
				self.dir_home = '/root'
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
				
	
		self.file_temp = tempfile.NamedTemporaryFile(delete=True).name
		self.dir_temp = tempfile.TemporaryDirectory().name
			

		self.dir_unpack = os.path.abspath(os.path.join(self.dir_temp, 'unpack'))
		self.dir_gitclone = os.path.abspath(os.path.join(self.dir_temp, 'gitclone'))

		self.user_dirs = {
			'home': self.dir_home,
			'cache': self.dir_cache,
			'config': self.dir_config,
			'bin': self.dir_bin,
			'icons': self.dir_icons,
			'gnupg': self.dir_gnupg,
			'dir_temp': self.dir_temp,
			'unpack': self.dir_unpack,
			'gitclone': self.dir_gitclone,
			'desktop_links': self.dir_desktop_links,
			}

		if create_dirs == True:
			for key in self.user_dirs:
				d = self.user_dirs[key]
				try:
					os.makedirs(d)
				except(FileExistsError):
					pass
				except Exception as err:
					print(type(err))
				else:
					print(f'Criado com sucesso {d}')
		
	