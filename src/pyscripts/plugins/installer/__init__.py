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
config = {
	'Main': {
		'enable': 'yes',
		'repo': 'http://github.com/downloads/harrythedevman/XSBS-plugins/'
		}
	}

class Install:
	def __init__(self):
		self.pluginList = []
		self.pyscriptsDir = os.getcwd()
		self.downloadDir = os.path.abspath(self.pyscriptsDir + "/plugins/installer/downloads")
		
	def getPluginList(self):
		file = open(self.fetch(config['Main']['repo']), 'r')
		self.pluginList = file.readlines()
		for line in self.pluginList:
			line.strip('\n')
		
	def fetch(self, name):
		file = url.split('/')[-1]
		urllib.urlretrieve(url, self.downloadDir + file)
		return os.path.abspath(self.downloadDir + file)
		
	def install(self, Name):
		self
		
	def parseINSTALL(self, file):
		self.paths = {'plugin_dir': self.pyscriptsDir + "/plugins"}	

@commandHandler('install')
@adminRequired
def onInstallCmd(cn, args):
	'''@description Install server plugins
	   @usage <plugin>
	   @admin'''
	p = player(cn)
	plugin = args
	installer = Install()
	if plugin in installer.pluginList:
		p.message(info("Plugin found. Downloading now."))
		installer.download(plugin)
		p.message(info("Plugin downloaded. Installing now."))
		installer.install(plugin)
		p.message(info("Plugin Installed."))
	else:
		p.message(info("Plugin \"%s\" not found." % plugin))
	
	return
	   
def init():
	print os.getcwd()

init()

	