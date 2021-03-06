from elixir import Entity, Field, String, Integer, Boolean, setup_all, session
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from xsbs.settings import loadPluginConfig
from xsbs.net import ipLongToString, ipStringToLong
from xsbs.timers import addTimer
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from xsbs.ui import info, notice
from xsbs.colors import colordict
from xsbs.events import eventHandler, policyHandler

import time, string
import logging
import sbserver

config = {
	'Main': {
		'message': 'Banning ${orange}${name}${white} for $seconds seconds for ${red}${reason}',
		}
	}

def init():
	loadPluginConfig(config, 'Bans')
	config['Main']['message'] = string.Template(config['Main']['message'])

class Ban(Entity):
	ip = Field(Integer, index=True)
	expiration = Field(Integer, index=True) # Epoch seconds
	reason = Field(String(50))
	nick = Field(String(15))
	banner_ip = Field(Integer)
	banner_nick = Field(String(15))
	time = Field(Integer)
	sticky = Field(Boolean, index=True)
	def __init__(self, ip, expiration, reason, nick, banner_ip, banner_nick, time, sticky):
		self.ip = ip
		self.expiration = expiration
		self.reason = reason
		self.nick = nick
		self.banner_ip = banner_ip
		self.banner_nick = banner_nick
		self.time = time
		self.sticky = sticky
	def isExpired(self):
		return self.expiration <= time.time()

class BanNick(Entity):
	nick = Column(String(15), index=True)
	reason = Column(String(50))
	def __init__(self, nick, reason):
		self.nick = nick
		self.reason = reason

def getCurrentBanByIp(ipaddress):
	return Ban.query.filter_by(ip=ipaddress).filter('expiration>'+str(time.time())).one()

def getCurrentBanByNick(nick):
	return BanNick.query.filter_by(nick=nick).one()

def isIpBanned(ipaddress):
	try:
		b = getCurrentBanByIp(ipaddress)
		return True
	except NoResultFound:
		return False
	except MultipleResultsFound:
		return True

def isNickBanned(nick):
	try:
		b = getCurrentBanByNick(nick)
		return True
	except NoResultFound:
		return False
	except MultipleResultsFound:
		return True

def ban(cn, seconds, reason, banner_cn, sticky=False):
	ip = sbserver.playerIpLong(cn)
	expiration = time.time() + seconds
	nick = sbserver.playerName(cn)
	if banner_cn != -1:
		banner_ip = sbserver.playerIpLong(banner_cn)
		banner_nick = sbserver.playerName(banner_cn)
	else:
		banner_ip = 0
		banner_nick = ''
	newban = Ban(ip, expiration, reason, nick, banner_ip, banner_nick, time.time(), sticky)
	session.commit()
	addTimer(200, sbserver.playerKick, (cn,))
	logging.info('Player %s (%s) banned for %s by %s (%s)',
		nick,
		ipLongToString(ip),
		reason,
		banner_nick,
		ipLongToString(banner_ip))
	sbserver.message(info(config['Main']['message'].substitute(colordict, name=nick, seconds=seconds, reason=reason)))

