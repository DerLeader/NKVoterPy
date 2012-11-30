#!/usr/bin/env python

""" GloriousLeader.py v1.0.0DL"""

""" This is a port of a small vbs program that was conceived by TheFeel. """
""" Ported by brother , with substantial help and support of orion"""
""" Modified by DerLeader """

Version="1.0.0DL"

import socks
import socket

import urllib
import urllib2

import Tkinter
import tkFileDialog, tkMessageBox

import threading

from sys import exit
from random import randint, choice
from time import sleep

#socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
socket.socket = socks.socksocket

proxies = []

#Constants
USE_TOR = False
RAND_UA = False
RUNNING = False
SHOULDRUN=False

CODES={'Kim Jong Un':'2128881_2128882_2129192','Mohamed Morsi':'2128881_2128882_2129194','Malala Yousafzai':'2128881_2128882_2129199','Psy':'2128881_2128882_2129210','The Mars Rover':'2128881_2128882_2129215','Stephen Colbert':'2128881_2128882_2129212','Bashar Assad':'2128881_2128882_2129195','Undocumented Immigrants':'2128881_2128882_2129191','Barack Obama':'2128881_2128882_2129179','The Higgs Boson Particle':'2128881_2128882_2129214','Felix Baumgartner':'2128881_2128882_2129208','Jon Stewart':'2128881_2128882_2129211','Pussy Riot':'2128881_2128882_2129209','Hillary Clinton':'2128881_2128882_2129184','Aung San Suu Kyi and Thein Sein':'2128881_2128882_2129196','Bill Clinton':'2128881_2128882_2129181','Michael Phelps':'2128881_2128882_2129204','Gabby Douglas':'2128881_2128882_2129203','Ai Weiwei':'2128881_2128882_2129193','Sandra Fluke':'2128881_2128882_2129176','Joe Biden':'2128881_2128882_2129188','Chris Christie':'2128881_2128882_2129182','John Roberts':'2128881_2128882_2129180','Mitt Romney':'2128881_2128882_2129178','Marissa Mayer':'2128881_2128882_2129205','Mo Farah':'2128881_2128882_2129202','Benjamin Netanyahu':'2128881_2128882_2129990','Michael Bloomberg':'2128881_2128882_2129183','Paul Ryan':'2128881_2128882_2129129','Jay-Z':'2128881_2128882_2129213','Tim Cook':'2128881_2128882_2129206','Mario Draghi':'2128881_2128882_2129200','Xi Jinping':'2128881_2128882_2129197','Bo Xilai':'2128881_2128882_2129198','Sheldon Adelson':'2128881_2128882_2129186','E.L. James':'2128881_2128882_2129207','Karl Rove':'2128881_2128882_2129190','Roger Goodell':'2128881_2128882_2129201'}

NAMES={}
TOTAL_VOTES={}
for i,j in CODES.items():
  NAMES[j]=i
  TOTAL_VOTES[i]=0

class MyTimer:
    def __init__(self, tempo, target, args= [], kwargs={}):
        self._target = target
        self._args = args
        self._kwargs = kwargs
        self._tempo = tempo

    def _run(self):
        self._timer = threading.Timer(self._tempo, self._run)
        self._timer.start()
        self._target(*self._args, **self._kwargs)
        
    def start(self):
        self._timer = threading.Timer(self._tempo, self._run)
        self._timer.start()

    def stop(self):
        self._timer.cancel()

def site(ad):
  try:
   page=urllib.urlopen(ad).read()
  except:
   page=" "
  return page

def readUA(filename):
	userAgents = []

	try:
		uFile = open(filename, 'r')
	except IOError:
		print "File " + filename + "not found. Terminate..."
		exit()
	for line in uFile:
		a = line.rstrip() # remove newline
		userAgents.append(a)

	return userAgents

def returnUA(ua, fixed=False):
	if fixed:
		return ua[0]
	if len(ua) == 0:
		return 0
	return choice(ua)

