#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
import tempfile
import urllib.request, urllib.parse, urllib.error
from pathlib import Path
from platform import system as kernel_type

class ConfigureDirs:
    def __init__(self):
        self.home = Path.home()
        self.destination_videos = self.home
        if (kernel_type() == 'Linux') or (kernel_type() == 'FreeBSD'):
            self.dir_config = os.path.abspath(os.path.join(self.home, '.config', 'youtube-dlq'))
            self.file_config = os.path.abspath(os.path.join(self.dir_config, 'youtube-dlq.conf'))
            self.script_youtube_dl_path = os.path.abspath(os.path.join(self.home, '.local', 'bin'))
            self.scriptYoutubeDl = os.path.abspath(os.path.join(self.script_youtube_dl_path, 'youtube-dl'))
        elif kernel_type() == 'Windows':
            self.dir_config = os.path.abspath(os.path.join(self.home, 'AppData', 'Local', 'youtube-dlq'))
            self.file_config = os.path.abspath(os.path.join(self.dir_config, 'youtube-dlq.conf'))
            self.script_youtube_dl_path = os.path.abspath(os.path.join(self.home, 'AppData', 'Local', 'Programs'))
            self.scriptYoutubeDl = os.path.abspath(os.path.join(self.script_youtube_dl_path, 'youtube-dl.exe'))
        else:
            print(f'ConfigureDirs: seu sistema não é suportado por este programa.')
            sys.exit()

        if os.path.isdir(self.dir_config) == False:
            os.makedirs(self.dir_config)

        if os.path.isdir(self.script_youtube_dl_path) == False:
            os.makedirs(self.script_youtube_dl_path)


    def set_dir_download(self, destination=''):
        '''
        Este metodo salva o caminho de um diretório em um arquivo de texto para 
        ser lido pelo metodo (get_dir_downloads).
           O diretório escolhido para ser o destino padrão de downloads pode ser 
        configurado atráves deste metodo usando self.set_dir_downloads('caminho/completo/aqui').
        '''

        if os.path.isdir(destination) == True:
            self.destination_videos = destination
           
        if os.path.isfile(self.file_config) == False:
            with open(self.file_config, 'w') as f:
                f.write(f'save_path={self.destination_videos}\n')
            return
            
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

    def set_script_youtube_dl(self):
        return self.scriptYoutubeDl

    def install(self):
        url_ytdl_win = 'https://yt-dl.org/downloads/2020.07.28/youtube-dl.exe'
        url_ytdl_linux = 'https://yt-dl.org/downloads/latest/youtube-dl'
        url_visualC = 'https://download.microsoft.com/download/5/B/C/5BC5DBB3-652D-4DCE-B14A-475AB85EEF6E/vcredist_x86.exe'
        os.chdir(self.script_youtube_dl_path)
        if os.path.isfile(self.scriptYoutubeDl) == True:
            return

        print(f'Instalando {self.scriptYoutubeDl}')
        if (kernel_type() == 'Linux') or (kernel_type() == 'FreeBSD'):
            urllib.request.urlretrieve(url_ytdl_linux, self.scriptYoutubeDl)
            os.system(f'chmod +x {self.scriptYoutubeDl}')
        elif kernel_type() == 'Windows':
            tempDir =  tempfile.mkdtemp()
            os.chdir(tempDir)
            urllib.request.urlretrieve(url_ytdl_win, self.scriptYoutubeDl)
            print(f'Baixando visual C x86 em: {tempDir}')
            urllib.request.urlretrieve(url_visualC, 'vcredist_x86.exe')
            os.system('vcredist_x86.exe')

class YoutubeDownload:
    def __init__(self):
        self.scriptYoutubeDl = ConfigureDirs().set_script_youtube_dl()

    def exec_download(self, url):
        # Verificar se o youtube-dl está instalado.
        ConfigureDirs().install()

        destination = ConfigureDirs().get_dir_download()
        os.chdir(destination)
        print(f'Baixando: {url}')
        os.system(f'{self.scriptYoutubeDl} --no-playlist --continue --format mp4 -o "%(title)s.%(ext)s" {url}')
        print('OK')

    


