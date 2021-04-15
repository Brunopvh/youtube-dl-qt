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
from threading import Thread
try:
	from PyQt5.QtWidgets import (
							QApplication, QWidget, QMainWindow,
							QMessageBox, QFileDialog, QLineEdit,
							QLabel, QProgressBar, QPushButton,
							QVBoxLayout, QHBoxLayout, QGridLayout,
							QGroupBox, QComboBox,  QAction,
							)
	from PyQt5.QtGui import QIcon
	from PyQt5.QtCore import Qt

except Exception as err:
	print(err)
	sys.exit(1)

 
_script = os.path.realpath(__file__)
dir_of_executable = os.path.dirname(_script)
sys.path.insert(0, dir_of_executable)

from configure import Configure
from video_formats import video_formats

__version__ = '0.1.0'
__author__ = 'Bruno Chaves'
__repo__ = 'https://github.com/Brunopvh/youtube-dl-qt'
appcfg = Configure()

class MessageWindow(QWidget):
	'''
	https://doc.qt.io/qtforpython/PySide2/QtWidgets/QMessageBox.html
	https://stackoverflow.com/questions/40227047/python-pyqt5-how-to-show-an-error-message-with-pyqt5
	'''
	def __init__(self):
		super().__init__()
		self.msgBox = QMessageBox()

	def msgOK(self, text: str):
		self.msgBox.setText(text)
		self.msgBox.exec()

	def msgError(self, text=''):
		self.msgBox.setIcon(QMessageBox.Critical)
		self.msgBox.setText(text)
		#self.msg.setInformativeText('More information')
		self.msgBox.setWindowTitle("Error")
		self.msgBox.exec_()

class YtWindow(QMainWindow):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setWindowTitle('Youtube Download QtGui')
		self.setGeometry(250, 150, 670, 400)
		self.setFixedSize(670, 400)

		self.container = QWidget()
		self.setCentralWidget(self.container)
		self.yt_widgets = YtWidgets(self.container)
		self.grid_master = QGridLayout(self)

		self.setupUI()


	def setupUI(self):
		self.setupTopBar()
		self.grid_master.addWidget(self.yt_widgets, 0, 0)
		self.setLayout(self.grid_master)
		self.show()

	def setupTopBar(self):
		self.statusBar()
		menubar = self.menuBar()

		#=== Menu Arquivo ===#
		fileMenu = menubar.addMenu('&Arquivo')

		# Ações do menu arquivo
		exitAct = QAction(QIcon('exit.png'), '&Sair', self)
		exitAct.setShortcut('Ctrl+Q')
		exitAct.setStatusTip('Sair do programa')
		exitAct.triggered.connect(self.yt_widgets.clickExit)
		fileMenu.addAction(exitAct)

		aboutMenu = menubar.addMenu('&Sobre')
		versionMenu = aboutMenu.addMenu('Versão')
		versionMenu.addAction(__version__)
		authorMenu = aboutMenu.addMenu('Autor')
		authorMenu.addAction(__author__)
		siteMenu = aboutMenu.addMenu('Site')
		siteMenu.addAction(__repo__)


