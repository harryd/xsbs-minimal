import sbserver, thread
import socketmonitor

events = {}
policy_events = {}

exec_queue = []
exec_queue_lock = thread.allocate_lock()
sockmon = socketmonitor.SocketMonitor()

def registerPolicyEventHandler(event, handler):
	if not policy_events.has_key(event):
		policy_events[event] = []
	policy_events[event].append(handler)

def registerEventHandler(event, handler):
	if not events.has_key(event):
		events[event] = []
	events[event].append(handler)

def triggerEvent(event, args):
	if events.has_key(event):
		for handler in events[event]:
			handler(*args)

def triggerPolicyEvent(event, args):
	if policy_events.has_key(event):
		for handler in policy_events[event]:
			if not handler(*args):
				return False
	return True

def sbExec(function, args):
	exec_queue_lock.acquire()
	exec_queue.append((function, args))
	exec_queue_lock.release()
	sbserver.checkExecQueue(True)

def triggerSbExecQueue():
	if exec_queue_lock:
		return
	exec_queue_lock.acquire()
	for action in exec_queue:
		try:
			action[0](*action[1])
		except:
			print 'Error occoured with enqueued exec action'
	exec_queue_lock.release()

