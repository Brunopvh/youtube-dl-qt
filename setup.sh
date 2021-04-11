#!/usr/bin/env bash

if [[ $(id -u) == 0 ]]; then
	echo "Você não pode ser o 'root'"
	exit 1
fi


if [[ ! -x $(command -v python3) ]]; then
	echo -e "Instale o python3 para prosseguir."
	echo -e "Caso tenha uma versão do python3 instalada, crie um link em PATH com o executável python3."
	exit 1
fi

work_dir=$(pwd)
_script=$(readlink -f "$0")
dir_of_project=$(dirname $_script)
destination_icons=~/.local/share/icons
destination_desktop_file=~/.local/share/applications
cd $dir_of_project

[[ -d $destination_icons ]] || mkdir -p "$destination_icons"
[[ -d $destination_desktop_file ]] || mkdir -p "$destination_desktop_file"



function _copy()
{
	# $1 = arquivo/diretório fonte(src)
	# $2 = destino(path)

	src="$1"
	path="$2"

	[[ -z $2 ]] && {
		echo "(_copy) ... parâmetros incorretos detectados."
		return 1
	}

	echo -ne "Copiando ... $(basename $src) ... $path "
	if cp -R "$src" "$path" 1> /dev/null; then
		echo "OK"
		return "$?"
	else
		echo "ERRO"
		return 1
	fi

}

# Verificar a integridade do arquivo .png
echo -ne "Verificando sha256sum "
local_png_hash=$(sha256sum ./data/youtube-dl-qt.png | cut -d ' ' -f 1)
default_png_hash=$(grep -m 1 'sha256=' ./data/info.txt | cut -d '=' -f 2)
if [[ "$local_png_hash" == "$default_png_hash" ]]; then
	echo "OK"
else
	echo "ERRO"
	exit 1
fi

_copy ./data/youtube-dl-qt.png "$destination_icons"/youtube-dl-qt.png || exit 1
_copy ./data/youtube-dl-qt.desktop "$destination_desktop_file"/youtube-dl-qt.desktop || exit 1
chmod +x "$destination_desktop_file"/youtube-dl-qt.desktop

[[ -x $(command -v gtk-update-icon-cache) ]] && gtk-update-icon-cache

python3 -m pip install PyQt5 --user
python3 setup.py install --user

cd $work_dir
exit "$?"