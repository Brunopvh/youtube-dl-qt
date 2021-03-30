#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
from platform import system as kernel_type
from lib.userconf import ConfigAppDirs

KERNEL_TYPE = kernel_type()
appname = 'youtube-dl-qt'

class Configure(ConfigAppDirs):
	'''
	Classe para configurações básicas do sistema operacional, diretórios
	pastas e arquivos necessários para este programa.
	'''
	def __init__(self):
		super().__init__(appname)
		
		self.kernel_type = KERNEL_TYPE
		self.create_dirs() # Criar diretórios do usuário
		self.create_common_dirs() # Criar diretórios deste app.
		self.file_config = self.get_file_config()
		self.__destination_videos = self.dir_home
		self.path_youtube_dl = os.path.join(self.dir_cache, 'youtube-dl')
		self.setDestinationVideos()

		if self.kernel_type == 'Linux':
			self.url_youtube_dl = 'https://yt-dl.org/downloads/latest/youtube-dl'
		elif self.kernel_type == 'Windows':
			self.path_youtube_dl += '.exe'
			self.url_youtube_dl = 'https://yt-dl.org/downloads/2020.07.28/youtube-dl.exe'
			self.url_visual_c = 'https://download.microsoft.com/download/5/B/C/5BC5DBB3-652D-4DCE-B14A-475AB85EEF6E/vcredist_x86.exe'
		else:
			print(f'{__class__.__name__}: seu sistema não é suportado por este programa.')
			sys.exit()
	# Getter
	@property
	def url_youtube_dl(self):
		return self._url_youtube_dl

	# Setter
	@url_youtube_dl.setter
	def url_youtube_dl(self, url):
		self._url_youtube_dl = url

	def setDestinationVideos(self):
		'''
		Setar o atributo self.__destination_videos em seguida gravar o caminho no
		arquivo de configuração.
		'''
		if os.path.isdir(self.__destination_videos) == False:
			print(f'O diretório não existe ... {self.__destination_videos}')
			sys.exit(1)

		# Verificar a existência do diretório de configuração deste programa.
		if os.path.isdir(self.get_dir_config()) == False:
			print(f'O diretório de configuração ... {self.get_dir_config()} não existe')
			sys.exit()
		   
		# Se o caminho de downloads ainda não existir no arquivo de 
		# configuração, ele será gravado no arquivo agora.
		if os.path.isfile(self.file_config) == False:
			with open(self.file_config, 'w') as f:
				f.write(f'save_path={self.__destination_videos}\n')
			return True
			
		# Se o arquivo já existir o programa irá ler o conteúdo da linha que
		# informa o caminho de downloads. Algo como save_path=/caminho/completo.
		with open(self.file_config, 'rt') as f:
			lines = f.readlines()
		
		for l in lines:
			if 'save_path=' in l:
				self.__destination_videos = l.replace('\n', '').replace('save_path=', '')
				break

	def set_dir_download(self, destination):
		if os.path.isdir(destination) == False:
			print(f'O diretório não existe ... {destination}')
			return False

		self.__destination_videos = destination
		with open(self.file_config, 'w') as f:
			f.write(f'save_path={self.__destination_videos}')

	def get_dir_download(self) -> str:
		try:
			with open(self.file_config, 'rt') as f:
				lines = f.readlines()
		except:
			print(__class__.__name__, "erro ao tentar abrir o arquivo", self.file_config)
			return False
		else:
			for l in lines:
				if 'save_path' in l:
					self.__destination_videos = l.replace('\n', '').replace('save_path=', '')
					break
			return self.__destination_videos

	def get_youtube_dl(self):
		'''	
		Baixar o youtube-dl para Linux ou Windows.
		'''
		if os.path.isfile(self.path_youtube_dl) == True:
			return True

		import urllib.request
		print(f'> Entrando no diretório ... {self.dir_cache}'); os.chdir(self.dir_cache)
		print(f'> Conectando ... {self.url_youtube_dl}', end=' ')

		try:
			urllib.request.urlretrieve(self.url_youtube_dl, self.path_youtube_dl)
		except Exception as err:
			print(__class.__name__, err)
			return False
		else:
			print('OK')

		if os.name == 'posix':
			os.system(f'chmod +x {self.path_youtube_dl}')
		elif os.name == 'nt':
			print(f'> Baixando visual C x86 ... {self.url_visual_c}')
			urllib.request.urlretrieve(self.url_visual_c, 'vcredist_x86.exe')
			print('> Instalando ... vcredist_x86.exe')
			os.system('vcredist_x86.exe')

		return True