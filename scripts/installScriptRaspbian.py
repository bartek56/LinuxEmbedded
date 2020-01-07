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


def tvHeadEndInstall():
    print ("\n\n\nInstall TvHeadEnd\n\n\n")
    output = subprocess.run(["sudo", "apt-get","--assume-yes", "install", "tvheadend"], check=True)
    print (output)

def apache2Install():
    print ("\n\n\nInstall Apache2\n\n\n")
    output = subprocess.run(["sudo", "apt-get","--assume-yes", "install", "apache2"], check=True)
    print (output)

def plexInstall():
    print ("\n\n\nInstall Plex\n\n\n")

    output = subprocess.run(["sudo", "apt", "install", "apt-transport-https", "ca-certificates", "curl"], check=True)
    print (output)
    output = subprocess.run(["curl", "https://downloads.plex.tv/plex-keys/PlexSign.key", "|", "sudo","apt-key", "add", "-"], check=True)
    print (output)
    output = subprocess.run(["echo","deb", "https://downloads.plex.tv/repo/deb", "public", "main", "|", "sudo","tee", "/etc/apt/sources.list.d/plexmediaserver.list"], check=True)
    print (output)

    output = subprocess.run(["sudo", "apt", "update"], check=True)
    print (output)

    output = subprocess.run(["sudo", "apt", "--assume-yes","install", "plexmediaserver"], check=True)

def main():
    upgrade()
#    getScripts()
#    rpi_update()
#    musicPlayerDaemonInstall()
#    websiteMusicPlayerClientInstall()
#    tvHeadEndInstall()
#    apache2Install()
#    plexInstall()
    



if __name__ == '__main__':
    main()

