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
import io
import urllib.request, urllib.parse, urllib.error
from pathlib import Path
from PyQt5 import QtWidgets, QtGui, QtCore

dir_of_executable = os.path.dirname(__file__)
dir_of_executable = os.path.abspath(os.path.join(dir_of_executable))
dir_local_libs = os.path.abspath(os.path.join(dir_of_executable, 'lib'))
sys.path.insert(0, dir_local_libs)
os.chdir(dir_of_executable)

from configure import Configure
from userconfig import UserDirs

__version__ = '2021-03-05'

appcfg = Configure()


class MessageWindow:
	'''
	https://doc.qt.io/qtforpython/PySide2/QtWidgets/QMessageBox.html
	'''
	def __init__(self):
		self.msgBox = QtWidgets.QMessageBox()

	def msgOK(self, text=''):
		self.msgBox.setText(text)
		self.msgBox.exec()

class MsgBox:
	'''
	https://stackoverflow.com/questions/40227047/python-pyqt5-how-to-show-an-error-message-with-pyqt5
	'''
	def __init__(self):
		self.msg_window = QtWidgets.QMessageBox()

	def error(self, text=''):
		self.msg_window.setIcon(QtWidgets.QMessageBox.Critical)
		self.msg_window.setText(text)
		#self.msg.setInformativeText('More information')
		self.msg_window.setWindowTitle("Error")
		self.msg_window.exec_()


class MainWindow(QtWidgets.QWidget):
	def __init__(self):
		super(MainWindow, self).__init__()
		# Configurações da janela principal
		self.setWindowTitle('Youtube Download QtGui')
		self.setGeometry(200, 200, 720, 320)

		# Definir tipo dos botões
		self.buttonUrlText = QtWidgets.QLineEdit(self)
		self.buttonShowAbout = QtWidgets.QLabel()
		self.buttonShowDirDownload = QtWidgets.QLabel()
		self.pbar = QtWidgets.QProgressBar(self)
		self.buttonSelectDestination = QtWidgets.QPushButton('Alterar pasta', self)
		self.buttonSelectDestination.clicked.connect(self.selectFolder)
		self.buttonAddUrl = QtWidgets.QPushButton('Adicionar url', self)
		self.buttonAddUrl.clicked.connect(self.add_url)
		self.buttonDownload = QtWidgets.QPushButton('Baixar', self)
		self.buttonDownload.clicked.connect(self.run_download)
		self.buttonExit = QtWidgets.QPushButton('Sair', self)
		self.buttonExit.clicked.connect(self.clickExit)

		layout = QtWidgets.QVBoxLayout(self)
		layout.addWidget(self.buttonUrlText)
		layout.addWidget(self.buttonShowAbout)
		layout.addWidget(self.buttonShowDirDownload)
		layout.addWidget(self.pbar)
		layout.addWidget(self.buttonSelectDestination)
		layout.addWidget(self.buttonAddUrl)
		layout.addWidget(self.buttonDownload)
		layout.addWidget(self.buttonExit)

		self.buttonUrlText.setText('Adicione uma url aqui - em seguida clique no botão "add-url"')
		self.buttonShowAbout.setText('Youtube Download - 1.0 Alpha')
		self.youtube_dl = appcfg.path_youtube_dl
		self.dir_downoload = appcfg.get_dir_download()
		self.buttonShowDirDownload.setText(f'Salvar em: {self.dir_downoload}')
		# Lista com url dos vídeos a serem baixados.
		self.list_urls = []
		
	def getUrl(self):
		return self.buttonUrlText.text()

	def run_download(self):
		'''
		Método para baixar o vídeo e mostrar o progresso de download.
		youtube-dl --no-playlist --continue --format mp4 -o "%(title)s.%(ext)s" URL
		'''
		# Verificar se o youtube-dl foi baixado no diretório de cache do usuário.
		if os.path.isfile(appcfg.path_youtube_dl) == False:
			return False

		os.chdir(appcfg.get_dir_download())
		print(f'Salvando vídeos em ... {appcfg.get_dir_download()}')

		# Verificar se a lista de url contém pelo menos um url adicionado.
		if len(self.list_urls) < 1:
			print('Adicione pelo menos um link de vídeo na caixa superior.')
			MessageWindow().msgOK('Adicione pelo menos um link de vídeo na caixa superior.')
			return False

		# Prosseguir com o download.
		for url in self.list_urls:
			print(f'Baixando ... {url}')
			OutPut = subprocess.Popen(
			[self.youtube_dl, 
			'--no-playlist', 
			'--continue', 
			'--format', 
			'mp4', 
			'-o', 
			'%(title)s.%(ext)s', 
			url], 
			stdout=subprocess.PIPE
			)

			Erro = True
			for line in io.TextIOWrapper(OutPut.stdout, encoding="utf-8"):
				print(line)
				if '%' in line:
					progress = line.split()[1].replace('%', '')
					print(f'\r{progress}', end='')
					if (progress != '100.0') and (progress != '100'):
						progress = progress[0: progress.find('.')]
						progress = int(progress)
						# Setar valor da barra de progresso.	
						self.pbar.setValue(progress)
					else:
						self.pbar.setValue(100)
						Erro = False
						break
					
			print()
			if Erro == True:
				MsgBox().error(f'Falha no download de ... {url}')
				return False
			elif Erro == False:
				#MessageWindow().msgOK('Download(s) finalizado(s)')
				pass

	def add_url(self):
		'''
		Método para obter o url digitado na caixa de urls e inserir na lista 'self.list_urls'
		'''
		url = self.getUrl()
		if url == '':
			print('Digite um URL de vídeo na caixa superior')
			MessageWindow().msgOK('Adicione um url de download na caixa superior.')
		else:
			self.list_urls.append(url)
			self.buttonUrlText.setText('')
			print(f'URL adicionada ... {url}')
		 
	def selectFolder(self):
		'''
		Usar janela do navegador de arquivos para selecionar uma pasta de destino
		para download dos vídeos.
		'''
		select_dir = QtWidgets.QFileDialog.getExistingDirectory(
						None, 
						'Selecione um diretório', 
						self.dir_downoload, 
						QtWidgets.QFileDialog.ShowDirsOnly
						)

		appcfg.set_dir_download(select_dir) # Gravar no arquivo de configuração.
		self.dir_downoload = select_dir     # Alterar o atributo.
		self.buttonShowDirDownload.setText(f'Salvar em: {self.dir_downoload}')

	def createFile(self):
		'''
		Este método está NÃO está em uso no momento.
		serve para selecionar o nome do arquivo antes de baixar.
		'''
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

	def openFileNameDialog(self):
		'''
		Caixa de seleção de arquivo.
		'''
		options = QtWidgets.QFileDialog.Options()
		options |= QtWidgets.QFileDialog.DontUseNativeDialog
		fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
		if fileName:
			return fileName
		else:
			return False


	def clickExit(self):
		exit_msg = QtWidgets.QMessageBox.question(
							self, 
							'MessageBox', 
							"Deseja sair?", 
							QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel
							)

		if exit_msg == QtWidgets.QMessageBox.Yes:
			print('QMessageBox.Yes: saindo')
			sys.exit()
 
	  
if __name__=="__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec_())
	
