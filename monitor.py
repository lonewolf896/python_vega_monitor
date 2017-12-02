#!python
import platform
import os
import subprocess
import time
import requests
import sys
import ctypes


#############################
## OPTIONS
miningProg = "xmr-stak.exe"
site = "localhost"
port = "420"
variance = 50
############################

dir = os.getcwd()
minerLoc = dir + "/" + miningProg


def main():
	miner = firstRun()

	rate = getHash()
	baseline = rate - variance

	while 1 == 1:
		while rate >= baseline:
			time.sleep(5)
			rate = getHash()

		print ("hashrate dropped to " + str(rate) + ". Reseting")

		miner.kill()
		print "Reseting Graphics"
		reset_cards()
		print "Starting Miner"
		miner = startMining()

		rate = getHash()

def firstRun():
	print "Reseting Graphics"
	reset_cards()
	print "Starting Miner"
	goof = startMining()
	return goof


def reset_cards():
	reset_status = dir + "/reset_graphics.ps1"
	subprocess.call(["powershell", reset_status], stdout=subprocess.PIPE)
	reset_variables = dir + "/OverdriveNTool.exe"
	subprocess.call([reset_variables, "-r1", "-p1Vega64"], stdout=subprocess.PIPE)

	return 

def getHash():
	query = "http://" + site + ":" + port + "/api.json" 

	while 1 == 1:
		try:
			r = requests.get(query)

			if str(r.json()["hashrate"]["total"][0]) != "None":
				break

			else:
				print "Waiting for hashing to start"
				time.sleep(1)

		except:
			print "Server not online yet..."
			time.sleep(1)
	
	return int(r.json()["hashrate"]["total"][0])

def startMining():
	miner = subprocess.Popen(minerLoc)

	return miner

def checkingVer():
	if (platform.python_version())[0:3] == "2.7":
		print "Correct version!"
		main()

	else:
		print "This needs to run on python 2.7...quiting" 

def testHash():
	rate = getHash()
	baseline = int(rate) - variance

	print "test"
	while 1 == 1:
		if int(rate) > baseline:
			time.sleep(5)
			rate = getHash()
			print int(rate)
		else:
			break

	return "Derp"

def run_as_admin(argv=None, debug=False):
	shell32 = ctypes.windll.shell32

	if argv is None and shell32.IsUserAnAdmin():
		return True

	if argv is None:
		argv = sys.argv

	if hasattr(sys, '_MEIPASS'):
		# Support pyinstaller wrapped program.
		arguments = map(unicode, argv[1:])

	else:
		arguments = map(unicode, argv)

	argument_line = u' '.join(arguments)

	executable = unicode(sys.executable)

	if debug:
		print 'Command line: ', executable, argument_line

	ret = shell32.ShellExecuteW(None, u"runas", executable, argument_line, None, 1)

	if int(ret) <= 32:
		return False

	return None


if __name__ == '__main__':

	ret = run_as_admin()

	if ret is True:
		main()
		raw_input('Press ENTER to exit.')

	elif ret is None:
		print 'I am elevating to admin privilege.'
		raw_input('Press ENTER to exit.')

	else:
		print 'Error(ret=%d): cannot elevate privilege.' % (ret, )
