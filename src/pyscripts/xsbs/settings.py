from ConfigParser import ConfigParser, NoOptionError, NoSectionError
from elixir import Entity, Field, String, Text

# Set this to wherever your configuration files lie.  Must end in a /
configuration_path = 'Config/'

# Set this to what you want config file names to end with
configuration_extension = '.conf'

##### DONT MODIFY BELOW HERE ######

class ConfigOption(Entity):
	plugin = Field(String(30))
	section = Field(String(30))
	name = Field(String(30))
	value = Field(Text)

def loadPluginConfig(dict, plugin):
	'''Accepts a dictionary and plugin name.
	   All stored values for the plugin will be loaded into dict[section][option] = value.
	   This allows you to pass a dictionary pre-loaded with default values. '''
	options = ConfigOption.query.filter_by(plugin=plugin).all()
	for option in options:
		try:
			sectdict = dict[option.section]
		except KeyError:
			dict[options.section] = {}
			sectdict = dict[option.section]
		sectdict[option.name] = option.value

class PluginConfig:
	'''Allows easy reading of configuration options from configuration files'''
	def __init__(self, plugin_name):
		'''Creates config reader for file plugin_name.conf'''
		self.is_modified = False
		self.parser = ConfigParser()
		self.plugin_name = plugin_name
		self.read = False
	def __del__(self):
		if self.is_modified:
			f = open(self.configPath(), 'w')
			self.parser.write(f)
		del self.parser
	def checkRead(self):
		if not self.read:
			self.read = True
			self.parser.read(self.configPath())
	def getOption(self, section, option, default, write_if_absent=True):
		'''
		Returns value of option if it is set.
		If the option does not exist the default value is written and
		returned.
		'''
		self.checkRead()
		try:
			return self.parser.get(section, option)
		except NoSectionError:
			if write_if_absent:
				self.parser.add_section(section)
		except NoOptionError:
			pass
		if write_if_absent:
			self.parser.set(section, option, default)
			self.is_modified = True
		return default
	def getAllOptions(self, section):
		'''
		Returns all options and their values in section.
		Returns a list of tuples with two items that are key/value pairs.
		'''
		self.checkRead()
		try:
			return self.parser.items(section)
		except NoSectionError:
			return []
	def configPath(self):
		return configuration_path + self.plugin_name + configuration_extension

