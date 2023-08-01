#!  /usr/bin/env python3
import subprocess
import configparser

def welcome():
	print("\n*----Welcome to SVN-installer 1.0 !!!---*")

#welcome()

def runUpdates():
	cmd= "sudo apt update"
	subprocess.run(cmd,shell=True)
	cmd_upgrade = "sudo apt upgrade"
	subprocess.run(cmd_upgrade,shell=True)

#runUpdates()

def install_apache():
	cmd="sudo apt install -y apache2 apache2-utils"
	subprocess.run(cmd,shell=True)
	
	cmd_additional = "sudo apt -y install vim tree subversion libsvn-dev libapache2-mod-svn subversion-tools"
	subprocess.run(cmd_additional,shell=True)
	
	
def enable_apache_modules():
	cmd="sudo 2enmod dav dav_svn"
	subprocess.run(cmd,shell=True)

	cmd_restart="sudo systemctl restart apache2"
	subprocess.run(cmd_restart,shell=True)
	
	
def config_apache2():
	subprocess.call(['sudo','-v'])
	config = configparser.ConfigParser()
	
	#config.read('/etc/apache2/mods-enabled/dav_svn.conf')
	# Define the text to be inserted
	text_to_insert = """
	<Location /svn>
	   DAV svn
	   SVNParentPath /var/lib/svn

	   AuthType Basic
	   AuthName "Subversion Repository"
	   AuthUserFile /etc/apache2/dav_svn.passwd
	   Require valid-user
	</Location>
	"""
	# Define the target file path
	file_path = "/etc/apache2/mods-enabled/dav_svn.conf"

	# Write the text to a temporary file with write mode
	with open("temp.txt", "w") as f:
		f.write(text_to_insert)

	# Use the sudo command to insert the contents of the temporary file into the target file
	cmd = f"sudo sh -c 'cat temp.txt >> {file_path}'"
	subprocess.call([cmd], shell=True)

	# Remove the temporary file
	subprocess.call(["rm", "temp.txt"])
	
	
def check_syntax():
	cmd="sudo apachectl -t"
	subprocess.run(cmd,shell=True)
	
	cmd_restart="sudo systemctl restart apache2"
	subprocess.run(cmd_restart,shell=True)
	
	
def add_user():
	print("\n use sudo htpasswd -cm or (-m for additional user) /etc/apache2/dav_svn.passwd <admin> to add a user\n")
	cmd_input = input("")
	subprocess.run(cmd_input,shell=True)
	
def create_repo():
	cmd_mkdir="sudo mkdir -p /var/lib/svn"
	subprocess.run(cmd_mkdir,shell=True)
	print("\n sudo svnadmin create /var/lib/svn/repo_name to create a repository\n")
	cmd_input = input("")
	subprocess.run(cmd_input,shell=True)
	
	
def change_permissions():
	cmd="sudo chown -R www-data:www-data /var/lib/svn"
	subprocess.run(cmd,shell=True)
	
	cmd_two="sudo chmod -R 775 /var/lib/svn"
	subprocess.run(cmd_two,shell=True)
	
def installation():
	welcome()
	runUpdates()
	install_apache()
	enable_apache_modules()
	config_apache2()
	check_syntax()
	add_user()
	create_repo()
	change_permissions()
	
#main
installation()
