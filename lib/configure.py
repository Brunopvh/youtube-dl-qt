#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
import platform
import urllib.request, urllib.parse, urllib.error
from pathlib import Path

app_name = 'youtube-dl-qt'
kernel_type = platform.system()

class Configure:
	'''
	Classe para configurações básicas do sistema operacional, diretórios
	pastas e arquivos necessários para este programa.
	'''
	def __init__(self):
		self.home = Path.home()
		# Diretório padrão caso o usuário não configure o diretório de downloads.
		self.destination_videos = self.home 

		if kernel_type == 'Linux':
			self.dir_config = os.path.abspath(os.path.join(self.home, '.config', app_name))
			self.dir_cache = os.path.abspath(os.path.join(self.home, '.cache', app_name))
			self.file_config = os.path.abspath(os.path.join(self.dir_config, '{}.conf'.format(app_name)))
			self.script_youtube_dl_path = os.path.abspath(os.path.join(self.dir_cache, 'youtube-dl'))
			self.url_youtube_dl = 'https://yt-dl.org/downloads/latest/youtube-dl'
		elif kernel_type == 'Windows':
			self.dir_config = os.path.abspath(os.path.join(self.home, 'AppData', 'Local', 'Programs', app_name))
			self.dir_cache = self.dir_config
			self.file_config = os.path.abspath(os.path.join(self.dir_config, '{}.conf'.format(app_name)))
			self.script_youtube_dl_path = os.path.abspath(os.path.join(self.dir_cache, 'youtube-dl.exe'))
			self.url_youtube_dl = 'https://yt-dl.org/downloads/2020.07.28/youtube-dl.exe'
			self.url_visual_c = 'https://download.microsoft.com/download/5/B/C/5BC5DBB3-652D-4DCE-B14A-475AB85EEF6E/vcredist_x86.exe'
		else:
			print(f'{__class__}: seu sistema não é suportado por este programa.')
			sys.exit()

		if os.path.isdir(self.dir_config) == False:
			os.makedirs(self.dir_config)

		if os.path.isdir(self.dir_cache) == False:
			os.makedirs(self.dir_cache)

	def set_file_youtube_dl(self):
		'''
		Setar o path completo do youtube-dl ou youtube-dl.exe no diretório cache.
		'''
		print(f'Script youtube-dl ... {self.script_youtube_dl_path}')
		return self.script_youtube_dl_path

	def set_dir_download(self, destination=''):
		'''
		Este metodo salva o caminho de um diretório em um arquivo de texto para 
		ser lido pelo metodo (get_dir_downloads).
		   O diretório escolhido para ser o destino padrão de downloads pode ser 
		configurado atráves deste metodo:

		   self.set_dir_downloads('caminho/completo/aqui').
		'''

		if os.path.isdir(destination) == True:
			self.destination_videos = destination
		   
		# Se o arquivo de configuração que contem o diretório de downloads ainda não existir 
		# ele será criado com o conteudo da variável self.destination_videos.
		if os.path.isfile(self.file_config) == False:
			with open(self.file_config, 'w') as f:
				f.write(f'save_path={self.destination_videos}\n')
			return
			
		# Se o arquivo já existir o programa irá ler o conteúdo para setar o
		# diretório de downloads.
		openFile = open(self.file_config, 'rt')
		Lines = openFile.readlines()
		for num in range(0, len(Lines)):
			line = Lines[num]
			if 'save_path' in line:
				del Lines[num]
				new_line = f'save_path={self.destination_videos}\n'
				Lines.insert(num, new_line)
				openFile.seek(0)
				openFile.close()
				break
		
		f = open(self.file_config, 'w')
		for L in Lines:
			f.write(L)
		f.seek(0)
		f.close()

	def get_dir_download(self):
		'''
		Este metodo lê o aquivo (self.file_config) e retorna como string o caminho
		padrão para downloads.
		'''

		# Primeira execução do programa no computador.
		if os.path.isfile(self.file_config) == False: 
			self.set_dir_download()

		f = open(self.file_config, 'rt').readlines()
		for line in f:
			if 'save_path=' in line:
				line = line.replace('\n', '').replace('save_path=', '')
				line = str(line)
				break
		return line

	def get_youtube_dl(self):
		'''	
		Baixar o youtube-dl para Linux ou Windows.
		'''
		if os.path.isfile(self.script_youtube_dl_path) == True:
			return True

		print(f'=> Entrando no diretório ... {self.dir_cache}') 
		os.chdir(self.dir_cache)
		print(f'=> Instalando ... {self.script_youtube_dl_path}')
		print(f'=> Conectando ... {self.url_youtube_dl}')

		try:
			urllib.request.urlretrieve(self.url_youtube_dl, self.script_youtube_dl_path)
		except Exception as err:
			print(err)
			return False
		else:
			print('OK')

		if platform.system() == 'Linux':
			os.system(f'chmod +x {self.script_youtube_dl_path}')
		elif platform.system() == 'Windows':
			print(f'Baixando visual C x86 ... {self.url_visual_c}')
			urllib.request.urlretrieve(self.url_visual_c, 'vcredist_x86.exe')
			print('=> Instalando ... vcredist_x86.exe')
			os.system('vcredist_x86.exe')

		return True