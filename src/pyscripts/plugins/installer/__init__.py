import sbserver
from elixir import session

from xsbs.events import triggerServerEvent
from xsbs.commands import commandHandler, UsageError, ExtraArgumentError, StateError
from xsbs.settings import loadPluginConfig
from xsbs.colors import red, yellow, blue, green, white, colordict
from xsbs.ui import error, info, notice, insufficientPermissions
from xsbs.net import ipLongToString
from xsbs.users import loggedInAs
from xsbs.users.privilege import isUserMaster, isUserAdmin, UserPrivilege
from xsbs.players import masterRequired, adminRequired, player, currentAdmin

import os
import urllib
import tarfile
import string

config = {
        'Main': {
		'enable': 'yes',
		'repo': 'http://github.com/harrythedevman/XSBS-plugins/',
		'list': 'http://github.com/harrythedevman/XSBS-plugins/raw/master/list'
		}
	}

class Install:
	def __init__(self):
		self.pluginDict = {}
		self.pyscriptsDir = os.getcwd()
		self.downloadDir = os.path.abspath(self.pyscriptsDir + "/plugins/installer/downloads/") + '/'
		self.pluginsDir = os.path.abspath(self.pyscriptsDir + "/plugins/") + '/'

	def getPluginList(self):
		path = self.download(config['Main']['list'])
		file = open(path, 'r')
		for line in file.readlines():
			line = line.split("#")
			self.pluginDict[line[0]] = line[1]
		os.remove(path)
		
	def download(self, url):
		file = url.split('/')[-1]
		urllib.urlretrieve(url, self.downloadDir + file)
		return os.path.abspath(self.downloadDir + file)
	
	def fetch(self, name):
		return self.download(self.pluginDict[name])
		
	def install(self, name):
		file = self.fetch(name)
		tf = tarfile.open(file)
		tf.extractall(self.downloadDir)
		installFile = self.downloadDir + '/' + name + "/install"
		moves = self.parseInstall(installFile)
		for k, v in moves.iteritems():
			os.rename(self.downloadDir + name + "/" + k , v + k)
			
	def parseInstall(self, file):
		paths = {'plugin_dir': self.pluginsDir, 'pyscripts_dir': self.pyscriptsDir}
		moves = {}
		for line in open(file, 'r').readlines():
			line = string.Template(line)
			line = line.substitute(paths)
			line = line.split(':')
			moves[line[0]] = line[1]
		return moves
			
@commandHandler('install')
@adminRequired
def onInstallCmd(cn, args):
	'''@description Install server plugins
	   @usage <plugin>
	   @admin'''
	p = player(cn)
	plugin = args
	installer = Install()
	installer.getPluginList()
	if plugin in installer.pluginDict:
		p.message(info("Plugin found. Downloading now."))
		print 1
		installer.fetch(plugin)
		p.message(info("Plugin downloaded. Installing now."))
		print 2
		installer.install(plugin)
		p.message(info("Plugin Installed."))
	else:
		p.message(info("Plugin \"%s\" not found." % plugin))
		return
	   
def init():
	print os.getcwd()

init()

	
