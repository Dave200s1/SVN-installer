#!  /usr/bin/env python3
import smtplib
import subprocess
import configparser



class Script():
	
	def __init__(self):
		pass
		
	def welcome(self):
		print("\n*----Welcome to SVN-installer 1.0 !!!---*")

	#welcome()

	def runUpdates(self):
		cmd= "sudo apt update"
		subprocess.run(cmd,shell=True)
		cmd_upgrade = "sudo apt upgrade"
		subprocess.run(cmd_upgrade,shell=True)

	#runUpdates()

	def install_apache(self):
		cmd="sudo apt install -y apache2 apache2-utils"
		subprocess.run(cmd,shell=True)
		
		cmd_additional = "sudo apt -y install vim tree subversion libsvn-dev libapache2-mod-svn subversion-tools"
		subprocess.run(cmd_additional,shell=True)
		
		
	def enable_apache_modules(self):
		cmd="sudo 2enmod dav dav_svn"
		subprocess.run(cmd,shell=True)

		cmd_restart="sudo systemctl restart apache2"
		subprocess.run(cmd_restart,shell=True)
		
		
	def config_apache2(self):
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
		
		
	def check_syntax(self):
		cmd="sudo apachectl -t"
		subprocess.run(cmd,shell=True)
		
		cmd_restart="sudo systemctl restart apache2"
		subprocess.run(cmd_restart,shell=True)
		
		
	def add_user(self):
		print("\n use sudo htpasswd -cm or (-m for additional user) /etc/apache2/dav_svn.passwd <admin> to add a user\n")
		cmd_input = input("")
		subprocess.run(cmd_input,shell=True)
		
	def create_repo(self):
		cmd_mkdir="sudo mkdir -p /var/lib/svn"
		subprocess.run(cmd_mkdir,shell=True)
		print("\n sudo svnadmin create /var/lib/svn/repo_name to create a repository\n")
		cmd_input = input("")
		subprocess.run(cmd_input,shell=True)
		
		
	def change_permissions(self):
		cmd="sudo chown -R www-data:www-data /var/lib/svn"
		subprocess.run(cmd,shell=True)
		
		cmd_two="sudo chmod -R 775 /var/lib/svn"
		subprocess.run(cmd_two,shell=True)
		
	def installation(self):
		self.welcome()
		self.runUpdates()
		self.install_apache()
		self.enable_apache_modules()
		self.config_apache2()
		self.check_syntax()
		self.add_user()
		self.create_repo()
		self.change_permissions()
		
	


