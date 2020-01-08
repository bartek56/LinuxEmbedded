import subprocess


def upgrade():
    print ("\n\n\napt-get update\n\n\n")
    output = subprocess.run(["sudo", "apt-get", "update"], check=True)
    print (output)

    print ("\n\n\napt-get upgrade\n\n\n")
    output = subprocess.run(["sudo", "apt-get","-y", "upgrade"], check=True)
    print (output)
    
#    print ("\n\n\nInstall git\n\n\n")
#    output = subprocess.run(["sudo", "apt-get","--assume-yes", "install", "git"], check=True)
#    print (output)

    print ("\n\n\nInstall wget\n\n\n")
    output = subprocess.run(["sudo", "apt-get","--assume-yes", "install", "wget"], check=True)
    print (output)
   
    print ("\n\n\nInstall vim\n\n\n")
    output = subprocess.run(["sudo", "apt-get","--assume-yes", "install", "vim"], check=True)
    print (output)

    print ("\n\n\nInstall ntfs-3g\n\n\n")
    output = subprocess.run(["sudo", "apt-get","--assume-yes", "install", "ntfs-3g"], check=True)
    print (output)


def getScripts():
    print ("\n\n\nget Scripts\n\n\n")
    output = subprocess.run(["git", "clone","https://github.com/bartek56/LinuxEmbedded.git"], check=True)
    print (output)


def rpi_update():
    print ("\n\n\nRPI update\n\n\n")
    output = subprocess.run(["sudo", "SKIP_WARNING=1","rpi-update"], check=True)
    print (output)


def musicPlayerDaemonInstall():
    print ("\n\n\nInstall Music Player Daemon\n\n\n")
    output = subprocess.run(["sudo", "apt-get","--assume-yes", "install", "mpd"], check=True)
    print (output)

def websiteMusicPlayerClientInstall(ver):
    print ("\n\n\nInstall YMPD\n\n\n")
    tarFile="ympd-"+ver+"-armhf.tar.bz2"
    websiteStart="https://ympd.org/downloads/"
    url=websiteStart+tarfile
    output = subprocess.run(["wget", url], check=True)
    print (output)
    output = subprocess.run(["tar", "-xvf",tarFile], check=True)
    print (output)

    output = subprocess.run(["sudo", "rm", tarFile], check=True)
    print (output)

    output = subprocess.run(["sudo", "mkdir","/opt/ympd"], check=True)
    print (output)

    output = subprocess.run(["sudo", "cp","ympd/ympd", "/opt/ympd/ympd"], check=True)
    print (output)

    output = subprocess.run(["sudo", "rm","-rf", "ympd"], check=True)
    print (output)

    output = subprocess.run(["sudo", "cp","../configFiles/ympd/ympd.service", "/lib/systemd/system/"], check=True)
    print (output)

    output = subprocess.run(["sudo","systemctl", "enable","ympd.service"], check=True)
    print (output)

    output = subprocess.run(["sudo", "systemctl","start", "ympd.service"], check=True)
    print (output)

def getWebsite()
    print ("\n\n\nwebsite download\n\n\n")
    output = subprocess.run(["sudo", "cp","../website/*", "/var/www/html/", "tvheadend"], check=True)
    print (output)

def sambaInstall()
    print ("\n\n\nInstall Samba\n\n\n")
    output = subprocess.run(["sudo", "apt-get","--assume-yes", "install", "samba"], check=True)
    print (output)
    
    output = subprocess.run(["sudo", "cp","../configFiles/Samba/smb.config", "/etc/samba/"], check=True)
    print (output)

def torrentClientInstall()
    print ("\n\n\nInstall transmission-da (Torrent Client)\n\n\n")
    output = subprocess.run(["sudo", "apt-get","--assume-yes", "install", "transmission-daemon"], check=True)
    print (output)

def tvHeadEndInstall():
    print ("\n\n\nInstall TvHeadEnd\n\n\n")
    output = subprocess.run(["sudo", "apt-get","--assume-yes", "install", "tvheadend"], check=True)
    print (output)

def apache2Install():
    print ("\n\n\nInstall Apache2\n\n\n")
    output = subprocess.run(["sudo", "apt-get","--assume-yes", "install", "apache2"], check=True)
    print (output)

