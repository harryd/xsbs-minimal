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

class Install:
	def __init__(self):
		self.pluginList = []
		
	def getPluginList(self):
		pass
	def download(self, Name):
		pass
	def install(self, Name):
		pass
	def parseINSTALL(self, file):
		pass

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
	

init()

	