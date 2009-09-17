/*
 *   Copyright (C) 2009 Gregory Haynes <greg@greghaynes.net>
 *
 *   This program is free software; you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation; either version 2 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with this program; if not, write to the
 *   Free Software Foundation, Inc.,
 *   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
 */

#include "servermodule.h"
#include "server.h"

#include <iostream>

namespace SbPy
{

static PyObject *numClients(PyObject *self, PyObject *args)
{
	return Py_BuildValue("i", server::numclients());
}

static PyObject *clients(PyObject *self, PyObject *args)
{
	PyObject *pTuple = PyTuple_New(server::numclients());
	PyObject *pInt;
	int y = 0;
	loopv(server::clients)
	{

		pInt = PyInt_FromLong(i);
		PyTuple_SetItem(pTuple, i, pInt);
		y++;
	}
	return pTuple;
}

static PyObject *players(PyObject *self, PyObject *args)
{
	server::clientinfo *ci;
	std::vector<int> spects;
	std::vector<int>::iterator itr;
	PyObject *pTuple;
	PyObject *pInt;
	int y = 0;
	
	loopv(server::clients)
	{
		ci = server::getinfo(i);
		if(ci && ci->state.state != CS_SPECTATOR)
			spects.push_back(i);
	}
	pTuple = PyTuple_New(spects.size());
	
	for(itr = spects.begin(); itr != spects.end(); itr++)
	{
		pInt = PyInt_FromLong(*itr);
		PyTuple_SetItem(pTuple, y, pInt);
		y++;
	}
	return pTuple;
}

static PyObject *spectators(PyObject *self, PyObject *args)
{
	server::clientinfo *ci;
	std::vector<int> spects;
	std::vector<int>::iterator itr;
	PyObject *pTuple;
	PyObject *pInt;
	int y = 0;
	
	loopv(server::clients)
	{
		ci = server::getinfo(i);
		if(ci->state.state == CS_SPECTATOR)
		{
			spects.push_back(i);
		}
	}
	pTuple = PyTuple_New(spects.size());
	
	for(itr = spects.begin(); itr != spects.end(); itr++)
	{
		pInt = PyInt_FromLong(*itr);
		PyTuple_SetItem(pTuple, y, pInt);
		y++;
	}
	return pTuple;
}

static PyObject *message(PyObject *self, PyObject *args)
{
	PyObject *pMsg = PyTuple_GetItem(args, 0);
	if(pMsg)
	{
		char *msg = PyString_AsString(pMsg);
		if(msg)
			server::sendservmsg(msg);
	}
	else
		fprintf(stderr, "Error sending message");
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *playerMessage(PyObject *self, PyObject *args)
{
	int cn;
	char *text;
	server::clientinfo *ci;
	if(!PyArg_ParseTuple(args, "is", &cn, &text))
		return 0;
	ci = server::getinfo(cn);
	if(!ci)
	{
		PyErr_SetString(PyExc_ValueError, "Invalid cn specified");
		return 0;
	}
	if(ci->state.aitype != AI_NONE)
	{
		PyErr_SetString(PyExc_ValueError, "Cannot send message to AI client");
		return 0;
	}
	sendf(cn, 1, "ris", SV_SERVMSG, text);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *playerName(PyObject *self, PyObject *args)
{
	int cn;
	server::clientinfo *ci;
	if(!PyArg_ParseTuple(args, "i", &cn))
		return 0;
	ci = server::getinfo(cn);
	if(!ci)
	{
		PyErr_SetString(PyExc_ValueError, "Invalid cn specified.");
		return 0;
	}
	if(!ci->name)
	{
		PyErr_SetString(PyExc_RuntimeError, "Client cn is valid but has no name.");
		return 0;
	}
	return Py_BuildValue("s", ci->name);
}

static PyObject *playerIpLong(PyObject *self, PyObject *args)
{
	int cn;
	server::clientinfo *ci;
	if(!PyArg_ParseTuple(args, "i", &cn))
		return 0;
	ci = server::getinfo(cn);
	if(!ci)
	{
		PyErr_SetString(PyExc_ValueError, "Invalid cn specified");
		return 0;
	}
	return Py_BuildValue("i", getclientip(ci->clientnum));
}

static PyObject *playerKick(PyObject *self, PyObject *args)
{
	int cn;
	if(!PyArg_ParseTuple(args, "i", &cn))
		return 0;
	disconnect_client(cn, DISC_KICK);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *playerPrivilege(PyObject *self, PyObject *args)
{
	int cn;
	server::clientinfo *ci;
	if(!PyArg_ParseTuple(args, "i", &cn))
		return 0;
	ci = server::getinfo(cn);
	if(!ci)
	{
		PyErr_SetString(PyExc_ValueError, "Invalid cn specified");
		return 0;
	}
	return Py_BuildValue("i", ci->privilege);
}

static PyObject *playerFrags(PyObject *self, PyObject *args)
{
	int cn;
	server::clientinfo *ci;
	if(!PyArg_ParseTuple(args, "i", &cn))
		return 0;
	ci = server::getinfo(cn);
	if(!ci)
	{
		PyErr_SetString(PyExc_ValueError, "Invalid cn specified");
		return 0;
	}
	return Py_BuildValue("i", ci->state.frags);
}

static PyObject *playerTeamkills(PyObject *self, PyObject *args)
{
	int cn;
	server::clientinfo *ci;
	if(!PyArg_ParseTuple(args, "i", &cn))
		return 0;
	ci = server::getinfo(cn);
	if(!ci)
	{
		PyErr_SetString(PyExc_ValueError, "Invalid cn specified");
		return 0;
	}
	return Py_BuildValue("i", ci->state.teamkills);
}

static PyObject *playerDeaths(PyObject *self, PyObject *args)
{
	int cn;
	server::clientinfo *ci;
	if(!PyArg_ParseTuple(args, "i", &cn))
		return 0;
	ci = server::getinfo(cn);
	if(!ci)
	{
		PyErr_SetString(PyExc_ValueError, "Invalid cn specified");
		return 0;
	}
	return Py_BuildValue("i", ci->state.deaths);
}

static PyObject *playerShots(PyObject *self, PyObject *args)
{
	int cn;
	server::clientinfo *ci;
	if(!PyArg_ParseTuple(args, "i", &cn))
		return 0;
	ci = server::getinfo(cn);
	if(!ci)
	{
		PyErr_SetString(PyExc_ValueError, "Invalid cn specified");
		return 0;
	}
	return Py_BuildValue("i", ci->state.shots);
}

static PyObject *playerHits(PyObject *self, PyObject *args)
{
	int cn;
	server::clientinfo *ci;
	if(!PyArg_ParseTuple(args, "i", &cn))
		return 0;
	ci = server::getinfo(cn);
	if(!ci)
	{
		PyErr_SetString(PyExc_ValueError, "Invalid cn specified");
		return 0;
	}
	return Py_BuildValue("i", ci->state.hits);
}

static PyObject *playerPing(PyObject *self, PyObject *args)
{
	int cn;
	server::clientinfo *ci;
	if(!PyArg_ParseTuple(args, "i", &cn))
		return 0;
	ci = server::getinfo(cn);
	if(!ci)
	{
		PyErr_SetString(PyExc_ValueError, "Invalid cn specified");
		return 0;
	}
	return Py_BuildValue("i", ci->ping);
}

// TODO: This should except on isufficient permissions
static PyObject *setBotLimit(PyObject *self, PyObject *args)
{
	int cn, limit;
	server::clientinfo *ci;
	if(!PyArg_ParseTuple(args, "ii", &cn, &limit))
		return 0;
	ci = server::getinfo(cn);
	if(!ci)
	{
		PyErr_SetString(PyExc_ValueError, "Invalid cn specified");
		return 0;
	}
	if(!ci->local && ci->privilege < PRIV_ADMIN)
		sendf(cn, 1, "ris", SV_SERVMSG, "Insufficient permissions to add bot.");
	else
		server::aiman::setbotlimit(ci, limit);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *hashPass(PyObject *self, PyObject *args)
{
	PyObject *pstr;
	int cn;
	char *pass;
	server::clientinfo *ci;
	string string;
	if(!PyArg_ParseTuple(args, "is", &cn, &pass))
		return 0;
	ci = server::getinfo(cn);
	if(!ci)
	{
		PyErr_SetString(PyExc_ValueError, "Invalid cn specified");
		return 0;
	}
	server::hashpassword(cn, ci->sessionid, pass, string, sizeof(string));
	pstr = PyString_FromString(string);
	return pstr;
}

static PyObject *setMaster(PyObject *self, PyObject *args)
{
	int cn;
	server::clientinfo *ci;
	if(!PyArg_ParseTuple(args, "i", &cn))
		return 0;
	ci = server::getinfo(cn);
	if(!ci)
	{
		PyErr_SetString(PyExc_ValueError, "Invalid cn specified");
		return 0;
	}
	server::setcimaster(ci);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *setAdmin(PyObject *self, PyObject *args)
{
	int cn;
	server::clientinfo *ci;
	if(!PyArg_ParseTuple(args, "i", &cn))
		return 0;
	ci = server::getinfo(cn);
	if(!ci)
	{
		PyErr_SetString(PyExc_ValueError, "Invalid cn specified");
		return 0;
	}
	server::setciadmin(ci);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *setPaused(PyObject *self, PyObject *args)
{
	bool val;
	if(!PyArg_ParseTuple(args, "b", &val))
		return 0;
	server::pausegame(val);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *setMap(PyObject *self, PyObject *args)
{
	const char *map;
	int mode;
	if(!PyArg_ParseTuple(args, "si", &map, &mode))
		return 0;
	server::setmap(map, mode);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *setMasterMode(PyObject *self, PyObject *args)
{
	int mm;
	if(!PyArg_ParseTuple(args, "i", &mm))
		return 0;
	server::setmastermode(mm);
	Py_INCREF(Py_None);
	return Py_None;
}


static PyObject *masterMode(PyObject *self, PyObject *args)
{
	return Py_BuildValue("i", server::mastermode);
}

static PyObject *gameMode(PyObject *self, PyObject *args)
{
	return Py_BuildValue("i", server::gamemode);
}

static PyObject *mapName(PyObject *self, PyObject *args)
{
	return Py_BuildValue("i", server::smapname);
}

static PyObject *modeName(PyObject *self, PyObject *args)
{
	int mm;
	const char *name;
	if(!PyArg_ParseTuple(args, "i", &mm))
		return 0;
	if(!m_valid(mm))
	{
		PyErr_SetString(PyExc_ValueError, "Invalid mode");
		return 0;
	}
	name = server::modename(mm);
	return Py_BuildValue("s", name);
}

static PyObject *restartPy(PyObject *self, PyObject *args)
{
	server::restart_py = true;
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject *uptime(PyObject *self, PyObject *args)
{
	return Py_BuildValue("i", server::gamemillis);
}

static PyMethodDef ModuleMethods[] = {
	{"numClients", numClients, METH_VARARGS, "Return the number of clients on the server."},
	{"message", message, METH_VARARGS, "Send a server message."},
	{"clients", clients, METH_VARARGS, "List of client numbers."},
	{"players", players, METH_VARARGS, "List of client numbers of active clients."},
	{"spectators", spectators, METH_VARARGS, "List of client numbers of spectating clients."},
	{"playerMessage", playerMessage, METH_VARARGS, "Send a message to player."},
	{"playerName", playerName, METH_VARARGS, "Get name of player from cn."},
	{"playerIpLong", playerIpLong, METH_VARARGS, "Get IP of player from cn."},
	{"playerKick", playerKick, METH_VARARGS, "Kick player from server."},
	{"playerPrivilege", playerPrivilege, METH_VARARGS, "Integer representing player privilege"},
	{"playerFrags", playerFrags, METH_VARARGS, "Number of frags by player in current match."},
	{"playerTeamkills", playerTeamkills, METH_VARARGS, "Number of teamkills by player in current match."},
	{"playerDeaths", playerDeaths, METH_VARARGS, "Number of deatds by player in current match."},
	{"playerShots", playerShots, METH_VARARGS, "Shots by player in current match."},
	{"playerHits", playerHits, METH_VARARGS, "Hits by player in current match."},
	{"playerPing", playerPing, METH_VARARGS, "Current ping of player."},
	{"setBotLimit", setBotLimit, METH_VARARGS, "Set server bot limit."},
	{"hashPassword", hashPass, METH_VARARGS, "Return hash for user + password"},
	{"setMaster", setMaster, METH_VARARGS, "Set cn to master."},
	{"setAdmin", setAdmin, METH_VARARGS, "Set cn to admin."},
	{"setPaused", setPaused, METH_VARARGS, "Set game to be paused."},
	{"setMap", setMap, METH_VARARGS, "Set to map and mode."},
	{"setMasterMode", setMasterMode, METH_VARARGS, "Set server master mode."},
	{"masterMode", masterMode, METH_VARARGS, "Server master mode."},
	{"gameMode", masterMode, METH_VARARGS, "Server master mode."},
	{"mapName", masterMode, METH_VARARGS, "Server master mode."},
	{"modeName", modeName, METH_VARARGS, "Name of game mode."},
	{"reload", restartPy, METH_VARARGS, "Reload python modules."},
	{"uptime", uptime, METH_VARARGS, "Number of milliseconds server has been running."},
	{NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initModule(const char *module_name)
{
	(void) Py_InitModule(module_name, ModuleMethods);
	return;
}


}
