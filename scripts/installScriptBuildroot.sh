#!/bin/bash

psplash()
{
    printf " ----- psplash  ----- \n \n "
    cp /home/Downloads/LinuxEmbedded/startImage/psplash /usr/bin/
}


configure_kernel()
{
   printf " ----- Kernel configuration  ----- \n\n "
   mkdir /boot
   mount /dev/mmcblk0p1 /boot
   cp /home/Downloads/LinuxEmbedded/configFiles/kernel/* /boot/
   umount /boot

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
    systemctl enable start.service
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
    wget https://github.com/ampache/ampache/releases/download/4.1.0/ampache-4.1.0_all.zip
    mkdir -p ampache
    mv ampache-4.1.0_all.zip ampache/
    unzip ampache-4.1.0_all.zip
    rm ampache-4.1.0_all.zip
    cp -r ampache /usr/htdocs/ampache
    rm -rf ampache

    cp /home/Downloads/LinuxEmbedded/website/* /usr/htdocs/
    
    cp /usr/htdocs/ampache/play/.htaccess.dist /usr/htdocs/ampache/play/.htaccess
    chmod 777 /usr/htdocs/ampache/play/.htaccess 
    cp /usr/htdocs/ampache/rest/.htaccess.dist /usr/htdocs/ampache/rest/.htaccess
    chmod 777 /usr/htdocs/ampache/rest/.htaccess

    cp /usr/htdocs/ampache/channel/.htaccess.dist /usr/htdocs/ampache/channel/.htaccess
    chmod 777 /usr/htdocs/ampache/channel/.htaccess
    chmod -R 777 /usr/htdocs/ampache/config


    cp /home/Downloads/LinuxEmbedded/configFiles/apache/php-fpm.conf /etc/php-fpm.conf
    cp /home/Downloads/LinuxEmbedded/configFiles/apache/httpd.conf /etc/apache2/httpd.conf
    cp /home/Downloads/LinuxEmbedded/configFiles/apache/apache.service /usr/lib/systemd/system/
    systemctl enable apache.service
    systemctl start apache.service
}

install_filemanager()
{
	printf " ----- FileBrowser install  ----- \n\n "
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
	printf " ----- vsftpd configuration  ----- \n\n "
	cp /home/Downloads/LinuxEmbedded/configFiles/vsftpd/vsftpd.service /usr/lib/systemd/system/
	systemctl enable vsftpd.service
}

install_youtubeDL()
{
    printf " ----- YoutubeDL install  ----- \n\n "
    wget https://files.pythonhosted.org/packages/1e/c7/8f0b6cb38fd9c44adb7c612c2f83bb0a53f04a82a29165f19c320ff4c243/youtube_dl-2020.1.24.tar.gz
    gunzip youtube_dl-2020.1.24.tar.gz
    tar xf youtube_dl-2020.1.24.tar
    mv youtube_dl-2020.1.24/youtube_dl /usr/lib/python2.7/youtube_dl
    rm youtube_dl-2020.1.24.tar
    rm -rf youtube_dl-2020.1.24
    cp /home/Downloads/LinuxEmbedded/configFiles/youtubedl/systemd-youtubedl.* /usr/lib/systemd/system/
    cp /home/Downloads/LinuxEmbedded/scripts/downloadFromYoutube.py /opt/
    systemctl enable systemd-youtubedl.timer
}

configure_transmission()
{
    printf " ----- transmission (Torrent Client) configuration  ----- \n\n "
    systemctl stop transmission-daemon
    cp /home/Downloads/LinuxEmbedded/configFiles/transmission/settings.json /var/lib/transmission/.config/transmission-daemon/settings.json
    systemctl start transmission-daemon
}

configure_samba()
{
    printf " ----- Samba configuration  ----- \n\n "
    systemctl stop smb.service
    systemctl stop nmb.service
    systemctl disable smb.service
    systemctl disable nmb.service
    cp /home/Downloads/LinuxEmbedded/configFiles/Samba/smbd.service /usr/lib/systemd/system/smb.service
    cp /home/Downloads/LinuxEmbedded/configFiles/Samba/nmbd.service /usr/lib/systemd/system/nmb.service
    cp /home/Downloads/LinuxEmbedded/configFiles/Samba/smb.conf /etc/samba/
    systemctl enable smb.service
    systemctl enable nmb.service
}

configure_minidlna()
{
    printf " ----- MiniDLNA configuration  ----- \n\n "
    systemctl stop minidlnad.service
    cp /home/Downloads/LinuxEmbedded/configFiles/miniDLNA/minidlna.conf /etc/
    systemctl start minidlnad.service
}

configure_mpd()
{
    printf " ----- MPD configuration  ----- \n\n "
    mkdir /var/lib/mpd
    mkdir /var/lib/mpd/playlists
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
#configure_kernel
#configure_MediaServer
#configure_X11
#configure_Ampache
#install_filemanager
#configure_vsftpd
#install_youtubeDL
#configure_transmission
#configure_samba
#configure_minidlna
#configure_mpd

