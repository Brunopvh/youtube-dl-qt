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
from pathlib import Path
from PyQt5 import QtWidgets, QtGui

dir_of_executable = os.path.dirname(__file__)
sys.path.insert(0, dir_of_executable)
os.chdir(dir_of_executable)

from lib.youtube_lib import YoutubeDownload, ConfigureDirs

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
		self.dir_downoload = ConfigureDirs().get_dir_download()
		self.buttonShowDirDownload.setText(f'Salvar em: {self.dir_downoload}')
		
	def getUrl(self):
		return self.buttonUrlText.text()

	def run_download(self):
		YoutubeDownload().exec_download(self.getUrl())
		MessageWindow().msgOK('Download finalizado')

	def selectFolder(self):
		select_dir = QtWidgets.QFileDialog.getExistingDirectory(
						None, 
						'Selecione um diretório', 
						self.dir_downoload, 
						QtWidgets.QFileDialog.ShowDirsOnly
						)
		ConfigureDirs().set_dir_download(select_dir)
		self.dir_downoload = ConfigureDirs().get_dir_download()
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
		exit_msg = QtWidgets.QMessageBox.question(
							self, 
							'MessageBox', 
							"Deseja sair?", 
							QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel, 
							QtWidgets.QMessageBox.Cancel
							)

		if exit_msg == QtWidgets.QMessageBox.Yes:
			print('QMessageBox.Yes: saindo')
			sys.exit()
 
      
if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
	