def ubooquityInstall(ver):
    print ("\n\n\nInstall ubooquity\n\n\n")
    zipFile="Ubooquity-"+ver+".zip"
    websiteStart="http://vaemendis.net/ubooquity/downloads/"
    url=websiteStart+tarfile
    output = subprocess.run(["wget", url], check=True)
    print (output)
    output = subprocess.run(["unzip", zipFile], check=True)
    print (output)

    output = subprocess.run(["sudo", "rm", zipFile], check=True)
    print (output)

    output = subprocess.run(["sudo", "mkdir","/opt/ubooquity"], check=True)
    print (output)

    output = subprocess.run(["sudo", "cp","ubooquity/Ubooquity.jar", "/opt/ubooquity/"], check=True)
    print (output)

    output = subprocess.run(["sudo", "rm","-rf", "ubooquity"], check=True)
    print (output)

    output = subprocess.run(["sudo", "cp","../configFiles/ubooquity/ubooquity.service", "/lib/systemd/system/"], check=True)
    print (output)

    output = subprocess.run(["sudo","systemctl", "enable","ubooquity.service"], check=True)
    print (output)

    output = subprocess.run(["sudo", "systemctl","start", "ubooquity.service"], check=True)
    print (output)

def fileBrowswerInstall():
    print ("\n\n\nInstall FileBrowser\n\n\n")
    
    output = subprocess.run(["sudo", "apt","--force-yes", "install", "curl"], check=True)
    print (output)

    output = subprocess.run(["curl", "-fsSL","https://filebrowser.xyz/get.sh", "|", "bash"], check=True)
    print (output)
  
    output = subprocess.run(["sudo", "cp","../configFiles/filebrowser/filebrowser.service", "/lib/systemd/system/"], check=True)
    print (output)

    output = subprocess.run(["sudo","systemctl", "enable","filebrowser.service"], check=True)
    print (output)

    output = subprocess.run(["sudo", "systemctl","start", "filebrowser.service"], check=True)
    print (output)


def plexInstall():
    print ("\n\n\nInstall Plex\n\n\n")

    output = subprocess.run(["sudo", "apt", "--force-yes", "install","apt-transport-https", "ca-certificates", "curl"], check=True)
    print (output)
    output = subprocess.run(["curl", "https://downloads.plex.tv/plex-keys/PlexSign.key", "|", "sudo","apt-key", "add", "-"], check=True)
    print (output)
    output = subprocess.run(["echo","deb", "https://downloads.plex.tv/repo/deb", "public", "main", "|", "sudo","tee", "/etc/apt/sources.list.d/plexmediaserver.list"], check=True)
    print (output)

    output = subprocess.run(["sudo", "apt", "update"], check=True)
    print (output)

    output = subprocess.run(["sudo", "apt", "--assume-yes","install", "plexmediaserver"], check=True)

def jellyfinInstall():
    print ("\n\n\nInstall Jellyfin\n\n\n")

    output = subprocess.run(["sudo", "apt", "--force-yes", "install", "apt-transport-https", "ca-certificates", "curl"], check=True)
    print (output)

    output = subprocess.run(["wget", "-O", "https://repo.jellyfin.org/debian/jellyfin_team.gpg.hey", "|", "sudo", "apt-key", "add", "-"], check=True)
    print (output)
    output = subprocess.run(["echo", "\"deb [arch=$( dpkg --print-architecture )] https://repo.jellyfin.org/debian $( lsb_release -c -s ) main\"", "|", "sudo","tee", "/etc/apt/sources.list.d/jellyfin.list"], check=True)
    print (output)

    output = subprocess.run(["sudo", "apt", "update"], check=True)
    print (output)

    output = subprocess.run(["sudo", "apt", "--assume-yes","install", "jellyfin"], check=True)




def main():
    upgrade()
    rpi_update()
    apache2Install()
    getWebsite()   
    musicPlayerDaemonInstall()
    websiteMusicPlayerClientInstall("1.2.3")
    sambaInstall()
    torrentClientInstall()
    ubooquityInstall("2.1.2")
    tvHeadEndInstall()
    fileBrowserInstall()
    plexInstall()
    jellyfinInstall()

if __name__ == '__main__':
    main()

