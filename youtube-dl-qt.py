#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Este programa e um GUI gráfico que usa o youtube-dl para baixar vídes do youtube.

Configuração:
   Debian/Ubuntu
	  $ sudo apt install python3-pyqt5

   Linux
	  $ pip3 install PyQt5

   Windows
	  $ pip install PyQt5
'''


import os, sys
import subprocess
import tempfile
import platform
import urllib.request, urllib.parse, urllib.error
from pathlib import Path
from pathlib import Path
from PyQt5 import QtWidgets, QtGui

dir_of_executable = os.path.dirname(__file__)

__version__='2020-09-20'


app_name = 'youtube-dl-qt'

class Configure:
	'''
	Classe para configurações básicas do sistema operacional.
	'''
	def __init__(self):
		self.home = Path.home()
		self.destination_videos = self.home
		if platform.system() == 'Linux':
			self.dir_config = os.path.abspath(os.path.join(self.home, '.config', app_name))
			self.dir_cache = os.path.abspath(os.path.join(self.home, '.cache', app_name))
			self.file_config = os.path.abspath(os.path.join(self.dir_config, '{}.conf'.format(app_name)))
			self.script_youtube_dl_path = os.path.abspath(os.path.join(self.dir_cache, 'youtube-dl'))
			self.url_youtube_dl = 'https://yt-dl.org/downloads/latest/youtube-dl'
		elif platform.system() == 'Windows':
			self.dir_config = os.path.abspath(os.path.join(self.home, 'AppData', 'Local', 'Programs', app_name))
			self.dir_cache = self.dir_cache
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
		print(f'Script {self.script_youtube_dl_path}')
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
		   
		# Se o arquivo de configuração ainda não existir no sistema ele será criado
		# com a configuração padrão.
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

		if os.path.isfile(self.file_config) == False: # Primeira execução do programa no computador.
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

		print(f'=> Entrando no diretório ... {self.dir_cache}'); os.chdir(self.dir_cache)
		print(f'=> Instalando ... {self.script_youtube_dl_path}')
		print(f'=> Conectando ... {self.url_youtube_dl}')
		urllib.request.urlretrieve(self.url_youtube_dl, self.script_youtube_dl_path)

		if platform.system() == 'Linux':
			os.system(f'chmod +x {self.script_youtube_dl_path}')
		elif platform.system() == 'Windows':
			print(f'Baixando visual C x86 ... {self.url_visual_c}')
			urllib.request.urlretrieve(self.url_visual_c, 'vcredist_x86.exe')
			os.system('vcredist_x86.exe')

		return True

class YoutubeDownload:
	def __init__(self):
		pass
		self.youtube_dl = Configure().set_file_youtube_dl()

	def exec_download(self, url):
		# Verificar se o youtube-dl foi baixado no diretório de cache.
		Configure().get_youtube_dl()

		destination = Configure().get_dir_download()
		os.chdir(destination)
		print(f'Baixando ... {url}')
		#os.system(f'{self.youtube_dl} --no-playlist --continue --format mp4 -o "%(title)s.%(ext)s" {url}')
		dow = subprocess.getstatusoutput(f'{self.youtube_dl} --no-playlist --continue --format mp4 -o "%(title)s.%(ext)s" {url}')
		
		if dow[0] == 0:
			print('OK')
			return 0
		else:
			print(f'FALHA: {dow[1]}')
			return dow[1]

class MessageWindow:
	'''
	https://doc.qt.io/qtforpython/PySide2/QtWidgets/QMessageBox.html
	'''
	def __init__(self):
		self.msgBox = QtWidgets.QMessageBox()

	def msgOK(self, text=''):
		self.msgBox.setText(text)
		self.msgBox.exec()


class MainWindow(QtWidgets.QWidget):
	def __init__(self):
		super(MainWindow, self).__init__()
		# Configurações da janela principal
		self.setWindowTitle('Youtube Download QtGui')
		self.setGeometry(200, 200, 640, 280)

		# Definir tipo dos botões
		self.buttonUrlText = QtWidgets.QLineEdit(self)
		self.buttonShowAbout = QtWidgets.QLabel()
		self.buttonShowDirDownload = QtWidgets.QLabel()
		self.buttonSelectDestination = QtWidgets.QPushButton('Alterar pasta', self)
		self.buttonSelectDestination.clicked.connect(self.selectFolder)
		self.buttonDownload = QtWidgets.QPushButton('Baixar', self)
		self.buttonDownload.clicked.connect(self.run_download)
		self.buttonExit = QtWidgets.QPushButton('Sair', self)
		self.buttonExit.clicked.connect(self.clickExit)

		layout = QtWidgets.QVBoxLayout(self)
		layout.addWidget(self.buttonUrlText)
		layout.addWidget(self.buttonShowAbout)
		layout.addWidget(self.buttonShowDirDownload)
		layout.addWidget(self.buttonSelectDestination)
		layout.addWidget(self.buttonDownload)
		layout.addWidget(self.buttonExit)

		self.buttonShowAbout.setText('Youtube Download - 1.0 Alpha')
		self.dir_downoload = Configure().get_dir_download()
		self.buttonShowDirDownload.setText(f'Salvar em: {self.dir_downoload}')
		
	def getUrl(self):
		return self.buttonUrlText.text()

	def run_download(self):
		action = YoutubeDownload().exec_download(self.getUrl())
		if action == 0:
			MessageWindow().msgOK('Download finalizado')
		else:
			MessageWindow().msgOK(action)

	def selectFolder(self):
		select_dir = QtWidgets.QFileDialog.getExistingDirectory(
						None, 
						'Selecione um diretório', 
						self.dir_downoload, 
						QtWidgets.QFileDialog.ShowDirsOnly
						)
		Configure().set_dir_download(select_dir)
		self.dir_downoload = Configure().get_dir_download()
		self.buttonShowDirDownload.setText(f'Salvar em: {self.dir_downoload}')

	def selectVideoFile(self):
		options = QtWidgets.QFileDialog.Options()
		options |= QtWidgets.QFileDialog.DontUseNativeDialog
		fileName= QtWidgets.QFileDialog.getSaveFileName(
						self,"QFileDialog.getSaveFileName()",
						"",
						"Video Files (*.mp4);;All Files (*)", 
						options=options)
		if fileName:
			f = fileName[0].strip().replace(' ', '_')
			return f
		else:
			return None

	def clickExit(self):
		'''
		exit_msg = QtWidgets.QMessageBox.question(
							self, 
							'MessageBox', 
							"Deseja sair?", 
							QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel, 
							QtWidgets.QMessageBox.Cancel
							)

		if exit_msg == QtWidgets.QMessageBox.Yes:
			print('QMessageBox.Yes: saindo')
		'''
		sys.exit()
 
	  
if __name__=="__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec_())
	
