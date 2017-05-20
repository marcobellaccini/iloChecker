iloChecker
===============
About iloChecker
--------------------------
iloChecker is a Python 3 script that helps you performing a bulk health check on a
list of HP ProLiant servers by using their HP iLO (Hewlett Packard Integrated Lights-Out management).

Give it a file with a list of systems as argument and it will do all the boring job for you.

The script uses Python `requests`_ module (you can get it through pip3).

For MS Windows users, a stand-alone `binary release`_ of iloChecker was prepared using `py2exe`_.

iloChecker is brought to you by Marco Bellaccini - marco.bellaccini(at!)gmail.com.

NOTE:
iloChecker is only compatible with HP ProLiant iLO 4 @ firmware version >= 2.00

Usage examples
------------------------
Get health and power status of systems listed in list.txt:

		iloChecker.py list.txt
		
...and here is a sample output:

		SYSTEMS SUMMARY:

		=========	========	========	========
		TARGET		HOSTNAME	HEALTH		POWER
		=========	========	========	========
		10.0.0.11	SRV001		OK 		On
		10.0.0.12	SRV002		OK		On
		HOST3-ilo	HOST3		OK		Off
		10.0.1.42	WEB001		OK		On
		=========	========	========	========

		Scanned 4 system(s):

		4/4 healthy

		3/4 powered on
		
Print help notes:

		iloChecker.py -h


.. _requests: https://pypi.python.org/pypi/requests
.. _binary release: https://github.com/marcobellaccini/iloChecker/releases
.. _py2exe: http://www.py2exe.org/
