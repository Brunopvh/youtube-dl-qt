#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
from userconfig import UserDirs

user_conf = UserDirs(True)
user_conf.appname = 'youtube-dl-qt'

class Configure(object):
	'''
	Classe para configurações básicas do sistema operacional, diretórios
	pastas e arquivos necessários para este programa.
	'''
	def __init__(self):

		self.kernel_type = user_conf.kernel_type
		self.dir_temp = user_conf.dir_temp
		self.file_temp = user_conf.file_temp
		self.dir_cache = user_conf.get_dir_cache()
		self.dir_config = user_conf.get_dir_config()
		self.file_config = user_conf.get_file_config()
		self.destination_videos = user_conf.dir_home 

		if self.kernel_type == 'Linux':
			self.path_youtube_dl = os.path.abspath(os.path.join(self.dir_cache, 'youtube-dl'))
			self.url_youtube_dl = 'https://yt-dl.org/downloads/latest/youtube-dl'
		elif self.kernel_type == 'Windows':
			self.path_youtube_dl = os.path.abspath(os.path.join(self.dir_cache, 'youtube-dl.exe'))
			self.url_youtube_dl = 'https://yt-dl.org/downloads/2020.07.28/youtube-dl.exe'
			self.url_visual_c = 'https://download.microsoft.com/download/5/B/C/5BC5DBB3-652D-4DCE-B14A-475AB85EEF6E/vcredist_x86.exe'
		else:
			print(f'{__class__.__name__}: seu sistema não é suportado por este programa.')
			sys.exit()


	#Getter
	@property
	def destination_videos(self):
		return self._destination_videos

	@destination_videos.setter
	def destination_videos(self, destination):
		'''
		Setar o atributo self.destination_videos em seguida gravar o caminho no
		arquivo de configuração.
		'''
		if os.path.isdir(destination) == True:
			self._destination_videos = destination
		   
		# Se o caminho de downloads ainda não existir no arquivo de 
		# configuração, ele será gravado no arquivo agora.
		if os.path.isfile(self.file_config) == False:
			with open(self.file_config, 'w') as f:
				f.write(f'save_path={self.destination_videos}\n')
			return True
			
		# Se o arquivo já existir o programa irá ler o conteúdo da linha que
		# informa o caminho de downloads. Algo como save_path=/caminho/completo.
		with open(self.file_config, 'rt') as f:
			lines = f.readlines()
		
		for l in lines:
			if 'save_path=' in l:
				self._destination_videos = l.replace('\n', '').replace('save_path=', '')
				break

	def set_dir_download(self, destination):
		if os.path.isdir(destination) == False:
			print(f'O diretório não existe ... {destination}')
			return False

		with open(self.file_config, 'w') as f:
			f.write(f'save_path={destination}')

	def get_dir_download(self) -> str:
		with open(self.file_config, 'rt') as f:
			lines = f.readlines()

		for l in lines:
			if 'save_path' in l:
				return l.replace('\n', '').replace('save_path=', '')
				break

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
			print(type(err))
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