class MainGui(Tkinter.Frame):
	def __init__(self):
		self.a = MyTimer(50000.0, returnUA, [])
		self.top = Tkinter.Tk()
		self.top.title("GloriousLeader.py")
		Tkinter.Frame.__init__(self)
		
		self.uaenabled = Tkinter.BooleanVar()
		
		self.conUi()
	def conUi(self):
		global CODES
		Tkinter.Label(text="Min Wait:").grid(row=0, column=0, pady=5, sticky="W")
		self.entry01 = Tkinter.Entry()
		self.entry01.grid(row=0, column=1, padx=5, pady=5)
		self.entry01.insert("1", "5")
		
		self.liste=Tkinter.Listbox(self.top,height=1)
		self.liste.insert(Tkinter.END, "Kim Jong Un")
		for element in CODES.keys():
			self.liste.insert(Tkinter.END, element)
		self.liste.grid(row=0, column=2, padx=0, pady=0)

		Tkinter.Label(text="Max Wait:").grid(row=1, column=0, pady=5, sticky="W")
		self.entry02 = Tkinter.Entry()
		self.entry02.grid(row=1, column=1, padx=5, pady=5)
		self.entry02.insert("1", "10")
		
		Tkinter.Label(text="Break Count:").grid(row=2, column=0, pady=5, sticky="W")
		self.entry03 = Tkinter.Entry()
		self.entry03.grid(row=2, column=1, padx=5, pady=5)
		self.entry03.insert("1", "50")
		
		Tkinter.Label(text="Break Length:").grid(row=3, column=0, pady=5, sticky="W")
		self.entry04 = Tkinter.Entry()
		self.entry04.grid(row=3, column=1, padx=5, pady=5)
		self.entry04.insert("1", "300")
		
		self.startbutton = Tkinter.Button(text="Start!", command=self.runbot)
		self.startbutton.grid(row=5, column=0, pady=5)
		
		self.startbutton = Tkinter.Button(text="Stop!", command=self.stop)
		self.startbutton.grid(row=5, column=1, pady=5)
		
		self.starttor = Tkinter.Button(text="Start (TOR)", command=self.starttor)
		self.starttor.grid(row=6, column=0, pady=5)
		
		self.loadProxies = Tkinter.Button(text="Load Proxies (.txt)", command=self.loadprox1)
		self.loadProxies.grid(row=5, column=2, padx=5, pady=5)
		
		self.viewProxies = Tkinter.Button(text="View Proxies", command=self.viewprox)
		self.viewProxies.grid(row=6, column=1, padx=5, pady=5)
		
		self.uaCheck = Tkinter.Checkbutton(text="Random User-Agent", variable=self.uaenabled)
		self.uaCheck.grid(row=6, column=2, padx=5, pady=5)
		
		Tkinter.Label(text="Add Proxys").grid(row=4, column=0, padx=5, pady=5)
		self.addProxyEntry = Tkinter.Entry()
		self.addProxyEntry.grid(row=4, column=1, padx=5, pady=5)
		self.addProxyButton = Tkinter.Button(text="Add", command=self.addproxy)
		self.addProxyButton.grid(row=4, column=2, padx=5, pady=5)
		
	def starttor(self):
		self.runbot(tor=True)
		
	def viewprox(self):
		tkMessageBox.showinfo("Proxies", str(proxies))
	
	def addproxy(self):
		p = self.addProxyEntry.get()
		if p == "":
			return
		elif p == "no":
			proxies.append([])
			return
		p = p.split(":")
		proxies.append(p)
	
	def loadprox1(self):
		fn = tkFileDialog.askopenfilename()
		
		try: f = open(fn, "r")
		except IOError: return
		
		for line in f.readlines():
			line = line.replace("\n", "")
			p = line.split(":")
			proxies.append(p)
		
	def stop(self):
		global RUNNING, SHOULDRUN
		SHOULDRUN=False
		self.a.stop()

	def runbot(self, tor=False):
		global RUNNING, SHOULDRUN
		SHOULDRUN=True

		try:
			name=self.liste.get(self.liste.curselection())
		except:
			name="Kim Jong Un"
		self.a = MyTimer(2.0, main, [int(self.entry01.get()), int(self.entry02.get()), int(self.entry03.get()), int(self.entry04.get()), tor, self.a, name])
		self.a.start()


		
def main(minwait, maxwait, breakcount, breakwait, tor, me, Name):
	global RUNNING, SHOULDRUN, TOTAL_VOTES, NAMES, CODES

	if RUNNING:
		return
	RUNNING=True
	print "\nRunning bot for "+Name+"..."
	print "Tor:", tor
	print "Fetching User Agents..."
	RAND_UA = gui.uaenabled.get()
	
	ua = readUA("useragent")
	counter = 0
	firstUrl = "http://polldaddy.com/n/113df4577acffec0e03c79cfc7210eb6/6685610?1111111111111)"
	GuyCode=CODES[Name]
	CoopCode=site("https://raw.github.com/DerLeader/NKVoterPy/master/misc/target")[:-1]
	if len(CoopCode)>8:
		GuyCode=CoopCode
	gloriousLeader = "http://polls.polldaddy.com/vote-js.php?p=6685610&b=1&a=30279773,&o=&va=16&cookie=0&url=http%3A//www.time.com/time/specials/packages/article/0%2C28804%2C"+GuyCode+"%2C00.html&n="
	if tor:
		proxies.append(["127.0.0.1", "9050"])
		print "Using TOR"
		socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
		socket.socket = socks.socksocket
#	print proxies

	if len(proxies)==0:
		proxies.append([])


	while SHOULDRUN:
		for prox in proxies:
			if not USE_TOR and len(prox)>0:
				socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, prox[0], int(prox[1]))
				socket.socket = socks.socksocket
			if RAND_UA:
				print "Using random UA"
				headers = { "User-Agent" : returnUA(ua) }
			else:
				headers = { "User-Agent" : returnUA(ua, True) }
				
			req = urllib2.Request(firstUrl, None, headers)
			longResp = urllib2.urlopen(req).read()
				
			voteID = longResp[14:].split("\'",1)[0]
	
			req = urllib2.Request(gloriousLeader + voteID, None, headers)
			voteRet = urllib2.urlopen(req).read()
			#print voteRet
	
			if "alert" in voteRet:
				print "You have been banned. Please try again later."
				exit()
	
			sleepTime = randint(minwait, maxwait)
			counter = counter + 1
			TOTAL_VOTES[Name] = TOTAL_VOTES[Name]+1
		
			if counter == breakcount:
				sleepTime = breakwait
		
			print "You supported our grorious reader!! Sleeping " + str(sleepTime) + " seconds ("+str(TOTAL_VOTES[Name])+" votes for "+Name+"). Using "+("no proxy" if prox==[] else str(prox))
			sleep(sleepTime)

	print "Loop stopped"
	RUNNING=False

if __name__ == "__main__":
	updateok=site("https://raw.github.com/DerLeader/NKVoterPy/master/misc/update")[:-1]
	lv=updateok.split("\n")[0]
	msgv="\n".join(updateok.split("\n")[1:])
	if lv!=Version:
		print msgv+"\n\n"
	gui = MainGui()
	gui.mainloop()
