#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, stat, sys
import json
from shutil import which
from userconf import ConfigAppDirs

appname = 'youtube-dl-qt'

class UserPreferences(ConfigAppDirs):
	'''
	Classe para gerenciar as preferências do usuário em um arquivo .json.
	'''
	def __init__(self):
		super().__init__(appname)
		self.create_common_dirs()
		self.isyoutubedl_bin = False
		self.youtube_dl_bin = 'youtube-dl'
		if os.name == 'nt':
			self.youtube_dl_bin += '.exe'
		self.path_youtube_dl = os.path.join(self.get_dir_cache(), self.youtube_dl_bin)

		# Verificar se youtube-dl está instalado no systema.
		self.youtube_dl_system = which(self.youtube_dl_bin)
		if (self.youtube_dl_system != None) and (os.path.isfile(self.youtube_dl_system)):
			self.path_youtube_dl = self.youtube_dl_system

		self._video_formats = ['mp4', 'mkv', 'mp3',]

		self._preferences = {
			'path_videos': self.dir_home,
			'path_youtube_dl': self.path_youtube_dl,
			'video_format': 'mp4',
		}
		self.set_user_preferences()

	def set_user_preferences(self):
		if os.path.isfile(self.get_file_config()) == False:
			try:
				with open(self.get_file_config(), 'w', encoding='utf8') as f:
					json.dump(self._preferences, f, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'))
			except Exception as err:
				print(err)
			finally:
				return

		_pref = self.get_json_config()
		self._preferences = _pref

	def get_json_config(self):
		'''
		https://cursos.alura.com.br/forum/topico-ler-um-arquivo-json-com-python-e-imprimir-os-dados-em-formato-tabular-107166
		'''
		try:
			with open(self.get_file_config(), 'rt', encoding='utf8') as f:
				content = json.load(f)
		except Exception as err:
			print(err)
			print('Não foi possível ler o arquivo de configuraçaõ ... {}'.format(self.get_file_config()))
			return self._preferences # Retornar preferências padrão caso a leitura do json falhe.
		else:
			return content

	def update_preference(self, key: str, value: str):
		'''Atualiza apenas uma preferência no arquivo json'''
		self.set_user_preferences()
		if not key in self._preferences:
			self._preferences.update({key: value})
		else:
			self._preferences[key] = value

		try:
			with open(self.get_file_config(), 'w', encoding='utf8') as f:
				json.dump(self._preferences, f, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'))
		except Exception as err:
			print(__class__.__name__, err)

		print(self._preferences)

class Configure(UserPreferences):
	'''
	Classe para configurações básicas do sistema operacional, diretórios
	pastas e arquivos necessários para este programa.
	'''
	def __init__(self):
		super().__init__()

		if os.name == 'nt':
			self.url_youtube_dl = 'https://yt-dl.org/downloads/2020.07.28/youtube-dl.exe'
			self.url_visual_c = 'https://download.microsoft.com/download/5/B/C/5BC5DBB3-652D-4DCE-B14A-475AB85EEF6E/vcredist_x86.exe'
		else:
			self.url_youtube_dl = 'https://yt-dl.org/downloads/latest/youtube-dl'

	# Getter
	@property
	def url_youtube_dl(self):
		return self._url_youtube_dl

	# Setter
	@url_youtube_dl.setter
	def url_youtube_dl(self, url):
		self._url_youtube_dl = url

	def download_youtube_dl_bin(self):
		'''	
		Baixar o youtube-dl para Linux ou Windows.
		'''
		if os.path.isfile(self._preferences['path_youtube_dl']) == True:
			# Aterar permissão de execução do arquiv se necessário.
			if os.access(self._preferences['path_youtube_dl'], os.X_OK):
				return True
			os.chmod(self._preferences['path_youtube_dl'], stat.S_IXUSR)
			return True

		import urllib.request
		print(f'> Entrando no diretório ... {self.get_dir_cache()}')
		os.chdir(self.get_dir_cache())
		print(f'> Conectando ... {self.url_youtube_dl}', end=' ')

		try:
			urllib.request.urlretrieve(self.url_youtube_dl, self._preferences['path_youtube_dl'])
		except Exception as err:
			print(__class.__name__, err)
			return False
		else:
			print('OK')

		if os.name == 'posix':
			# Aterar permissão de execução do arquiv se necessário.
			if os.access(self._preferences['path_youtube_dl'], os.X_OK):
				return True
			os.chmod(self._preferences['path_youtube_dl'], stat.S_IXUSR)
		elif os.name == 'nt':
			print(f'> Baixando visual C x86 ... {self.url_visual_c}')
			try:
				urllib.request.urlretrieve(self.url_visual_c, 'vcredist_x86.exe')
			except Exception as err:
				print(__class__.__name__, err)
				return False
			else:
				print('> Instalando ... vcredist_x86.exe')
				os.system('vcredist_x86.exe')

		return True