class YtWidgets(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self._min_width = 650
		self._min_height = 180
		self.__total_urls = 0

		self.group_A = QGroupBox('Adicioner URLs abaixo')
		self.group_B =QGroupBox('Selecione a pasta de destino e o formato de vídeo')
		self.group_C = QGroupBox('Download')
		self.horizontal1 = QHBoxLayout()
		self.grid1 = QGridLayout()
		self.grid2 = QGridLayout()
		self.grid_master = QGridLayout()
		self.group_master = QGroupBox()

		self.youtube_dl = appcfg.path_youtube_dl
		self.dir_downoload = appcfg.get_dir_download()
		# Lista com url dos vídeos a serem baixados.
		self.list_urls = []

		self.setupUI()

	def setupUI(self):
		# Widigets do primeiro grupo
		self.line_edit_url = QLineEdit(self, placeholderText='Adicione um url aqui')
		self.line_edit_url.setFixedSize(550, 50)
		self.btn_add_url = QPushButton('Adicionar', self)
		self.btn_add_url.setFixedSize(70, 50)
		self.btn_add_url.clicked.connect(self.add_url)
		self.grid1.addWidget(self.btn_add_url, 0, 0)
		self.grid1.addWidget(self.line_edit_url, 0, 1)
		self.group_A.setLayout(self.grid1)
		self.group_A.setFixedSize(self._min_width, 90)

		# Widigets do segundo grupo
		self.btn_select_destination = QPushButton('Alterar pasta', self)
		self.btn_select_destination.setFixedSize(130, 30)
		self.btn_select_destination.clicked.connect(self.selectFolder)
		self.label_dir_download = QLabel(self.dir_downoload, self)
		self.label_dir_download.setFixedSize(250, 30)
		self.combo_video_formats = QComboBox()
		self.combo_video_formats.addItems(video_formats)
		self.horizontal1.addWidget(self.btn_select_destination)
		self.horizontal1.addWidget(self.label_dir_download)
		self.horizontal1.addWidget(self.combo_video_formats)
		self.group_B.setLayout(self.horizontal1)
		self.group_B.setFixedSize(self._min_width, 90)

		# Adicionar o terceiro grupo de widgtes.
		self.btn_download = QPushButton('Baixar', self)
		self.btn_download.clicked.connect(self.thread_download)
		self.pbar = QProgressBar(self)
		self.grid2.addWidget(self.btn_download)
		self.grid2.addWidget(self.pbar)
		self.group_C.setLayout(self.grid2)

		# Adicionar todos os grupos na janela principal
		self.grid_master.addWidget(self.group_A, 0, 0)
		self.grid_master.addWidget(self.group_B, 1, 0)
		self.grid_master.addWidget(self.group_C, 2, 0)
		self.setLayout(self.grid_master)


	def getUrl(self):
		return self.line_edit_url.text()

	def thread_download(self):
		Thread(target=self.run_download).start()

	def run_download(self):
		'''
		Método para baixar o vídeo e mostrar o progresso de download.
		youtube-dl --no-playlist --continue --format mp4 -o "%(title)s.%(ext)s" URL
		'''
		# Verificar se o youtube-dl foi baixado no diretório de cache do usuário.
		appcfg.get_youtube_dl()

		os.chdir(appcfg.get_dir_download())
		print(f'Salvando vídeos em ... {appcfg.get_dir_download()}')

		# Verificar se a lista de url contém pelo menos um url adicionado.
		if len(self.list_urls) < 1:
			print('Adicione pelo menos um link de vídeo na caixa superior.')
			MessageWindow().msgOK('Adicione pelo menos um link de vídeo na caixa superior.')
			return False

		_list_url = self.list_urls
		for url in _list_url:
			print(f'Baixando ... {url}')

			commands = [
					self.youtube_dl,
					'--no-playlist',
					'--continue',
					'-o', '%(title)s.%(ext)s',
					'--format',
					]

			commands.append(self.combo_video_formats.currentText())
			commands.append(url)
			print('Opções de download', commands)
			OutPut = subprocess.Popen(commands, stdout=subprocess.PIPE, encoding="utf-8")

			Erro = True
			for line in OutPut.stdout:
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
				MessageWindow().msgError(f'Falha no download de ... {url}')
				return False
			elif Erro == False:
				MessageWindow().msgOK('Download(s) finalizado(s)')

	def add_url(self):
		'''
		Método para obter o url digitado na caixa de urls e inserir na lista 'self.list_urls'
		'''
		url = self.getUrl()
		if url == '':
			MessageWindow().msgOK('Adicione um url de download na caixa ao lado.')
		else:
			if url in self.list_urls:
				MessageWindow().msgOK('URL já foi adicionada. Adicione outra URL')
				return

			self.list_urls.append(url)
			self.line_edit_url.setText('')
			self.__total_urls += 1
			print(f'URL adicionada ... {url}')
		 
	def selectFolder(self):
		'''
		Usar janela do navegador de arquivos para selecionar uma pasta de destino
		para download dos vídeos.
		'''
		select_dir = QFileDialog.getExistingDirectory(
						None, 
						'Selecione um diretório', 
						self.dir_downoload, 
						QFileDialog.ShowDirsOnly
						)

		appcfg.set_dir_download(select_dir) # Gravar no arquivo de configuração.
		self.dir_downoload = select_dir     # Alterar o atributo.
		self.label_dir_download.setText(f'Salvar em: {self.dir_downoload}')

	def createFile(self):
		'''
		Este método está NÃO está em uso no momento.
		serve para selecionar o nome do arquivo antes de baixar.
		'''
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName= QFileDialog.getSaveFileName(
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
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
		if fileName:
			return fileName
		else:
			return False


	def clickExit(self):
		sys.exit()
		'''
		exit_msg = QMessageBox.question(
							self, 
							'MessageBox', 
							"Deseja sair?", 
							QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
							)

		if exit_msg == QMessageBox.Yes:
			print('QMessageBox.Yes: saindo')
			sys.exit()
		'''

	  
def main():
	app = QApplication(sys.argv)
	window = YtWindow()
	window.show()
	sys.exit(app.exec_())

if __name__== "__main__":
	main()
	
