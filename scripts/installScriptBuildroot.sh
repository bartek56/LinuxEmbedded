#!/bin/bash

psplash()
{
    printf " ----- psplash  ----- \n \n "
    cp /home/Downloads/LinuxEmbedded/startImage/psplash /usr/bin/
}

configure_MediaServer()
{
    printf " ----- MediaServer Configuration  ----- \n\n "
    cp /home/Downloads/LinuxEmbedded/configFiles/*.sh /opt/
    cp /home/Downloads/LinuxEmbedded/configFiles/start.service /usr/lib/systemd/system/
    systemctl enable start.service
    unlink /etc/localtime
    ln -s /usr/share/zoneinfo/Europe/Warsaw /etc/localtime
    date -u
    systemctl start start.service
}

configure_X11()
{
    printf " ----- X11 Configuration  ----- \n\n "
    cp /home/Downloads/LinuxEmbedded/configFiles/x11/99-calibration.conf /usr/share/X11/xorg.conf.d/
    mv /usr/share/X11/xorg.conf.d/10-evdev.conf /usr/share/X11/xorg.conf.d/45-evdev.conf
}

configure_Ampache()
{
    printf " ----- Ampache configuration  ----- \n\n "
    wget https://github.com/ampache/ampache/archive/4.1.0.tar.gz
    mkdir ampache
    gunzip 4.1.0.tar.gz
    tar -xf 4.1.0.tar -C ampache/
    mkdir -p /usr/htdocs/ampache
    mv ampache/ampache-4.1.0/* /usr/htdocs/ampache/
    rm -rf ampache
    rm 4.1.0.tar
    cp /home/Downloads/LinuxEmbedded/website/* /usr/htdocs/
    cp /usr/htdocs/ampache/play/.htaccess.dist /usr/htdocs/ampache/play/.htaccess
    cp /usr/htdocs/ampache/rest/.htaccess.dist /usr/htdocs/ampache/rest/.htaccess
    cp /usr/htdocs/ampache/channel/.htaccess.dist /usr/htdocs/ampache/channel/.htaccess
    cp /home/Downloads/LinuxEmbedded/configFiles/apache/httpd.conf /etc/apache2/httpd.conf
    cp /home/Downloads/LinuxEmbedded/configFiles/apache/apache.service /usr/lib/systemd/system/
    systemctl enable apache.service
    systemctl start apache.service
}

install_filemanager()
{
	trap 'echo -e "Aborted, error $? in command: $BASH_COMMAND"; trap ERR; return 1' ERR
	filemanager_os="unsupported"
	filemanager_arch="unknown"
	install_path="/usr/local/bin"

	# Termux on Android has $PREFIX set which already ends with /usr
	if [[ -n "$ANDROID_ROOT" && -n "$PREFIX" ]]; then
		install_path="$PREFIX/bin"
	fi

	# Fall back to /usr/bin if necessary
	if [[ ! -d $install_path ]]; then
		install_path="/usr/bin"
	fi

	# Not every platform has or needs sudo (https://termux.com/linux.html)
	((EUID)) && [[ -z "$ANDROID_ROOT" ]] && sudo_cmd="sudo"

	#########################
	# Which OS and version? #
	#########################

	filemanager_bin="filebrowser"
	filemanager_dl_ext=".tar.gz"
	filemanager_dl_ext2=".tar"

	# NOTE: `uname -m` is more accurate and universal than `arch`
	# See https://en.wikipedia.org/wiki/Uname
	unamem="$(uname -m)"
	case $unamem in
	*aarch64*)
		filemanager_arch="arm64";;
	*64*)
		filemanager_arch="amd64";;
	*86*)
		filemanager_arch="386";;
	*armv5*)
		filemanager_arch="armv5";;
	*armv6*)
		filemanager_arch="armv6";;
	*armv7*)
		filemanager_arch="armv7";;
	*)
		echo "Aborted, unsupported or unknown architecture: $unamem"
		return 2
		;;
	esac

	unameu="$(tr '[:lower:]' '[:upper:]' <<<$(uname))"
	if [[ $unameu == *DARWIN* ]]; then
		filemanager_os="darwin"
	elif [[ $unameu == *LINUX* ]]; then
		filemanager_os="linux"
	elif [[ $unameu == *FREEBSD* ]]; then
		filemanager_os="freebsd"
	elif [[ $unameu == *NETBSD* ]]; then
		filemanager_os="netbsd"
	elif [[ $unameu == *OPENBSD* ]]; then
		filemanager_os="openbsd"
	elif [[ $unameu == *WIN* || $unameu == MSYS* ]]; then
		# Should catch cygwin
		sudo_cmd=""
		filemanager_os="windows"
		filemanager_bin="filebrowser.exe"
		filemanager_dl_ext=".zip"
	else
		echo "Aborted, unsupported or unknown OS: $uname"
		return 6
	fi

	########################
	# Download and extract #
	########################

	echo "Downloading File Browser for $filemanager_os/$filemanager_arch..."
	filemanager_file="${filemanager_os}-$filemanager_arch-filebrowser$filemanager_dl_ext"
        filemanager_file2="${filemanager_os}-$filemanager_arch-filebrowser$filemanager_dl_ext2"

	filemanager_tar="v2.0.16"
	filemanager_url="https://github.com/filebrowser/filebrowser/releases/download/v2.0.16/$filemanager_file"
	echo "$filemanager_url"


	if type -p curl >/dev/null 2>&1; then
		echo "curl"
                
	elif type -p wget >/dev/null 2>&1; then
		echo "wget"
                wget "$filemanager_url"
	else
		echo "Aborted, could not find curl or wget"
		return 7
	fi

	echo "Extracting..."

        gunzip "$filemanager_file" 
        tar xf "$filemanager_file2"

	chmod +x "$filemanager_bin"

	echo "Putting filemanager in $install_path (may require password)"
	$sudo_cmd mv "$filemanager_bin" "$install_path/$filemanager_bin"
	if setcap_cmd=$(PATH+=$PATH:/sbin type -p setcap); then
		$sudo_cmd $setcap_cmd cap_net_bind_service=+ep "$install_path/$filemanager_bin"
	fi
	$sudo_cmd rm -- "$filemanager_file2"

	cp /home/Downloads/LinuxEmbedded/configFiles/fileBrowser/filebrowser.service /usr/lib/systemd/system/fileBrowser.service

	if type -p $filemanager_bin >/dev/null 2>&1; then
		echo "Successfully installed"
		trap ERR
		return 0
	else
		echo "Something went wrong, File Browser is not in your path"
		trap ERR
		return 1
	fi
}

configure_vsftpd()
{
	cp /home/Downloads/LinuxEmbedded/configFiles/vsftpd/vsftpd.service /usr/lib/systemd/system/
}

install_youtubeDL()
{
    wget https://files.pythonhosted.org/packages/b0/20/c8ac7a62f566059f2e7812326327a648943c1837d64a66054b9f17d9aa58/youtube_dl-2020.1.15.tar.gz
    gunzip youtube_dl-2020.1.15.tar.gz
    tar xf youtube_dl-2020.1.15.tar
    mv youtube_dl-2020.1.15/youtube_dl /usr/lib/python2.7/dist-packages/youtube_dl
    rm youtube_dl-2020.1.15.tar
    rm -rf youtube_dl-2020.1.15
    cp /home/Downloads/LinuxEmbedded/configFiles/youtubedl/systemd-youtubedl.* /usr/lib/systemd/system/
    cp /home/Downloads/LinuxEmbedded/scripts/downloadFromYoutube.py /opt/
    systemctl enable systemd-youtubedl.timer
}

configure_transmission()
{
    systemctl stop transmission-daemon
    cp /home/Downloads/LinuxEmbedded/configFiles/transmission/settings.json /var/lib/transmission/.config/transmission-daemon/settings.json
    systemctl start transmission-daemon
}

configure_samba()
{
    #systemctl stop smb.service
    #systemctl stop nmb.service
    systemctl disable smb.service
    systemctl disable nmb.service
    cp /home/Downloads/LinuxEmbedded/configFiles/Samba/smbd.service /usr/lib/systemd/system/smb.service
    cp /home/Downloads/LinuxEmbedded/configFiles/Samba/nmbd.service /usr/lib/systemd/system/nmb.service
    cp /home/Downloads/LinuxEmbedded/configFiles/Samba/smb.conf /etc/samba/
    systemctl enable smb.service
    systemctl enable nmb.service
    systemctl start smb.service
    systemctl start nmb.service
}

configure_minidlna()
{
    systemctl stop minidlnad.service
    cp /home/Downloads/LinuxEmbedded/configFiles/miniDLNA/minidlna.conf /etc/
    systemctl start minidlnad.service
}

configure_mpd()
{
#    mkdir /var/lib/mpd
#    mkdir /var/lib/mpd/playlists
    cp /home/Downloads/LinuxEmbedded/configFiles/mpd/mpd.conf /etc/
    cp /home/Downloads/LinuxEmbedded/configFiles/mpd/mpd.service /usr/lib/systemd/system/
    systemctl enable mpd.service
    systemctl start mpd.service
    
    cp /home/Downloads/LinuxEmbedded/configFiles/ympd/ympd.service /usr/lib/systemd/system/

    systemctl enable ympd
    systemctl start ympd
}



set -e
#psplash
#configure_MediaServer
#configure_X11
#configure_Ampache
#install_filemanager
#install_youtubeDL
#configure_transmission
#configure_samba
#configure_minidlna
#configure_mpd

