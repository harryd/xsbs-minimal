import sbserver
from events import registerServerEventHandler, registerPolicyEventHandler
from colors import red
from xsbs.ui import error, insufficientPermissions
import logging
import sys, traceback
import xsbs.help

class CommandManager:
	def __init__(self):
		self.prefixes = '#!@'
		self.command_handlers = {}
		registerPolicyEventHandler('allow_message', self.onMsg)
	def register(self, command, func):
		if not self.command_handlers.has_key(command):
			self.command_handlers[command] = []
		self.command_handlers[command].append(func)
	def trigger(self, cn, command, text):
		if self.command_handlers.has_key(command):
			for func in self.command_handlers[command]:
				try:
					func(cn, text)
				except:
					exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()	
					logging.warn('Uncaught exception occured in command handler.')
					logging.warn(traceback.format_exc())
					logging.warn(traceback.extract_tb(exceptionTraceback))
		else:
			sbserver.playerMessage(cn, error('Command not found'))
	def onMsg(self, cn, text):
		if len(text) > 0 and self.prefixes.find(text[0]) != -1:
			cmd = text[1:].split(' ')[0]
			self.trigger(cn, cmd, text[len(cmd)+2:])
			return False
		return True

commandmanager = CommandManager()

def registerCommandHandler(command, func):
	xsbs.help.loadCommandInfo(command, func)
	commandmanager.register(command, func)

class command(object):
	def __init__(self, name):
		self.command_name = name
		pass
	def __call__(self, f):
		self.__doc__ = f.__doc__
		self.__name__ = f.__name__
		registerCommandHandler(self.command_name, f)
		return f

def allowTeamSwitch(cn, team):
	sbserver.playerMessage(cn, 'You cannot switch to team %s' % team)
	return False


registerCommandHandler('help', xsbs.help.onHelpCommand)

