#!/usr/bin/env python3

from setuptools import setup


DESCRIPTION = 'Baixar vídeos do youtube'
LONG_DESCRIPTION = 'Baixa vídeos do youtube em um diretório configurado pelo usuário'

setup(
	name='youtube_dl_qt',
	version='0.1.0',
	description=DESCRIPTION,
	long_description=LONG_DESCRIPTION,
	author='Bruno Chaves',
	author_email='brunodasill@gmail.com',
	license='MIT',
	packages=['youtube_dl_qt'],
	
	zip_safe=False,
	url='https://github.com/Brunopvh/youtube-dl-qt',
	project_urls = {
		'Código fonte': 'https://github.com/Brunopvh/youtube-dl-qt',
		'Download': 'https://github.com/Brunopvh/youtube-dl-qt/archive/refs/heads/version-dev.zip'
	},
)


#install_requires=['PyQt5'],