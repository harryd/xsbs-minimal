import irclib
import os, sys, time
import threading
import getopt

logfile = ''
servername = 'irc.gamesurge.net'
nickname = 'xsbs-serverbot'
channel = '#xsbs'
adminpass = 'foo'

_win = (sys.platform == 'win32')

class FileMonitor(threading.Thread):
    def __init__(self, file, lock):
        threading.Thread.__init__(self)
        self.daemon = True
        self.mtimes = {}
        self.file = file
        self.lock = lock
        self.queue = []
    def run(self):
        print 'running'
        while True:
            self._scan()
            time.sleep(1)
    def _scan(self):
		filename = self.file
		try:
			stat = os.stat(filename)
		except OSError:
			return
		mtime = stat.st_mtime
		if _win:
			mtime -= stat.st_ctime
		if filename not in self.mtimes:
			self.mtimes[filename] = mtime
			return
		if mtime != self.mtimes[filename]:
			self.lock.acquire()
			self.queue.append(filename)
			self.lock.release()
			self.mtimes[filename] = mtime

def onWelcome(server, event):
	server.join(channel)

def main():
	f = open(logfile, 'r')
	f.seek(0, os.SEEK_END)
	irc = irclib.IRC()
	server = irc.server()
	lock = threading.Lock()
	mon = FileMonitor(logfile, lock)
	mon.start()
	server.add_global_handler('welcome', onWelcome)
	server.connect(servername, 6667, nickname)
	while 1:
		if len(mon.queue) > 0:
			lock.acquire()
			buff = f.read()
			lines = buff.split('\n')
			for line in lines:
					server.privmsg(channel, line)
			del mon.queue[:]
			lock.release()
		irc.process_once(timeout=.4)

def help():
	print 'XSBS Server IRC Bot'
	print 'usage: python ircbot.py --logfile <path-to-log> --server <irc server> --channel <channel> --nickname <nickname> --adminpass <admin password>'
	
if __name__ == "__main__":
	opts, args = getopt.getopt(sys.argv[1:], 'hlscnp', ['help', 'logfile='])
	logfile = ''
	for opt, arg in opts:
		if opt in ('-h', '--help'):
			help()
		elif opt in ('-l', '--logfile'):
			logfile = arg
		elif opt in ('-c', '--channel'):
			channel = arg
	if logfile != '' and servername != '' and channel != '' and nickname != '' and adminpass != '':
		main()
	else:
		help()
