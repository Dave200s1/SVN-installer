from svn_script import Script
from io import StringIO
import sys
import unittest

from unittest.mock import patch
import subprocess
import configparser
import os

class Test_Script(unittest.TestCase):
    

    def test_welcome_message(self):
        #Arrange
        captured_output = StringIO()
        sys.stdout = captured_output
        test_object = Script()
        #Act
        test_object.welcome()
        output = captured_output.getvalue().strip()
        #Assert
        self.assertEqual("*----Welcome to SVN-installer 1.0 !!!---*",output)

         # Reset the standard output
        sys.stdout = sys.__stdout__
    
    @patch('subprocess.run')
    def test_if_update_runs(self, mock_run):
        #Arrange
        test_object = Script()
       
        #Act
        test_object.runUpdates()

        #Assert
       
        mock_run.assert_any_call("sudo apt update", shell=True)

        mock_run.assert_any_call("sudo apt upgrade", shell=True)
        # Reset the standard output
        sys.stdout = sys.__stdout__

    @patch('subprocess.run')
    def test_if_apache_can_be_installed(self,mock_run):
        #Arrange
        test_object = Script()
        #Act
        test_object.install_apache()
        #Assert
        mock_run.assert_any_call("sudo apt install -y apache2 apache2-utils", shell=True)
        # Reset the standard output
        sys.stdout = sys.__stdout__

    
    @patch('subprocess.run')
    def test_if_apache_dependencies_vim_tree_can_be_installed(self,mock_run):
        #Arrange
        test_object = Script()
        #Act
        test_object.install_apache()
        #Assert
        mock_run.assert_any_call("sudo apt -y install vim tree subversion libsvn-dev libapache2-mod-svn subversion-tools",shell=True)
        # Reset the standard output
        sys.stdout = sys.__stdout__

    @patch('subprocess.run')
    def  test_if_apache_modules_are_enabled(self,mock_run):
        #Arrange
        test_object = Script()
        #Act
        test_object.enable_apache_modules()
        #Assert
        mock_run.assert_any_call("sudo 2enmod dav dav_svn",shell=True)
        #Reset teh standard output
        sys.stdout = sys.__stdout__


    @patch('subprocess.run')
    def test_if_apache2_can_restart(self,mock_run):
        #Arrange
        test_object = Script()
        #Act
        test_object.enable_apache_modules()
        #Assert
        mock_run.assert_any_call("sudo systemctl restart apache2",shell=True)
        #Reset teh standard output
        sys.stdout = sys.__stdout__

    @patch('subprocess.run')
    def test_if_systax_is_correct(self,mock_run):
        #Arrange
        test_object = Script()
        #Act
        test_object.check_syntax()
        #Assert
        mock_run.assert_any_call("sudo apachectl -t",shell=True)
        #Reset teh standard output
        self.test_if_apache2_can_restart()
        sys.stdout = sys.__stdout__
    
    @patch('subprocess.run')
    def test_if_change_permissions_works(self,mock_run):
        #Arrange
        test_object = Script()
        #Act
        test_object.change_permissions()
        #Assert
        mock_run.assert_any_call("sudo chown -R www-data:www-data /var/lib/svn",shell=True)
        mock_run.assert_any_call("sudo chmod -R 775 /var/lib/svn",shell=True)
        #Reset teh standard output
        sys.stdout = sys.__stdout__


if __name__ == '__main__':
    unittest.main()